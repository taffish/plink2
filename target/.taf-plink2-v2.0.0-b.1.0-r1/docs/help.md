plink2 2.0.0-b.1.0-r1

Purpose: Genotype conversion, QC, allele frequencies, PCA and association analysis.

Usage:
  taf-plink2 -- --help
  taf-plink2 -- --version
  taf-plink2 -- --vcf input.vcf.gz --make-pgen --out cohort
  taf-plink2 -- --pfile cohort --freq --hardy --missing --out qc
  taf-plink2 -- --pfile cohort --grm-maf 0.05 --pca 10 --out pca
  taf-plink2 -- --pfile cohort --glm --pheno pheno.tsv --covar covar.tsv --out gwas
  taf-plink2 vcf_subset --in input.vcf.gz --out selected.vcf --extract variants.txt
  taf-plink2 ldsc --h2 trait.sumstats --ref-ld ref --w-ld weights --out h2
  taf-plink2 mtag --sumstats trait1,trait2 --ldscore ref.ldscore --out joint
  taf-plink2 pgen_compress cohort.bed converted.pgen SAMPLE_COUNT

Inputs and options:
  --pfile PREFIX     Reads PREFIX.pgen/.pvar/.psam; add vzs for .pvar.zst.
  --bfile PREFIX     Reads PLINK 1 .bed/.bim/.fam files.
  --vcf FILE         Imports VCF; --bcf/--bgen accept other genotype formats.
  --out PREFIX       Writable output prefix, including the .log file.
  --threads N        CPU limit. --memory N sets workspace MiB, not total RAM.
  Paths with spaces need inner quotes, including helper path options:
  taf-plink2 -- --pfile "'my cohort'" --freq --out "'my result'"
  Use simple names for quotes or shell metacharacters; see README for details.

Key outputs:
  .pgen/.pvar/.psam   Genotype datasets.
  .afreq/.hardy       Frequency and Hardy-Weinberg tables.
  .smiss/.vmiss       Missingness; .eigenvec/.eigenval PCA; .glm.* associations.

Choose backend (same analysis commands):
  TAFFISH_CONTAINER_BACKEND=docker taf-plink2 -- --version
  TAFFISH_CONTAINER_BACKEND=podman taf-plink2 -- --version
  TAFFISH_CONTAINER_BACKEND=apptainer taf-plink2 -- --version
  Apptainer needs native Linux; Docker/Podman also work through their Mac VM.

Optional reference resources (no default download):
  taf-plink2 plink2-resources list
  taf-plink2 plink2-resources install \
    --member hgdp-grch38-chry-noannot-20260930 --dry-run
  Prepare a persistent directory, then run from its parent:
  mkdir -p plink2-resources
  TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT=0 taf-plink2 plink2-resources install \
    --member hgdp-grch38-chry-noannot-20260930 --resource-root plink2-resources
  The same command verifies/skips a complete install. HTTP resume needs Range;
  a checksum mismatch fails closed. --source-dir DIR uses exact offline files.
  Personal root: ~/.local/share/taffish/resources/plink2
  Shared root: /usr/local/share/taffish/resources/plink2 (admin prepares once).

Read a prepared root (automatic mounts are read-only):
  export TAFFISH_PLINK2_RESOURCE_PATH=/usr/local/share/taffish/resources/plink2
  TAFFISH_CONTAINER_BACKEND=docker \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  TAFFISH_CONTAINER_BACKEND=podman \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  TAFFISH_CONTAINER_BACKEND=apptainer \
    taf-plink2 plink2-resources verify --resource-root /references \
    --member hgdp-grch38-chry-noannot-20260930
  Discovery needs host Python 3: personal -> /usr/local/share -> /opt/taffish.
  Invalid roots/receipts fail closed; custom catalogs are user-pinned, not signed.
  Set TAFFISH_PLINK2_RESOURCE_AUTO_MOUNT=0 for setup or manual mounts.
  Explicit legacy/custom mount fallback, with AUTO_MOUNT=0 (HOST is absolute):
  Docker: TAFFISH_DOCKER_RUN_ARGS="--volume 'HOST:/references:ro'"
  Podman: TAFFISH_PODMAN_RUN_ARGS="--volume 'HOST:/references:ro'"
  Apptainer: TAFFISH_APPTAINER_RUN_ARGS="--bind 'HOST:/references:ro'"
  Export the matching variable; colon/comma in host paths are not supported.
  Decompress .pgen.zst into your writable workdir:
  taf-plink2 -- --zst-decompress \
    /references/hgdp-grch38-chry-noannot-20260930/hgdp_chrY.pgen.zst hgdp_chrY.pgen
  Use --pgen hgdp_chrY.pgen --pvar /references/MEMBER/hgdp_chrY.pvar.zst
  and --psam /references/MEMBER/hgdp_chrY.psam (replace MEMBER with the ID).

Immediate notes:
  Tagged beta 1.0, not PLINK 1.9. PCA/GRM now reject very-low-MAF variants;
  --grm-maf explicitly filters them. Choose thresholds appropriate to your data.
  PGEN does not preserve genotype-probability triplets, read depths or quality.
  Choose reference callset/build explicitly; chrY is not a genome.
  Run from a writable project directory; missing local input does not download.

More help:
  taf-plink2 -- --help glm
  taf-plink2 plink2-resources --help
  https://www.cog-genomics.org/plink/2.0/
Wrapper options:
  taf-plink2 --help       Show this TAFFISH help.
  taf-plink2 --version    Show wrapper version.
  taf-plink2 --compile    Print generated shell; -- --help shows upstream help.
