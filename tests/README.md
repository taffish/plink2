# 资源安装器离线回归

在 app 根运行 `python3 tests/test-resources.py docker/plink2-resources`。
在 Linux 容器内需使用本候选中的 Python 与 helper；测试只在唯一临时目录创建合成资料。
覆盖固定清单、锁、缓存恢复、原子完成、权限、幂等、校验损坏、额外文件、symlink、
receipt 和无效 URL/大小/SHA/文件名。Apptainer 默认私有 umask 下也必须通过0644/0755门。
不下载真实数据；生产下载和真实wrapper只读共享是独立验收层。
