---
doc_type: troubleshooting
domain: Troubleshooting
status: active
quality: imported_reference
platform: MTK
source: Notion MTK 网络通信模块知识库 / MediaTek Online 5G NAS FAQs
source_url: https://www.notion.so/35df72d579ba810da1c7f7ea2aa970b1
search_tier: supplemental
---

# MTK 5G注册与PDU排障入口

<!-- SUPPLEMENTAL_BOUNDARY_START -->
## 使用边界

- 本页是补充资料或短专题，适合查局部步骤、旧来源和零散技巧。
- 若需要直接定位问题，优先回到对应主流程、配置方法、排障流程或 Case。
- 后续新增结论应沉淀到主文档，本页只保留来源和辅助说明。
<!-- SUPPLEMENTAL_BOUNDARY_END -->


## 使用入口

这篇用于 MTK 5G SA/NR 注册和 5G 数据承载的第一轮排查。适用现象包括：5G 注册失败、收到 5GMM reject、N1 mode 被禁用、过一段时间又尝试 SA、5G 已注册但数据不通、PDU session reject、DNN / S-NSSAI / URSP 相关异常。

通用判断已经回填到 [注册失败排障流程](注册失败排障流程.md#MTK-5GMM-快速判断) 和 [数据业务失败排障流程](数据业务失败排障流程.md#MTK-5G-PDU--URSP-快速判断)。本页只保留 MTK 专项关键词、补充来源和最小证据包。

## 总体判断

5G 问题先分两层：

```text
VGMM / NWSEL / NR camping
-> 5GMM Registration 是否完成
-> VGSM / PDU Session
-> DNN / S-NSSAI / URSP / EBI / QFI
-> IP / DNS / route / 应用流量
```

如果 Registration 没完成，不要先查 PDU；如果 Registration 已完成但 PDU 失败，重点看 DNN、slice、URSP、FOR bit/T3540、invalid EBI 和网络返回 cause。

## 5GMM Registration快速路径

1. 确认 registration type：Initial、Mobility Registration Updating、Periodic，还是 inter-system change。
2. 找 `5GMM_REGISTRATION_REQUEST` 和 `5GMM_REGISTRATION_REJECT`。
3. 记录 reject cause、T3346、T3502、完整性保护状态。
4. 看 UE 是否 disabled N1 mode，是否 fallback 到 LTE。
5. 看 NWSEL 是否对 PLMN 设置 timer / barring / disabled status。
6. 看 SBP/operator requirement 是否要求永久禁用、定时恢复或继续重试 SA。

## 5GMM关键场景

| 场景 | 关键判断 | 优先证据 |
|---|---|---|
| Cause 27 `N1 mode not allowed` | UE 可按 PLMN 禁用 N1 mode，并启动 re-enable timer；部分策略可永久禁用直到 USIM 移除或关机 | `5GMM_REGISTRATION_REJECT`、N1 mode disabled、SBP timer |
| N1 re-enable timer | “过一段时间又尝试 SA”可能是 timer 到期，不是随机重试 | `SBP_PLMN_TIMER_N1_MODE_NOT_ALLOW*`、NWSEL timer |
| T3346 vs T3502 | Reject 携带有效 T3346 时，UE 可 abort initial registration，不进入 T3502 abnormal case | T3346、attempt counter、5GS update status |
| T3502 | Reject 携带 T3502 且有效时，UE 使用网络给定值，NR PLMN 可能 disabled | `GPRS timer 2 value decoded`、NR PLMN disabled |
| IKE 中 N1 capability | ePDG/IKE 场景中 operator 可能要求带 N1-Mode-Capability | `n1_mode_cap`、`AT+EN3CFGSET="n1_mode_cap","1"` |

## PDU Session快速路径

1. 确认 5GMM Registration 已完成。
2. 找 `VGSM_PDU_SESSION_ESTABLISHMENT_REQUEST`，记录 PTI、PSI、DNN、S-NSSAI、request type。
3. 找 `5GMM_UL_NAS_TRANSPORT` / `5GMM_DL_NAS_TRANSPORT`，确认 N1 SM info 是否正常转发。
4. 找 reject：`VGSM_PDU_SESSION_ESTABLISHMENT_REJECT` 或 not forwarded cause。
5. 判断 cause 是 DNN、slice、routing failure、UAC/T3540、invalid EBI，还是 emergency special rule。
6. 涉及应用路由时继续看 URSP / D2PM 规则匹配。

## PDU / URSP关键场景

| 场景 | 判断口径 | 优先证据 |
|---|---|---|
| DNN / S-NSSAI 不匹配 | 网络侧可能因 slice 中不支持或未签约 DNN，导致消息未转发或 PDU reject | `DNN_NOT_SUPPORT_IN_SLICE`、`VGSM_CAUSE_MISSING_OR_UNKNOWN_DNN` |
| 核心网未转发 vs SMF reject | 没有转发到 SMF 时，不应直接当成 SMF 明确拒绝 | not forwarded cause、UL/DL NAS transport |
| Emergency PDU | emergency request 不应携带 DNN / S-NSSAI | request type、DNN/S-NSSAI 是否为空 |
| FOR bit / T3540 | Registration Request 中 FOR bit 为 0 可能触发 T3540，影响后续 PDU 处理 | DUT/REF Registration Request 对比 |
| Invalid EBI | Accept 中 EBI 合法范围应为 5-15；EBI 0 可能触发 modification | `SMIC_INVALID_MAPPED_EBI`、cause #85 |
| PDCP ICD EBI 仍为 0 | 可能是 trace 打印早于 VGSM accept，不代表最终 EBI 未更新 | PDCP event 与 VGSM accept 时序 |
| URSP 应用路由 | 应用走错 PDU、切片不对、DNN 不对时查规则优先级和 RSD 命中 | `AT+EGUEPOLICY`、`ursp_eval`、DNN/S-NSSAI |

## 常用日志关键词

```text
VGMM
VGSM
NWSEL
PAM
D2PM
SMIC
5GMM_REGISTRATION_REQUEST
5GMM_REGISTRATION_REJECT
5GMM_UL_NAS_TRANSPORT
5GMM_DL_NAS_TRANSPORT
N1_SM_INFO
VGSM_PDU_SESSION_ESTABLISHMENT_REQUEST
VGSM_PDU_SESSION_ESTABLISHMENT_ACCEPT
VGSM_PDU_SESSION_ESTABLISHMENT_REJECT
N1 mode not allowed
T3346
T3502
FOR bit
DNN not supported or not subscribed in the slice
VGSM_CAUSE_MISSING_OR_UNKNOWN_DNN
SMIC_INVALID_MAPPED_EBI
AT+EGUEPOLICY
ursp_eval
S-NSSAI
```

## 最小证据包

| 证据 | 用途 |
|---|---|
| MD NAS / VGMM / VGSM log | 判断注册、reject、PDU 建链和 cause |
| RRC / NR camping 信息 | 判断是否已有可用 NR 小区和连接基础 |
| AP radio / Telephony log | 对齐 ServiceState、data call、APN/DNN 请求 |
| APN / DNN / URSP 配置 | 判断应用路由、DNN、S-NSSAI 是否匹配 |
| DUT/REF 同场景对比 | 特别用于 FOR bit、T3540、timer、slice/DNN 差异 |

## 本地关联

- [NR注册流程](../20_Service-Flows/Network-Registration/NR注册流程.md)
- [注册失败排障流程](注册失败排障流程.md)
- [数据业务失败排障流程](数据业务失败排障流程.md)
- [APN配置方法](../60_Configuration/Core-Config/APN配置方法_重构.md)
- [MTK-配置关系与生效链路](../60_Configuration/MTK-配置关系与生效链路.md)
