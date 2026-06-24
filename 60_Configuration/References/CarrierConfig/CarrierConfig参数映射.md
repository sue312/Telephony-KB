---
doc_type: config
domain: Configuration
status: active
quality: curated
search_tier: reference_only
layer: AP/Framework/CarrierConfig
source: 运营商配置参考.xlsx; CarrierConfigManager.java
---

# CarrierConfig参数映射

<!-- REFERENCE_ONLY_BOUNDARY_START -->
## 使用边界

- 本页是字段表、参数表或外部片段，只用于查字段、查来源、做关键词回溯。
- 不作为流程结论、配置生效结论或真实问题第一坏点引用。
- 需要判断问题时，先回到对应主文档、排障流程或 Case。
<!-- REFERENCE_ONLY_BOUNDARY_END -->


## 阅读入口

- 本文是 CarrierConfig key 的总入口，只保留配置原则、分组统计和参数索引。
- 字段级大表已按 Group 拆到本目录；查具体 key 时先用索引定位分组，再回目标平台 CarrierConfigManager.java 复核默认值和消费者。



<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| AOSP CarrierConfig key | 按 APN / IMS / Call / MMS / Network 等分组索引 | `dumpsys carrier_config` |
| 字段级参考表 | `References/CarrierConfig` | 主文档只做入口，不重复大表 |
| 业务文档 | APN、IMS、ECC、SMS、网络图标等配置方法 | 关联业务现象和验证动作 |

### 使用链路

```text
业务现象
-> 本文定位 CarrierConfig key 分组
-> References/CarrierConfig 查字段
-> 对应配置方法文档验证生效链路
```

### 平台差异

| 平台 | 重点看点 | 验证口径 |
|---|---|---|
| Android common | AOSP 公共 XML、Provider、framework 读取点 | 先证明 common 默认值和运行时 dump 是否一致 |
| UNISOC | carrier overlay、CarrierService、Operator NV、modem profile | 同时看 AP log、产物配置、NV/readback 和 modem trace |
| MTK | vendor/mediatek 私有配置、SBP/DSBP/CXP、NVRAM | 结合 debuglogger、ELT/MD log、AP dump 验证最终值 |
| Qualcomm | CarrierConfig overlay、MCFG/QCRIL、modem profile | 结合 dumpsys、QXDM/QCAT、MCFG 产物确认 |

### 验证命令与 log

| 目标 | 证据入口 | 预期结论 |
|---|---|---|
| 源配置存在 | CarrierConfig XML / overlay / CarrierService | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | dumpsys carrier_config、CarrierConfigLoader log | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | 读取方业务 log，必要时结合 IMS/Data/Call trace | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

### 关联入口

| 入口 | 用途 |
|---|---|
| [配置目录 README](../../README.md) | 回到配置分类和放置规则 |
| [Case横向索引](../../../40_Case-Library/Case横向索引.md) | 查历史同类问题和第一坏点 |
| [平台代码入口](../../../50_Platform-Code/README.md) | 查厂商代码读取位置 |
| [常用命令](../../../70_Tools-Debug/Commands/常用命令.md) | 查 dumpsys、logcat 和 adb 命令 |

### 常见失败模式

| 现象 | 优先检查 | 第一坏点判断 |
|---|---|---|
| key 存在但无效 | 读取模块是否消费该 key、平台是否覆盖 | dump 正确不等于业务已采用 |
| key 找不到 | Android 版本、厂商私有 key、命名变化 | 先确认基线和平台差异 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 学习摘要

| 项目 | 结论 |
|---|---|
| 来源 | 早期运营商配置参考表；当前已按目标分支 `CarrierConfigManager.java` 过滤和补充。 |
| 默认值基准 | 字段级映射表的 `Default` 列作为日常配置的默认值缓存；来源快照为 `/home/wx/Project/Common/SPRDROID16_SYS_MAIN_W25.22.4/alps/frameworks/base/telephony/java/android/telephony/CarrierConfigManager.java` 中的 key 和 `sDefaults`。缓存缺失、冲突、目标平台大版本不同或准备落地前，再切到目标平台源码复核。 |
| 当前覆盖 | 平台列按 UNISOC、MTK、Qualcomm(qssi) 三份 `CarrierConfigManager.java` 计算；三平台均存在记为 `common`，否则记录实际支持平台。厂商自定义 key 不放入 common 映射。 |
| 使用边界 | 本表是字段含义和默认值索引，不等于可直接配置清单；实际配置仍需确认 MCC/MNC、carrier id、specific carrier id、GID/SPN/IMSI 匹配条件和运行时覆盖顺序。 |

## CarrierConfig配置原则

1. 日常解析需求表时，先以字段级映射表的 `Default` 列作为默认值缓存，不要每个 key 都重复回源码查 `sDefaults`。
2. 运营商 XML 只配置映射表或目标 `CarrierConfigManager.java` 中能证明存在的 key；如果查不到常量或默认值，先标记为 `Needs study`。
3. 需求值与默认值缓存一致时通常不配置，避免冗余覆盖；只有需要改变默认行为时才写入 carrier XML。
4. 缓存缺失、含义冲突、平台大版本不同、目标平台疑似私有修改或准备给出直接可应用补丁时，再回目标分支 `CarrierConfigManager.java` 复核 key 和 `sDefaults`。
5. 其他运营商 XML、厂商文档和历史知识库只用于辅助理解，不替代当前分支源码判断。
6. `平台` 列为 `common` 表示 UNISOC、MTK、Qualcomm(qssi) 三平台均存在；如果不是三平台都有，则写实际支持平台，例如 `UNISOC/MTK`。
7. 本文件不再维护原生标记列；厂商自定义 key 若后续确有代码消费者，应另建厂商扩展映射并标明读取点。

## 分组统计

| Group | 数量 |
|---|---:|
| 5G | 7 |
| APN | 7 |
| Call | 50 |
| DATA | 6 |
| Dialer | 8 |
| IMS | 30 |
| MMS | 31 |
| Network | 25 |
| Other | 7 |
| SIM | 4 |
| Statusbar | 1 |
| VVM | 6 |
| WIFI | 1 |

## 使用规则

1. 先用需求术语匹配 `Group` 和 `Description`，不要只凭英文描述改值。
2. 使用 `Default` 作为默认值缓存进行初筛；只有缓存缺失、冲突或落地前复核时，再到目标平台搜索 `Name`。
3. 如果需求值等于 `Default`，通常不要写入运营商 XML；如果仍需显式覆盖，必须说明原因。
4. 修改前记录匹配条件、旧值、目标文件；修改后用 `adb shell dumpsys carrier_config` 或相关日志验证运行时值。

## 拆分说明

字段级表格已按 Group 拆到 References/CarrierConfig。主文件只维护配置原则和索引；如果需要新增或刷新 key，优先刷新对应分组文件，同时保持本页统计和索引一致。

## 参数映射索引

| Group | 数量 | 入口 |
|---|---:|---|
| 5G | 7 | [5G.md](5G.md) |
| APN | 7 | [APN.md](APN.md) |
| Call | 50 | [Call.md](Call.md) |
| DATA | 6 | [DATA.md](DATA.md) |
| Dialer | 8 | [Dialer.md](Dialer.md) |
| IMS | 30 | [IMS.md](IMS.md) |
| MMS | 31 | [MMS.md](MMS.md) |
| Network | 25 | [Network.md](Network.md) |
| Other | 7 | [Other.md](Other.md) |
| SIM | 4 | [SIM.md](SIM.md) |
| Statusbar | 1 | [Statusbar.md](Statusbar.md) |
| VVM | 6 | [VVM.md](VVM.md) |
| WIFI | 1 | [WIFI.md](WIFI.md) |
