---
doc_type: case
quality: curated
domain: Registration
rat: LTE/GSM
feature: UE Capability / Preferred Network Mode
platform: UNISOC
layer: AP/CarrierConfig/RIL/Modem/RRC
symptom: "运营商实验室反馈 LTE UECapabilityInformation 中未上报 2G/GSM 能力"
cause: "运营商配置 key_oem_pref_network_mode 触发 AP 下发网络模式，RIL 最终通过 AT+SPTESTMODEM=24,6 让 modem 按 4G/3G 模式工作，后续能力上报不再包含 2G"
source_log: "Old Outline knowledge base; split from IMS问题案例补充.md and CQWeb SPCSS01532727"
first_bad_point: "CarrierConfig 客制化网络模式触发 updateOemAllowedNetworkMode -> setPreferredNetworkType -> AT+SPTESTMODEM=24,6"
confidence: high
search_tier: case_summary
status: summarized
tags:
  - imported
  - registration
  - ue-capability
  - network-mode
  - carrierconfig
---

# UECapability 不带 2G 能力：网络模式客制化影响能力上报

## 用户现象

澳电实验室反馈 LTE 注册过程中，`UECAPABILITYINFORMATION` 未上报 2G/GSM 能力。期望 UE 能力中包含 2G。

## 结论

第一坏点不在语音域注册，也不是网络侧能力解析错误。根因是 AP 侧运营商客制化网络模式触发 `setPreferredNetworkType`，最终通过 RIL 向 modem 下发：

```text
AT+SPTESTMODEM=24,6
```

该 workmode 相当于把当前能力限制到 4G/3G，后续 LTE `UECapabilityInformation` 不再携带 GSM/2G 能力。

## 关键证据

实验室问题日志：

```text
ATC_RecNewLineSig ... AT+SPTESTMODEM=24,6
```

实网验证正常场景：

```text
ATC_RecNewLineSig ... AT+SPTESTMODEM=6,6
```

触发配置：

```xml
<string name="key_oem_pref_network_mode">0,1,0,0,0,0</string>
```

该配置表示优先选择 `4G/3G Auto`。项目逻辑中 `updateOemAllowedNetworkMode()` 首次应用该值，并调用 `telephonyManager.setPreferredNetworkType()`，最终走到 RIL / modem workmode 更新。

## SIM PIN 分叉

| 场景 | 现象 | 结论 |
|---|---|---|
| SIM 无 PIN，非首次插卡 | 已下发 `SPTESTMODEM=24,6`，后续能力不带 2G | 符合客制化配置结果 |
| SIM 带 PIN | 读取到默认 CC 配置，`SPTESTMODEM=6,6` | 客制逻辑未正确处理 PIN/PUK/SimLock 状态 |

需要在 SIM 异常状态下避免使用错误 CC：

```java
int simState = getContext().getSystemService(TelephonyManager.class).getSimState();
if (simState == TelephonyManager.SIM_STATE_PUK_REQUIRED
        || simState == TelephonyManager.SIM_STATE_PIN_REQUIRED
        || simState == TelephonyManager.SIM_STATE_NETWORK_LOCKED) {
    return;
}
```

## 处理建议

- 如果运营商明确要求禁用 2G 能力，应保证默认 modem workmode 和后续客制化 workmode 一致。
- 如果运营商要求上报 2G，就不能配置成只允许 4G/3G 的默认模式。
- 首次插卡、开关飞行、重启、SIM PIN/PUK、SimLock 场景都要回归，因为网络模式可能在不同阶段下发。
- 验证时同时保留 AP `setPreferredNetworkType`、RILJ/HAL、`AT+SPTESTMODEM` 和 RRC `UECapabilityInformation`。

## 关联入口

- [[../../20_Service-Flows/Network-Registration/网络模式更新流程]]
- [[../../60_Configuration/Core-Config/CarrierConfig配置方法_重构]]
