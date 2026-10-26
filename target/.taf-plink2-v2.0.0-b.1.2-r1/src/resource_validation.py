"""Shared host/container validation for installed PLINK reference members.

Custom catalogs are user-pinned declarations, not upstream-authenticated data.
This validates identity, inventory and bytes; it never selects scientific input.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

MARKERS = {"receipt.json", "SHA256SUMS", "READY"}


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate_member(member):
    if not isinstance(member, dict):
        raise ValueError("member must be an object")
    if not isinstance(member.get("id"), str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9_.-]*", member["id"]):
        raise ValueError("invalid member ID")
    for field in ("version", "license", "source"):
        if not isinstance(member.get(field), str) or not member[field].strip():
            raise ValueError("version/license/source required")
    if not isinstance(member.get("files"), list) or not member["files"]:
        raise ValueError("nonempty files array required")
    names = set()
    for item in member["files"]:
        if not isinstance(item, dict):
            raise ValueError("file record must be an object")
        name = item.get("name")
        if (not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name)
                or name in names or name in MARKERS):
            raise ValueError("invalid or duplicate filename")
        names.add(name)
        if (not isinstance(item.get("url"), str) or not item["url"].startswith("https://")
                or not isinstance(item.get("sha256"), str)
                or not re.fullmatch("[0-9a-f]{64}", item["sha256"])):
            raise ValueError("HTTPS URL and exact SHA256 required")
        if type(item.get("bytes")) is not int or item["bytes"] <= 0:
            raise ValueError("positive fixed byte count required")


def load_catalog(path):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or data.get("schema") != 1 or not isinstance(data.get("members"), list):
        raise ValueError("expected schema=1 and members array")
    seen = set()
    for member in data["members"]:
        validate_member(member)
        if member["id"] in seen:
            raise ValueError("duplicate member ID")
        seen.add(member["id"])
    return data


def verify(member, target, markers=True, installed=False):
    validate_member(member)
    if target.is_symlink() or not target.is_dir():
        raise ValueError("not a regular installed member directory")
    if installed and target.name != member["id"]:
        raise ValueError("receipt ID does not match installed directory")
    receipt = target / "receipt.json"
    if receipt.is_symlink() or not receipt.is_file():
        raise ValueError("missing regular receipt")
    if json.loads(receipt.read_text()) != member:
        raise ValueError("receipt does not match selected fixed member")
    expected = (MARKERS if markers else {"receipt.json"}) | {item["name"] for item in member["files"]}
    if {entry.name for entry in target.iterdir()} != expected:
        raise ValueError("unexpected or missing files")
    for item in member["files"]:
        path = target / item["name"]
        if (path.is_symlink() or not path.is_file() or path.stat().st_size != item["bytes"]
                or digest(path) != item["sha256"]):
            raise ValueError("checksum/size mismatch: " + item["name"])
    if markers:
        for name in ("SHA256SUMS", "READY"):
            if (target / name).is_symlink() or not (target / name).is_file():
                raise ValueError("missing regular integrity marker")
        sums = "".join(digest(target / name) + "  " + name + "\n"
                       for name in sorted({"receipt.json"} | {item["name"] for item in member["files"]}))
        if ((target / "SHA256SUMS").read_text() != sums
                or (target / "READY").read_text() != digest(target / "SHA256SUMS") + "\n"):
            raise ValueError("integrity marker mismatch")


def verify_root(root):
    if not root.is_dir():
        raise ValueError("missing resource root")
    members = [entry for entry in root.iterdir() if not entry.name.startswith(".")]
    if not members:
        raise ValueError("empty resource family")
    for target in members:
        if target.is_symlink() or not target.is_dir():
            raise ValueError("not a regular installed member directory")
        receipt = target / "receipt.json"
        if receipt.is_symlink() or not receipt.is_file():
            raise ValueError("missing regular receipt")
        verify(json.loads(receipt.read_text()), target, installed=True)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("expected exactly one resource root")
        verify_root(Path(sys.argv[1]))
    except (ValueError, OSError) as error:
        print("plink2-resource-validation: " + str(error), file=sys.stderr)
        sys.exit(1)
