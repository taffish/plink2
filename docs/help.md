plink2 2.0.0-a.7.2-r1

Purpose:
  PLINK 2.0 alpha runtime for large-scale genotype data management,
  population-genetics statistics, GWAS, PGEN workflows, and VCF sample or
  variant-ID subsetting.

Usage:
  taf-plink2 -- --help
  taf-plink2 -- --version
  taf-plink2 -- --dummy 100 1000 --make-pgen --out tiny
  taf-plink2 -- --pfile cohort --freq --out freq
  taf-plink2 -- --pfile cohort --glm --pheno pheno.tsv --out assoc
  taf-plink2 vcf_subset --help

Packaged commands:
  plink2        PLINK 2.0 command-line application
  vcf_subset    sample and variant-ID subsetting helper for VCF/VCF.GZ inputs

Common workflows:
  taf-plink2 -- --vcf input.vcf.gz --make-pgen --out cohort
  taf-plink2 -- --pfile cohort --freq --hardy --missing --out qc
  taf-plink2 -- --pfile cohort --pca approx --out pca
  taf-plink2 -- --pfile cohort --glm --covar covar.tsv --out gwas
  taf-plink2 vcf_subset --in input.vcf.gz --out subset.vcf.gz --keep samples.txt
  taf-plink2 vcf_subset --in input.vcf.gz --out selected.vcf.gz \
    --extract variants.txt
  taf-plink2 vcf_subset --in input.vcf.gz --out excluded.vcf.gz \
    --exclude variants.txt

Inputs:
  PLINK 2 PGEN sets    .pgen + .pvar + .psam
  PLINK 1 binary sets  .bed + .bim + .fam
  Variant formats      VCF/BCF/BGEN/Oxford formats supported by PLINK 2.0
  Metadata tables      phenotypes, covariates, sample and variant lists

Key outputs:
  .pgen/.pvar/.psam    PLINK 2 binary genotype datasets
  .afreq/.hardy/etc.   statistics and QC tables
  .glm.*               association-test outputs
  .vcf/.bed/etc.       exported formats requested with --export/--make-*

Platform and resources:
  Built from the upstream v2.0.0-a.7.2 source tag with the upstream
  build_dynamic CPU baseline: no AVX2 and no SSE4.2 requirement. BLAS/LAPACK
  are provided by Debian OpenBLAS/LAPACK dynamic libraries.
  Native container platforms are linux/amd64 and linux/arm64.

Boundaries:
  This is PLINK 2.0 alpha 7.2, not PLINK 1.9/1.07.
  The container does not bundle reference panels, phenotype files, covariates,
  genome FASTA files, or tutorial datasets.
  CUDA/GPU proof-of-concept builds and the Python/R pgen libraries are not
  exposed as runtime commands in this app.
  Smoke tests use tiny synthetic data and do not replace scientific validation
  on production GWAS datasets.

Detailed documentation:
  https://www.cog-genomics.org/plink/2.0/

Wrapper options:
  taf-plink2 --help       Show this TAFFISH help.
  taf-plink2 --version    Show TAFFISH wrapper version.
  taf-plink2 --compile    Compile the TAFFISH wrapper.
  taf-plink2 -- --help    Pass option-leading arguments to plink2.
