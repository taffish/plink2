# plink2

`plink2` packages PLINK 2.0 alpha 7.11 for TAFFISH.

Package identity:

- name: `plink2`
- command: `taf-plink2`
- kind: `tool`
- version: `2.0.0-a.7.11-r1`
- image: `ghcr.io/taffish/plink2:2.0.0-a.7.11-r1`
- license: Apache-2.0 for TAFFISH packaging
- upstream tag: `v2.0.0-a.7.11`
- runtime: `PLINK v2.0.0-a.7.11` and `vcf_subset v1.1.0`
- upstream: <https://www.cog-genomics.org/plink/2.0/>

## What This App Packages

This app builds PLINK 2.0 from the official `chrchang/plink-ng` source tag
`v2.0.0-a.7.11`, posted on 1 October 2026. The default command is `plink2`; the
same source tree also provides the upstream `vcf_subset` helper.

This continues the existing alpha 7 maintenance track, not the separate beta 1
development build. The a.7.10 to a.7.11 source delta fixes negative-position
`--update-map`, mismatched-allele `--read-freq`, very small Sidak-adjusted P values,
long alleles in `--adjust-file`, and malformed-input diagnostics. Beta-only new commands are not
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
`target/taf-plink2-v2.0.0-a.7.11-r1`; building a local candidate is not publishing.

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
`receipt.json` and atomic same-filesystem promotion. Download concurrency is one.
Required free space is selected member bytes plus 16 MiB; decompression requires
additional project space. Completed files are reused after hashing; partial files
remain in `.partial-*`. A server refusing Range causes failure, not unsafe append.
Corruption fails closed. No destructive `--force`: preserve a damaged root for
inspection and install into a new root; directory existence alone never passes.

Personal root: `~/.local/share/taffish/resources/plink2`. Site alternatives:
`/usr/local/share/taffish/resources/plink2` or `/opt/taffish/resources/plink2`.
An administrator prepares the site root and installs once; member directories
are 0755, files 0644. Ensure all parents are traversable. Only the installer needs
write access; ordinary users verify/read via a read-only bind. This helper never
changes system permissions or installs into site directories automatically.

Discovery/override decision: no automatic host reference discovery/mounting.
Reference genotypes may be sensitive, and PLINK supports multiple scientifically
distinct paths; exposing a user's/site's repository implicitly is undesirable.
`TAFFISH_PLINK2_RESOURCE_PATH` below is only shell shorthand, not an interpreted
app setting. Choose a root explicitly; unset backend run arguments to disable
exposure. Resolve symlinks with `cd PATH && pwd -P` and use paths without spaces,
colon or comma in the examples. Member selection always remains explicit.

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

Set `TAFFISH_PLINK2_RESOURCE_PATH` to the absolute prepared host root, then export
the matching optional policy (append rather than overwrite existing site policy):

| Backend | Read-only exposure |
| --- | --- |
| Docker | `TAFFISH_DOCKER_RUN_ARGS="-v $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro"` |
| Podman | `TAFFISH_PODMAN_RUN_ARGS="-v $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro"` |
| Apptainer | `TAFFISH_APPTAINER_RUN_ARGS="--bind $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro"` |

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
- Upstream tag: `v2.0.0-a.7.11`
- Upstream commit: `5061eab9b72dc3c554f5f58fd756185c375963c2`
- Source archive:
  `https://github.com/chrchang/plink-ng/archive/refs/tags/v2.0.0-a.7.11.tar.gz`
- Source SHA256:
  `6b83f2ff0a2d59ed9693c7270935d59893729f451831e60fc7b646d91042ddce`
- Debian 12 slim base index:
  `sha256:3783cc01769c7b2b1b83a5c5ad96c815348e28ed7da68e2e3687004faa906251`

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
Native amd64 and arm64 app-root builds passed on 2026-10-03. Docker and Podman passed on
both architectures, normal and read-only roots; native amd64 Apptainer passed
with a read-only SIF from the same OCI.
The candidate passed 225 exact fresh/offline probes, 125 real-wrapper checks, 35 intentional
fault injections, and 16 resource-contract cases on each of five backend/platform
routes. Real wrapper tests include PCA/GWAS, stdin/quoted paths, persistent output,
fixed reference install/verify/decompression/frequencies and denied reference writes.
Fresh HTTPS download, partial-download continuation and read-only reuse by a second
ordinary UID were additionally validated on 2026-10-03. A control run against
a.7.10 reproduced premature Sidak underflow, while a.7.11 passed the same fixture.
Arm64 Apptainer is not separately validated; no architecture-specific mount/GPU/
GUI coupling was found. No backend exception is used. Actual root/system-wide
production deployment and entire resource-family scientific validation were not run.

Final image sizes: amd64 188,944,753 bytes, arm64 191,715,233 bytes. Multi-stage
builds keep compiler/source archives out of final images; size is primarily linear
algebra/runtime libraries and Python standard library. Runtime notices are retained;
headers/apt cache are negligible (48 KiB/12 KiB), not removable large build payloads.

Publication validation (2026-10-03): ordinary
`taf publish --build --release --dry-run` passed (`remote: checked`, `outcome: planned`),
without version renaming or a `--pre` bypass. The existing Action is unchanged and byte-identical to a freshly generated
`taf new` canonical workflow. These checks establish local readiness,
not actual publication, subsequent Action/GHCR/Index success or scientific acceptance.

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
