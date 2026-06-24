---
doc_type: case
quality: imported_reference
domain: Call
rat: LTE/UMTS
feature: 'CSFB / RF calibration'
platform: Mixed
layer: 'RF/Modem'
symptom: '一台DUT插联通卡通话正常，其它DUT fail；插移动卡问题不复现'
cause: 'Fail DUT 无 RF 校准数据，CSFB 后无法驻留 3G 小区；Pass DUT 同卡可完成 CSFB、3G 通话并回 LTE'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: 'Fail DUT log 提示 no RF calibration data，随后 MT CSFB 到 3G 扫频但未完成 3G 驻留'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - csfb
  - rf-calibration
  - call-fail
search_tier: case_summary
---

# 一台DUT插联通卡通话正常，其它DUT fail；插移动卡问题不复现

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，已提炼为 CSFB 失败背后的 RF 校准缺失案例。

## 用户现象
一台DUT插联通卡通话正常，其它DUT fail；插移动卡问题不复现

## 结论

首坏点在 Fail DUT 的 RF 校准数据缺失。Pass DUT 使用同一张联通卡可完成 CSFB、3G 驻留、通话建立和回 LTE；Fail DUT 同卡收到 MT CSFB 后无法驻留到 3G，并且 log 明确提示无 RF calibration data。因此该问题优先归 RF 校准/单机硬件，不应归因到联通卡、AP 拨号或 CSFB 协议策略。

## 关键证据

- 原始分类：四、语音通话
- 来源：通话问题案例补充.md
- 拆分序号：7
- Pass DUT：`EMM_Extended_Service_Request(service type="MO_CSFB")` 后 LTE release redirect 到 3G，`CM_SERVICE_ACCEPT`、`SETUP`、`CONNECT` 正常，结束后回 LTE。
- Fail DUT：同卡 IMSI 一致，但 log 出现 `There is no any RF calibration data in DUT`。
- Fail DUT：收到 `EMM_Extended_Service_Request(service type="MT_CSFB")` 和 LTE release 后，3G 搜频未完成正常驻留。

## 定位口径

| 判断点 | 结论 |
|---|---|
| 同 SIM 在 Pass DUT 正常 | 排除卡/签约优先级提高 |
| Fail DUT 缺 RF calibration data | 优先查校准/NV/单机硬件 |
| CSFB 触发存在但 3G 驻留失败 | 不按“未触发 CSFB”处理 |
| 插移动卡不复现 | 可能与运营商 RAT/频段/覆盖有关，仍需先处理 RF 校准缺失 |

## 复用边界

- 适用于“通话失败表象下，首坏点实际在 RF 校准/3G 承接”的问题。
- 若 Fail DUT RF 校准完整，再继续查 3G 频点、RRC 建链、CS 注册和网络侧 release cause。

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例1：一台DUT插联通卡通话正常，其它DUT fail；插移动卡问题不复现

分析：首先要确认插入的sim是否是同一张，然后对比modem log搜网流程的差异

**PASS DUT** 查看log发现，DUT成功csfb并驻留到3G小区，整个通话流程正常，结束后重新回到4G

| **Type** | **Index** | **Time** | **Local Time** | **Module** | **Message** | **Comment** | **Time Differences** |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| SYS | 45349 | 18345625 | 15:19:04:806 | NIL | The RF calibration data of the following modules are missing: <br> CDMA2000: RX, TX, RF self-cal, DPD |    |    |
| SYS | 49073 | 18356138 | 15:19:05:406 | NIL | \[AT_RX p39,ch3\]ATD10010; |    |    |
| OTA | 50700 | 18356413 | 15:19:05:406 | EMM_NASMSG | \[MS->NW\] EMM_Extended_Service_Request(service type="MO_CSFB", CSFB response="CSFB_UNUSED") | csfb |    |
| OTA | 51464 | 18357101 | 15:19:05:606 | ERRC_CONN | \[NW->MS\] ERRC_RRCConnectionRelease(EARFCN\[1650\], PCI\[442\])(cause:\[ReleaseCause_other\], redirectInfo:\[1\]) |    |    |
| PS | 52929 | 18357761 | 15:19:05:606 | MM - RATCM | MSG_ID_MM_RATCM_RAT_CHANGE_REQ |    |    |
| PS | 58637 | 18367828 | 15:19:06:210 | RATDM | \[RATDM\] RAT change from 4G to 3G |    |    |
| OTA | 61536 | 18369355 | 15:19:06:410 | ADR_FDD | \[MS->NW\] FDD_RRC__RRC_CONNECTION_REQUEST |    |    |
| OTA | 62643 | 18371519 | 15:19:06:410 | ADR_FDD | \[NW->MS\] FDD_RRC__RRC_CONNECTION_SETUP |    |    |
| OTA | 63498 | 18373180 | 15:19:06:610 | ADR_FDD | \[MS->NW\] FDD_RRC__RRC_CONNECTION_SETUP_COMPLETE |    |    |
| OTA | 64612 | 18377368 | 15:19:06:816 | MM | \[NW->MS\] MM__IDENTITY_REQUEST |    |    |
| OTA | 64615 | 18377369 | 15:19:06:816 | MM | \[MS->NW\] MM__IDENTITY_RESPONSE (Type: MM_IMSI_TYPE) | \[Association IMSI: 460012275241579\]<br> Mobile Country Code (MCC): China (460)<br> Mobile Network Code (MNC): China Unicom (01) |    |
| OTA | 65665 | 18382080 | 15:19:07:216 | MM | \[MS->NW\] MM__CM_SERVICE_REQUEST | 3G驻网 |    |
| PS | 66266 | 18382175 | 15:19:07:216 | SDM | \[SDM\] Service status: current RAT = RAT_UMTS | 3G UMTS |    |
| PS | 66268 | 18382175 | 15:19:07:216 | SDM | \[SDM\] Service status: PLMN id = MCC1\[4\] MCC2\[6\] MCC3\[0\] MNC1\[0\] MNC2\[1\] MNC3\[15\] |    |    |
| OTA | 67703 | 18384089 | 15:19:07:216 | MM | \[NW->MS\] MM__CM_SERVICE_ACCEPT |    |    |
| OTA | 67712 | 18384094 | 15:19:07:216 | CC | \[MS->NW\] CC__SETUP |    |    |
| OTA | 68098 | 18386434 | 15:19:07:416 | CC | \[NW->MS\] CC__CALL_PROCEEDING |    |    |
| OTA | 72290 | 18417528 | 15:19:09:416 | ADR_FDD | \[NW->MS\] FDD_RRC__RADIO_BEARER_SETUP |    |    |
| OTA | 73184 | 18421750 | 15:19:09:616 | ADR_FDD | \[MS->NW\] FDD_RRC__RADIO_BEARER_SETUP_COMPLETE |    |    |
| SYS | 74090 | 18423765 | 15:19:09:816 | NIL | The RF calibration data of the following modules are missing: <br> CDMA2000: RX, TX, RF self-cal, DPD |    |    |
| OTA | 76439 | 18430513 | 15:19:10:216 | CC | \[NW->MS\] CC__ALERTING |    |    |
| OTA | 77632 | 18431128 | 15:19:10:216 | CC | \[NW->MS\] CC__CONNECT |    |    |
| OTA | 77637 | 18431129 | 15:19:10:216 | CC | \[MS->NW\] CC__CONNECT_ACKNOWLEDGE |    |    |
| OTA | 86298 | 18451794 | 15:19:11:616 | MM | \[MS->NW\] GMM__SERVICE_REQUEST |    |    |
| OTA | 89966 | 18456752 | 15:19:11:816 | MM | \[NW->MS\] GMM__SERVICE_ACCEPT |    |    |
| OTA | 91004 | 18459876 | 15:19:12:016 | ADR_FDD | \[NW->MS\] FDD_RRC__RADIO_BEARER_SETUP |    |    |
| OTA | 95913 | 18471767 | 15:19:12:816 | ADR_FDD | \[MS->NW\] FDD_RRC__RADIO_BEARER_SETUP_COMPLETE |    |    |
| OTA | 98102 | 18476756 | 15:19:13:216 | SM | \[NW->MS\] SM__MODIFY_PDP_CONTEXT_REQUEST_NW |    |    |
| OTA | 98173 | 18476765 | 15:19:13:216 | SM | \[MS->NW\] SM__MODIFY_PDP_CONTEXT_ACCEPT_MS |    |    |
| OTA | 106429 | 18495309 | 15:19:14:416 | CC | \[MS->NW\] CC__DISCONNECT | MO挂断 |    |
| OTA | 108842 | 18498628 | 15:19:14:616 | CC | \[NW->MS\] CC__RELEASE |    |    |
| OTA | 108847 | 18498630 | 15:19:14:616 | CC | \[MS->NW\] CC__RELEASE_COMPLETE | 通话结束 |    |
| PS | 122311 | 18523685 | 15:19:16:216 | ERRC - RSVAE | MSG_ID_EAS_RSVAE_FREQUENCY_SCAN_START_REQ |    |    |
| PS | 126564 | 18525877 | 15:19:16:416 | RATDM | \[RATDM\] RAT change from 3G to 4G | 回到4G |    |
| SYS | 136793 | 18534092 | 15:19:16:818 | NIL | \[ATCI_AT_R_0 s35\]460012275241579 |    |    |
| PS | 136811 | 18534098 | 15:19:16:818 | SDM | \[SDM\] Service status: current RAT = RAT_LTE | 4G LTE |    |

**FAILE DUT**

查看log，插入的卡和PASS DUT一致，发现没有驻留到3G小区

| **Type** | **Index** | **Time** | **Local Time** | **Module** | **Message** | **Comment** | **Time Differences** |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| SYS | 127658 | 210044333 | 17:24:51:709 | NIL | \[ATCI_AT_R_0 s35\]460012275241579 |    |    |
| SYS | 158077 | 210104248 | 17:24:55:517 | NIL | There is no any RF calibration data in DUT, please perform RF calibration or download calibration data. |    |    |
| OTA | 174393 | 210151044 | 17:24:58:522 | EMM_NASMSG | \[NW->MS\] EMM_CS_Service_Notification(paging identity="TMSI_PAGING_TYPE") |    |    |
| OTA | 175072 | 210151148 | 17:24:58:522 | EMM_NASMSG | \[MS->NW\] EMM_Extended_Service_Request(service type="MT_CSFB", CSFB response="CSFB_ACCEPTED_BY_UE") |    |    |
| OTA | 175634 | 210151407 | 17:24:58:522 | ERRC_CONN | \[NW->MS\] ERRC_RRCConnectionRelease(EARFCN\[1650\], PCI\[442\])(cause:\[ReleaseCause_other\], redirectInfo:\[1\]) |    |    |
| PS | 176993 | 210151833 | 17:24:58:522 | MM - RATCM | MSG_ID_MM_RATCM_RAT_CHANGE_REQ |    |    |
| PS | 189900 | 210346082 | 17:25:10:948 | RRM_FDD - RSVAG | MSG_ID_GAS_RSVAG_FREQUENCY_SCAN_START_REQ |    |    |
| PS | 189906 | 210346083 | 17:25:10:948 | RSVAG - RRM_FDD | MSG_ID_RSVAG_GAS_FREQUENCY_SCAN_START_CNF |    |    |
| PS | 189924 | 210346086 | 17:25:10:948 | MRS | \[MRS\] LLA Occupy by RAT:\[MRS_GSM_RAT\], Current occupied RAT:\[MRS_GSM_RAT\] |    |    |
| PS | 189933 | 210346087 | 17:25:10:948 | MPAL_FDD - GISE_FDD | MSG_ID_MPHC_POWER_SCAN_REQ |    |    |
| PS | 191903 | 210392023 | 17:25:13:983 | GISE_FDD - MPAL_FDD | MSG_ID_MPHC_POWER_SCAN_CNF |    |    |

对比两台设备射频参数，发现FAILE DUT参数无法读取，怀疑是没有校准，需硬件同事核查

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
