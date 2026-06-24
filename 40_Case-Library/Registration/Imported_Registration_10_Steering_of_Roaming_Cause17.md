---
doc_type: case
quality: imported_reference
domain: Registration
rat: 2G/3G
feature: 'LU/RAU Reject / Steering of Roaming'
platform: MTK
layer: 'Modem/NWSEL/MM/SBP'
symptom: 'Steering of Roaming Cause17'
cause: '测试 SIM 下 SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL 关闭，连续 LU/RAU reject cause 17 后不触发 VPLMN 搜索'
source_log: 'Old Outline knowledge base; split from 注网问题案例补充.md'
first_bad_point: 'NWSEL SBP dump 中 SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL = KAL_FALSE'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - roaming
  - nwsel
  - sbp
  - reject-cause-17
search_tier: case_summary
---

# Steering of Roaming Cause17

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
Steering of Roaming Cause17

## 结论

这是 Steering of Roaming / abnormal LU 后是否触发 VPLMN 搜索的 SBP 策略问题。网络连续返回 `LOCATION UPDATING REJECT / ROUTING AREA UPDATE REJECT`，cause 17 `Network failure`；期望 4 次后搜索 VPLMN，但测试 SIM 场景下 `SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL` 为关闭，导致 5 次异常后没有按预期触发 PLMN search。

解决方向是在 SBP / make option 中打开异常 LU 后 PLMN selection，并用 NWSEL SBP dump 与后续 `NWSEL_MM_PLMN_SEARCH_REQ` 验证。

## 关键证据

- 原始分类：六、搜网驻网策略
- 来源：注网问题案例补充.md
- 拆分序号：10
- `SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL = KAL_FALSE` 时，5 次异常 RAU/LU reject 后不搜索 VPLMN。
- reject 证据：`GMM__ROUTING_AREA_UPDATE_REJECT` / `MM__LOCATION_UPDATING_REJECT`，cause 17 `Network failure`。
- 修复验证：SBP dump 中该项为 `KAL_TRUE` 后，出现 `MSG_ID_NWSEL_MM_PLMN_SEARCH_REQ`。

## 定位口径

| 检查项 | 判断 |
|---|---|
| reject 类型 | 区分 LU reject、RAU reject、Attach reject，不要只看 cause 17 |
| 尝试计数 | 看 abnormal counter / attempt counter 是否达到策略阈值 |
| SBP 配置 | 重点查 `SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL` |
| 测试 SIM | 原始说明中测试 SIM 默认不执行该 PLMN selection，需要额外 make option |
| 验证点 | 修复后必须看到 NWSEL 发起 PLMN search，并尝试注册 VPLMN |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例1：Steering of Roaming Cause#17

【REPRODUCING PROCEDURES】
1.插入22201 sim卡
2.通过网络22601触发LOCATION UPDATING REJECTED(#17GMM Cause: Network failure )流程
3.被拒5次，没有搜索VPLMN网络。---NOK

【EXPECTED BEHAVIOUR】
被拒4次，搜索VPLMN网络,并注册到VPLMN网络

**分析**：

当前的日志显示测试中已插入 SIM 卡，所以默认行为不会在 5 次异常的 RAU 重连拒绝后执行 PLMN 搜索以查找 VPLMN。

| Type | Index | Time | Local Time | Module | TraceType | Message | Comment | Time Differences |
|----|----|----|----|----|----|----|----|----|
| PS | 2195 | 89740724 | 17:16:37:423 | NWSEL - NWSEL |  | MSG_ID_NWSEL_NWSEL_SBP_DUMP_IND | sbp_name = **SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL** (enum 26)<br>value = KAL_FALSE (enum 0) |  |
| PS | 2245 | 89740731 | 17:16:37:423 | RAC - MM |  | MSG_ID_GMMREG_SET_RAT_MODE_REQ | rat_mode = RAT_GSM_UMTS_LTE<br>active_rat = RAT_GSM_UMTS |  |
| PS | 2249 | 89740731 | 17:16:37:423 | MM |  | \[MM\] Is test SIM: KAL_TRUE |  |   |
| PS | 5124 | 89741588 | 17:16:37:423 | RAC - MM |  | MSG_ID_GMMREG_ATTACH_REQ | attach_type = CS_PS_DOMAIN |  |
| PS | 5195 | 89741600 | 17:16:37:423 | NWSEL |  | \[NWSEL Context\]PLMN_ID: 22201f |  |   |
| PS | 6359 | 89741708 | 17:16:37:423 | DDM |  | d2_get_config(), DSBP enable; SIM_SBP_ID:130 |  |   |
| PS | 18212 | 89813968 | 17:16:42:096 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 22201F<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| OTA | 18396 | 89813993 | 17:16:42:096 | MM |  | \[MS->NW\] GMM__ATTACH_REQUEST | .... .001 = Type of attach: GPRS attach (1) |  |
| OTA | 22500 | 89831588 | 17:16:43:098 | MM |  | \[NW->MS\] GMM__ATTACH_ACCEPT |  |   |
| OTA | 22559 | 89831604 | 17:16:43:098 | MM |  | \[MS->NW\] GMM__ATTACH_COMPLETE |  |   |
| PS | 30870 | 89855086 | 17:16:44:724 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 22201F<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| PS | 30874 | 89855087 | 17:16:44:724 | MM |  | Cell Change Action Type: MM_NO_CHANGE |  |   |
| PS | 120642 | 90780966 | 17:17:44:000 | NWSEL - MM |  | MSG_ID_NWSEL_MM_PLMN_SEARCH_REQ |  |   |
| PS | 141564 | 91125848 | 17:18:06:055 | NWSEL - MM |  | MSG_ID_NWSEL_MM_PLMN_SEARCH_REQ |  |   |
| PS | 147430 | 91160872 | 17:18:08:254 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| PS | 147435 | 91160873 | 17:18:08:254 | MM |  | Cell Change Action Type: MM_LAI_CHANGE |  |   |
| PS | 147447 | 91160876 | 17:18:08:254 | MM |  | MM new State: MM_IDLE_NO_CELL_AVAILABLE |  |   |
| PS | 147460 | 91160878 | 17:18:08:254 | MM - RAC |  | MSG_ID_GMMREG_DETACH_IND | detach_type = CS_DOMAIN<br>cause = NO_COVERAGE |  |
| OTA | 147599 | 91160896 | 17:18:08:254 | MM |  | \[MS->NW\] GMM__ROUTING_AREA_UPDATE_REQUEST |  |   |
| OTA | 151381 | 91175023 | 17:18:09:058 | MM |  | \[NW->MS\] GMM__ROUTING_AREA_UPDATE_REJECT | GMM Cause: Network failure (17) |  |
| PS | 151486 | 91175041 | 17:18:09:058 | MM |  | \[GMM\]gprs_rau_attempt_counter=1, gprs_rau_abnormal_counter=1 |  |   |
| PS | 151487 | 91175041 | 17:18:09:058 | MM - NWSEL |  | MSG_ID_NWSEL_MM_REGN_RESULT_IND | lr_result = LR_ABNORMAL<br>mm_proc = MM_PROC_RAU<br>attempt_counter = 1 |  |
| PS | 154424 | 91197583 | 17:18:10:668 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| OTA | 162003 | 91409441 | 17:18:24:134 | MM |  | \[MS->NW\] GMM__ROUTING_AREA_UPDATE_REQUEST |  |   |
| OTA | 164577 | 91432992 | 17:18:25:558 | MM |  | \[NW->MS\] GMM__ROUTING_AREA_UPDATE_REJECT | GMM Cause: Network failure (17) |  |
| PS | 164678 | 91433007 | 17:18:25:558 | MM |  | \[GMM\]gprs_rau_attempt_counter=2, gprs_rau_abnormal_counter=2 |  |   |
| PS | 164679 | 91433007 | 17:18:25:558 | MM - NWSEL |  | MSG_ID_NWSEL_MM_REGN_RESULT_IND | lr_result = LR_ABNORMAL<br>mm_proc = MM_PROC_RAU<br>attempt_counter = 2 |  |
| PS | 167479 | 91455088 | 17:18:26:967 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| OTA | 172085 | 91667410 | 17:18:40:658 | MM |  | \[MS->NW\] GMM__ROUTING_AREA_UPDATE_REQUEST |  |   |
| OTA | 174501 | 91692991 | 17:18:42:298 | MM |  | \[NW->MS\] GMM__ROUTING_AREA_UPDATE_REJECT | GMM Cause: Network failure (17) |  |
| PS | 174602 | 91693007 | 17:18:42:298 | MM |  | \[GMM\]gprs_rau_attempt_counter=3, gprs_rau_abnormal_counter=3 |  |   |
| PS | 174603 | 91693007 | 17:18:42:298 | MM - NWSEL |  | MSG_ID_NWSEL_MM_REGN_RESULT_IND | lr_result = LR_ABNORMAL<br>mm_proc = MM_PROC_RAU<br>attempt_counter = 3 |  |
| PS | 177364 | 91715082 | 17:18:43:708 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| OTA | 181908 | 91927410 | 17:18:57:354 | MM |  | \[MS->NW\] GMM__ROUTING_AREA_UPDATE_REQUEST |  |   |
| OTA | 184302 | 91952679 | 17:18:58:978 | MM |  | \[NW->MS\] GMM__ROUTING_AREA_UPDATE_REJECT | GMM Cause: Network failure (17) |  |
| PS | 184403 | 91952695 | 17:18:58:978 | MM |  | \[GMM\]gprs_rau_attempt_counter=4, gprs_rau_abnormal_counter=4 |  |   |
| PS | 184404 | 91952695 | 17:18:58:978 | MM - NWSEL |  | MSG_ID_NWSEL_MM_REGN_RESULT_IND | lr_result = LR_ABNORMAL<br>mm_proc = MM_PROC_RAU<br>attempt_counter = 4 |  |
| PS | 187127 | 91973835 | 17:19:00:187 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |
| OTA | 191671 | 92187098 | 17:19:13:818 | MM |  | \[MS->NW\] GMM__ROUTING_AREA_UPDATE_REQUEST |  |   |
| OTA | 194138 | 92213305 | 17:19:15:668 | MM |  | \[NW->MS\] GMM__ROUTING_AREA_UPDATE_REJECT | GMM Cause: Network failure (17) |  |
| PS | 194245 | 92213324 | 17:19:15:668 | MM |  | **GMM new State: GMM_REG_ATTEMPT_TO_UPDATE_STATE** |  |   |
| PS | 194255 | 92213325 | 17:19:15:668 | MM |  | \[GMM\]gprs_rau_attempt_counter=5, gprs_rau_abnormal_counter=0 |  |   |
| PS | 194256 | 92213325 | 17:19:15:668 | MM - NWSEL |  | MSG_ID_NWSEL_MM_REGN_RESULT_IND | lr_result = LR_ABNORMAL<br>mm_proc = MM_PROC_RAU<br>attempt_counter = 5 |  |
| PS | 197425 | 92235082 | 17:19:16:877 | NWSEL - MM |  | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | PLMN: 26201f<br>cell_support_cs = KAL_FALSE<br>cell_support_ps = KAL_TRUE |  |

**解决方案**：

路径：**alps-release-s0.mp1.rc-tb-default_modem/modem/mcu/custom/service/sbp/sbp_nvram_config.c**
else if (sbp_id == 130) //for TIM Italy
{
   sbp_set_md_feature(SBP_MM_TRY_ABNORMAL_LAI_ONCE_MORE, KAL_TRUE, (nvram_ef_sbp_modem_config_struct\*)&sbp_feature_buf);
}

SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL: 1 "NWSEL performs search after LU abnormal."

{

**0x0: "Turn-off. Not perform PLMN selection when test SIM is inserted"**;

**0x01: "Turn-on. Perform PLMN selection"**;

};

如果是测试卡，还需要在mak文件添加，
CUSTOM_OPTION += __MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL__

log确认如下

| Type | Index | Time | Local Time | Module | Message | Comment | Time Differences |
|----|----|----|----|----|----|----|----|
| PS | 50960 | 48471258 | 09:13:30:239 | NWSEL - NWSEL | MSG_ID_NWSEL_NWSEL_SBP_DUMP_IND | nwsel_sbp_array\[2\] = (struct)<br>   sbp_name = **SBP_MM_TRY_ABNORMAL_LAI_ONCE_MORE** (enum 2)<br>   value = KAL_TRUE (enum 1)<br>nwsel_sbp_array\[26\] = (struct)<br>   sbp_name = SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL (enum 26)<br>   value = KAL_TRUE (enum 1) |  |
| OTA | 199573 | 50205530 | 09:15:21:140 | SIBE_FDD | \[NW->MS\] RRC_SI_SIB1 (UARFCN:\[412\], PSC:\[149\]) | element-0<br>   cn-DomainIdentity = ps-domain<br>   cn-Type<br>       gsm-MAP = '1401'H<br>   cn-DRX-CycleLengthCoeff = 6<br>element-1<br>   cn-DomainIdentity = cs-domain<br>   cn-Type<br>       gsm-MAP = '1401'H<br>   cn-DRX-CycleLengthCoeff = 6 |  |
| OTA | 200237 | 50209662 | 09:15:21:344 | MM | \[MS->NW\] MM__LOCATION_UPDATING_REQUEST (LU type: MM_NORMAL_LU) |  |   |
| OTA | 203531 | 50222707 | 09:15:22:150 | MM | \[NW->MS\] MM__LOCATION_UPDATING_REJECT | Reject cause: Network failure (17) |  |
| OTA | 215818 | 50478729 | 09:15:38:690 | MM | \[MS->NW\] MM__LOCATION_UPDATING_REQUEST (LU type: MM_NORMAL_LU) |  |   |
| OTA | 217114 | 50480988 | 09:15:38:690 | MM | \[NW->MS\] MM__LOCATION_UPDATING_REJECT | Reject cause: Network failure (17) |  |
| OTA | 226273 | 50735760 | 09:15:55:170 | MM | \[MS->NW\] MM__LOCATION_UPDATING_REQUEST (LU type: MM_NORMAL_LU) |  |   |
| OTA | 228554 | 50741611 | 09:15:55:370 | MM | \[NW->MS\] MM__LOCATION_UPDATING_REJECT | Reject cause: Network failure (17) |  |
| OTA | 238677 | 50997479 | 09:16:11:890 | MM | \[MS->NW\] MM__LOCATION_UPDATING_REQUEST (LU type: MM_NORMAL_LU) |  |   |
| OTA | 240177 | 51001456 | 09:16:12:096 | MM | \[NW->MS\] MM__LOCATION_UPDATING_REJECT | Reject cause: Network failure (17) |  |
| PS | 250638 | 51260694 | 09:16:28:600 | MM - NWSEL | MSG_ID_NWSEL_MM_REGN_RESULT_IND | attempt_counter = 0x05 |  |
| PS | 250863 | 51260763 | 09:16:28:600 | NWSEL - MM | MSG_ID_NWSEL_MM_PLMN_SEARCH_REQ | **rat = RAT_UMTS (enum 2) 26202** |  |
| PS | 253486 | 51269339 | 09:16:29:229 | NWSEL - MM | MSG_ID_NWSEL_MM_SYS_INFO_UPDATE_REQ | 26202 |  |

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
