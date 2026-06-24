---
doc_type: case
quality: imported_reference
domain: IMS
rat: LTE
feature: 'VideoCall'
platform: Mixed
layer: 'IMS/ESM/AP/Modem'
symptom: 'DUT视频通话闪退'
cause: 'DUT 只建立 QCI1 语音专载，未建立视频所需 QCI2 专载；同时存在视频分辨率设置失败和 DUT/REF 分辨率能力差异'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: 'ViLTE 建呼中缺少 QCI2 dedicated bearer，AP 侧 `RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION` 返回 RADIO_NOT_AVAILABLE'
confidence: medium
status: summarized_with_log_gap
tags:
  - imported
  - split_from_bucket
  - ims
  - vilte
  - qci2
  - video-resolution
search_tier: case_summary
---

# DUT视频通话闪退

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，已收敛为 IMS/ViLTE 专项待补证 case，不归 LTE 注册或普通 CS Call。

## 用户现象
DUT视频通话闪退

## 结论

当前能确认的第一异常是 DUT ViLTE 建呼只建立了 QCI1 语音专载，没有像对比 MTK 一样同时建立 QCI1/QCI2 两个 dedicated bearer。资料还提到 DUT 视频分辨率为 `VGA-30`，REF 为 `QVGA-15`，AP 侧 `RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION` 返回 `RADIO_NOT_AVAILABLE`。

因此该 case 不能只写成“视频通话闪退”。排查应围绕 ViLTE 视频承载、视频分辨率能力、IMS service 状态和 AP/modem 能力同步补证。

## 关键证据

- 原始分类：五、视频通话
- 来源：通话问题案例补充.md
- 拆分序号：10
- DUT：IMS PDN 默认承载 QCI5 正常，INVITE 后只收到 QCI1 dedicated bearer。
- REF：同类流程里同时收到 QCI1 和 QCI2 dedicated bearer。
- AP：`RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION error: RADIO_NOT_AVAILABLE`。
- 能力差异：DUT 使用 `VGA-30`，REF 使用 `QVGA-15`。

## 定位口径

| 判断点 | 结论 |
|---|---|
| QCI1 有、QCI2 无 | 重点查视频专载建立、SDP/QoS、网络/IMS profile |
| 分辨率设置失败 | 查 AP IMS service、modem video capability 和配置 |
| REF 分辨率更低且可通 | 可能是视频能力协商或 profile 差异 |
| 闪退 | 需要 AP crash/tombstone/logcat 才能判断 UI/应用崩溃根因 |

## 下次复现补证清单

| 必抓证据 | 具体内容 | 能证明什么 |
|---|---|
| AP logcat / tombstone / ANR | Dialer/IMS service/media/camera/SurfaceFlinger 崩溃栈，闪退准确时间点 | “闪退”是应用崩溃、native 崩溃还是 call session 被释放 |
| modem SIP/SDP log | INVITE、183、UPDATE、200 OK 中 video codec、profile-level-id、分辨率、带宽 | 视频能力协商是否超出 DUT 支持 |
| ESM/QoS log | IMS default QCI5、audio QCI1、video QCI2 dedicated bearer 建立/拒绝 | QCI2 是网络未下发、终端未接受还是 AP 未触发 |
| AP IMS capability dump | ViLTE 开关、video resolution、RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION 返回值 | AP 与 modem 视频能力是否同步 |
| 对比机同卡日志 | REF 的 SDP、QCI2、分辨率、UI 行为 | 区分网络策略和 DUT 能力/profile 差异 |
| 设备性能证据 | CPU/GPU/memory、thermal、camera/codec log | 排除视频启动瞬间 AP 资源或 codec 问题 |

判定口径：

- 没有 tombstone/ANR 时，不要把“闪退”写成 AP 崩溃根因。
- 有 SIP 200 OK 但无 QCI2，只能说明视频承载缺失，仍需区分网络未下发和终端未接受。
- `RADIO_NOT_AVAILABLE` 需要同时看 radio/modem 是否重启、IMS service 是否断开、video request 是否发错时机。

## 原始案例内容

### 案例1：DUT视频通话闪退

分析思路：重点检查modem侧log，检查通话建立流程

对比两台设备log发现，MTK视频通话成功建了两个承载(QCI1 QCI2)，展锐只有一个(QCI1)，展锐视频通话承载未成功建立
ZR MODEM LOG,
-> PDN_CONNECTIVITY_REQUEST   lg   16:45:14.686
<- ACTIVATE_DEFAULT_EPS_BEARER_CONTEXT_REQUEST   lg   16:45:14.826   QCI 5
-> ACTIVATE_DEFAULT_EPS_BEARER_CONTEXT_ACCEPT   lg   16:45:14.826
-> \[0\]INVITE   lg   16:45:23.678   VILTE
<- \[0\]100   lg   16:45:23.736
<- \[0\]183   lg   16:45:24.504
<- ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_REQUEST   lg   16:45:24.547   QCI 1
-> ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_ACCEPT   lg   16:45:24.547
<- \[0\]200   lg   16:45:24.655
MTK MODEM LOG,
Type   Index   Time   Local Time   Module   Message   Comment   Time Differences
OTA   132150   449738   16:16:54:134   ESM   \[MS->NW\] ESM_MSG_PDN_CONNECTIVITY_REQUEST (PTI:2, EBI:0)   ims pdn
OTA   134915   450923   16:16:54:134   ESM   \[NW->MS\] ESM_MSG_ACTIVATE_DEFAULT_EPS_BEARER_CONTEXT_REQUEST (PTI:2, EBI:6)   QCI 5
OTA   135049   450941   16:16:54:134   ESM   \[MS->NW\] ESM_MSG_ACTIVATE_DEFAULT_EPS_BEARER_CONTEXT_ACCEPT (PTI:0, EBI:6)
SIP   818314   1547477   16:18:04:402   \[MS->NW\]\[P1\]\[S1\]INVITE tel:0211914294;phone-context=ims.mnc001.mcc530.3gppnetwork.org SIP/2.0   vilte
SIP   830434   1552297   16:18:04:602   \[NW->MS\]\[P1\]\[S1\]SIP/2.0 100 Trying
SIP   842834   1566793   16:18:05:602   \[NW->MS\]\[P1\]\[S1\]SIP/2.0 183 Session Progress
OTA   845940   1568673   16:18:05:802   ESM   \[NW->MS\] ESM_MSG_ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_REQUEST (PTI:0, EBI:7)   QCI 1
OTA   846010   1568681   16:18:05:802   ESM   \[NW->MS\] ESM_MSG_ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_REQUEST (PTI:0, EBI:8)   QCI 2
OTA   846190   1568697   16:18:05:802   ESM   \[MS->NW\] ESM_MSG_ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_ACCEPT (PTI:0, EBI:7)
OTA   846505   1568744   16:18:05:802   ESM   \[MS->NW\] ESM_MSG_ACTIVATE_DEDICATED_EPS_BEARER_CONTEXT_ACCEPT (PTI:0, EBI:8)
SIP   854841   1571402   16:18:06:002   \[MS->NW\]\[P1\]\[S1\]UPDATE sip:pcgw-prim.imsgroup0-323-0000003.wtsbc01.ims.internal.vfnz:6000;x-afi=175;encoded-parm=QbkRBthOEgsTXgYSERwIGVteQwcCA18fHRdFRkZWFBkid3B0a3UgODkkLjg6IT07fz0hM29jZ25p;b2bdlg=6844b5e9-68b129fe2b78a576-gm-po-lucentPCSF-074645 SIP/2.0
SIP   859620   1576284   16:18:06:202   \[NW->MS\]\[P1\]\[S1\]SIP/2.0 200 OK
SIP   861776   1576873   16:18:06:202   \[NW->MS\]\[P1\]\[S1\]SIP/2.0 180 Ringing
SIP   889458   1603103   16:18:08:002   \[NW->MS\]\[P1\]\[S1\]SIP/2.0 200 OK

进一步分析，发现DUT ims服务异常，但两者是同卡，不应该出现这种差异。经展锐确认，发现DUT视频分辨率更高(VGA-30)，REF(QVGA-15)

//DUT video resolution

\[0162\]< RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION error 1 \[SUB0\] \[0162\]< RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION error: com.android.internal.telephony.CommandException: RADIO_NOT_AVAILABLE

## 原始资料边界

- 当前资料足以作为 ViLTE QCI2 / resolution 补证模板，但不足以闭合到单一代码根因。
- 后续 IMS 视频通话专项应与 [视频通话拨号流程](../../20_Service-Flows/IMS/视频通话拨号流程.md)、[视频通话来电流程](../../20_Service-Flows/IMS/视频通话来电流程.md) 和 [视频通话界面与Log](../../20_Service-Flows/IMS/视频通话界面与Log.md) 互链。
