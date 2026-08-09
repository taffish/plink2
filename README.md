# plink2

`plink2` packages PLINK 2.0 alpha 7.3 for TAFFISH.

Package identity:

- name: `plink2`
- command: `taf-plink2`
- kind: `tool`
- version: `2.0.0-a.7.3-r1`
- image: `ghcr.io/taffish/plink2:2.0.0-a.7.3-r1`
- license: Apache-2.0 for TAFFISH packaging
- upstream tag: `v2.0.0-a.7.3`
- runtime: `PLINK v2.0.0-a.7.3` and `vcf_subset v1.1.0`
- upstream: <https://www.cog-genomics.org/plink/2.0/>

## What This App Packages

This app builds PLINK 2.0 from the official `chrchang/plink-ng` source tag
`v2.0.0-a.7.3`, posted on 8 August 2026. The default command is `plink2`; the
same source tree also provides the upstream `vcf_subset` helper.

Compared with alpha 7.2, alpha 7.3 fixes an overflow path that could make
`--hardy` and chromosome-X `--hwe` hang on biobank-scale inputs, and corrects
an autosomal `--hwe` corner case at thresholds just below the minimum positive
normal double. The upstream command surface, build dependencies, bundled
`vcf_subset` 1.1.0 helper, and layered license set are unchanged.

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

The container is built from source with the upstream `build_dynamic` baseline:
`NO_AVX2=1`, `NO_SSE42=1`, and `CPU_CHECK=1`. This avoids requiring AVX2 or
SSE4.2 instructions while still using OpenBLAS/LAPACK for linear algebra.

## Usage

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

No database or reference panel is bundled or required for basic PLINK 2.0
operation. Workflows needing phenotype/covariate tables, reference FASTA files,
genetic maps, LD reference panels, or imputation/reference resources should pass
those files explicitly through upstream PLINK 2.0 flags.

This app is intended to build natively on `linux/amd64` and `linux/arm64` from
source. The official upstream binary assets are primarily platform-specific
prebuilt zips; this TAFFISH app uses the source tag to provide a reproducible
container build.

## Reproducibility

- Upstream repository: <https://github.com/chrchang/plink-ng>
- Upstream documentation: <https://www.cog-genomics.org/plink/2.0/>
- Upstream tag: `v2.0.0-a.7.3`
- Upstream commit: `7b30cf1733c4f50c6699268a9f07fb6af206ed49`
- Source archive:
  `https://github.com/chrchang/plink-ng/archive/refs/tags/v2.0.0-a.7.3.tar.gz`
- Source SHA256:
  `7f0124c2f14b68a10ff4fcf79644858abde7d367e0e7f6ee1728e53ed025d0e6`

## Boundaries

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
The upstream a.7.3 regression involves biobank-scale genotype counts and is
therefore documented from the official release note and source diff rather
than recreated inside the tiny container smoke.

## License and Citation

TAFFISH app packaging is Apache-2.0.

PLINK 2.0 upstream licensing is layered: the main application is GPL-3.0-or-later,
the include libraries and `vcf_subset` are LGPL-3.0-or-later, and bundled SIMDe,
libdeflate, and zstd components retain their own upstream licenses. License
files are copied into the container under `/opt/plink2/share/licenses/plink2/`.

If you use PLINK 2.0 in research, cite:

Chang CC, Chow CC, Tellier LCAM, Vattikuti S, Purcell SM, Lee JJ.
Second-generation PLINK: rising to the challenge of larger and richer datasets.
GigaScience. 2015;4:7. doi: `10.1186/s13742-015-0047-8`.
