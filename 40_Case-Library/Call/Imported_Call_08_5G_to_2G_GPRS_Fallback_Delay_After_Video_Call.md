---
doc_type: case
quality: imported_reference
domain: Call
rat: LTE/UTRAN/GERAN
feature: 'CSFB / redirection'
platform: Mixed
layer: 'RRC/Modem/Network'
symptom: '5G to 2G (GPRS) Fallback Delay After Video Call'
cause: '网络重定向到 3G 10738 未测到小区，后续全 band 搜到 10763 但 PLMN 为 60302，与当前 60303 不匹配，最终 3G 承接失败再转 2G'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: 'RRC release 指向 utra-FDD 10738 后测量结果为 0；可测 10763 小区 PLMN 不匹配'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - csfb
  - redirection
  - plmn-mismatch
search_tier: case_summary
---

# 5G to 2G (GPRS) Fallback Delay After Video Call

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，已提炼为 CSFB / RAT change 中目标 3G 小区不可用和 PLMN 不匹配案例。

## 用户现象
5G to 2G (GPRS) Fallback Delay After Video Call

## 结论

首坏点在 3G 重定向承接阶段：网络释放 LTE 并指向 UTRA FDD `10738`，但 UE 对 `10738` 初始测量结果为 0；随后全 band 搜到 `10763` 小区，但该小区 PLMN 是 `60302`，与当前卡 `60303` 不匹配，也不在 ePLMN 中，导致 3G 承接失败，后续再转 2G。

因此该现象不应简单写成“5G/视频通话导致回落慢”，而应拆成网络重定向目标、3G 小区可用性和 PLMN 匹配问题。

## 关键证据

- 原始分类：四、语音通话
- 来源：通话问题案例补充.md
- 拆分序号：8
- LTE release 指向：`utra-FDD = 10738`。
- `WL1C_WRCC_INIT_MEAS_IND Num_Rslts = 0`，目标频点未测到小区。
- 全 band 搜到 `DL_UARFCN = 10763`，但 SIB18 PLMN 为 `60302`。
- 当前卡 PLMN 为 `60303`，`WRCC_COM_CheckExistInEPLMN_List = 0`，`not ePLMN`。
- `MSG_ID_TM_LTE_CHG_TO_UTRAN_CNF ho_status = DM_HO_FAILURE` 后转 GSM。

## 定位口径

| 判断点 | 结论 |
|---|---|
| LTE release 指向具体 UTRA 频点 | 先确认该频点是否能测到小区 |
| 目标频点测量结果为 0 | 重点查网络配置、覆盖或测量/RF |
| 搜到其它 3G 小区但 PLMN 不匹配 | 不能驻留，继续查 ePLMN/漫游/网络规划 |
| 3G 承接失败后转 2G | 这是后续回退结果，不是第一坏点 |

## 复用边界

- 适用于 CSFB/RAT change 后 3G 承接失败、再转 2G 的问题。
- 若目标 3G 频点可测且 PLMN 匹配，再继续查 RRC 建链、LAU/CM Service 和 CS call setup。

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例2：5G to 2G (GPRS) Fallback Delay After Video Call

**分析**：确认sim注册的网络，以及信号强度和质量

//网侧通知回落3G的10738频点，但是10738频点没有测到小区
64331-49   09:45:07.602   --   FF   -> EXTENDED_SERVICE_REQUEST   24:42:19.805
64452-6   09:45:07.880   SIM1   LTE   FF   <- RRCCONNECTIONRELEASE   24:42:20.083
   utra-FDD = 10738
6   64528-1   09:45:07.969   FF   MSG_ID_TM_LTE_CHG_TO_UTRAN_FDD_REQ   MOD_LASM_1->MOD_WRRC_1   0x04EC

7   64534-84   09:45:07.970   FF   WL1C_WRCC_INIT_MEAS_REQ   MOD_WRCC_1->MOD_WRCC_1   0x0294
   DL_UARFCN
   \[0\] = 10738
9   64588-1   09:45:08.241   FF   WL1C_WRCC_INIT_MEAS_IND   MOD_FAKEL1->MOD_WRCC_1   0x0296
   Num_Rslts = 0
//然后3G进行全band搜搜到了10763的小区363，但是其PLMN是60302，当前卡的PLMN是60303，PLMN不匹配所以不能驻上
16   64600-87   09:45:08.782   FF   WL1C_WRCC_INIT_MEAS_REQ   MOD_WRCC_1->MOD_WRCC_1   0x0294
   Init_ARFCN_Meas
   Num_Band = 2
   Num_Band_Prior = 0
   Meas_Band
   \[0\] = 1
   \[1\] = 8
18   64601-43   09:45:09.550   FF   WL1C_WRCC_INIT_MEAS_IND   MOD_FAKEL1->MOD_WRCC_1   0x0296
   Num_Rslts = 1
   Init_Report
   \[0\]
   DL_UARFCN = 10763
   PGC = 363
   UTRA_RSSI = 43
   CPICH_Ec_No = 112
   CPICH_RSCP = 380
   RF_ScanBand = 1
24   64614-44   09:45:09.754   FF   <- SIB18
   plmnsOfIntraFreqCellsList

   plmn-Identity
   mcc
   = 6
   = 0
   = 3
   mnc
   = 0
   = 2
//PLMN不匹配所以不能驻上，重定向到3G失败，然后重定向到2G
64615-69   09:45:09.755   09:45:09.755   WRCC:  WRCC_CS_CTRL, WRCC_COM_CheckPLMN_Match   WPS_WRCC   24:42:21.958
64615-70   09:45:09.755   09:45:09.755   WRCC:  Single cell WRCC_CS_CTRL WRCC_COM_CheckPLMN_Match NumMultiPLMN  0   WPS_WRCC   24:42:21.958
64615-71   09:45:09.755   09:45:09.755   WRCC :\*\*\* PLMN_ID MCC: 6,0,3   WPS_WRCC   24:42:21.958
64615-72   09:45:09.755   09:45:09.755   WRCC: \*\*\* PLMN_ID MNC: 0,2,15   WPS_WRCC   24:42:21.958
64615-73   09:45:09.755   09:45:09.755   WRCC : WRCC  ST_PLMN_Id   WPS_WRCC   24:42:21.958
64615-74   09:45:09.755   09:45:09.755   WRCC :\*\*\* PLMN_ID MCC: 6,0,3   WPS_WRCC   24:42:21.958
64615-75   09:45:09.755   09:45:09.755   WRCC: \*\*\* PLMN_ID MNC: 0,3,0   WPS_WRCC   24:42:21.958
64615-76   09:45:09.755   09:45:09.755   WRCC:WRCC_COM_CheckExistInEPLMN_List =0   WPS_WRCC   24:42:21.958
64615-77   09:45:09.755   09:45:09.755   WRCC :\*\*\* PLMN_ID MCC: 6,0,3   WPS_WRCC   24:42:21.958
64615-78   09:45:09.755   09:45:09.755   WRCC: \*\*\* PLMN_ID MNC: 0,3,0   WPS_WRCC   24:42:21.958
64615-79   09:45:09.755   09:45:09.755   WRCC:not ePLMN   WPS_WRCC   24:42:21.958
64615-87   09:45:09.755   09:45:09.755   WRCC:CS_FailCause:1
34   64845-79   09:45:20.865   FF   MSG_ID_TM_LTE_CHG_TO_UTRAN_CNF   MOD_WRRC_1->MOD_LASM_1   0x0349
   ho_status = DM_HO_FAILURE
35   64871-12   09:45:20.890   FF   MSG_ID_TM_LTE_RAT_CHG_TO_GSM_REQ   MOD_LASM_1->MOD_GRR_1   0x0270
(20260227T08:42:57)

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
