# 资源安装器离线回归

在 app 根运行 `python3 tests/test-resources.py docker/plink2-resources`。
在 Linux 容器内需使用本候选中的 Python 与 helper；测试只在唯一临时目录创建合成资料。
覆盖固定清单、锁、缓存恢复、原子完成、权限、幂等、校验损坏、额外文件、symlink、
receipt 和无效 URL/大小/SHA/文件名。Apptainer 默认私有 umask 下也必须通过0644/0755门。
不下载真实数据；生产下载和真实wrapper只读共享是独立验收层。

## 资源发现与路径边界

运行 `python3 tests/test-discovery.py --out <新的私有测试目录>`。
测试直接提取当前 `src/main.taf` 的资源发现函数，仅将两个site固定路径映射到该私有目录，
解析冻结validator路径后逐字逆变换断言其余函数未改，保存source/function SHA与69项回执。覆盖个人/site/override
优先级、失效symlink、损坏或空的高优先级root不回退、关闭开关和真实含空格物理目录。
这是隔离发现契约，不是生产system部署；须配合当前冻结wrapper的真实三backend只读bind。
空格参数测试还必须区分普通shell引号的已知失败与literal-quote成功，覆盖输入、输出及helper。
host `RESOURCE_PATH` 使用普通环境变量引号，不能误加literal-quote；见README与help。
新增READY重新签名后的错误ID、大小、缺许可证负向；helper与自动挂载必须同时拒绝。
缺宿主Python3明确失败，不能静默跳过校验；关闭开关及手动bind另行验证。

## b.1.2 后继验收（2026-10-25）

当前共有36个exact探针：combined exist、18个单exist、17个独立test。
新增`beta-missing`：默认/精简列输出的sample missingness与独立合成计数一致，
6,005字符位点ID原样保留。官方GLM线性batch回归脚本原样在真实wrapper执行，
覆盖多表型、多等位位点、covariates与7种模型的batch/逐表型结果对照。
不修改上游算法，也不将这些完整数值测试放入Dockerfile构建硬门。

资源单元回归27项，另断言目标已存在时不覆盖、模拟不支持原子操作时明确失败并保留stage。
新成员安装/幂等复用/verify与自动发现统一校验整个已有库：坏的无关成员不能被绕过，
恢复和重复安装必须保持原有效成员SHA。xjp原生三后端重跑7窗口×INT/TERM/HUP，
各84份安装/中断/恢复/幂等回执；ARM64 Podman补3窗口的36回执，不冒称全部组合。
Docker Desktop gRPC FUSE不支持no-replace目录重命名：单独验收拒绝、partial保留、
Podman同路径恢复及Docker只读复用，不把该宿主共享目录的直接安装记作PASS。
Docker容器内/tmp资源单元门仍实跑通过。原始失败、环境限制及最终矩阵见维护者证据。

## b.1.0 历史后继验收

`beta-merge` 用16个合成样本拆分后纵向合并，检查16样本和24位点零基因型差异。
`ldsc` 使用300个合成记录的精确线性模型，独立检查h2=0.3，采用浮点容差。
`mtag` 用200个合成记录/两个trait/显式协方差，保留maxFDR计算，检查有限输出和正SE。
`compress` 覆盖 BED→PGEN→BED 逐字节往返，以及独立 PGI 索引模式。
这些验证封装可运行和基本数据通路，不冒充生产统计适用性；不改上游算法。
新版本必须重跑所有后端，不能引用历史版本PASS代替。当时共有35个exact探针：
combined exist、18个单exist、16个独立test；root context原生双架构构建另取证。

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
