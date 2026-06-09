---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# Supplementary-Service Cases

## 阅读入口

- 本目录放补充业务真实问题和旧资料集合入口，包括 Call Forwarding、Call Barring、USSD、UT/XCAP、USSI、CISS、CSFB 回落等。
- 普通 MO/MT call、call drop、SRVCC、ECC 仍放 `Call`；IMS 注册、SIP REGISTER、VoLTE/VoWiFi 能力仍放 `IMS`；XCAP APN 建链或 APN UI 问题仍放 `Data` 或 `60_Configuration`。
- 配置字段和验证方法看 [补充业务配置方法](../../60_Configuration/Business-Config/补充业务配置方法.md)，第一轮分诊看 [补充业务失败排障流程](../../30_Troubleshooting/补充业务失败排障流程.md)。

## 已整理案例

| Case | 场景 | 用途 |
|---|---|---|
| [[2025-09-09_SS_UNISOC_CF_XCAP_AUID误配导致HTTP400后CSFB]] | Call Forwarding 走 XCAP 失败后 CSFB | 检查 `ss_XcapAuid`、XCAP URL、HTTP 401/200/400 和 CSFB 时间点 |
| [[2024-07-19_SS_UNISOC_USSD域选需按运营商走CS]] | USSD 走 IMS/USSI 失败 | 按运营商能力确认 USSD 应走 IMS/USSI 还是 CS/CISS |
| [[补充业务问题案例]] | 旧 Outline 补充业务集合入口 | 已收敛到 XCAP/USSD 独立 case、配置方法和排障入口 |

## 放置规则

| 内容 | 放置位置 |
|---|---|
| CF/CB/CW/CLIR/CLIP/USSD/UT/XCAP 的真实问题 | `40_Case-Library/Supplementary-Service` |
| XCAP APN 或 APN type 显示问题 | `40_Case-Library/Data` 或 `60_Configuration/Core-Config/APN配置方法_重构.md` |
| IMS 注册、SIP 注册、VoLTE 能力问题 | `40_Case-Library/IMS` |
| 普通语音通话建立、掉话、SRVCC、ECC | `40_Case-Library/Call` |
