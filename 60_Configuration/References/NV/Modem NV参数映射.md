---
doc_type: config
domain: Configuration
status: active
quality: imported_reference
search_tier: reference_only
platform: Cross-Platform
current_coverage: UNISOC, Qualcomm, MTK
future_coverage: TBD
layer: Modem/Operator NV
source: 运营商配置参考.xlsx; 105256__4G平台Modem运营商NV参数配置指南V1.1.pdf; Qualcomm QUTS nvGetItemDefinition/parseMBN; Qualcomm qcom4490 MCFG source
---

# Modem NV参数映射

<!-- REFERENCE_ONLY_BOUNDARY_START -->
## 使用边界

- 本页是字段表、参数表或外部片段，只用于查字段、查来源、做关键词回溯。
- 不作为流程结论、配置生效结论或真实问题第一坏点引用。
- 需要判断问题时，先回到对应主文档、排障流程或 Case。
<!-- REFERENCE_ONLY_BOUNDARY_END -->


本文件是 Modem/Operator NV 参数映射总入口，只做“字段映射和资料索引”。当前已沉淀 UNISOC、Qualcomm MCFG/MBN 与 MTK NV 参数映射；不同平台不能直接套用字段名和默认值。

## 阅读入口

1. 本文件很大，后续处理运营商需求时不要全文顺序读取；先用章节索引、平台名、EFS路径、NV名、字段名或 id 定位。
2. 字段级大表已拆到本目录；不要把运营商案例写进参数映射主表。
3. 本文件和同目录字段表同时作为候选映射索引和默认值缓存；日常解析需求表时先用缓存初筛，缓存缺失、冲突、版本敏感或准备落地前，再结合目标分支默认值、源码上下文、生成产物和设备运行值确认。
4. 具体写入、生成、刷机、版本和 running NV 验证看 [NV参数配置](../../Core-Config/NV参数配置.md)。

职责边界：

| 本文负责 | 不在本文证明 |
|---|---|
| 字段候选、来源文档、默认表、平台差异和 `References/NV` 大表入口 | 某个字段已经在目标设备生效 |
| UNISOC / MTK / Qualcomm 字段名、LID、EFS path、MCFG XML 的索引读法 | 工具写入、生成 bin/image、刷入和回读 |
| 标注字段含义置信度和跨平台不可套用边界 | 项目级最终 patch 和实机结论 |

<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| UNISOC Operator NV 文档 | 字段定义和分组说明 | NVTool / readback 对照 |
| Qualcomm MCFG / NV 映射 | 字段级大表入口 | MCFG 产物和运行时 modem 行为 |
| 拆分字段表 | `References/NV` 下的大表 | 主文档只做索引和读法，不承载全量字段 |

### 使用链路

```text
需求字段 / 历史问题关键词
-> 本文找到 NV 分组
-> References/NV 查字段含义
-> 回到 NV参数配置 确认写入和运行时验证
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
| 源配置存在 | fixnv / operator NV / MCFG / NVTool 导入文件 | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | NVTool readback、版本号、modem 运行时读取值 | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | modem NV trace、能力开关、profile 选择 | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

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
| 查到字段但不知道怎么验证 | 回到 `NV参数配置.md` 的读写和回读方法 | 映射表只解释字段，不证明生效 |
| 字段名相似 | 平台、分组、版本、operator profile | 不跨平台套用字段 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 学习摘要

| 项目 | 结论 |
|---|---|
| 来源 | UNISOC：`运营商配置参考.xlsx` 的 `Modem NV`、`TS.32`、`Default NV` sheets，以及 `105256__4G平台Modem运营商NV参数配置指南V1.1.pdf`。 |
| 抽取规模 | Excel：Modem NV 136 条；TS.32 82 条；Default NV 671 条。PDF：55 页，识别到约 309 个 NV/字段项。 |
| 适用范围 | UNISOC Operator NV / RDNV / NVTool 口径已确认；Qualcomm 已沉淀 MCFG/MBN 中 IMS、MMODE、Data 相关常用 EFS NV 字段；MTK 已补充面向运营商需求配置的 IMS、UT/XCAP、网络能力 NV 字段映射表。 |
| 配置链路 | NV 不能只看源文件，需要同时确认 NV 工程/工具、版本或 VERNO、生成 bin/image、打包/刷入路径和设备端 running NV。 |
| 验证边界 | 插卡触发运营商参数加载后，才能用 running NV、Adaptive Parameter Configuration、modem log 或工具导出确认运行值。 |

## UNISOC Operator NV配置原则

1. 日常解析需求表时，先用 `*字段映射.md` 的默认值作为缓存基线，不要每个字段都重复回 `default.nv` 搜索。
2. 运营商 `.nv` 中只配置与默认值缓存不同的项；需求值等于默认值时不配置，避免冗余和后续维护误判。
3. 除 `PLMN=` 这类运营商匹配入口外，待配置项必须能在字段映射表或同平台 `default.nv` 中找到同一路径；如果找不到，先标记为 `Needs study`，不要直接写入运营商 `.nv`。
4. 缓存缺失、含义冲突、目标 modem 包版本不同、涉及私有/风险 NV 或准备给出直接可应用补丁时，再回目标 `OperatorNV/Operator_Cfg/default.nv` 复核路径和默认值。
5. XML schema、PDF、其他运营商样例只能用于理解含义和取值，不能替代 `default.nv` 做最终落地判断。

## UNISOC PDF学习摘要（105256 V1.1）

### 文档定位

| 项目 | 结论 |
|---|---|
| 文档 | `105256__4G平台Modem运营商NV参数配置指南V1.1.pdf` |
| 标题 | 4G 平台 Modem 运营商 NV 参数配置指南 |
| 版本日期 | V1.1，2025-09-04 |
| 页数 | 55 页 |
| 作用 | 说明 modem 侧可配置运营商 NV 的加载方式、使用说明和适用范围，不只是参数清单。 |
| 字段口径 | 每项围绕 `NV 名称`、`加载方式`、`使用说明`、`作用域` 理解。 |
| 加载方式 | PDF 中常见 `随卡`、`随网` 两类；配置和验证时必须确认触发条件。 |

### 章节与参数主题

| PDF章节 | 识别项数 | 主题 | 代表参数 |
|---|---:|---|---|
| 2.1 搜选网 | 9 | PLMN 搜索、漫游、RPLMN、band 优先级 | `chg_to_auto_mode_cfg`、`hplmn_search_time`、`band_priority_list[0~9]` |
| 2.2 注册 | 99 | 2G/3G/LTE 安全算法、IMS 注册、IPsec、VoWiFi 基础开关和定时器 | `a5_config[0]\a5_1`、`eea_eia_config`、`sip_regExpireSec`、`sip_ipsecEnabled`、`ims_over_wifi_enable[0]` |
| 2.3 数据服务 | 18 | 默认 APN、IMS PDP、PDP 类型和漫游数据行为 | `need_config_default_apn`、`default_APN_info\apn_name`、`inner_ip_type_ims` |
| 2.4.1 普通电话 | 42 | VoLTE/VoWiFi 普通语音、RTP/RTCP、SIP 会话策略 | `audio_RTCPEnabled`、`audioRtpTimeout`、`NoAnswerTimer` |
| 2.4.2 视频电话 | 8 | ViLTE 媒体能力和视频协商 | `video_codec_type`、`video_rtcpFbEnable`、`imageattr_support` |
| 2.4.3 会议电话 | 3 | IMS conference 策略 | `conf_uri`、`confSubscribe_inDialog`、`confRefer_inDialog` |
| 2.4.4 紧急电话 | 25 | SOS APN、紧急呼叫 IMS/VoWiFi 策略、紧急场景切换 | `sos_APN_info\apn_name`、`vowifi_ecc`、`epdg_apn_sos` |
| 2.4.5 语音编码 | 24 | AMR/AMR-WB/EVS codec 能力、mode set、payload | `audio_codec_type`、`evs_prim_min_bw`、`evs_payloadtype` |
| 2.5 附加业务 | 28 | UT/SS、呼转、补充业务定时器和 URI | `ss_BsfUri`、`ss_ActCFNLEnable` |
| 2.6 短信业务 | 4 | IMS SMS、CS SMS、NAS SMS 策略 | `sms_using_ims`、`mn_forbid_send_nas_sms` |
| 2.7 彩信业务 | 3 | MMS 相关承载或策略 | `epdg_apn_mms`、`inner_ip_type_mms`、`no_init_notify_mms` |
| 2.8 VoWiFi 和 3GPP 间 handover | 22 | WiFi/蜂窝阈值、漫游、VoLTE/VoWiFi 切换抑制 | `wifi_idle_rssi_low`、`cell_pref_4g_dbm_low`、`volte_vowifi_call_ho_forbidden` |
| 2.9 测量 | 1 | EUTRA measurement report 能力 | `eutra_measure_and_report_supported` |
| 2.10 3GPP 能力属性 | 21 | UE capability、HSPA/LTE 能力开关 | `cellcap_current`、`pdcp_sn_extension_r11`、`ue_specificrefsigssupported` |
| 2.11 虚拟运营商加载 | 1 | MVNO 运营商 NV 选择条件 | `mvno_info[0]` |
| 2.12 伪基站过滤 | 1 | 伪基站过滤策略 | `avoid_pseudo_base_station` |

### 关键学习结论

1. PDF 是 UNISOC modem 侧 Operator NV 的机制文档，配置时要同时看参数名、加载方式、使用说明和作用域。
2. `随卡` 参数依赖 SIM/运营商匹配，通常需要目标 SIM 或白卡触发后验证；`随网` 参数依赖当前注册网络或 PLMN 条件，不能只用静态文件判断是否生效。
3. 数据服务章节包含默认 APN 相关 modem NV。当前知识库仅把它作为 modem NV 学习内容记录，后续若要实际维护 APN provisioning，应单独扩展范围。
4. `need_config_default_apn=0` 时，AP/CP 默认 APN 配置不会被使用；如果 AP 侧下发默认 APN 且与 CP 侧注册后行为不一致，可能触发 reattach，部分认证场景可能不允许。
5. IMS、VoLTE、VoWiFi 相关项大量使用 bitmask、timer、algorithm list 和 profile 组合，不能只根据运营商需求表中的英文描述盲配单个字段。
6. `vowifi_ecc` 是紧急呼叫 VoWiFi/3GPP 策略 bitmask，bit1 与 bit3、bit2 与 bit4 等组合存在冲突风险，必须成组检查。
7. `mvno_info[0]` 用 SPN、IMSI、GID、PNN、ICCID 等条件选择虚拟运营商 NV，属于运营商匹配入口，不是普通功能开关。
8. `avoid_pseudo_base_station` 是伪基站过滤相关 NV，适用范围和网络侧条件需要结合 modem log 验证。

## 平台扩展结构

| 平台 | 当前状态 | 后续映射入口 | 注意 |
|---|---|---|---|
| UNISOC | 已沉淀 | 本文件的 UNISOC PDF 摘要、UNISOC Modem NV、UNISOC TS.32、UNISOC Default NV 章节 | 按 Operator NV / RDNV / NVTool / running NV 口径验证。 |
| Qualcomm | 已沉淀常用 MCFG/MBN 字段级映射 | 本文件的 Qualcomm Modem NV / MCFG 字段级映射章节 | 不能套用 UNISOC 字段名；落地以 MCFG XML、MBN parse 结果、QUTS/NV Browser 字段定义和设备端运行值共同验证。 |
| MTK | 已沉淀面向运营商需求配置的 NV 参数映射表 | `MTK-Modem-NV字段映射.md` | 仅保留需求到 NV/LID/字段的映射；SBP/OTA/代码统计不放在映射表中。 |
## UNISOC代码侧学习（SPRDROID13 unisoc_bin）

### 学习范围

| 项目   | 结论                                                                                                                                                               |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 代码路径 | `/home/wx/Project/Common/SPRDROID13_VND_RLS_23A/alps/vendor/sprd/release/unisoc_bin`                                                                             |
| 本次重点 | `4g_modem_22b`、`5g_modem_v2_23b` 下的 modem release package；WCN、GNSS、AudioDSP 目录不作为本次 Operator NV 学习范围。                                                            |
| 4G样例 | `4g_modem_22b/9863a/sharkl3_pubcp_customer_builddir/sharkl3_pubcp_customer_nvitem`：OperatorNV XML 351 个，Operator_Cfg `.nv` 771 个，RDNV XML 146 个，CustNV XML 98 个。 |
| 5G样例 | `5g_modem_v2_23b/ums9621/QogirN6Lite_PS_builddir/QogirN6Lite_PS_nvitem`：OperatorNV XML 361 个，Operator_Cfg `.nv` 791 个，RDNV XML 212 个，CustNV XML 738 个。           |
| 版本线索 | `4g_modem_22b/9863a/version.txt` 显示 `4G_MODEM_22B_W25.26.1`。                                                                                                     |

### 源文件与产物关系

| 类型 | 位置/示例 | 作用 | 配置判断 |
|---|---|---|---|
| Operator NV 模块定义 | `*_nvitem/OperatorNV/*.xml` | 定义 `OPERATOR_NV_*` 模块、item 名、id、结构体类型、字段路径、数组维度、默认值和描述。 | 查字段是否存在、默认值是什么、完整路径怎么写。 |
| Operator NV 工程 | `*_nvitem/OperatorNV/operator_nvitem.xprj` | `nvtype="1"`，目标通常是 `../*_operator_nvitem.bin`，并列出参与编译的 OperatorNV XML 模块。 | 新增 XML 模块或确认模块是否入工程时必须检查。 |
| Operator NV 槽位配置 | `*_nvitem/OperatorNV/operator_nvitem.cfg` | 定义 `OPERATOR_NV_BIN_*` 这类 operator NV bin 槽位。 | 目前只作为工程结构线索，槽位含义还需结合工具或 modem 代码继续确认。 |
| 运营商覆盖 | `*_nvitem/OperatorNV/Operator_Cfg/*.nv` | 按运营商/PLMN 覆盖 Operator NV，格式通常是 `PLMN=...` 加 `OPERATOR_NV_模块\item\字段=value`。 | 做运营商差异配置时优先看这里，而不是直接改全局默认 XML。 |
| RDNV 工程 | `*_nvitem/RDNV/rd_nvitem.xprj` | `nvtype="0"`，目标通常是 `../*_nvitem.bin`；RDNV 工程尾部会引用 `../OperatorNV/operator_nvitem.xprj` 和 `../CustNV/cust_nvitem.xprj`。 | `*_nvitem.bin` 不是只看 RDNV XML，需要确认 OperatorNV/CustNV 子工程也参与生成。 |
| CustNV 工程 | `*_nvitem/CustNV/cust_nvitem.xprj` | `nvtype="2"`，目标通常是 `../*_cust_nvitem.bin`。 | RF、音频、客户定制、SIMLock 等不属于当前 Operator NV 配置主线，修改需谨慎。 |
| DeltaNV | `*_nvitem/DeltaNV/*.nv`、`*_deltanv.bin` | 产品/客户 delta 覆盖，示例路径使用 `PS_NV_PARAMS\...`，和 Operator_Cfg 的 `OPERATOR_NV_*` 路径不同。 | 不能把 DeltaNV 当成运营商 Operator NV；它更像产品差异或客户差异。 |
| 打包入口 | `vendor/sprd/release/pac_config/*.ini` | PAC 中可见 `NV_LTE`/`NV_NR` 指向 `*_nvitem.bin`，`Modem_LTE_DELTANV`/`Modem_NR_DELTANV` 指向 `*_deltanv.bin`。 | 验收不能只看 XML 或 `.nv`，要追到 PAC/镜像实际使用的 bin。 |

### Operator_Cfg格式

```text
PLMN=42403
OPERATOR_NV_IMS\ims_over_3gpp\ims_over_3gpp_enable\ims_over_3gpp_enable[0]=1
OPERATOR_NV_IMS\ims_reg_retry_timer\sip_regRetryTimer\sip_regRetryTimer[0]\sip_regRetryMaxTime=600
OPERATOR_NV_MN\mn_apn_info\apn_info_all\apn_info_all[0]\ims_APN_info\apn_name="ims"
```

1. `PLMN=` 支持多个 PLMN，用逗号分隔；要保留 5 位/6 位 MCCMNC 精度，不能把 `72201` 这类 5 位写成 6 位。
2. 覆盖路径格式是 `OPERATOR_NV_模块\item\结构字段\数组索引\子字段=value`，应回到对应 XML 校验 item、字段名、数组下标和默认值。
3. 文件名可以体现运营商或 MVNO，例如 `AR_Movistar_mvno.nv`；是否真实 MVNO 还要结合 `PLMN=`、`mvno_info[0]` 和 SIM 条件验证。
4. `.nv` 中可能出现 APN 相关字段。当前只把它作为 modem Operator NV 结构事实记录，不代表 APN provisioning 已纳入当前配置范围。

### 代码侧验证要点

1. 定位参数时先用 `rg` 查 `OperatorNV/*.xml`，确认完整字段路径，例如 `mn_need_config_default_apn.xml` 中 `need_config_default_apn[0]` 默认值为 `0`，`ims_reg_expire.xml` 中 `sip_regExpireSec[0]` 默认值为 `600000`。
2. 做运营商专属值时查 `Operator_Cfg/<operator>.nv` 是否已有覆盖；如果只改 XML 默认值，会影响全局默认，不等价于某个运营商需求。
3. `mn_vowifi_ecc.xml` 的 `vowifi_ecc[0]` 默认值为 `0`，XML 描述里的 bit0-bit4 与 PDF 中紧急呼叫 VoWiFi 策略一致，配置时必须按 bit 组合验证。
4. `gas_avoid_pseudo_base_station.xml` 属于 `OPERATOR_NV_GAS`，字段 `avoid_pseudo_base_station[0]` 默认值为 `0`，需要结合 GSM 场景 modem log 验证运行值。
5. 生成物至少要核对 `*_operator_nvitem.bin`、`*_cust_nvitem.bin`、`*_nvitem.bin`、`*_deltanv.bin` 是否更新；PAC 样例主要引用 `*_nvitem.bin` 与 `*_deltanv.bin`，不能只看单独的 `*_operator_nvitem.bin`。
6. RDNV、CustNV、OperatorNV、DeltaNV 的边界必须分清。Operator NV 用 `OPERATOR_NV_*` 路径，DeltaNV 示例用 `PS_NV_PARAMS\...` 路径，两者不是同一类配置入口。
7. 代码中的 XML `flag` 字段暂不直接等同 PDF 的 `随卡/随网`，这个映射还需要结合 NV 工具或 modem 加载代码继续确认。

## 分组统计

### UNISOC Modem NV sheet

| Category | 数量 |
|---|---:|
| VoLTE | 71 |
| VoWiFi | 20 |
| Ut | 19 |
| ViLTE | 12 |
| EVS | 12 |
| NR | 2 |

### UNISOC TS.32 sheet

| Index | 数量 |
|---|---:|
| LTE | 41 |
| HSPA | 18 |
| GSM | 12 |
| UTRA | 7 |
| LTE FGI | 4 |

### UNISOC Default NV sheet

| Module | 数量 |
|---|---:|
| OPERATOR_NV_IMS | 299 |
| OPERATOR_NV_NAS | 126 |
| OPERATOR_NV_MN | 117 |
| OPERATOR_NV_N3GPP | 51 |
| OPERATOR_NV_LAS | 48 |
| OPERATOR_NV_WAS | 25 |
| OPERATOR_NV_GAS | 4 |
| OPERATOR_NV_NRAS | 1 |

## 使用规则

1. 先判断需求是否属于 modem 行为；AP 显示/菜单/Framework 门控优先看 CarrierConfig。
2. 对 TS.32/能力项，先确认运营商要求、制式和默认值，再定位 `字段 values` 对应的 Operator NV 路径。
3. 对 Default NV，`模块 + 子模块/路径 + 属性名` 才是完整定位信息。
4. 修改后必须验证源文件、生成 bin/image、版本策略、刷入产物和设备端 running NV。
5. 涉及 fixnv、IMEI、RF 校准、工厂个体化参数时，不要用公共 base nvitem 直接覆盖现场机。
## 拆分说明

本文件现在只作为 Modem / Operator NV 的总入口，保留配置原则、平台边界和阅读口径。字段级大表已拆到本目录，避免主文档变成不可阅读的大表。

## 参数映射索引

| 内容 | 入口 | 用途 |
|---|---|---|
| UNISOC Modem NV需求映射 | [UNISOC-Modem-NV需求映射](UNISOC-Modem-NV需求映射.md) | 运营商需求到 Operator NV 字段的候选映射 |
| UNISOC TS.32能力项映射 | [UNISOC-TS32能力项映射](UNISOC-TS32能力项映射.md) | TS.32/能力项与 Operator NV 对应关系 |
| UNISOC Default NV字段映射 | [UNISOC-Default-NV字段映射](UNISOC-Default-NV字段映射.md) | default NV 字段、模块和默认值索引 |
| Qualcomm MCFG字段映射 | [Qualcomm-MCFG字段映射](Qualcomm-MCFG字段映射.md) | Qualcomm NvEfsItemData / Member 字段索引 |
| MTK Modem NV字段映射 | [MTK-Modem-NV字段映射](MTK-Modem-NV字段映射.md) | MTK NV 参数映射入口 |
| MTK IMS NV字段映射 | [MTK-IMS-NV字段映射](MTK-IMS-NV字段映射.md) | IMS/VoLTE/VoWiFi/SIP/SDP/codec/emergency 需求到 MTK NV 字段 |
| MTK UT/XCAP NV字段映射 | [MTK-UT-XCAP-NV字段映射](MTK-UT-XCAP-NV字段映射.md) | UT/XCAP/补充业务需求到 MTK NV 字段 |
| MTK 网络与能力 NV字段映射 | [MTK-网络能力-NV字段映射](MTK-网络能力-NV字段映射.md) | 网络选择、LTE能力、NAS、C2K、UMTS/RF 能力需求到 MTK NV 字段 |
