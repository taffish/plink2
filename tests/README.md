# 资源安装器离线回归

在 app 根运行 `python3 tests/test-resources.py docker/plink2-resources`。
在 Linux 容器内需使用本候选中的 Python 与 helper；测试只在唯一临时目录创建合成资料。
覆盖固定清单、锁、缓存恢复、原子完成、权限、幂等、校验损坏、额外文件、symlink、
receipt 和无效 URL/大小/SHA/文件名。Apptainer 默认私有 umask 下也必须通过0644/0755门。
不下载真实数据；生产下载和真实wrapper只读共享是独立验收层。

## a.7.11 上游变化回归

manifest 中的 `plink2-smoke adjust/read-freq/update-map` 各自从空 scratch 开始：
小 P 值 Sidak 用独立公式和相对容差检查（不写死跨架构浮点尾数），
频率文件错配等位基因不能污染下一位点，负坐标删除后校验 PGEN/位点表一致。
另保留缺失 TEST 列的非零诊断。完整测试是 runtime smoke，不加入 Dockerfile
构建期硬门，也不修改上游算法。维护者证据包含旧 a.7.10 Sidak 负向对照、
错误版本/动态库/频率/校正结果/位点位置注入与原退出码保留。
