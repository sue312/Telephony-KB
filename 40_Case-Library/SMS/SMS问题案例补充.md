---
quality: curated
doc_type: reference
domain: SMS
rat: LTE
platform: MTK
layer: IMS/SDM/Modem
symptom: imported SMS case collection
cause: consolidated
source_log: Old Outline knowledge base
first_bad_point: see linked curated case
confidence: medium
search_tier: reference_only
status: reference
---

# SMS问题案例补充

## 收敛状态

这篇是旧 Outline 中 SMS 问题集合的迁入入口，不再作为独立 case 扩写。可复用结论已经沉淀到下面位置：

| 原始主题 | 已沉淀位置 | 复用点 |
|---|---|---|
| 无语音 / 无 VoLTE 项目仍要求 SMS over IMS | [[../IMS/2025-07-29_IMS_SMS-over-IP配置缺失]] | `wans_ims_no_voice_sup_sms_enable` 关闭会导致无 IMS 注册，SMS over IMS 无法闭环 |
| 配置 SMS over IMS 后仍走 SGs | [[../IMS/2025-07-29_IMS_SMS-over-IP配置缺失]] | `sdm_cust_prefer_sms_over_sgs_to_ims_tbl` 命中后优先 SGs |
| RAC 允许但 SDM 禁止 SMS over IP | [[../IMS/2025-07-29_IMS_SMS-over-IP配置缺失]] | `sdm_cust_sms_over_ip_allowed_tbl` 可导致 `from SDM = KAL_FALSE` |
| SMS over IMS 配置速查 | [[../../60_Configuration/Business-Config/SMS配置方法#SMS over IMS / SGs 域选]] | 按 IMS 注册、SDM 域选、IMS profile、SIP MESSAGE 分层 |
| IMS 流程入口 | [[../../20_Service-Flows/IMS/IMS业务流程#SMS over IP流程]] | SMS over IP / SGs / CS 三种传输路径对比 |

## 关键字段索引

```text
wans_ims_no_voice_sup_sms_enable
sdm_cust_prefer_sms_over_sgs_to_ims_tbl
sdm_cust_sms_over_ip_allowed_tbl
ua_config.sms_network_types
imc_config.sms_support
AT+EIMSCFG
[SDM][ADS] Prefer SMS over SGs to IMS in LTE
[SDM] Current SMS over IP config from RAC = SDM_SMS_OVER_IP_ALLOWED, from SDM = KAL_FALSE
```

## 来源记录

- [SMS问题案例](http://192.168.3.94:8888/doc/sms-148EcfAnQm) (`148EcfAnQm`)
