---
doc_type: case
quality: curated
domain: IMS
rat: IWLAN/LTE
feature: VoWiFi / IKE / ePDG
platform: Mixed
layer: Modem/IKE/IMS
symptom: "6032+ Spark 开启 Wi-Fi Calling 后无法 VoWiFi 注册或拨号，飞行模式下拨号提示需关闭飞行模式"
cause: "VoWiFi handover 触发后 IKE 会话启动失败，配置的完整性算法 ike_intg=18 不被支持"
source_log: "Old Outline knowledge base; split from IMS问题案例补充.md"
first_bad_point: "IKE_SessCheckAlgorithms unsupported integ algo:18，导致 IKE_ATTACH_FAILED"
confidence: high
search_tier: case_summary
status: summarized
tags:
  - imported
  - ims
  - vowifi
  - ike
  - epdg
---

# Spark VoWiFi 注册失败：IKE 完整性算法配置错误

## 用户现象

Spark 卡开启 Wi-Fi Calling 后，Wi-Fi 图标显示正常，但 VoWiFi 无法真正可用。开启飞行模式再通过 Wi-Fi 拨号时，系统提示需要关闭飞行模式才能拨打电话。

## 结论

第一坏点在 VoWiFi 的 IKE/IPsec 建链阶段。终端已经触发 handover 到 VoWiFi，但 IKE 检查配置时发现完整性算法不支持，导致 IKE attach 失败，后续 IMS over IWLAN 不会注册成功。

## 关键证据

```text
[cmcp]HandleWfcEnable: is_wfc_enable=1
ims_over_wifi_enable: 1
MSG_ID_CMCP_HANDOVER_TO_VOWIFI_REQ
MSG_ID_IKE_ATTACH_REQ
IKE: nv: ike_intg = 18
IKE: cfg: ike_integ_alg=18
IKE_SessCheckAlgorithms unsupported integ algo:18
IKE: Session start failed!
MSG_ID_IKE_ATTACH_FAILED
MSG_ID_CMCP_HANDOVER_TO_VOWIFI_RSP
```

## 判断边界

| 现象 | 结论 |
|---|---|
| WFC 开关可打开 | 只说明 AP/CarrierConfig 基本允许 WFC |
| LTE/VoLTE 注册正常 | 不能证明 IWLAN/ePDG/IKE 链路正常 |
| `IKE_ATTACH_FAILED` | 问题发生在 SIP REGISTER 之前 |
| `unsupported integ algo:18` | 优先查 IKE 完整性算法配置，不先查 IMS 账号或 P-CSCF |

## 处理建议

- 修正 `ike_intg` / `ike_integ_alg`，确保配置值落在平台支持的 IKE 完整性算法集合内。
- 出临时软件后，至少验证：WFC enable、IKE SA 建立、IMS over IWLAN REGISTER、飞行模式下 VoWiFi MO call。
- 让客户提供对比机 pass log 时，重点对比 IKE proposal、完整性算法、加密算法、ePDG 地址和网络环境。

## 关联入口

- [[../../20_Service-Flows/IMS/IMS业务流程#VoWiFi注册流程]]
- [[../../60_Configuration/IMS配置方法#VoWiFi-IKE配置]]
- [IKE消息解密SOP](../../70_Tools-Debug/Debug-Tips/IKE消息解密SOP.md)

