# plink2

`plink2` packages the tagged PLINK 2.0 beta 1.2 for TAFFISH.

Package identity:

- name: `plink2`
- command: `taf-plink2`
- kind: `tool`
- version: `2.0.0-b.1.2-r1`
- image: `ghcr.io/taffish/plink2:2.0.0-b.1.2-r1`
- license: Apache-2.0 for TAFFISH packaging
- upstream tag: `v2.0.0-b.1.2`
- runtime: `PLINK v2.0.0-b.1.2`, `vcf_subset v1.1.0`, `ldsc (plink-ng) v0.1`,
  `mtag (plink-ng) v0.1`, and same-tag `pgen_compress`
- upstream: <https://www.cog-genomics.org/plink/2.0/>

## What This App Packages

This app builds PLINK 2.0 from the official `chrchang/plink-ng` source tag
`v2.0.0-b.1.2`, released on 25 October 2026 (runtime date: 24 October).
The default command is `plink2`; the same source tree supplies `vcf_subset`,
`ldsc`, `mtag` and `pgen_compress`.

This updates tagged beta 1.0 to beta 1.2. GitHub marks the Release
`draft=false, prerelease=false`, but upstream still calls PLINK 2 beta:
this is an official versioned beta release, not a final stable-version claim.
On 25 October 2026 the maintainer approved routine tracking of official,
versioned beta Releases meeting those two flags, without asking each time.
Rolling development snapshots, drafts and explicitly marked prereleases remain
outside that policy. Each successor still requires identity, compatibility and
full packaging checks; the policy does not waive failures or authorize publishing.
No upstream algorithm/source patch is applied.

Beta 1.1 fixes LD-score window handling and show-tags output-buffer corruption;
beta 1.2 fixes reduced-column missingness, multiallelic linear-batch covariate
output and several very-long-identifier/allele paths, and restores multiallelic
multinomial GLM support. See the official
[beta 1.2 notes](https://github.com/chrchang/plink-ng/releases/tag/v2.0.0-b.1.2).

Compatibility changes include low-MAF checks for PCA/GRM (`--grm-maf` makes
filtering explicit), stronger allele-uniqueness validation and new output/merge
paths. New PGEN features may not work with very old readers. Review upstream
release notes and keep the old version for reproducible existing analyses.

## Scope

This app supports:

- PLINK 2.0 genotype data management and conversion workflows.
- PGEN/PVAR/PSAM, PLINK 1 binary files, VCF/BCF/BGEN/Oxford-style inputs
  supported by upstream PLINK 2.0.
- Common QC/statistics/GWAS operations such as `--freq`, `--hardy`, `--missing`,
  `--pca`, `--glm`, `--make-pgen`, `--make-bed`, and `--export`.
- VCF sample and variant-ID subsetting through `vcf_subset`.
- Upstream C++ `ldsc` and `mtag` utilities for explicitly supplied summary
  statistics and LD-score inputs; these are not the separate Python projects.

This app does not package:

- PLINK 1.9/1.07 as a separate `plink` command.
- Reference panels, phenotype/covariate files, genome FASTA files, or tutorial
  datasets.
- CUDA/GPU proof-of-concept builds.
- The Python `pgenlib` wheel or R `pgenlibr` package as runtime libraries.

## Container Contents

- `plink2`: PLINK 2.0 beta command-line application.
- `vcf_subset`: helper for sample and variant-ID subsetting of VCF/VCF.GZ
  inputs.
- `ldsc`, `mtag`: the matching official C++ bundled utilities.
- `pgen_compress`: upstream pgenlib I/O utility; includes BED/PGEN conversion
  and separate-index output. Its source tag, rather than a version option,
  identifies the program.
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
`target/taf-plink2-v2.0.0-b.1.2-r1`; building a local candidate is not publishing.

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

Bundled summary-statistics utilities:

```sh
taf-plink2 ldsc --h2 trait.sumstats --ref-ld ref --w-ld weights --out h2
taf-plink2 mtag --sumstats trait1.sumstats,trait2.sumstats --ldscore ref.ldscore --out joint
```

Choose scientifically compatible LD scores, alleles and sample-size columns.
`mtag` without arguments prints usage and returns 1, as upstream implements it;
this is not a container failure. No reference or summary statistics download is
implicit. These tools write into their `--out` prefix, not the installation.

See the official [bundled utilities documentation](https://www.cog-genomics.org/plink/2.0/bundle)
for their supported interfaces and the LD Score regression (Bulik-Sullivan et al.,
2015) and MTAG (Turley et al., 2018) citation requirements.

The upstream pgenlib I/O utility also supports BED/PGEN conversion:

```sh
taf-plink2 pgen_compress cohort.bed converted.pgen SAMPLE_COUNT
taf-plink2 pgen_compress -u converted.pgen restored.bed
```

Replace `SAMPLE_COUNT` with the number of samples in the BED file. This utility
converts genotype storage only; keep the corresponding sample/variant metadata.
Use PLINK2's normal conversion commands for a complete dataset.

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
sample tables, a single FASTA, or an explicitly selected LD-score file family
with matching weights/annotation files, not the entire evolving resource family.
Summary statistics and estimated covariance matrices are project inputs, not
automatically chosen shared reference models.

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
Installation requires filesystem support for atomic no-replace directory rename.
Docker Desktop's gRPC FUSE host shares may reject it with `Invalid argument`;
the helper fails closed and retains the completed partial, never using an unsafe
overwriting rename. On macOS, retry the same install against the same host root
with `TAFFISH_CONTAINER_BACKEND=podman`; then Docker can verify and read that
prepared root. Native Linux filesystems are another supported preparation path.
Read-only reuse and normal analysis do not require this rename operation.
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
colon/comma in host paths are rejected. Host Python 3 is required when a managed
root is selected; without it, disable auto-mount and use explicit manual binds.
Installation, selected-member verification and automatic discovery first validate
all already installed members, including unrelated members outside the selected
catalog. A broken sibling blocks adding a new member before mutation; recovery
requires restoring valid bytes or selecting a new root, never deleting old members.
The frozen host validator and container helper share the same implementation:
member ID, version/license/source, exact inventory, bytes, hashes and integrity
markers must agree. Custom catalogs are user-pinned declarations, not signatures
or a guarantee of scientific suitability. Re-signing READY after corrupting the
receipt ID, byte count or required metadata cannot bypass these checks.
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
- Upstream tag: `v2.0.0-b.1.2`
- Upstream commit: `cc2c95e61c509d49aaf884d2ec0956a921770745`
- Source archive:
  `https://github.com/chrchang/plink-ng/archive/refs/tags/v2.0.0-b.1.2.tar.gz`
- Source SHA256:
  `cae10bba9c470c1adb336d8871f1ca071b9e57e2bf6c86677c208184c7dc4a42`
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
and tutorial companions were checked: no PLINK 2 beta GUI/plugin extra is
packaged upstream. RStudio is an external tutorial environment; legacy gPLINK/
Haploview are PLINK 1-era clients, not a PLINK 2 GUI contract. This app starts no
browser service. A future compatible GUI needs its own explicit review.

PLINK 2.0 is under active beta development. This app pins a specific tagged
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
The beta-specific checks add a non-concatenating sample merge with zero genotype
differences, a synthetic LD-score regression with an independent h2=0.3 oracle,
BED/PGEN/BED byte-for-byte round trips (embedded and separate indexes),
and a two-trait MTAG path with finite outputs. They do not substitute for large
cohort or estimator-validation studies. All these checks run at runtime, not
as fragile performance/numerical gates in the Docker build.

Current b.1.2-r1 runtime validation completed on 25 October 2026. No beta 1.0
PASS is reused as beta 1.2 evidence. The new `beta-missing` regression compares complete
and reduced-column sample missingness against explicit synthetic counts and
checks a 6,005-character variant ID survives the report.

| Native environment | Exact offline smoke | Real wrapper / resources |
| --- | --- | --- |
| xjp amd64 Docker | 36 normal + 36 non-root read-only | 52 checks; 84 signal/recovery/idempotency receipts |
| xjp amd64 Podman | 36 normal + 36 non-root read-only | 52 checks; 84 signal/recovery/idempotency receipts |
| xjp amd64 Apptainer | 36 on the same OCI converted to a read-only SIF | 52 checks; 84 signal/recovery/idempotency receipts |
| macOS ARM64 Docker VM | 36 normal + 36 non-root read-only | 51 Docker checks plus 2 explicitly recorded Podman preparation calls; gRPC FUSE install refusal and Docker read-only reuse verified |
| macOS ARM64 Podman VM | 36 normal + 36 non-root read-only | 52 checks; 36 signal receipts covering lock, pre-promotion and child-allocation windows |

The Docker/macOS row does **not** claim direct resource installation or signal
recovery on gRPC FUSE; use the preparation fallback above. The other four signal
windows were not separately rerun on ARM64 Podman. Full seven-window coverage
is from native xjp, not extrapolated to those untested combinations.
All five axes also passed ordinary-user directory/permission negative controls,
final image-source identity, expected failure diagnostics, and the unchanged
official GLM linear-batch regression. Resource-unit tests run inside the actual
wrapper, including Docker's supported container scratch filesystem.

An additional 41 xjp receipts cover fixed official **software source** HTTPS
downloads, empty/prefix partial recovery, idempotency, administrator-once
installation and three-backend read-only reuse. GitHub refused Range with curl
exit 33; the existing prefix survived and recovery used the exact verified
offline source, not a claim of successful online continuation. The isolated
Podman online fixture used slirp4netns after pasta rejected its private namespace;
all ordinary smoke remained offline. No host networking/security setting changed.

Final Docker inspect sizes: amd64 191,924,240 bytes (about 183 MiB),
ARM64 194,346,388 bytes (about 185 MiB). `/opt/plink2` is 7.3/6.4 MiB;
the remaining main cost is Debian/Python/OpenBLAS/LAPACK runtime libraries.
The multi-stage final image has no compiler or source tree; APT indexes and
download caches are cleared. Installed package lists and full layer history were
recorded; they are not dependency locks.

ARM64 Apptainer is not separately validated. No production reference-family
download, real-cohort scientific correctness or production site deployment is
claimed. Host-side discovery contract tests and actual read-only backend binds
are recorded separately from production system deployment.

The Action is byte-identical to fresh `taf new -d -t` output and is unchanged.
Publication, public CI/GHCR/Index success and scientific acceptance are separate
gates; this update task does not publish.

## License and Citation

TAFFISH app packaging is Apache-2.0.

PLINK 2.0 upstream licensing is layered: the main application is GPL-3.0-or-later,
the include libraries and `vcf_subset` are LGPL-3.0-or-later, and bundled SIMDe,
libdeflate, zstd and QD components retain their own upstream licenses. The new
`ldsc` and `mtag` sources are GPL-3.0-or-later. License
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
