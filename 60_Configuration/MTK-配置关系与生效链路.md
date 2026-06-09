---
doc_type: config
domain: Configuration
status: active
quality: imported_reference
platform: MTK
source: Notion MTK 网络通信模块知识库 / MediaTek Online FAQ
source_url: https://www.notion.so/35df72d579ba814ca3f2f106aa8a93da
search_tier: supplemental
---

# MTK配置关系与生效链路

<!-- SUPPLEMENTAL_BOUNDARY_START -->
## 使用边界

- 本页是补充资料或短专题，适合查局部步骤、旧来源和零散技巧。
- 若需要直接定位问题，优先回到对应主流程、配置方法、排障流程或 Case。
- 后续新增结论应沉淀到主文档，本页只保留来源和辅助说明。
<!-- SUPPLEMENTAL_BOUNDARY_END -->


## 使用入口

这篇专门处理 MTK 上“功能支持但开关不显示、IMS 不注册、同 operator 行为不同、换 SIM 后配置不刷新、APN/IMS APN 生效异常”这类配置链问题。

核心原则：配置问题不要只看一个 XML。按 `支持能力 -> 编译开关 -> AP/Framework 配置 -> modem operator 行为 -> 承载建立 -> 运行时生效证据` 顺序查。

## 速查结论

- `平台/branch/modem 版本` 决定目标 feature 是否具备基础支持。
- `Project feature option` 决定 IMS、VoLTE、WFC、EPDG、RAT 能力是否编进版本。
- `CarrierConfig / IMS Config / native carrier config` 决定 AP/Telephony 侧开关、策略和 capability。
- `SBP / DSBP / NVRAM` 决定 modem/operator 侧行为，特定 SIM、roaming 或 operator 差异优先查这里。
- `APN / IMS APN / MMS APN` 决定 data、IMS、MMS、WFC 承载能否建立。
- 最终必须在设备上用生成文件、APN DB、dump、Telephony/radio/modem log 证明生效。

## 配置层地图

| 层级 | 典型配置 | 影响 | 常见问题 |
|---|---|---|---|
| 支持计划 / branch / modem 版本 | IMS Support Plan、AP branch、MD branch | 国家/operator/feature 是否支持 | 版本太旧、需要 patch、support plan 未覆盖 |
| Project feature option | `MTK_IMS_SUPPORT`、`MTK_VOLTE_SUPPORT`、`MTK_WFC_SUPPORT`、`MTK_EPDG_SUPPORT`、RAT config | 编译期能力 | feature 没编进版本、WFC 缺 patch |
| CarrierConfig / IMS Config | `carrier_volte_available_bool`、`carrier_wfc_ims_available_bool`、IMS device config | UI 开关、IMS capability、AP 策略 | 开关不显示、灰掉、配置没刷新 |
| TelephonyWare / native carrier config | `carrier_config_xxx_xx.h`、RFX status key | Android P 后部分 93 modem dynamic IMS switch | operator native config 缺失 |
| SBP / DSBP | SBP guideline、operator behavior | NAS/IMS/Data/SMS 等 modem 行为 | 同平台不同 SIM 行为不同 |
| NVRAM | AP/Modem NVRAM | 持久化参数、operator 定制值 | 恢复出厂/换版本后行为变化 |
| APN / IMS APN | `apns-conf.xml`、`wifi-apns.xml`、`network_type_bitmask` | data、IMS、MMS、WFC 承载 | IMS PDN 不建、MMS fail、VoWiFi APN 不支持 |
| RAT mode | `MTK_PROTOCOL1_RAT_CONFIG`、preferred network mode、`AT+ERAT` | 制式能力、默认网络模式、搜网能力 | 默认网络模式错误、无法 camp-on |

## 推荐排查顺序

1. 支持：查 support plan，确认 Country、Operator、AP branch、MD branch 是否支持目标 feature。
2. 打开：查 project feature option，例如 IMS/VoLTE/WFC/EPDG/RAT config。
3. 配置：查 CarrierConfig、IMS Config、native carrier config、APN/IMS APN、SBP/NVRAM。
4. 生效：查设备生成的 carrierconfig、APN DB、Telephony log、IMS support status。
5. 行为：用 AP + modem log 验证 IMS PDN、SIP REGISTER、VoPS、NAS/RRC、SBP 行为。

## CarrierConfig检查点

| 检查点 | 说明 |
|---|---|
| 匹配条件 | MTK CarrierConfig 可按 `mcc`、`mnc`、`gid1`、`gid2`、`spn`、`imsi`、`device` 匹配 |
| 覆盖顺序 | 默认值 -> `carrier_config_mccmnc.xml` -> vendor 配置，后加载 key 覆盖前值 |
| 运行时文件 | 设备侧可查 `/data/user_de/0/com.android.phone/files/carrierconfig-com.android.carrierconfig-(iccId).xml` 类生成文件 |
| 风险 | 不要在没有 MCC/IMSI 等限制的 vendor 配置里写 default 值，SIM PIN 未解锁时可能污染默认配置 |
| 双卡 | 使用正确 `subId` 读取 `getConfigForSubId()`，避免看错卡槽 |

## IMS / VoLTE / VoWiFi feature option

| Feature | 基础依赖 |
|---|---|
| VoLTE | `MTK_IMS_SUPPORT=yes`、`MTK_VOLTE_SUPPORT=yes` |
| ViLTE | 先支持 VoLTE，再开 `MTK_VILTE_SUPPORT=yes` |
| VoWiFi / WFC | 先支持 VoLTE，再开 `MTK_WFC_SUPPORT=yes`、`MTK_EPDG_SUPPORT=yes` |
| ViWiFi | 需要 ViLTE + VoWiFi，再开 `MTK_VIWIFI_SUPPORT=yes` |
| Dual VoLTE | 关注 `MTK_MULTI_PS_SUPPORT`、`MTK_MULTIPLE_IMS_SUPPORT`、`MTK_PROTOCOL2_RAT_CONFIG` |

关闭某个 IMS feature 时也要检查相关选项是否一致关闭，避免 AP 侧开关、modem capability、IMS service 状态互相矛盾。

## TelephonyWare / native carrier config

Android P 后，93 modem 的部分 IMS config 会走 TelephonyWare/native flow。常见代码范围：

```text
vendor/mediatek/proprietary/hardware/ril/fusion/mtk-ril/telcore/ims/config/
```

新增 operator 的 VoLTE / ViLTE / VoWiFi / VoNR / ViNR 支持时，可能需要增加对应 MCC/MNC 的 `carrier_config_xxx_xx.h`。不要轻易把 capability 默认置 1；网络不支持 IMS 时，设备仍尝试注册可能带来副作用。

## APN / IMS APN检查点

| 检查点 | 说明 |
|---|---|
| APN DB | 先证明 XML 已加载到数据库，不能只证明改了 XML |
| type | IMS 需要 `type="ims"`，MMS 需要包含 `mms` |
| protocol | 合法值用 `IP`、`IPV6`、`IPV4V6`；不要把 `IPV4` 当 Android APN 合法值 |
| 5G | full RAT APN 需要把 5G network type 纳入 `network_type_bitmask` |
| VoWiFi | Wi-Fi 支持要看 bitmask，常见 Wi-Fi 对应值为 18 |
| 冲突 | 同 MCC/MNC 下同 type APN 应避免重复 entry 或同 type 冲突 |

## 常见症状入口

| 症状 | 优先看 | 联动 |
|---|---|---|
| VoLTE 开关不显示 | support plan、feature option、CarrierConfig | SBP、IMS config、Telephony log |
| VoWiFi 开关不显示 | `MTK_WFC_SUPPORT`、`MTK_EPDG_SUPPORT`、CarrierConfig | IMS APN、ePDG、WFC/ePDG |
| IMS 不注册 | IMS APN、CarrierConfig、VoPS、SBP | NAS/RRC、IMS log |
| 特定 operator 行为不同 | CarrierConfig、SBP/DSBP、NVRAM | IMS/Data/SMS log |
| 换 SIM 后配置没变 | CarrierConfig cache、SIM PIN/unlock、subId | iccid XML、Telephony log |
| MMS fail | MMS APN、Message app、APN DB | Data/PDU、MMS log、Netlog |
| 默认网络模式不对 | preferred network mode、RAT config | NAS/RRC、`AT+ERAT` |
| CT VoLTE 默认 off | CT VoLTE logic、`AT+EIMSCFG` | ImsService、RIL unsolicited event |

## 本地关联

- [CarrierConfig配置方法_重构](Core-Config/CarrierConfig配置方法_重构.md)
- [IMS配置方法](IMS配置方法.md)
- [APN配置方法](Core-Config/APN配置方法_重构.md)
- [MTK-WFC-ePDG配置与排查索引](MTK-WFC-ePDG配置与排查索引.md)
- [MTK-5G注册与PDU排障入口](../30_Troubleshooting/MTK-5G注册与PDU排障入口.md)
