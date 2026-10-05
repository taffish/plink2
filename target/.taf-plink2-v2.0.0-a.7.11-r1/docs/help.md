plink2 2.0.0-a.7.11-r1

Purpose:
  Genotype conversion, QC, allele frequencies, PCA and association analysis.

Usage:
  taf-plink2 -- --help
  taf-plink2 -- --version
  taf-plink2 -- --vcf input.vcf.gz --make-pgen --out cohort
  taf-plink2 -- --pfile cohort --freq --hardy --missing --out qc
  taf-plink2 -- --pfile cohort --maf 0.01 --pca 10 --out pca
  taf-plink2 -- --pfile cohort --glm --pheno pheno.tsv --covar covar.tsv --out gwas
  taf-plink2 vcf_subset --in input.vcf.gz --out selected.vcf --extract variants.txt

Inputs and options:
  --pfile PREFIX     Reads PREFIX.pgen/.pvar/.psam; add vzs for .pvar.zst.
  --bfile PREFIX     Reads PLINK 1 .bed/.bim/.fam files.
  --vcf FILE         Imports VCF; --bcf/--bgen accept other genotype formats.
  --out PREFIX       Writable output prefix, including the .log file.
  --threads N        CPU limit. --memory N sets workspace MiB, not total RAM.
  --seed N           Fix random seed where applicable.

Key outputs:
  .pgen/.pvar/.psam   Genotype datasets.
  .afreq/.hardy       Frequency and Hardy-Weinberg tables.
  .smiss/.vmiss       Missingness tables.
  .eigenvec/.eigenval PCA results; .glm.* contains association results.

Choose backend (same analysis commands):
  TAFFISH_CONTAINER_BACKEND=docker taf-plink2 -- --version
  TAFFISH_CONTAINER_BACKEND=podman taf-plink2 -- --version
  TAFFISH_CONTAINER_BACKEND=apptainer taf-plink2 -- --version
  Apptainer needs native Linux; Docker/Podman also work through their Mac VM.

Optional reference resources:
  List fixed members; no resource is chosen or downloaded by default:
  taf-plink2 plink2-resources list
  taf-plink2 plink2-resources install \
    --member hgdp-grch38-chry-noannot-20260930 --dry-run
  Prepare a persistent directory, then run from its parent:
  mkdir -p plink2-resources
  taf-plink2 plink2-resources install \
    --member hgdp-grch38-chry-noannot-20260930 --resource-root plink2-resources
  The same command verifies/skips a complete install. Partial downloads resume;
  a checksum mismatch fails closed. See README for a custom pinned catalog.
  Personal root: ~/.local/share/taffish/resources/plink2
  Shared root: /usr/local/share/taffish/resources/plink2 (admin prepares once).
  Users need read/traverse permissions; only the installer needs write access.

Read an already prepared root (replace the host path; all mounts are read-only):
  export TAFFISH_PLINK2_RESOURCE_PATH=/usr/local/share/taffish/resources/plink2
  TAFFISH_CONTAINER_BACKEND=docker \
    TAFFISH_DOCKER_RUN_ARGS="-v $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro" \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  TAFFISH_CONTAINER_BACKEND=podman \
    TAFFISH_PODMAN_RUN_ARGS="-v $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro" \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  TAFFISH_CONTAINER_BACKEND=apptainer \
    TAFFISH_APPTAINER_RUN_ARGS="--bind $TAFFISH_PLINK2_RESOURCE_PATH:/references:ro" \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  No automatic mount/discovery: the variable above is only your shell shorthand.
  Unset backend RUN_ARGS to stop mounting. Use host paths without spaces.
  Keep these mount settings for analysis. Decompress .pgen.zst into your workdir:
  taf-plink2 -- --zst-decompress \
    /references/hgdp-grch38-chry-noannot-20260930/hgdp_chrY.pgen.zst hgdp_chrY.pgen
  Use --pgen hgdp_chrY.pgen --pvar /references/MEMBER/hgdp_chrY.pvar.zst
  and --psam /references/MEMBER/hgdp_chrY.psam (replace MEMBER with the ID).

Immediate notes:
  Alpha 7 maintenance build, not beta 1 or PLINK 1.9. Review upstream caveats.
  PGEN does not preserve genotype-probability triplets, read depths or quality.
  Choose reference callset/build/sample policy explicitly; chrY is not a genome.
  Run from a writable project directory; missing local input does not download.

More help:
  taf-plink2 -- --help glm
  taf-plink2 vcf_subset --help
  taf-plink2 plink2-resources --help
  https://github.com/taffish/plink2
  https://www.cog-genomics.org/plink/2.0/

Wrapper options:
  taf-plink2 --help       Show this TAFFISH help.
  taf-plink2 --version    Show wrapper version.
  taf-plink2 --compile    Print generated shell; -- --help shows upstream help.
