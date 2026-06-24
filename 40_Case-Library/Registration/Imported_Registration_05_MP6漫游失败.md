---
doc_type: case
quality: imported_reference
domain: Registration
rat: 3G
feature: Roaming / APN / PDP
platform: MTK
layer: APN/Modem/Network
symptom: MP6漫游失败
cause: 设备已注册到 20205 3G 漫游网络，但 23430 APN 配置只匹配虚拟运营商，非对应 MVNO SIM 无法匹配 APN，导致不发起 PDP 请求
source_log: Old Outline knowledge base; split from 注网问题案例补充.md
first_bad_point: AT +EGREG 已显示 roaming 注册成功，但打开漫游后仍无 PDP 请求，首坏点转为 APN 匹配
confidence: medium
status: summarized
tags:
  - imported
  - split_from_bucket
  - roaming
  - apn
  - pdp
search_tier: case_summary
---

# MP6漫游失败

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
MP6漫游失败

## 结论

这不是纯注册失败。log 显示设备已经注册到 `20205` 3G 漫游网络，并上报 roaming 状态；真正的首坏点是后续没有发起 PDP 请求。原始分析定位到 `23430` APN 配置均为虚拟运营商专用，非对应 MVNO SIM 无法匹配 APN，导致数据业务异常。

复用时应按“注册成功后数据失败”处理，并回填到 APN 配置方法。

## 关键证据

- 原始分类：二、网络Reject
- 来源：注网问题案例补充.md
- 拆分序号：5
- `GMM__ATTACH_ACCEPT` 后有 `+EGREG: 5,...`，说明已处于 roaming registered。
- 打开 / 关闭漫游开关均无 PDP 请求，和对比机“打开漫游开关能发起 PDP 请求”不同。
- 原始结论：`23430` APN 均为虚拟运营商配置，SIM 不匹配时无法命中。

## 定位口径

| 检查项 | 判断 |
|---|---|
| 注册状态 | 先看 `+EGREG: 5` / Attach Accept，确认是否已经 roaming 注册 |
| 漫游开关 | 漫游开关只决定是否允许数据，不能替代 APN 匹配 |
| APN 匹配 | 检查 MCCMNC、MVNO type/value、APN type 是否命中当前 SIM |
| 归属边界 | 注册已成功时，应转到 Data / APN，而不是继续查 PLMN reject |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：MP6漫游失败

分析：英国国外漫游失败，检查NV和APN配置

【REPRODUCING PROCEDURES】
1.插入23430 sim卡
2.注册到20205 3G网络
3.漫游开关默认打开
4.打开和关闭漫游开关，均无发起PDP请求---NOK

【EXPECTED BEHAVIOUR】
4.打开漫游开关时能发起PDP请求

打开和关闭漫游开关，均无发起PDP请求，信号良好

| Type | Index | Time | Local Time | Module | Message | Comment | Time Differences |
|----|----|----|----|----|----|----|----|
| PS | 104643 | 508645 | 18:12:03:014 | NWSEL - MM | MSG_ID_NWSEL_MM_PLMN_SEARCH_REQ | rat = RAT_UMTS |  |
| OTA | 106779 | 516992 | 18:12:03:616 | SIBE_FDD | \[NW->MS\] RRC_SI_SIB11 (UARFCN:\[1537\], PSC:\[21\]) |  |   |
| PS | 107506 | 534184 | 18:12:04:679 | CSE_FDD | \[CSE\] The band of DB_CELL \[index = 0, UARFCN = 1537, PHYSCELLID = 21\] is Band 4 |  |   |
| OTA | 108112 | 534576 | 18:12:04:679 | MM | \[MS->NW\] GMM__ATTACH_REQUEST |  |   |
| OTA | 110175 | 535864 | 18:12:04:879 | ADR_FDD | \[MS->NW\] FDD_RRC__RRC_CONNECTION_REQUEST |  |   |
| OTA | 110740 | 543018 | 18:12:05:285 | ADR_FDD | \[NW->MS\] FDD_RRC__RRC_CONNECTION_SETUP |  |   |
| OTA | 111251 | 544757 | 18:12:05:485 | ADR_FDD | \[MS->NW\] FDD_RRC__RRC_CONNECTION_SETUP_COMPLETE |  |   |
| PS | 111580 | 546141 | 18:12:05:485 | MEME_FDD | MEME: PSC 21, RSCP -84, EcN0 -4, RRC_FDD_DB_CellType_monitored, SyncInfo(1), TM(0), OFF(0), CIO 0, dbIdx 0, active 1 |  |   |
| OTA | 111921 | 549411 | 18:12:05:685 | MM | \[NW->MS\] GMM__AUTHENTICATION_AND_CIPHERING_REQ |  |   |
| OTA | 112027 | 550038 | 18:12:05:685 | MM | \[MS->NW\] GMM__AUTHENTICATION_AND_CIPHERING_RSP |  |   |
| OTA | 112527 | 553319 | 18:12:05:885 | MM | \[NW->MS\] GMM__ATTACH_ACCEPT | 20205 |  |
| OTA | 112606 | 553336 | 18:12:05:885 | MM | \[MS->NW\] GMM__ATTACH_COMPLETE |  |   |
| SYS | 113546 | 553489 | 18:12:05:885 | NIL | \[AT_URC p37,ch1\]+EGREG: 5,"000E","0000000E",4,"03",0,0,0,0 | roaming |  |

检查APN配置，发现23430 APN都是虚拟运营商的，如果sim卡不是对应虚拟运营商的卡，则不会匹配相应的APN配置，所以会导致网络功能出问题。

**解决方案**：

MTK提供非虚拟运营商的APN，这样插卡后会优先匹配该配置。
