---
doc_type: config
domain: Configuration
status: active
quality: curated
search_tier: supplemental
---

# SMS配置方法

## 速查结论

- SMS 问题先分层：应用/API、AP `SMSDispatcher`、RILJ `SEND_SMS`、modem CP/RP 层、网络/SMSC 响应。
- SMSC（短信中心号码）发送时由 modem 提供，常见来源是 SIM 卡；不要把所有短信失败都归因到 AP 设置项。
- FDN 开启时，SMS 会同时检查 SMSC 和最终收件人号码；只把收件人加入 FDN list 不够。
- 短码短信如果没有 RILJ `SEND_SMS`，优先查 AP `SMSDispatcher`、premium short code 分类和权限确认流程。
- SMS over IMS 问题要同时看 IMS 注册、SDM 域选择和 IMS profile；SGs/CS 发送成功不代表满足运营商 SMS over IP 要求。
- Voicemail 号码要区分 line number、fax number、data number 和 voicemail retrieval number，不同字段的 SIM/本地配置能力不同。


<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| SIM EF / SMSC | SMSP、SMSC、FDN | UICC log、RILJ `SEND_SMS` 前检查 |
| CarrierConfig / short code XML | premium SMS、短码、voicemail、SMS over IMS | `dumpsys carrier_config`、SMSDispatcher log |
| IMS / SDM profile | SMS over IP / SGs / CS 域选 | SDM/IMS log、SIP MESSAGE / SGs trace |
| modem / network | RP/CP 层、网络返回 cause | modem SMS trace |

### 匹配与生效链路

```text
App / Dialer / SMS provider
-> SMSDispatcher / FDN / short code 判断
-> 域选 IMS / SGs / CS
-> RILJ SEND_SMS 或 SIP MESSAGE
-> modem / network response
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
| 源配置存在 | SMSC / FDN / short code / voicemail / CarrierConfig | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | RILJ SEND_SMS、SmsDispatcher、TelephonyProvider | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | RP/CP/SMS over SGs 或 SMS over IMS trace | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

### 关联入口

| 入口 | 用途 |
|---|---|
| [配置目录 README](../README.md) | 回到配置分类和放置规则 |
| [Case横向索引](../../40_Case-Library/Case横向索引.md) | 查历史同类问题和第一坏点 |
| [平台代码入口](../../50_Platform-Code/README.md) | 查厂商代码读取位置 |
| [常用命令](../../70_Tools-Debug/Commands/常用命令.md) | 查 dumpsys、logcat 和 adb 命令 |

### 常见失败模式

| 现象 | 优先检查 | 第一坏点判断 |
|---|---|---|
| RILJ 无 SEND_SMS | short code、permission、FDN、AP 拦截 | AP 分发前失败 |
| 配了 SMS over IMS 仍走 SGs | SDM prefer rule、IMS 注册、profile 开关 | 域选配置优先级问题 |
| FDN 下短信失败 | 收件人和 SMSC 是否都在 FDN | FDN 双重校验问题 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## SMS发送分层检查

| 层级 | 关键证据 | 判断 |
|---|---|---|
| 应用/API | `SmsManager.sendTextMessage()`、sentIntent 回调 | 应用是否真正发起发送 |
| AP Telephony | `SMSDispatcher`、短码确认、权限、FDN check | 没有 RILJ `SEND_SMS` 时先查这里 |
| RILJ | `SEND_SMS` | 出现后说明已下发到 RIL/modem |
| Modem / NAS | CP-DATA、RP-DATA、RP-ACK/RP-ERROR | 判断网络是否接收/拒绝 |
| 网络/SMSC | RP cause、SMSC 地址、运营商限制 | 已到网络后再查 SMSC/签约 |

## SMS over IMS / SGs 域选

MTK 平台上，SMS over IMS 不是单一开关。至少要形成下面的闭环：

| 检查项 | 关键字段 / 日志 | 判断 |
|---|---|---|
| IMS 是否会启动 | `wans_ims_no_voice_sup_sms_enable`、IMS REGISTER | 无语音 / 无 VoLTE 项目若仍要求 SMS over IMS，需要保留 IMS 注册 |
| AP/IMS 能力 | `AT+EIMSCFG` 中 `ims_sms=1` | 只能证明能力配置，不能单独证明实际走 IMS |
| SDM 是否允许 SMS over IP | `sdm_cust_sms_over_ip_allowed_tbl`、`from SDM = KAL_FALSE` | 命中禁用表时，即使 RAC 允许也可能不走 IMS |
| SGs 是否优先 | `sdm_cust_prefer_sms_over_sgs_to_ims_tbl`、`Prefer SMS over SGs to IMS in LTE` | 命中后 LTE 下会优先 SGs |
| IMS profile 是否完整 | `ua_config.sms_network_types`、`imc_config.sms_support` | SDM 选 IMS 后仍失败时回看 IMS profile |
| IMS 提交证据 | SIP `MESSAGE`、`RP-DATA`、`+g.3gpp.smsip` | 证明短信实际封装到 IMS/SIP |

典型结论写法：

```text
当前短信能通过 SGs/CS 发出，但运营商需求是 SMS over IP。
日志中 SDM 命中 SGs 优先或 SMS over IP disabled，第一坏点在运营商域选配置，不是 SMSC 或应用发送。
```

参考案例：[[../../40_Case-Library/IMS/2025-07-29_IMS_SMS-over-IP配置缺失]]。

## SMSC来源与FDN边界

从 CQWeb 历史问题 `SPCSS01579117` 看，发送短信时 SMSC 由 modem 提供，短信中心号码支持从 SIM 卡获取。不要在 AP 层找不到设置项时就判断“不支持 SMSC”。

从 CQWeb 历史问题 `SPCSS01630213` 看，终端可按 `EF_SMSP` 确定 SMS parameters。遇到 SMSC 或短信参数争议时，要先确认 SIM 卡内 `EF_SMSP` 是否存在、是否被 modem 读取、AP/RIL 最终是否使用该值。

从 `SPCSS01310994` 看，FDN 对 SMS 的检查范围包含两部分：

```text
Service Center address
end-destination address
```

处理建议：

- FDN + SMS 测试时，FDN list 中需要同时包含短信中心号码和收件人号码。
- UI 提示“请添加号码到固定拨号列表”时，缺失的可能是 SMSC，不一定是收件人。
- 如果 SMSC 错误，先确认 SIM/USIM 中的短信中心号码、modem 上报值和 AP 读取路径。

## SIM短信能力边界

认证类需求中常见的 SMS / USIM 能力可以先按下表分开：

| 需求 | 历史口径 | 证据 |
|---|---|---|
| 按 `EF_SMSP` 确定 SMS parameters | 支持 | SIM EF 读取、modem/AP 最终使用值 |
| command packet 拼接至少 5 条 | 支持 | 测试用例、SMS 拼接日志 |
| USIM data download SMS-Deliver 不显示到屏幕 | 支持 | SMS-PP / UICC data download 路径，无普通短信 UI 展示 |

注意：这些是能力确认，不等于具体短信失败都在 SIM EF。真实问题仍要回到应用、`SMSDispatcher`、RILJ、modem CP/RP 和网络/SMSC 分层。

## 短码与premium SMS

短码失败时先看有没有下发到 RILJ：

```text
RILJ: SEND_SMS
```

没有 `SEND_SMS` 时，优先查：

| 检查项 | 说明 |
|---|---|
| `sms_short_codes.xml` | 短码分类是否与测试包/地区规则一致 |
| premium short code 分支 | 是否进入 `EVENT_CONFIRM_SEND_TO_POSSIBLE_PREMIUM_SHORT_CODE` / `EVENT_CONFIRM_SEND_TO_PREMIUM_SHORT_CODE` |
| 权限和确认弹框 | 是否被用户确认、策略拦截或本地白名单绕过 |
| 本地修改 | 是否改过 `SMSDispatcher` 对 `SmsTracker` 的处理 |

参考案例：[[../../40_Case-Library/SMS/2025-03-22_SMS_UNISOC_短码发送未到RILJ_SEND_SMS]]。

## Voicemail号码

从 CQWeb 历史问题 `SPCSS01579117` 看，功能机/RTOS voicemail 相关号码需要区分来源和能力：

| 项目 | 历史结论 |
|---|---|
| Voicemail centre / retrieval number | 支持从 SIM 获取，历史说明提到 EFADN 或 EFMBDN |
| Line number | 支持从 SIM 获取；SIM 无号码时，可从本地配置获取 |
| 本地 line number 配置 | 历史资料提到 `sms_voicemail_romaing.h` 和 `sms_voicemailnoroaming.h` |
| Data number | 如果指 voicemail data number，支持从 SIM 获取、编辑和拨打；历史结论是不支持本地设置 |
| 类型标识 | data number 对应 `MMISMS_VOICEMAIL_DATA` / `MN_VOICE_MAIL_EMAIL` 相关类型 |

注意：

- “Voicemail centre”不一定等同于 UI 中的 line number，需要结合运营商测试项定义确认。
- data number 的实际业务用途历史答复中未完全展开，遇到认证问题时应保留 SIM 文件读取、UI 菜单和 MMI/modem 类型映射证据。
- 本地配置文件名按历史 CQ 原文记录，实际项目中需要以当前分支代码路径为准。

## 关联案例

- [[../../40_Case-Library/SMS/2024-03-11_SMS_UNISOC_FDN发送短信需同时放行SMSC和收件人]]
- [[../../40_Case-Library/SMS/2025-03-22_SMS_UNISOC_短码发送未到RILJ_SEND_SMS]]
- [[../../40_Case-Library/IMS/2025-07-29_IMS_SMS-over-IP配置缺失]]
- [[../../40_Case-Library/SIM/2026-02-27_SIM_UNISOC_PLMN列表与SIM短信参数能力确认]]
