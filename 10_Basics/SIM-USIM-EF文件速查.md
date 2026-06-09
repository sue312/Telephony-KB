---
doc_type: concept
domain: Basics
status: active
quality: curated
search_tier: supplemental
---

# SIM / USIM EF 文件速查

## 速查结论

- SIM/USIM 问题先确认“需求指的是哪个 EF 文件”，不要把 PLMN 列表、SMSC、SPN、ECC、FDN 混成一个配置入口。
- EF 文件的“平台支持容量”和“当前 SIM 卡实际写入内容”是两件事；认证问题必须同时保留 SIM 文件读取值和平台最终使用值。
- 短信、PLMN 选择、运营商名称、紧急号码、FDN 都会读 SIM 文件，但归属模块不同，定位时要按业务链路分开。

## 常见 EF 文件

| EF | 中文口径 | 常见用途 | 排查入口 |
|---|---|---|---|
| `EF_IMSI` | IMSI | MCC/MNC、注册、运营商匹配 | SIM 初始化、PLMN 选择 |
| `EF_ICCID` | 卡号 | subscription / 卡标识 | SIM 识别 |
| `EF_SPN` | 服务提供商名称 | 状态栏 SIM / SPN 显示 | 运营商名称 |
| `EF_PNN` | PLMN Network Name | EONS / 运营商名称 | PNN/OPL |
| `EF_OPL` | Operator PLMN List | LAC/TAC 到 PNN record 映射 | PNN/OPL |
| `EF_PLMNwACT` | 用户/卡侧优选 PLMN 及接入技术 | 自动选网优先级 | PLMN 选择 |
| `EF_OPLMNwACT` | 运营商控制优选 PLMN 及接入技术 | 自动选网优先级 | PLMN 选择 |
| `EF_FPLMN` | Forbidden PLMN | reject 后禁用/避让 PLMN | 注册失败 |
| `EF_ECC` | Emergency Call Codes | 有卡紧急号码 | ECC |
| `EF_SMSP` | SMS Parameters | SMSC / 短信参数 | SMS 发送 |
| `EF_ADN` / `EF_MBDN` | 电话本 / Mailbox Dialling Number | voicemail retrieval number 等 | Voicemail |

## PLMN 列表容量

CQWeb 历史问题 `SPCSS01630213` 确认过需求口径：终端支持 `EF_PLMNwACT + EF_OPLMNwACT >= 50`。这个结论用于能力确认，不等于当前 SIM 一定写满 50 条，也不等于 UI 手动搜网列表要显示 50 个网络。

排查时要分三层：

| 层级 | 要确认什么 |
|---|---|
| SIM 文件 | 卡内 `EF_PLMNwACT` / `EF_OPLMNwACT` 实际记录数量和内容 |
| 平台读取 | modem/AP 是否完整读取并缓存这些记录 |
| PLMN 选择 | 自动选网是否按 HPLMN、RPLMN、UPLMN、OPLMN、FPLMN 等顺序使用 |

## SMS 参数

同一历史问题还确认过 SMS 相关需求：

- 终端可参考 `EF_SMSP` 确定 SMS parameters。
- SMS / command packet 拼接能力至少支持 5 条级别的需求口径。
- 收到带有 USIM data download 的 SMS-Deliver 时，终端不应在屏幕显示普通短信内容。

这些是能力和行为边界，不替代具体问题定位。真实短信发送失败仍要按 `SMSDispatcher`、RILJ `SEND_SMS`、modem CP/RP、SMSC、网络响应逐层看。

## UICC 低功耗去激活

3GPP TS 31.102 中有 UICC deactivate / re-activate 相关低功耗能力要求。CQWeb `SPCSS01630213` 的历史答复口径是：该能力当时不支持，如项目需要需走需求评估。

判断时不要把它和普通 SIM absent / radio off 混淆：

| 场景 | 说明 |
|---|---|
| SIM absent | 卡物理不在或检测不到 |
| radio off / flight mode | 射频关闭，不等于 UICC 去激活 |
| UICC deactivate / re-activate | 面向低功耗的卡应用/接口去激活与重新激活能力 |

## 证据包

遇到 SIM EF / 认证需求问题，最小证据包建议包含：

```text
1. 需求原文：具体 EF、容量、行为要求、引用 3GPP 条款
2. SIM 文件读取：EF 内容、record 数量、是否空值
3. 平台日志：SIMRecords / modem SIM / RIL 上报
4. 最终业务行为：PLMN 选择、短信发送、运营商名、ECC、FDN 等实际结果
5. 平台答复口径：支持、暂不支持、需需求评估或需运营商资料确认
```

## 关联入口

- [[../20_Service-Flows/SIM/SIM业务流程]]
- [[../60_Configuration/Business-Config/SMS配置方法]]
- [[../60_Configuration/Business-Config/运营商名称配置方法]]
- [[通信基础概念]]
