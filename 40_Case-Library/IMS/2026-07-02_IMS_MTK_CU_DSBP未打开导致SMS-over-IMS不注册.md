---
quality: curated
search_tier: case_summary
doc_type: case
target_doc_type: case
domain: IMS
rat: LTE
feature: SMS over IMS / SMS over IP
platform: MTK
layer: AP vendor property / RIL / Modem DSBP / IMSM / ImsSmsDispatcher
symptom: "46001/CU 卡在 LTE 有数据域但 CS 被拒绝时短信发送失败，IMS 未注册，最终走 AT+CMGS 返回 +CMS ERROR:331"
cause: "WM18 未打开 persist.vendor.radio.mtk_dsbp_support=2，AP 虽识别 46001 -> SBP 2，但未向 modem 打开 DSBP mode，modem 未按 CU SBP/IMS profile 发起 IMS 注册"
operator: 46001/CU
project: WM18
chipset: MTK
vendor_customization: vendor property / DSBP / IMS profile
android_version: TBD
modem_version: WM18 modem baseline
source_log: "F:\\Log\\WM18短信无法发送\\debuglogger; F:\\Log\\WM18短信无法发送\\pass\\debuglogger; F:\\Log\\WM18短信无法发送\\MP6debuglogger\\debuglogger; F:\\Log\\WM18短信无法发送\\SMSOIP\\debuglogger"
first_bad_point: "RIL 下发 AT+EDSBP=0，modem 侧 DSBP disable / SIM_SBP_ID:-1，导致没有 +ESBPID:0,2 和 IMSM sbp_id[2]"
confidence: high
status: summarized
tags:
  - ims
  - sms-over-ims
  - sms-over-ip
  - dsbp
  - sbp
  - mtk
  - cu
  - 46001
---

# Case: MTK 46001/CU DSBP 未打开导致 SMS over IMS 不注册

## 基本信息

| 项目        | 内容                                                                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 日期        | 2026-07-02                                                                                                                                                 |
| 项目        | WM18                                                                                                                                                       |
| 平台        | MTK                                                                                                                                                        |
| 芯片/基线     | WM18 modem baseline；对比含 MP6 / SMSOIP 可注册日志                                                                                                                 |
| 厂商客制化     | vendor property / DSBP / SBP / modem IMS profile                                                                                                           |
| Android版本 | TBD                                                                                                                                                        |
| Modem版本   | WM18 modem baseline                                                                                                                                        |
| 原始log     | `F:\Log\WM18短信无法发送\debuglogger`；`F:\Log\WM18短信无法发送\pass\debuglogger`；`F:\Log\WM18短信无法发送\MP6debuglogger\debuglogger`；`F:\Log\WM18短信无法发送\SMSOIP\debuglogger` |
| 第一坏点      | AP 识别到 `46001 -> SBP 2` 后，RIL 仍下发 `AT+EDSBP=0`，modem 未进入动态 SBP2 profile                                                                                    |
| SIM/运营商   | `46001` / China Unicom                                                                                                                                     |
| RAT       | LTE                                                                                                                                                        |
| 场景        | 开机注册后发送短信；联通 3G 退网、CS fallback 不可用                                                                                                                         |
| 复现概率      | 同配置稳定复现；打开 DSBP 后同卡通过                                                                                                                                      |

## 状态说明

`summarized`：已有失败日志、打开 DSBP 后 PASS 日志、MP6 成功日志和同类 SMSOIP 对比日志，证据链可复用。

## 用户现象

中国联通卡在 WM18 上无法发送短信。Google Messages 发起发送后，上层最终报 modem error，短信没有发出。

## 结论

根因不是短信应用、SMSC、VoPS 或单纯缺少 `android.hardware.telephony.calling`，而是 WM18 AP/vendor 未打开 DSBP。AP 虽然识别出 `46001` 应使用 `SBP 2`，但没有通过 `AT+EDSBP=2` 让 modem 动态应用 CU SBP/IMS profile，导致 modem 不发起 IMS 注册；CS 又因联通 3G 退网/CS domain denied 不可用，最终非 IMS 短信 `AT+CMGS` 返回 `+CMS ERROR:331`。

打开 `persist.vendor.radio.mtk_dsbp_support=2` 后，同张卡、同样 CS denied 环境下可以 IMS 注册，短信走 IMS 成功。

## 输入材料

- AP log：`F:\Log\WM18短信无法发送\debuglogger\mobilelog`
- Modem log：`F:\Log\WM18短信无法发送\debuglogger\mdlog1`
- PASS AP/Modem log：`F:\Log\WM18短信无法发送\pass\debuglogger`
- MP6 对比 log：`F:\Log\WM18短信无法发送\MP6debuglogger\debuglogger`
- SMSOIP 对比 log：`F:\Log\WM18短信无法发送\SMSOIP\debuglogger`
- 代码侧参考：WM18 modem repo `/home/wx/Modem/alps-release-s0.mp1.rc-tb-default_modem/modem`

## 时间线

| 时间       | 来源                   | 事件                                                          | 含义                            | 重要性 |
| -------- | -------------------- | ----------------------------------------------------------- | ----------------------------- | --- |
| 13:26:55 | FAIL AP/RIL          | `AT+EDSBP=0`                                                | AP 未打开 modem DSBP mode        | 高   |
| 13:27:19 | FAIL AP/RIL          | `MCC/MNC: 46001`，`RFX_STATUS_KEY_SBP_ID ... new value = 2`  | AP 识别运营商/SBP 正确               | 高   |
| 13:27:45 | FAIL AP/Telephony    | `ImsSmsDispatcher ... reg=false, cap=false`                 | SMS over IMS 不可用              | 高   |
| 13:27:47 | FAIL AT              | `AT+CMGS` 后 `+CMS ERROR:331`                                | 回落到非 IMS SMS，modem 返回失败       | 高   |
| 20:02:31 | PASS AP/RIL          | `AT+EDSBP=2`                                                | AP 打开 DSBP mode               | 高   |
| 20:02:32 | PASS AP/RIL          | `+ESBPID: 0,2`                                              | modem 上报当前 SIM 使用 SBP2        | 高   |
| 20:02:43 | PASS IMSM            | `unmerge sbp id ... sbp_id[2]`                              | IMSM 使用 CU SBP profile        | 高   |
| 20:02:50 | PASS AP/ServiceState | CS `DENIED rejectCause=18 availableServices=[]`，PS LTE HOME | CS fallback 仍不可用，成功不是因为 CS 恢复 | 高   |
| 20:03:06 | PASS AP/Telephony    | `ImsSmsDispatcher ... reg=true, cap=true`                   | SMS over IMS 已可用              | 高   |
| 20:03:08 | PASS IMS SMS         | `sendSmsRsp ... status=1, reason=0`                         | IMS SMS 发送成功                  | 高   |

## 正常流程对比

参考流程：

- [[IMS业务流程#IMS注册流程|IMS注册流程]]
- [[IMS业务流程#SMS over IP流程|SMS over IP流程]]
- [[../Registration/2026-05-14_Registration_MTK_LTE开机注册成功|MTK LTE开机注册成功]]
- [[2025-07-29_IMS_SMS-over-IP配置缺失|SMS over IP / SMS over IMS 配置缺失]]

正常链路应为：

```text
SIM MCC/MNC 识别 46001
-> AP/RIL 计算 SBP_ID=2
-> DSBP enabled 时下发 AT+EDSBP=2
-> modem 上报 +ESBPID: 0,2
-> IMSM 使用 sbp_id[2] / CU IMS profile
-> IMS APN / IMS PDN 激活
-> SIP REGISTER 成功，AP 收到 +EIREG / onImsConnected
-> MtkMmTelFeature 上报 SMS:true
-> ImsSmsDispatcher reg=true cap=true
-> SMS 走 IMS，sendSmsRsp status=1 reason=0
```

失败链路为：

```text
SIM MCC/MNC 识别 46001
-> AP/RIL 计算 SBP_ID=2
-> 但 DSBP 未打开，下发 AT+EDSBP=0
-> modem 侧 DSBP disable / SIM_SBP_ID:-1
-> 无 +ESBPID:0,2，无 IMSM sbp_id[2]
-> 无可用 IMS SMS capability
-> CS domain denied，无法可靠回落 CS SMS
-> AT+CMGS 返回 +CMS ERROR:331
```

## 第一个异常点

```text
第一个坏点：
RIL 开机阶段下发 AT+EDSBP=0，而不是 AT+EDSBP=2。

上一条正常证据：
AP 能识别 46001，并把 RFX_STATUS_KEY_SBP_ID 更新为 2。

下一条异常证据：
modem log 中反复出现 DSBP disable; SIM_SBP_ID:-1，且没有 +ESBPID:0,2 / IMSM sbp_id[2]。

影响层级：
AP vendor property -> RIL AT command -> modem DSBP/SBP profile -> IMSM/IMC -> Android IMS SMS capability。
```

## 关键证据

失败版本：

```text
APLog_2026_0701_132721__3/boot__normal/radio_log_2__2026_0701_132721:672
07-01 13:26:55.852376 I AT: [0] AT> AT+EDSBP=0

APLog_2026_0701_132721__3/radio_log_3__2026_0701_132754:394
07-01 13:27:19.818287 D RtcCarrier: [0] [onUiccGsmMccMncChanged]MCC/MNC: 46001

APLog_2026_0701_132721__3/radio_log_3__2026_0701_132754:402
07-01 13:27:19.819486 D RtcCarrier: key = RFX_STATUS_KEY_SBP_ID, default value = 0, new value = 2

MDLog1_2026_0701_132614.muxz
sim0, d2_get_config(), DSBP disable; SIM_SBP_ID:-1

APLog_2026_0701_132721__3/radio_log_3__2026_0701_132754:4525
07-01 13:27:45.384391 D ImsSmsDispatcher [0]: isAvailable: up=true, reg= false, cap= false

APLog_2026_0701_132721__3/radio_log_3__2026_0701_132754:4805
07-01 13:27:47.163866 I AT: [0] AT> AT+CMGS=***

APLog_2026_0701_132721__3/radio_log_3__2026_0701_132754:4806
07-01 13:27:47.166697 I AT: [0] AT< +CMS ERROR: 331
```

打开 DSBP 后的 PASS 版本：

```text
APLog_2026_0701_200254__4/properties:1247
[persist.vendor.radio.mtk_dsbp_support]: [2]

APLog_2026_0701_200254__4/properties:1248
[persist.vendor.mtk_dynamic_ims_switch]: [1]

APLog_2026_0701_200254__4/boot__normal/radio_log_3__2026_0701_200254:675
07-01 20:02:31.709897 I AT: [0] AT> AT+EDSBP=2

APLog_2026_0701_200254__4/boot__normal/radio_log_3__2026_0701_200254:898
07-01 20:02:32.369933 I AT: [0] AT< +ESBPID: 0,2

APLog_2026_0701_200254__4/boot__normal/radio_log_3__2026_0701_200254:915
07-01 20:02:32.391831 D RtcCarrier: key = RFX_STATUS_KEY_SBP_ID, default value = 0, new value = 2

APLog_2026_0701_200254__4/main_log_1__2026_0701_200321:16919
07-01 20:03:19.175721 D VoLTE IMSM: unmerge sbp id, original_id[0x200], sbp_id[2], unmerged_id[0x0], is_test_sim[0]

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:171
CS transportType=WWAN registrationState=DENIED rejectCause=18 availableServices=[];
PS transportType=WWAN registrationState=HOME accessNetworkTechnology=LTE availableServices=[DATA,MMS]

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:1810
07-01 20:03:06.153088 D ImsSmsDispatcher [0]: isAvailable: up=true, reg= true, cap= true

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:1885
07-01 20:03:08.434219 D ImsSmsDispatcher [0]: sendSms: mRetryCount=0 mMessageRef=0 SS=0

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:1904
07-01 20:03:08.831798 D MtkMmTelFeature: [0] sendSmsRsp, token 1, messageRef 152, status 1, reason 0

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:1906
07-01 20:03:08.835087 D ImsSmsDispatcher [0]: onSendSmsResult token=1 messageRef=152 status=1 reason=0

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:4113
07-01 20:03:19.994071 I AT: [0] AT< +EIREG: 1,0,5,0,0,0,1

APLog_2026_0701_200254__4/radio_log_2__2026_0701_200321:4123
07-01 20:03:20.002698 D ImsSmsDispatcher [0]: onImsConnected imsRadioTech=1
```

## 异常分析

### 事实

- 失败版本的 SMSC 可读，短信由 Google Messages 正常发起，不是应用权限或短信中心号问题。
- 失败版本 PS LTE HOME，但 CS domain 为 `DENIED rejectCause=18`，`availableServices=[]`，所以 2G/3G/CS fallback 对短信不可用。
- 失败版本 VoPS 不是主因，log 中 LTE VoPS 支持信息为 supported。
- 失败版本 AP 可识别 `46001 -> SBP 2`，但 DSBP 未打开，RIL 下发 `AT+EDSBP=0`。
- 失败版本没有 `+ESBPID:0,2`，没有 IMSM 使用 `sbp_id[2]` 的证据。
- PASS 版本设置 `persist.vendor.radio.mtk_dsbp_support=2` 后，RIL 下发 `AT+EDSBP=2`，modem 上报 `+ESBPID:0,2`，IMSM 使用 `sbp_id[2]`。
- PASS 版本 CS 仍为 `DENIED rejectCause=18`，但 IMS 注册和 SMS over IMS 成功，说明 DSBP 修复的是 IMS 路径，不是 CS fallback。

### 推断

- `persist.vendor.mtk_dynamic_ims_switch=1` 只保证 dynamic IMS switch 开启，不等价于 DSBP 已打开。
- `AT+EIMSCFG=... ims_sms=1/eims=1` 只能说明 modem 侧 IMS SMS 配置可用，不等价于 Android framework 已有 `MmTel SMS capability=true`，也不等价于一定会触发 IMS REGISTER。
- 在这个产品形态下，AP 普通 MMTEL capability 可能被关掉；真正让 CU SMS over IMS 可用的关键，是 DSBP 使 modem 动态套用 `SBP 2 / CU` IMS profile 并触发 IMS 注册/能力上报。
- modem 侧 `wans_ims_no_voice_sup_sms_enable` 更像 IMS PDN 已 active 后的保活/不释放策略；本案第一触发点仍是 AP/vendor DSBP property。

### 待确认

- WM18 Android 产品树中 `persist.vendor.radio.mtk_dsbp_support` 最终应落在哪个产品 overlay / `vendor.prop` / `product.mk` 文件，需要结合 AP 源码路径确认。
- 需要确认客户最终配置是否所有目标 SKU 都应打开 `=2`，还是只对移除 telephony calling feature 的数据优先 SKU 打开。
- Android 版本、具体芯片名和正式 modem build 号待补。

## 平台差异检查

| 检查项 | 结果 |
|---|---|
| 是否只在单一平台复现 | 已在 WM18 失败，MP6 / SMSOIP / WM18 PASS 对比可注册 |
| Qualcomm/MTK/UNISOC是否路径不同 | 本案为 MTK RIL + DSBP + modem IMSM 路径 |
| 是否涉及NV或modem配置 | 涉及 modem SBP/IMS profile 的动态选择，但第一控制点是 AP/vendor property |
| 是否涉及vendor RIL/IMS service实现 | 是，`AT+EDSBP`、`+ESBPID`、`MtkMmTelFeature`、`ImsSmsDispatcher` 均在链路中 |
| 是否涉及客户overlay或CarrierConfig | 涉及 AP/vendor property；不是 CarrierConfig 主导 |
| 是否需要平台侧工具解析 | MTK ELT 可辅助看 mdlog；AP log 已足够证明第一坏点 |

## 可能原因排序

| 排名 | 可能原因 | 证据 | 置信度 |
|---|---|---|---|
| 1 | WM18 未配置 `persist.vendor.radio.mtk_dsbp_support=2` | FAIL 无该 property 且 `AT+EDSBP=0`；PASS 有 property 且 `AT+EDSBP=2` / `+ESBPID:0,2` / IMS 注册成功 | 高 |
| 2 | modem 未按 CU profile 主动触发 SMS-only IMS 注册 | 打开 DSBP 后同 modem 路径可注册，说明不是注册状态机完全不支持；但 profile 应用依赖 DSBP | 低 |
| 3 | CS fallback 不可用导致 `AT+CMGS` 失败 | CS `DENIED rejectCause=18` 与 `+CMS ERROR:331` 成立，但它解释失败结果，不解释为何 IMS 未注册 | 中 |
| 4 | AP 移除 `android.hardware.telephony.calling` 导致 IMS 不注册 | 对比日志中同样缺 calling feature 仍可注册，不能作为主因 | 低 |

## 处理方案

- 临时规避：打开 DSBP 后验证同卡是否出现 `AT+EDSBP=2`、`+ESBPID:0,2`、`onImsConnected`、`SMS:true`、`ImsSmsDispatcher reg=true cap=true`。
- 正式修复：在 WM18 产品/vendor 属性中加入或恢复：

```makefile
PRODUCT_VENDOR_PROPERTIES += persist.vendor.radio.mtk_dsbp_support=2
```

也可以落在项目实际生效的 `vendor.prop` / `system.prop` / 产品 `*.mk` 属性文件中，最终以设备 `getprop persist.vendor.radio.mtk_dsbp_support` 返回 `2` 为准。

- 保留配置：`persist.vendor.mtk_dynamic_ims_switch=1` 应继续保留，但它不是本案充分条件。
- modem 侧：若项目目标是“无语音/无 CS fallback 但仍要求 SMS over IMS”，可保留 `WANS_IMS_NO_VOICE_SUP_SMS_ENABLE=KAL_TRUE`；但本案日志证明第一修复点不是它，而是 DSBP mode。
- 需要供应商/运营商确认：确认目标 SKU 是否允许默认打开 DSBP mode 2，以及 CU SMS over IMS 是否为正式商用要求。

## 验证清单

设备侧：

```bash
adb shell getprop persist.vendor.radio.mtk_dsbp_support
adb shell getprop persist.vendor.mtk_dynamic_ims_switch
```

期望：

```text
persist.vendor.radio.mtk_dsbp_support = 2
persist.vendor.mtk_dynamic_ims_switch = 1
```

日志侧：

```text
AT+EDSBP=2
+ESBPID: 0,2
RFX_STATUS_KEY_SBP_ID ... new value = 2
VoLTE IMSM ... sbp_id[2]
+EIMSPDN: "notify", 1, 1, "ims"
+ESIPREGINFO
+EIREG: 1
onImsConnected
MtkMmTelFeature capabilities ... SMS:true
ImsSmsDispatcher isAvailable: up=true, reg=true, cap=true
sendSmsRsp status=1 reason=0
```

反向排除：

```text
不应再出现短信发送前 ImsSmsDispatcher reg=false cap=false
不应再主要依赖 AT+CMGS 发送普通短信
不应再出现同场景 +CMS ERROR:331 作为最终失败点
```

## 复盘

下次遇到类似问题，优先检查：

- 先区分“AP 识别 SBP_ID”与“modem DSBP mode 已打开”。`RFX_STATUS_KEY_SBP_ID=2` 不等于 `AT+EDSBP=2`。
- `AT+EIMSCFG` 中 `ims_sms=1` 只说明 modem 侧 SMS over IMS 配置具备，不等于 IMS 已注册。
- LTE DATA HOME 不代表 CS SMS 可用；要看 CS domain 的 registration state、reject cause 和 `availableServices`。
- 对“数据优先/移除 telephony calling feature”的项目，SMS over IMS 是否能注册必须看 `+ESBPID`、IMSM `sbp_id`、`+EIREG`、`onImsConnected` 和 `SMS:true`，不能只看 framework feature 声明。
- PASS log 若仍有 CS denied，但 IMS SMS 成功，说明问题定位应回到 IMS/SBP profile 触发链路，而不是继续追 CS fallback。
