---
quality: curated
doc_type: index
domain: Platform
layer: AP/RIL/IMS/Modem/Build
status: active
search_tier: main_entry
---

# 50_Platform-Code

## 阅读入口

- 本页是当前目录入口，优先按表格进入已整理主题；来源记录只用于回溯。
- 可复用结论应沉淀到主流程/配置/排障/case；本文只保留溯源材料和操作细节。

## 定位入口

- 先切清模块边界：Android Framework、RIL、厂商服务、modem、配置资源。
- 再补齐代码路径、开关来源、log 关键字、编译产物和运行时验证方式。
- 本文图片已转成本地附件；非图片附件仍保留原 Outline 链接作为资料索引。

这里回答“代码从哪里看、状态如何同步、平台实现差异在哪里、产物怎么生成”。配置字段细节放 `60_Configuration`，真实问题证据放 `40_Case-Library`。

## 入口

| 文档 | 用途 |
|---|---|
| [Telephony系统架构](Cross-Platform/Telephony系统架构.md) | Android Telephony、RIL / IMS / Modem 边界、平台差异和迁入架构补充 |
| [Telephony函数级入口速查](Cross-Platform/Telephony函数级入口速查.md) | 按现象定位 Android / UNISOC / MTK 函数、handler、log 证据 |
| [平台代码与产物速查](Cross-Platform/平台代码与产物速查.md) | LTE 注册代码入口、MTK / UNISOC 实现、modem image、patch、流水线产物 |
| [[Android/Android国内卡模拟运营商]] | Android侧模拟运营商 MCC/MNC/CarrierConfig/APN 的实现思路 |
| [[UNISOC/Telephony代码架构速查]] | UNISOC 标准 RIL、扩展 Radio HAL、RadioInteractor、CarrierConfig 代码入口 |
| [UNISOC CarrierService启动与CarrierConfig加载流程](UNISOC/UNISOC-CarrierService启动与CarrierConfig加载流程.md) | UNISOC `CarrierConfigLoader`、默认 `CarrierService`、carrier app 长连接绑定和运行时验证 |
| [[MTK/Telephony代码架构速查]] | MTK RIL / RFX / Rtc/Rmc/Rmm handler、注册态和 IA APN 代码入口 |
| [[MTK/MTK-Online-QuickStart入口地图]] | MTK Online Modem / Telephony QuickStart 栏目入口，按 NAS/RRC/IMS/Data/SBP/NVRAM/Telephony 问题选资料 |
| [[MTK/MTK-Modem编译环境配置]] | MTK modem 编译环境配置 |
| [Qualcomm平台代码](Qualcomm/README.md) | Qualcomm Modem、RF Card/FEM、MCFG、编译产物和打包链路入口 |
| [[Qualcomm/Qualcomm-Modem-RF配置与编译链路]] | Qualcomm RF Card、FEM/RFFE、RF NV、RF Target 的配置、生成、链接、RFPD 和打包边界 |

## 建议阅读顺序

1. 先看 [[Cross-Platform/Telephony系统架构|Telephony系统架构]]，确认 AP、RIL、vendor RIL、modem、IMS 的边界。
2. 再看 [[Cross-Platform/Telephony函数级入口速查|Telephony函数级入口速查]]，按现象定位函数、handler 和 log 证据。
3. 再看 [[Cross-Platform/平台代码与产物速查|平台代码与产物速查]]，按 MTK / UNISOC / Qualcomm 找具体代码入口和产物链路。
4. 如果已经确定平台，直接进入 [[UNISOC/Telephony代码架构速查]]、[[MTK/Telephony代码架构速查]] 或 [[Qualcomm/README|Qualcomm平台代码]]。
5. 如果问题是 AP 状态不同步，优先对齐 RIL response、`NetworkRegistrationInfo`、`ServiceStateTracker`。
6. 如果问题是产物或 patch，优先对齐 patch list、modem image、编译流水线参数和刷入版本。

## 放置规则

| 内容 | 应放目录 |
|---|---|
| 系统边界、平台代码路径、状态同步链路、产物链路 | `50_Platform-Code` |
| APN / ECC / NV / CarrierConfig / SIMLock 配置字段 | `60_Configuration` |
| Attach / TAU / bearer / PDU Session 等业务步骤 | `20_Service-Flows` |
| 某次 log 的时间线、第一坏点、根因 | `40_Case-Library` |
| log 抓取 SOP、关键字、字段解释 | `70_Tools-Debug` |
| cause code、缩写、标签 | `10_Basics` |
