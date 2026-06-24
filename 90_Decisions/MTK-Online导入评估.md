---
doc_type: guide
domain: Meta
status: archived
quality: imported_reference
platform: MTK
source: Notion MTK 网络通信模块知识库
source_url: https://www.notion.so/35df72d579ba8119b35afddb83be1fa8
search_tier: supplemental
---

# MTK Online导入评估

<!-- SUPPLEMENTAL_BOUNDARY_START -->
## 使用边界

- 本页是补充资料或短专题，适合查局部步骤、旧来源和零散技巧。
- 若需要直接定位问题，优先回到对应主流程、配置方法、排障流程或 Case。
- 后续新增结论应沉淀到主文档，本页只保留来源和辅助说明。
<!-- SUPPLEMENTAL_BOUNDARY_END -->


## 阅读入口

这篇记录对 Notion 页面“MTK 网络通信模块知识库”的导入判断。该 Notion 页本身已经是对 MediaTek Online QuickStart / FAQ / DCC 的二次整理，适合作为本地 KB 的 MTK 专项入口、配置排查链和抓 log 模板来源。

本次导入原则：不整页复制，不把未验证 FAQ 摘要写成最终根因；只提取可复用的排查入口、配置层级、日志证据要求和关键词。

## 结论

可以提取，而且价值较高。最适合落到本地 KB 的内容有 5 类：

| Notion 内容 | 本地落点 | 处理方式 |
|---|---|---|
| Modem / Telephony QuickStart 栏目总览 | `50_Platform-Code/MTK` | 做成 MTK Online 入口地图 |
| CarrierConfig / IMS Config / SBP / NVRAM / APN 配置关系 | `60_Configuration` | 做成 MTK 配置生效链和排查顺序 |
| WFC / ePDG 配置与排查 | `60_Configuration` + `30_Troubleshooting` | 提取 FQDN / DNS / IKE / 证书 / DPD / HO 参数链 |
| 5G Registration / PDU Session / URSP | `30_Troubleshooting` | 做成 5G 注册与数据问题第一轮排查入口 |
| Modem 日志工具索引 + 抓 log SOP | `70_Tools-Debug` | 做成 MTK 网络问题 log 包和 eService 提交模板 |

## 已新增条目

| 文档 | 作用 |
|---|---|
| [MTK-Online-QuickStart入口地图](../50_Platform-Code/MTK/MTK-Online-QuickStart入口地图.md) | 按问题类型选择 MTK Online Modem / Telephony 栏目 |
| [MTK-配置关系与生效链路](../60_Configuration/MTK-配置关系与生效链路.md) | 从支持能力、编译开关、AP 配置、SBP/NVRAM 到承载建立的检查顺序 |
| [MTK-WFC-ePDG配置与排查索引](../60_Configuration/MTK-WFC-ePDG配置与排查索引.md) | VoWiFi / ePDG 断点、参数、日志关键字和现场证据 |
| [MTK-5G注册与PDU排障入口](../30_Troubleshooting/MTK-5G注册与PDU排障入口.md) | 5GMM reject、N1 mode、T3346/T3502、DNN/S-NSSAI、URSP |
| [MTK-网络通信问题抓Log与提交模板](../70_Tools-Debug/Log-Capture/MTK-网络通信问题抓Log与提交模板.md) | 通信问题复现信息、必抓 log、eService issue 描述模板 |

## 不建议直接导入的部分

| 内容 | 原因 | 后续处理 |
|---|---|---|
| Notion 根页进度、待办、更新记录 | 只对 Notion 原库维护有意义 | 不进入本地 KB 主文档 |
| 重复的 VoNR / WFC 子页 | 根页已标记为重复页 | 暂不导入 |
| 大量 FAQ / DCC 标题列表 | 本地 KB 应回答怎么定位，不应只堆链接 | 只在入口地图里保留关键资料方向 |
| 具体 operator 支持计划结论 | 会随 MTK support plan、branch、modem 版本变化 | 只保留“如何查 support plan”的方法 |

## 仍可继续拆分

| 候选专题 | 建议落点 | 说明 |
|---|---|---|
| IMS Registration / Handover 总流程图 | `20_Service-Flows/IMS` | 需要继续读取 IMS handover training DCC |
| EMM / ESM / 5GMM / 5GSM cause 字典 | `10_Basics` | 当前本地 CauseCode 已有基础，可扩展 MTK FAQ 索引 |
| Network Slice / Configured NSSAI / Allowed NSSAI / Rejected NSSAI | `10_Basics` 或 `30_Troubleshooting` | 当前只导入 PDU / URSP 第一轮排查 |
| LTE/NR Band capability 与 RF/AS 搜网排查 | `30_Troubleshooting` | 需要结合 RRC / RF 专项资料继续沉淀 |
| SMS/MMS/CB 应用层排查 | `30_Troubleshooting` + `70_Tools-Debug` | 当前只在抓 log 模板里保留证据要求 |
