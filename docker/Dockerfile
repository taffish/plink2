FROM debian:12-slim@sha256:3783cc01769c7b2b1b83a5c5ad96c815348e28ed7da68e2e3687004faa906251 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ARG PLINK2_VERSION=2.0.0-b.1.0
ARG PLINK2_TAG=v2.0.0-b.1.0
ARG PLINK2_SHA256=07e08fe3a2c3287d5b85697fea95cb7885fbf0d877f792817237c3bf1343411f

# 基础镜像 digest 不锁定活动 APT 仓库；包修订/可得性可能变化。先区分网络、索引与下架，
# 核对 Debian 官方来源和架构；采用新依赖须重建双架构并复验离线 smoke/真实 wrapper。
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

# 固定 tag+SHA256 不保证永久可下载。404/TLS/截断先分类；旧材料仅接受同 SHA256 可信副本。
# 若采用新源码，核实 tag/commit/许可后更新上述身份并全量重验，不跳过校验或盲目重算哈希。
RUN set -eux; \
    curl -fsSL "https://github.com/chrchang/plink-ng/archive/refs/tags/${PLINK2_TAG}.tar.gz" -o plink2.tar.gz; \
    echo "${PLINK2_SHA256}  plink2.tar.gz" | sha256sum -c -; \
    tar -xzf plink2.tar.gz; \
    src="plink-ng-${PLINK2_VERSION}/2.0"; \
    make -C "$src/build_dynamic" -j"$(nproc)" SFX=; \
    make -C "$src/utils/vcf_subset" -j"$(nproc)" SFX=; \
    make -C "$src/utils/ldsc" -j"$(nproc)" SFX=; \
    make -C "$src/utils/mtag" -j"$(nproc)" SFX=; \
    mkdir -p /opt/plink2/bin /opt/plink2/share/doc/plink2 /opt/plink2/share/licenses/plink2; \
    cp "$src/build_dynamic/plink2" /opt/plink2/bin/plink2; \
    cp "$src/utils/vcf_subset/vcf_subset" /opt/plink2/bin/vcf_subset; \
    cp "$src/utils/ldsc/ldsc" /opt/plink2/bin/ldsc; \
    cp "$src/utils/mtag/mtag" /opt/plink2/bin/mtag; \
    cp "$src/README.md" /opt/plink2/share/doc/plink2/README.md; \
    cp "$src/COPYING" /opt/plink2/share/licenses/plink2/COPYING; \
    cp "$src/COPYING.LESSER" /opt/plink2/share/licenses/plink2/COPYING.LESSER; \
    cp "$src/simde/COPYING" /opt/plink2/share/licenses/plink2/simde-COPYING; \
    cp "$src/libdeflate/COPYING" /opt/plink2/share/licenses/plink2/libdeflate-COPYING; \
    cp "$src/zstd/COPYING" /opt/plink2/share/licenses/plink2/zstd-COPYING; \
    cp "$src/zstd/LICENSE" /opt/plink2/share/licenses/plink2/zstd-LICENSE; \
    cp "$src/include/LICENSE.QD" /opt/plink2/share/licenses/plink2/LICENSE.QD; \
    { \
      echo "PLINK 2.0 ${PLINK2_VERSION}"; \
      echo "Tag: ${PLINK2_TAG}"; \
      echo "Source: https://github.com/chrchang/plink-ng/archive/refs/tags/${PLINK2_TAG}.tar.gz"; \
      echo "SHA256: ${PLINK2_SHA256}"; \
      echo "Build: 2.0/build_dynamic plink2 plus 2.0/utils/{vcf_subset,ldsc,mtag}"; \
      echo "BLAS/LAPACK: Debian OpenBLAS/LAPACK dynamic libraries"; \
      echo "CPU baseline: upstream build_dynamic defaults NO_AVX2=1 NO_SSE42=1"; \
    } > /opt/plink2/share/doc/plink2/source.txt; \
    chmod 0755 /opt/plink2/bin/plink2 /opt/plink2/bin/vcf_subset /opt/plink2/bin/ldsc /opt/plink2/bin/mtag; \
    strip /opt/plink2/bin/plink2 /opt/plink2/bin/vcf_subset /opt/plink2/bin/ldsc /opt/plink2/bin/mtag

# Keep the upstream pgenlib I/O utility built by build_dynamic as well.
RUN cp "/tmp/plink2-build/plink-ng-${PLINK2_VERSION}/2.0/build_dynamic/pgen_compress" /opt/plink2/bin/pgen_compress \
 && chmod 0755 /opt/plink2/bin/pgen_compress \
 && strip /opt/plink2/bin/pgen_compress \
 && printf '%s\n' 'Bundled I/O utility: 2.0/build_dynamic/pgen_compress (same source tag)' >> /opt/plink2/share/doc/plink2/source.txt

FROM debian:12-slim@sha256:3783cc01769c7b2b1b83a5c5ad96c815348e28ed7da68e2e3687004faa906251

ENV DEBIAN_FRONTEND=noninteractive

# final APT 仍为活动仓库，非完整输入 lock；同 builder 的排查/更新门，已发布身份用后继修复。
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      bash \
      curl \
      python3 \
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
# helper 的 resources.json 固定 URL/大小/SHA，但第三方资源仍可能下架；保留许可边界。
# 下载失败不改 checksum；可信旧副本可用 --source-dir，新资源需新 catalog 身份和完整重验。
COPY docker/plink2-resources /opt/plink2/bin/plink2-resources
COPY src/resource_validation.py /opt/plink2/bin/resource_validation.py
COPY docker/resources.json /opt/plink2/share/resources.json
COPY docker/plink2-smoke /opt/plink2/bin/plink2-smoke

RUN chmod 0755 /opt/plink2/bin/plink2-resources /opt/plink2/bin/plink2-smoke

RUN set -eux; \
    ln -s /opt/plink2/bin/plink2 /usr/local/bin/plink2; \
    ln -s /opt/plink2/bin/vcf_subset /usr/local/bin/vcf_subset; \
    ln -s /opt/plink2/bin/ldsc /usr/local/bin/ldsc; \
    ln -s /opt/plink2/bin/mtag /usr/local/bin/mtag; \
    ln -s /opt/plink2/bin/pgen_compress /usr/local/bin/pgen_compress; \
    test -x /opt/plink2/bin/pgen_compress; \
    plink2 --version 2>&1 | grep -Fx "PLINK v2.0.0-b.1.0 64-bit (19 Oct 2026)" >/dev/null; \
    ldsc --version 2>&1 | grep -Fx "ldsc (plink-ng) v0.1" >/dev/null; \
    mtag --version 2>&1 | grep -Fx "mtag (plink-ng) v0.1" >/dev/null; \
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
