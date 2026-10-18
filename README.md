# plink2

`plink2` packages PLINK 2.0 alpha 7.13 for TAFFISH.

Package identity:

- name: `plink2`
- command: `taf-plink2`
- kind: `tool`
- version: `2.0.0-a.7.13-r1`
- image: `ghcr.io/taffish/plink2:2.0.0-a.7.13-r1`
- license: Apache-2.0 for TAFFISH packaging
- upstream tag: `v2.0.0-a.7.13`
- runtime: `PLINK v2.0.0-a.7.13` and `vcf_subset v1.1.0`
- upstream: <https://www.cog-genomics.org/plink/2.0/>

## What This App Packages

This app builds PLINK 2.0 from the official `chrchang/plink-ng` source tag
`v2.0.0-a.7.13`, posted on 15 October 2026. The default command is `plink2`; the
same source tree also provides the upstream `vcf_subset` helper.

This continues the existing alpha 7 maintenance track, not the separate beta 1
development build. The a.7.11 to a.7.13 source delta includes large-test-count
adjustment, merge-filter defaults, allele/LD/column parsing fixes and a Mendelian
error scan memory-write fix. Beta-only new commands are not
claimed. The dynamic build dependencies, `vcf_subset` 1.1.0 and layered software
license set remain unchanged. No upstream algorithm/source patch is applied.

## Scope

This app supports:

- PLINK 2.0 genotype data management and conversion workflows.
- PGEN/PVAR/PSAM, PLINK 1 binary files, VCF/BCF/BGEN/Oxford-style inputs
  supported by upstream PLINK 2.0.
- Common QC/statistics/GWAS operations such as `--freq`, `--hardy`, `--missing`,
  `--pca`, `--glm`, `--make-pgen`, `--make-bed`, and `--export`.
- VCF sample and variant-ID subsetting through `vcf_subset`.

This app does not package:

- PLINK 1.9/1.07 as a separate `plink` command.
- Reference panels, phenotype/covariate files, genome FASTA files, or tutorial
  datasets.
- CUDA/GPU proof-of-concept builds.
- The Python `pgenlib` wheel or R `pgenlibr` package as runtime libraries.

## Container Contents

- `plink2`: PLINK 2.0 alpha command-line application.
- `vcf_subset`: helper for sample and variant-ID subsetting of VCF/VCF.GZ
  inputs.
- Runtime libraries: Debian OpenBLAS/LAPACK/LAPACKE, zlib, libstdc++ and their
  runtime dependencies.
- `plink2-resources`: explicit, checksum-pinned reference installation and
  verification helper (Python standard library + curl); not an upstream command.
- `plink2-smoke`: independent offline packaging checks, not an analysis frontend.

The container is built from source with the upstream `build_dynamic` baseline:
`NO_AVX2=1`, `NO_SSE42=1`, and `CPU_CHECK=1`. This avoids requiring AVX2 or
SSE4.2 instructions while still using OpenBLAS/LAPACK for linear algebra.

## Usage

Install the published package through your usual TAFFISH workflow. From a source
checkout, `taf check` and `taf build` generate
`target/taf-plink2-v2.0.0-a.7.13-r1`; building a local candidate is not publishing.

Access upstream help and version:

```sh
taf-plink2 -- --help
taf-plink2 -- --version
```

Create a tiny synthetic PGEN dataset:

```sh
taf-plink2 -- --dummy 100 1000 --make-pgen --out tiny
```

Import VCF to PGEN:

```sh
taf-plink2 -- --vcf input.vcf.gz --make-pgen --out cohort
```

Run common QC/statistics:

```sh
taf-plink2 -- --pfile cohort --freq --hardy --missing --out qc
```

Run association testing:

```sh
taf-plink2 -- --pfile cohort --glm --pheno pheno.tsv --covar covar.tsv --out gwas
```

Subset VCF samples with the packaged helper:

```sh
taf-plink2 vcf_subset --in input.vcf.gz --out subset.vcf.gz --keep samples.txt
```

Filter VCF records by variant ID with `vcf_subset 1.1.0`:

```sh
taf-plink2 vcf_subset --in input.vcf.gz --out selected.vcf.gz --extract variants.txt
taf-plink2 vcf_subset --in input.vcf.gz --out excluded.vcf.gz --exclude variants.txt
```

## Command Mode

TAFFISH tool apps support automatic command mode. For option-leading PLINK 2.0
flags, use `taf-plink2 -- ...` so arguments are passed to the default `plink2`
command. For non-option-leading helper commands, use command mode:

```sh
taf-plink2 vcf_subset --help
```

### Paths Containing Spaces

The current TAFFISH command wrapper assembles a shell command line. Ordinary
shell quoting alone does not preserve an argument containing spaces: for
example, `--out "my result"` is split before PLINK2 receives it. This is a
wrapper boundary, not a PLINK2 input-format or analysis limitation.

Prefer simple relative filenames. For a path containing spaces but no quotes
or shell metacharacters, retain literal inner single quotes:

```sh
taf-plink2 -- --pfile "'my cohort'" --freq --out "'my result'"
taf-plink2 plink2-resources verify --catalog "'chosen catalog.json'" \
  --member synthetic-v1 --resource-root "'prepared root'"
```

The second example requires your own pinned catalog and its selected member;
`synthetic-v1` is an example ID, not a bundled production reference. The same
quoting applies to `--vcf`, `--source-dir` and other command/helper path options,
and to explicit `taf-plink2 plink2 ...` command mode on all three backends.
Do not extrapolate this simple-space workaround to quotes, dollar signs,
backticks, newlines or other shell syntax: use a simple-named local copy or
symlink to the input and a simple output prefix instead. Avoid untrusted shell
text. Host discovery is different: set
`TAFFISH_PLINK2_RESOURCE_PATH="/absolute/prepared root"` with normal shell quotes
and **without** embedded quote characters. Manual backend run-argument strings
retain their own quoting as shown below.

## Inputs

| Input | Meaning | Notes |
| --- | --- | --- |
| `.pgen/.pvar/.psam` | PLINK 2 genotype dataset | Native PLINK 2 format |
| `.bed/.bim/.fam` | PLINK 1 binary dataset | Supported by PLINK 2.0 import paths |
| VCF/BCF/BGEN/Oxford files | Variant/genotype imports | Some rich fields may be filtered during import but not re-exported |
| phenotype/covariate/list files | Metadata and filters | User-provided; no reference panels are bundled |

## Output Notes

Output files are controlled by upstream PLINK 2.0 flags and `--out`. Typical
outputs include `.pgen/.pvar/.psam` datasets, `.afreq`, `.hardy`, `.vmiss`,
`.smiss`, `.glm.*`, `.eigenvec`, `.eigenval`, `.log`, and exported VCF/BED-style
files. See the upstream output-file index for exhaustive details.

## Resources, Databases, and Platform

No reference is needed for basic operation, but references are **not all N/A**.
Project cohorts/phenotypes are project-specific inputs. The official resources
page also links reusable 1000 Genomes callsets, HGDP panels and GRCh37/38 FASTA.
The independently fixed unit is a callset/chromosome with matching variant and
sample tables, or a single FASTA, not the entire evolving resource family.

`plink2-resources` supports explicit repeated `--member`, `list`, `install`,
`verify`, `--dry-run`, `--resource-root` and a schema-1 JSON `--catalog`.
The bundled catalog pins one complete representative member:
`hgdp-grch38-chry-noannot-20260930` (three files, 5,281,419 download bytes).
This is **chrY, not a whole-genome reference**. Other official members/FASTA can
use a custom pinned catalog; this is not an exhaustive built-in upstream mirror.

```sh
taf-plink2 plink2-resources list
taf-plink2 plink2-resources install --member hgdp-grch38-chry-noannot-20260930 --dry-run
mkdir -p plink2-resources
taf-plink2 plink2-resources install --member hgdp-grch38-chry-noannot-20260930 --resource-root plink2-resources
```

Catalog schema: `{"schema":1,"members":[{"id":"...","version":"...",
"source":"...","license":"...","files":[{"name":"...","url":"https://...",
"sha256":"64 lowercase hex characters","bytes":123}]}]}`. Match the installed
`/opt/plink2/share/resources.json` example. Use `--catalog chosen.json` for both
installation and verification of a custom member. Resolve the scientific callset
and resource terms first; pin each source independently. Missing SHA256, sizes
and license statements are rejected. No implicit `all`, live `latest`, fallback
or silent checksum refresh. Bundled hashes are TAFFISH's 2026-09-30 observations,
not claimed upstream-published checksums. Data download from official Dropbox
links and are not redistributed in the image.

The root must exist and be a persistent host directory (working-directory bind
or explicit writable bind). Installation uses a root lock, private deterministic
staging, two retries, curl Range continuation, SHA256/size verification, a per-member
`receipt.json`, `SHA256SUMS` and `READY`, and atomic no-replace promotion.
The private staging parent remains 0700 even when its completed child becomes
0755; interruption in that window is recoverable. INT/TERM/HUP stop an owned
download child and exit 130/143/129; installed members are never deleted.
Download concurrency is one.
Required free space is selected member bytes plus 16 MiB; decompression requires
additional project space. Completed files are reused after hashing; partial files
remain in `.partial-*`. A server refusing Range causes failure, not unsafe append.
`--source-dir DIR` resumes missing, empty or matching-prefix offline files without
relaxing the pinned SHA/size; mismatched prefixes are retained and rejected.
Corruption fails closed. No destructive `--force`: preserve a damaged root for
inspection and install into a new root; directory existence alone never passes.

Personal root: `~/.local/share/taffish/resources/plink2`. Site alternatives:
`/usr/local/share/taffish/resources/plink2` or `/opt/taffish/resources/plink2`.
An administrator prepares the site root and installs once; member directories
are 0755, files 0644. Ensure all parents are traversable. Only the installer needs
write access; ordinary users verify/read via a read-only bind. This helper never
changes system permissions or installs into site directories automatically.

Discovery exposes only integrity-marked managed roots, not arbitrary project
genotypes. Priority is explicit `TAFFISH_PLINK2_RESOURCE_PATH`, then the personal
root, then `/usr/local/share`, then `/opt/taffish`. An existing but invalid root
fails closed without searching lower priorities. A partial family is acceptable
only when every installed member passes its recorded inventory/checksums; it
does not imply the requested scientific member exists. Symlinks for the root are
physically resolved; symlink members/files are rejected. Spaces are supported;
colon/comma in host paths are rejected. Host `sha256sum` or `shasum` is required.
Resources are mounted read-only at `/references` on all three backends; PLINK
still requires explicit input/member paths. Set `TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT=0`
to disable discovery, including during installation or manual binds. The wrapper
does not parse scientific argv, inject an input choice, or download anything.

Legacy a.7.11 roots have no integrity markers: use the explicit read-only manual
fallback to consume them, or install exact files with `--source-dir` into a new
managed root. The helper never silently rewrites an existing legacy or damaged
member. Scratch `.partial-*` folders and the lock are not installed members;
an interrupted empty private parent can be retained harmlessly.

Runtime write map: project outputs, logs and conversion intermediates use the
writable output prefix; smoke uses unique `/tmp`. Installed code/catalogs and
reference inputs are read-only. PLINK itself has no implicit downloader/cache;
missing local data fail. Never write derived indexes or decompressed data into
a read-only shared member.

## Backend Usage and Capability Matrix

Choose `TAFFISH_CONTAINER_BACKEND=docker`, `podman` or `apptainer`; analysis
commands are otherwise identical. Both `linux/amd64` and `linux/arm64` are native
source builds. Apptainer needs Linux; macOS uses Docker/Podman Linux VMs. No GPU,
service, device or emulation flags are intrinsic requirements.

Set `TAFFISH_PLINK2_RESOURCE_PATH` to an absolute managed root for automatic
read-only exposure. For legacy/custom roots, export
`TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT=0` and the matching manual policy (append
rather than overwrite existing site policy; single quotes preserve spaces):

| Backend | Read-only exposure |
| --- | --- |
| Docker | `TAFFISH_DOCKER_RUN_ARGS="--volume '$TAFFISH_PLINK2_RESOURCE_PATH:/references:ro'"` |
| Podman | `TAFFISH_PODMAN_RUN_ARGS="--volume '$TAFFISH_PLINK2_RESOURCE_PATH:/references:ro'"` |
| Apptainer | `TAFFISH_APPTAINER_RUN_ARGS="--bind '$TAFFISH_PLINK2_RESOURCE_PATH:/references:ro'"` |

```sh
taf-plink2 plink2-resources verify --resource-root /references --member hgdp-grch38-chry-noannot-20260930
taf-plink2 -- --zst-decompress /references/hgdp-grch38-chry-noannot-20260930/hgdp_chrY.pgen.zst hgdp_chrY.pgen
taf-plink2 -- --pgen hgdp_chrY.pgen --pvar /references/hgdp-grch38-chry-noannot-20260930/hgdp_chrY.pvar.zst --psam /references/hgdp-grch38-chry-noannot-20260930/hgdp_chrY.psam --freq --out reference-freq
```

For Docker output ownership, add `--user UID:GID` using your numeric IDs;
rootless Podman can use `--userns keep-id`; Apptainer uses the ordinary caller.
An administrator can separately prepare an uncompressed derived PGEN with its
own provenance/hash; do not insert it into the immutable fixed member directory.

## Reproducibility

- Upstream repository: <https://github.com/chrchang/plink-ng>
- Upstream documentation: <https://www.cog-genomics.org/plink/2.0/>
- Upstream tag: `v2.0.0-a.7.13`
- Upstream commit: `b3a93fafb680aa8134f2df3b06b0c188bda0bae8`
- Source archive:
  `https://github.com/chrchang/plink-ng/archive/refs/tags/v2.0.0-a.7.13.tar.gz`
- Source SHA256:
  `d125cd76cc284aa41c133add511b5030413e764b40d731fd38588dbd5104c6f6`
- Debian 12 slim base index:
  `sha256:3783cc01769c7b2b1b83a5c5ad96c815348e28ed7da68e2e3687004faa906251`

These identities do not archive upstream materials permanently. Debian APT
repositories remain active; the final installed package inventory is evidence,
not an input lock. Source/resource 404, TLS/transport failure and hash mismatch
must be distinguished. Recover old bytes only from a matching trusted copy;
new materials require a new reviewed identity and full validation, never skipped
checksums. Relevant Dockerfile instructions carry maintenance notes.

## Boundaries

Official source entry points, recommended installation, developer documentation
and tutorial companions were checked: no PLINK 2 alpha GUI/plugin extra is
packaged upstream. RStudio is an external tutorial environment; legacy gPLINK/
Haploview are PLINK 1-era clients, not a PLINK 2 GUI contract. This app starts no
browser service. A future compatible GUI needs its own explicit review.

PLINK 2.0 is under active alpha development. This app pins a specific alpha
release and checks the runtime version, but users should still review upstream
release notes before interpreting results from production GWAS workflows.

The upstream README notes that `.pgen` cannot represent genotype probability
triplets, read depths, per-call quality scores, and similar fields; use
specialized tools such as BCFtools or qctool when those fields must be retained
outside PLINK 2.0's supported import/filter paths.

## Testing

The smoke test covers:

- source identity and bundled license files
- `plink2` and `vcf_subset` version/help output
- OpenBLAS/LAPACK/zlib dynamic library resolution
- synthetic `--dummy` to PGEN generation
- `--freq`, `--hardy`, VCF export, and `vcf_subset` sample subsetting
- `vcf_subset --extract/--exclude` variant-ID filtering
- fresh-container, fail-fast execution for every independent smoke case

It does not replace validation on real GWAS cohorts, imputed dosage data,
multi-phenotype association models, or production-scale reference panels.
Additional checks cover exact runtime identity, multiallelic phased allele
frequencies, PCA, malformed/missing input diagnostics, and resource selection.
The a.7.11 regression modes cover small-P Sidak adjustment against an independent
formula, missing TEST-column diagnostics, mismatched-allele frequency import,
and negative-position removal with PGEN validation after `--update-map`.
These are runtime checks; Docker build-time tests remain lightweight.
Biobank-scale regressions, full-genome reference downloads, CUDA, Python/R API
workflows and production site deployment are not claimed by tiny smoke.
Current a.7.13-r1 validation (2026-10-16) uses the current candidate, not historical
a.7.11 receipts. Repository-root native Docker builds passed on amd64 and arm64.
The 27 exact probes (combined existence, 14 individual existence, 12 tests) passed
in all nine groups: Docker/Podman normal and read-only on both architectures,
plus the amd64 read-only Apptainer SIF from the same OCI content (243 commands).
Real wrapper checks passed on amd64 Docker/Podman/Apptainer and arm64 Podman
(120 checks), with final frozen-help/runtime/file-SHA/failure-log rechecks.
The additional arm64 Docker wrapper run was interrupted by Docker Desktop
becoming unavailable; it is not recorded as a completed combination. Native
arm64 build/exact smoke and the Docker backend axis are independently complete.
ARM64 Apptainer is not separately validated; no architecture-specific resource
or service dependency is claimed.

Closeout rechecked the current frozen help and its literal-quote examples on
amd64 Docker/Podman/Apptainer and arm64 Podman: 19 targeted checks per route
(76 total), plus 30 full wrapper checks and seven final identity/failure-log
checks per route. The ordinary-quote negative case is recorded as an expected
failure, not silently treated as supported argv behavior. The unchanged image
content also passed 135 fresh amd64 exact probes and 27 arm64 Podman read-only
probes during closeout; earlier native builds and the other exact groups remain
bound to the same Dockerfile, manifest and image contents.

Resource discovery has 57 isolated contract checks on each of macOS and Linux.
Only the two fixed site-root literals are mapped into private test directories;
the remaining production function is verified byte-for-byte. Tests cover root
priority, invalid higher-priority roots without fallback, symlinks, disable and
space-containing physical paths. Selected physical roots are then paired with
the actual wrapper's read-only mounts on all three backends. This validates the
selection contract and backend binding separately; it is not a claim that the
production `/usr/local/share` or `/opt/taffish` directories were deployed.

On amd64, seven resource interruption windows across INT/TERM/HUP passed on
all three backends (63 interruptions; 252 install/interrupt/recover/idempotent
receipts). Valid old members remained unchanged. Another 41 checks cover
private root-owned once-only installation, ordinary-user read-only reuse,
actual HTTPS/empty partial downloads, missing/bad/duplicate inventories and
recovery. The fixed GitHub software archive endpoint refused Range with curl 33;
the prefix was preserved, no member was promoted, and the exact offline source
recovered successfully. This is not a claim of successful HTTP Range service.
No production reference callset was downloaded or analyzed in this update.
Full production references, real-cohort correctness and actual production
system deployment remain outside the evidence.

Final image sizes: amd64 188,956,779 bytes; arm64 196,438,736 bytes.
Runtime libraries dominate (/usr/lib approximately 137/131 MiB); PLINK2 itself
uses approximately 4.5/3.9 MiB. Multi-stage builds exclude compiler/source archives;
APT indexes/cache are empty or negligible, and headers only 48/44 KiB.
Runtime and dependency license notices are retained rather than deleted for size.
The existing Action is unchanged and byte-identical to fresh `taf new` output.
Readiness, actual publication, Action/GHCR/Index success and scientific acceptance
remain separate gates.

## License and Citation

TAFFISH app packaging is Apache-2.0.

PLINK 2.0 upstream licensing is layered: the main application is GPL-3.0-or-later,
the include libraries and `vcf_subset` are LGPL-3.0-or-later, and bundled SIMDe,
libdeflate, and zstd components retain their own upstream licenses. License
files are copied into the container under `/opt/plink2/share/licenses/plink2/`.

Resource terms are separate: the official [resource page](https://www.cog-genomics.org/plink/2.0/resources)
describes HGDP as freely available for analyses and requests citation of
Bergström et al. (2020), Science 367. Review exact source terms/citation for
1000 Genomes/FASTA custom members; software GPL does not license those data.
System dependency copyright notices remain under `/usr/share/doc`.

If you use PLINK 2.0 in research, cite:

Chang CC, Chow CC, Tellier LCAM, Vattikuti S, Purcell SM, Lee JJ.
Second-generation PLINK: rising to the challenge of larger and richer datasets.
GigaScience. 2015;4:7. doi: `10.1186/s13742-015-0047-8`.
