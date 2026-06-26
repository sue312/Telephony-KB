---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# 20_Service-Flows

## 阅读顺序

- 先看入口触发，再看 AP 到 modem 的消息链路，再看协议层关键消息，最后看状态同步和异常分支。
- 厂商客制化需要记录开关来源、默认值、配置路径、log 关键字和回退条件。
- 本文作为流程补充，主线结论仍优先沉淀到对应业务流程文档。

这里放“业务正常应该怎么走、常见分叉在哪里、厂商客制化会影响哪一步”。真实 log 证据和项目结论不要写在流程正文里，放到 `40_Case-Library`。

## 业务域

| 目录 | 内容 |
|---|---|
| [Network Registration](Network-Registration/LTE注册流程.md) | LTE/NR 注册、PLMN、RRC、NAS、ESM、AP 状态同步 |
| [Data](Data/Data业务流程.md) | APN、数据连接、默认承载/PDU Session、吞吐量 |
| [IMS](IMS/IMS业务流程.md) | IMS 注册、VoLTE、VoWiFi、VoNR、SMS over IP、USSD |
| [Call](Call/Call业务流程.md) | CS Call、ECC、SRVCC、EPSFB、掉话、补充业务 |
| [SIM](SIM/SIM业务流程.md) | 卡识别、应用选择、READY、鉴权前置 |
| [BT](BT/README.md) | 蓝牙开关、扫描发现、配对绑定、Profile连接、BLE/GATT、蓝牙音频 |
| [Stability](Stability/Modem稳定性与Assert.md) | modem assert、radio restart、稳定性前置判断 |

## 迁入资料补充

| 文档 | 用途 |
|---|---|
| [[Network-Registration/注册流程补充]] | 迁入 LTE/GSM/WCDMA 注册流程资料补充 |
| [[Network-Registration/网络模式更新流程]] | preferred network type 从 AP 到 modem 的更新链路 |
| [[Call/CS-Call流程补充]] | CS Call / ECC Call 代码与流程补充 |
| [[IMS/VoLTE-Call基础流程]] | VoLTE Call 基础调用链和关键类 |
| [[IMS/VoLTE-Call-AP日志流程]] | VoLTE Call AP 侧调用链和 log |
| [[IMS/VoLTE-Call-Modem日志流程]] | VoLTE Call modem 侧证据 |
| [[IMS/视频通话拨号流程]] | 视频通话 MO 拨号入口和调用链 |
| [[IMS/视频通话来电流程]] | 视频通话 MT 来电入口和调用链 |
| [[IMS/视频通话界面与Log]] | 视频通话界面状态、AP log 和 modem log |

## 流程文档写法

每篇流程建议固定包含：

1. 入口场景：开机、飞行模式、手动搜网、业务发起、弱网恢复等。
2. 正常时间线：AP 请求、RIL 交互、modem 信令、状态上报。
3. 第一坏点：每一步失败时应看什么证据。
4. 平台差异：MTK / UNISOC / Qualcomm 的代码入口和 log 关键字。
5. 关联配置：APN、CarrierConfig、NV、运营商文件等。
6. 关联案例：能复用的历史问题。
