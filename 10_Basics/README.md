---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# 10_Basics

## 阅读重点

- 本文用于补充协议和基础概念；实际问题定位时需要回到对应业务流程、平台代码和案例库交叉验证。
- 图片已转成本地附件，适合在 HTML 中快速查看流程图和字段截图。

基础区只放跨业务可复用的概念，不放真实 case，也不放某个平台的完整代码路径。

## 入口

| 文档 | 用途 |
|---|---|
| [[CauseCode与缩写]] | EMM/ESM/5GMM/SIP/Q.850 cause、常用 log 标签、缩写、标签体系 |
| [[PLMN基础与术语]] | HPLMN、RPLMN、EPLMN、FPLMN、VPLMN、RAT、suitable cell 等基础概念 |
| [[3GPP协议阅读方法]] | 3GPP 官网、协议编号、协议栈和目录阅读方法 |
| [[RF基础概念]] | RF 信号链、dB/dBm、链路预算、PA/ASM/eLNA/RFFE、RSRP/RSRQ/SINR、TRP/TIS 和自检边界 |
| [[手机连接基站与数据传输基础]] | UE—无线接入网—核心网总体链路、找网/接入、数据转发与多用户无线资源共享的科普入口 |
| [[通信基础概念]] | FDN 等基础概念补充 |
| [[SIM-USIM-EF文件速查]] | IMSI、ICCID、SPN、PNN/OPL、PLMNwACT、SMSP、ECC、FDN 等 SIM/USIM EF 文件速查 |

## 放置规则

| 内容 | 应放位置 |
|---|---|
| cause code 基础含义、通用定位方向 | `10_Basics` |
| 某次 reject 的真实证据链 | `40_Case-Library` |
| Attach / TAU / bearer 过程细节 | `20_Service-Flows` |
| 按现象的排查步骤 | `30_Troubleshooting` |
| 厂商代码路径和实现差异 | `50_Platform-Code` |

## 后续补充方向

- Android Telephony 基础对象：Phone、ServiceState、DataProfile、Subscription。
- 3GPP 分层基础：RRC、NAS、EMM、ESM、5GMM、5GSM。
- SIM/USIM/ISIM 基础文件后续可继续补 ISIM / IMS 相关 EF，IMS 专项另文维护。
