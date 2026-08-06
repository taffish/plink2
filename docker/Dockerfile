FROM debian:12-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive
ARG PLINK2_VERSION=2.0.0-a.7.2
ARG PLINK2_TAG=v2.0.0-a.7.2
ARG PLINK2_SHA256=427455047b636c742d55098d4471fd2c4cbacb87fad2c201c32a8fb4efe00eb3

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      build-essential \
      liblapack-dev \
      liblapacke-dev \
      libopenblas-dev \
      zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/plink2-build

RUN set -eux; \
    curl -fsSL "https://github.com/chrchang/plink-ng/archive/refs/tags/${PLINK2_TAG}.tar.gz" -o plink2.tar.gz; \
    echo "${PLINK2_SHA256}  plink2.tar.gz" | sha256sum -c -; \
    tar -xzf plink2.tar.gz; \
    src="plink-ng-${PLINK2_VERSION}/2.0"; \
    make -C "$src/build_dynamic" -j"$(nproc)" SFX=; \
    make -C "$src/utils/vcf_subset" -j"$(nproc)" SFX=; \
    mkdir -p /opt/plink2/bin /opt/plink2/share/doc/plink2 /opt/plink2/share/licenses/plink2; \
    cp "$src/build_dynamic/plink2" /opt/plink2/bin/plink2; \
    cp "$src/utils/vcf_subset/vcf_subset" /opt/plink2/bin/vcf_subset; \
    cp "$src/README.md" /opt/plink2/share/doc/plink2/README.md; \
    cp "$src/COPYING" /opt/plink2/share/licenses/plink2/COPYING; \
    cp "$src/COPYING.LESSER" /opt/plink2/share/licenses/plink2/COPYING.LESSER; \
    cp "$src/simde/COPYING" /opt/plink2/share/licenses/plink2/simde-COPYING; \
    cp "$src/libdeflate/COPYING" /opt/plink2/share/licenses/plink2/libdeflate-COPYING; \
    cp "$src/zstd/COPYING" /opt/plink2/share/licenses/plink2/zstd-COPYING; \
    cp "$src/zstd/LICENSE" /opt/plink2/share/licenses/plink2/zstd-LICENSE; \
    { \
      echo "PLINK 2.0 ${PLINK2_VERSION}"; \
      echo "Tag: ${PLINK2_TAG}"; \
      echo "Source: https://github.com/chrchang/plink-ng/archive/refs/tags/${PLINK2_TAG}.tar.gz"; \
      echo "SHA256: ${PLINK2_SHA256}"; \
      echo "Build: 2.0/build_dynamic plink2 plus 2.0/utils/vcf_subset vcf_subset"; \
      echo "BLAS/LAPACK: Debian OpenBLAS/LAPACK dynamic libraries"; \
      echo "CPU baseline: upstream build_dynamic defaults NO_AVX2=1 NO_SSE42=1"; \
    } > /opt/plink2/share/doc/plink2/source.txt; \
    chmod 0755 /opt/plink2/bin/plink2 /opt/plink2/bin/vcf_subset; \
    strip /opt/plink2/bin/plink2 /opt/plink2/bin/vcf_subset

FROM debian:12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      bash \
      gawk \
      gzip \
      grep \
      liblapack3 \
      liblapacke \
      libopenblas0-pthread \
      sed \
      zlib1g \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/plink2 /opt/plink2

RUN set -eux; \
    ln -s /opt/plink2/bin/plink2 /usr/local/bin/plink2; \
    ln -s /opt/plink2/bin/vcf_subset /usr/local/bin/vcf_subset; \
    plink2 --version 2>&1 | grep -F "PLINK v2.0.0-a.7.2" >/dev/null; \
    plink2 --help 2>&1 | grep -F -- "--make-pgen" >/dev/null; \
    vcf_subset --version 2>&1 | grep -F "vcf_subset v1.1.0" >/dev/null; \
    vcf_subset --help 2>&1 | grep -F "Usage: vcf_subset" >/dev/null; \
    vcf_subset --help 2>&1 | grep -F -- "--extract" >/dev/null; \
    vcf_subset --help 2>&1 | grep -F -- "--exclude" >/dev/null; \
    tmp=/tmp/taf-plink2-build-check; \
    rm -rf "$tmp"; \
    mkdir -p "$tmp"; \
    cd "$tmp"; \
    plink2 --dummy 8 12 --make-pgen --out tiny > dummy.log 2>&1; \
    test -s tiny.pgen; \
    test -s tiny.psam; \
    test -s tiny.pvar; \
    plink2 --pfile tiny --freq --out freq > freq.log 2>&1; \
    test -s freq.afreq; \
    grep -F "#CHROM" freq.afreq >/dev/null; \
    printf '%s\n' '##fileformat=VCFv4.2' '##contig=<ID=chr1,length=1000>' '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' '#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	s1	s2' 'chr1	10	rs1	A	G	50	PASS	.	GT	0/0	0/1' > tiny.vcf; \
    vcf_subset --in tiny.vcf --out keep.vcf --indv s2 > vcf_subset.log 2>&1; \
    test -s keep.vcf; \
    grep "^#CHROM" keep.vcf | grep -F "s2" >/dev/null; \
    if grep "^#CHROM" keep.vcf | grep -F "s1"; then exit 1; fi; \
    cd /; \
    rm -rf "$tmp"; \
    ldd "$(command -v plink2)" > /tmp/plink2-ldd.txt; \
    grep -F "libopenblas" /tmp/plink2-ldd.txt >/dev/null; \
    grep -F "liblapack" /tmp/plink2-ldd.txt >/dev/null; \
    grep -F "libz.so" /tmp/plink2-ldd.txt >/dev/null; \
    if grep -F "not found" /tmp/plink2-ldd.txt; then exit 1; fi

ENV TAFFISH_ENV=TAFFISH
ENV TAFFISH_NAME=plink2
ENV PATH=/opt/plink2/bin:${PATH}

WORKDIR /work
