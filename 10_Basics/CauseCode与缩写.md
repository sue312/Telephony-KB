---
quality: curated
search_tier: main_entry
doc_type: index
domain: Meta
status: active
---

# CauseCode与缩写

跨业务域都会用到的 cause、log 标签、缩写和标签体系统一放这里。`00_Index/速查` 只保留导航入口，具体内容以这篇为准。
## CauseCode速查

> 这里先放定位常用项。遇到真实 case 时，把项目/运营商特殊含义补进来。

## LTE EMM Reject 常见方向

| Cause | 常见含义 | 定位方向 |
|---|---|---|
| 3 | Illegal UE | 用户身份或签约异常，需核查SIM/网络侧 |
| 6 | Illegal ME | 设备身份被拒，关注IMEI/白名单/黑名单 |
| 7 | EPS services not allowed | EPS服务不允许，关注签约、SIM、PLMN |
| 8 | EPS and non-EPS services not allowed | EPS和非EPS都不允许，通常偏网络/签约 |
| 10 | Implicitly detached | 网络认为UE已隐式分离，关注恢复流程 |
| 11 | PLMN not allowed | PLMN不允许，关注SIM禁用PLMN、漫游策略 |
| 12 | Tracking area not allowed | TA不允许，关注位置区/漫游/网络配置 |
| 13 | Roaming not allowed in this tracking area | 当前TA不允许漫游 |
| 14 | EPS services not allowed in this PLMN | 当前PLMN不允许EPS |
| 15 | No suitable cells in tracking area | 当前TA无合适小区，关注小区选择/网络覆盖 |

## 5GMM Reject 常见方向

| Cause | 常见含义 | 定位方向 |
|---|---|---|
| 3 | Illegal UE | 用户身份或签约异常 |
| 5 | PEI not accepted | 设备身份不接受，关注IMEI/PEI |
| 7 | 5GS services not allowed | 5GS服务不允许 |
| 11 | PLMN not allowed | PLMN不允许 |
| 12 | Tracking area not allowed | TA不允许 |
| 13 | Roaming not allowed in this tracking area | 当前TA不允许漫游 |
| 15 | No suitable cells in tracking area | 当前TA无合适小区 |

## IMS SIP 常见响应

| SIP码 | 常见含义                    | 定位方向                          |
| ---- | ----------------------- | ----------------------------- |
| 100  | Trying                  | 临时响应，说明请求已被接收                 |
| 180  | Ringing                 | 被叫振铃                          |
| 183  | Session Progress        | 早期媒体/协商中                      |
| 200  | OK                      | 成功                            |
| 401  | Unauthorized            | 注册鉴权挑战，首次出现通常正常               |
| 403  | Forbidden               | 注册或业务被禁止，关注签约、IMPU/IMPI、运营商策略 |
| 404  | Not Found               | 用户或路由不存在                      |
| 408  | Request Timeout         | 请求超时，关注网络、P-CSCF、传输链路         |
| 480  | Temporarily Unavailable | 对端暂不可达                        |
| 486  | Busy Here               | 对端忙                           |
| 500  | Server Internal Error   | IMS网络内部异常                     |
| 503  | Service Unavailable     | IMS服务不可用或拥塞                   |

## CS Call Q.850 常见方向

| Cause | 常见含义 | 定位方向 |
|---|---|---|
| 16 | Normal call clearing | 正常释放 |
| 17 | User busy | 用户忙 |
| 18 | No user responding | 无响应 |
| 19 | No answer from user | 用户未应答 |
| 21 | Call rejected | 呼叫被拒 |
| 34 | No circuit/channel available | 无可用电路或信道 |
| 38 | Network out of order | 网络故障 |
| 41 | Temporary failure | 临时故障 |
| 47 | Resource unavailable | 资源不可用 |
| 57 | Bearer capability not authorized | 承载能力未授权 |
| 58 | Bearer capability not presently available | 承载能力当前不可用 |
| 88 | Incompatible destination | 目的端不兼容 |

## 记录规则

每遇到一个 cause code，要补三件事：

- 发生在哪个过程：Attach/TAU/Registration/IMS REGISTER/INVITE/CS Call。
- AP是否正确上报：ServiceState、IMS状态、DisconnectCause。
- Modem侧是否有更底层原因：NAS/RRC/SIP/Q.850/内部状态机。

## Log标签速查

## Android Telephony 常见标签

| 标签 | 关注点 |
|---|---|
| `RILJ` | Framework发起的RIL请求、RIL响应、UNSOL上报 |
| `RILC` | Native RIL层行为，是否转发到vendor RIL |
| `RadioResponse` | AIDL/HIDL radio response |
| `RadioIndication` | AIDL/HIDL radio indication |
| `ServiceStateTracker` | 注册状态、服务状态、RAT、PLMN变化 |
| `NetworkRegistrationManager` | 网络注册状态查询和回调 |
| `GsmCdmaPhone` | Phone对象状态、CS call相关入口 |
| `PhoneInterfaceManager` | 上层telephony API调用 |
| `TelephonyRegistry` | 对外广播服务状态、信号、数据状态 |
| `CarrierConfigLoader` | 运营商配置加载 |
| `SubscriptionInfoUpdater` | SIM插拔、订阅信息更新 |
| `UiccController` | UICC卡状态、slot状态 |
| `UiccCard` | 卡对象状态 |
| `SIMRecords` | IMSI、SPN、EF文件加载 |
| `IccCardProxy` | SIM状态对外呈现 |

## IMS / Call 常见标签

| 标签 | 关注点 |
|---|---|
| `ImsResolver` | IMS服务绑定和feature发现 |
| `ImsManager` | IMS开关、能力、注册入口 |
| `ImsService` | 设备厂商IMS服务行为 |
| `MmTelFeature` | MMTEL能力、语音/视频能力 |
| `ImsPhone` | IMS phone层呼叫状态 |
| `ImsPhoneCallTracker` | IMS call状态机 |
| `ImsCallSession` | SIP会话和call session |
| `ImsRegistrationImplBase` | IMS注册状态回调 |
| `Wfc` / `Epdg` | VoWiFi/ePDG相关，具体标签随平台变化 |

## Data / Signal 常见标签

| 标签 | 关注点 |
|---|---|
| `DcTracker` | 旧数据连接管理 |
| `DataNetworkController` | 新数据网络管理 |
| `PhoneSwitcher` | 多卡数据切换 |
| `QualifiedNetworksService` | APN/RAT推荐网络 |
| `SignalStrengthController` | 信号强度上报 |
| `CellInfo` | 小区信息 |

## 常用logcat过滤

```powershell
adb logcat -b radio -v threadtime
adb logcat -b main,system,radio -v threadtime
adb logcat -v threadtime | findstr /i "RILJ ServiceStateTracker Ims Uicc SIMRecords CarrierConfig"
```

## bugreport常看位置

- `dumpsys telephony.registry`
- `dumpsys phone`
- `dumpsys ims`
- `dumpsys carrier_config`
- `dumpsys activity service com.android.phone`
- radio log buffer

## 常用缩写

## Android / Telephony

| 缩写 | 含义 | 备注 |
|---|---|---|
| AP | Application Processor | Android侧 |
| BP | Baseband Processor | Modem侧 |
| RIL | Radio Interface Layer | Android与modem之间的接口层 |
| HIDL | HAL Interface Definition Language | 老一代Android HAL接口 |
| AIDL | Android Interface Definition Language | 新一代Android HAL接口 |
| SST | ServiceStateTracker | 维护注册和服务状态 |
| DCT | DcTracker | 旧数据连接管理 |
| DNC | DataNetworkController | 新数据连接管理 |
| UICC | Universal Integrated Circuit Card | SIM/USIM卡框架 |
| EF | Elementary File | SIM文件 |
| ICCID | Integrated Circuit Card Identifier | SIM卡识别号 |
| IMSI | International Mobile Subscriber Identity | 用户身份 |

## 3GPP / 网络

| 缩写 | 含义 | 备注 |
|---|---|---|
| PLMN | Public Land Mobile Network | MCC+MNC |
| RAT | Radio Access Technology | 2G/3G/4G/5G/IWLAN |
| LAI | Location Area Identity | 2G/3G位置区 |
| TAI | Tracking Area Identity | LTE/5G跟踪区 |
| TAC | Tracking Area Code | 跟踪区码 |
| RRC | Radio Resource Control | 无线资源控制 |
| NAS | Non-Access Stratum | UE与核心网之间的信令 |
| AS | Access Stratum | UE与基站之间的接入层 |
| EPS | Evolved Packet System | LTE核心系统 |
| EPC | Evolved Packet Core | LTE核心网 |
| 5GS | 5G System | 5G系统 |
| AMF | Access and Mobility Management Function | 5G核心网移动性管理 |
| MME | Mobility Management Entity | LTE核心网移动性管理 |
| GMM | GPRS Mobility Management | 2G/3G PS域移动性 |
| EMM | EPS Mobility Management | LTE NAS移动性 |
| 5GMM | 5G Mobility Management | 5G NAS移动性 |

## IMS / Call

| 缩写 | 含义 | 备注 |
|---|---|---|
| IMS | IP Multimedia Subsystem | IP多媒体子系统 |
| P-CSCF | Proxy-CSCF | UE接入IMS的代理节点 |
| I-CSCF | Interrogating-CSCF | 查询/路由节点 |
| S-CSCF | Serving-CSCF | 注册和业务控制节点 |
| SIP | Session Initiation Protocol | IMS信令 |
| SDP | Session Description Protocol | 媒体协商 |
| RTP | Real-time Transport Protocol | 语音/视频媒体 |
| MMTEL | Multimedia Telephony | IMS语音/视频业务 |
| VoLTE | Voice over LTE | LTE上的IMS语音 |
| VoWiFi | Voice over Wi-Fi | IWLAN/ePDG上的IMS语音 |
| VoNR | Voice over NR | 5G NR上的IMS语音 |
| SRVCC | Single Radio Voice Call Continuity | LTE到CS域连续性 |
| CSFB | Circuit Switched Fallback | LTE回落2G/3G做CS语音 |
| MO | Mobile Originated | 主叫 |
| MT | Mobile Terminated | 被叫 |

## 标签体系

## Frontmatter模板

每篇 case 的 frontmatter 必须从文件第一行开始，便于 Obsidian/Dataview 和脚本检索。建议字段：

```yaml
---
doc_type: case
domain: Registration
rat: LTE
feature: LTE registration
platform: Qualcomm/MTK/UNISOC/Common
layer: AP/Modem/Network/SIM
symptom: no service
cause: Attach Reject cause 6
operator: CMCC/CU/CT
project:
chipset:
vendor_customization:
android_version:
modem_version:
source_log:
first_bad_point:
confidence: medium
status: open
tags:
  - registration
  - lte
---
```

必填字段：`doc_type`、`domain`、`rat`、`platform`、`layer`、`symptom`、`cause`、`source_log`、`first_bad_point`、`confidence`、`status`。

## 领域标签

- `#SIM`
- `#PLMN`
- `#Registration`
- `#IMS`
- `#VoLTE`
- `#VoWiFi`
- `#VoNR`
- `#CSCall`
- `#CallDrop`
- `#ModemAssert`
- `#SignalQuality`
- `#CarrierConfig`

## 平台标签

- `#Qualcomm`
- `#MTK`
- `#UNISOC`
- `#PlatformDiff`
- `#VendorCustomization`
- `#NV`
- `#ModemConfig`
- `#QXDM`
- `#QCAT`
- `#ELT`
- `#Logel`

## RAT标签

- `#GSM`
- `#WCDMA`
- `#LTE`
- `#NR`
- `#NSA`
- `#SA`
- `#IWLAN`

## 层级标签

- `#AP`
- `#Framework`
- `#RIL`
- `#VendorRIL`
- `#IMSStack`
- `#Modem`
- `#Network`
- `#SIMCard`
- `#CarrierConfig`

## 现象标签

- `#NoService`
- `#LimitedService`
- `#RegistrationReject`
- `#IMSNotRegistered`
- `#CallFail`
- `#CallDrop`
- `#SMSFail`
- `#DataFail`
- `#SIMNotReady`
- `#ModemCrash`
- `#RadioRestart`

## 状态标签

- `#Open`
- `#Analyzing`
- `#NeedModemLog`
- `#NeedAPLog`
- `#NeedNetworkConfirm`
- `#Workaround`
- `#Fixed`
- `#Closed`
