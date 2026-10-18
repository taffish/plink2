# 资源安装器离线回归

在 app 根运行 `python3 tests/test-resources.py docker/plink2-resources`。
在 Linux 容器内需使用本候选中的 Python 与 helper；测试只在唯一临时目录创建合成资料。
覆盖固定清单、锁、缓存恢复、原子完成、权限、幂等、校验损坏、额外文件、symlink、
receipt 和无效 URL/大小/SHA/文件名。Apptainer 默认私有 umask 下也必须通过0644/0755门。
不下载真实数据；生产下载和真实wrapper只读共享是独立验收层。

## 资源发现与路径边界

运行 `python3 tests/test-discovery.py --out <新的私有测试目录>`。
测试直接提取当前 `src/main.taf` 的资源发现函数，仅将两个site固定路径映射到该私有目录，
逐字逆变换断言其余函数未改，保存source/function SHA与57项回执。覆盖个人/site/override
优先级、失效symlink、损坏或空的高优先级root不回退、关闭开关和真实含空格物理目录。
这是隔离发现契约，不是生产system部署；须配合当前冻结wrapper的真实三backend只读bind。
空格参数测试还必须区分普通shell引号的已知失败与literal-quote成功，覆盖输入、输出及helper。
host `RESOURCE_PATH` 使用普通环境变量引号，不能误加literal-quote；见README与help。

## a.7.13 后继验收

`plink2-smoke mendel` 使用100个合成个体、20个位点和明确亲子关系，覆盖本次
Mendel error scan修复邻近路径；不修改上游科学代码，不主张完整科学正确性。
资源单元回归共23项，区分不存在/空/有效前缀/损坏partial、只读复用及no-replace promotion。
本轮另在app外保存真实wrapper三后端回执：7窗口×INT/TERM/HUP、中断恢复和幂等，
每例先安装有效旧成员并比较完整SHA。Apptainer外层先退出时独立限时检查清理。
HTTPS测试使用官方固定软件源码而非研究数据；GitHub tar端点不支持Range时应非零失败、
保留原前缀，用相同SHA离线文件恢复；不能把Range拒绝写成在线续传成功。

## a.7.11 上游变化回归

manifest 中的 `plink2-smoke adjust/read-freq/update-map` 各自从空 scratch 开始：
小 P 值 Sidak 用独立公式和相对容差检查（不写死跨架构浮点尾数），
频率文件错配等位基因不能污染下一位点，负坐标删除后校验 PGEN/位点表一致。
另保留缺失 TEST 列的非零诊断。完整测试是 runtime smoke，不加入 Dockerfile
构建期硬门，也不修改上游算法。维护者证据包含旧 a.7.10 Sidak 负向对照、
错误版本/动态库/频率/校正结果/位点位置注入与原退出码保留。
