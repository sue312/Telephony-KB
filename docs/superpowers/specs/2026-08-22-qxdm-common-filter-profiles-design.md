# QXDM 常见业务筛选配置包设计

## 背景与目标

基于本机 `C:\Program Files\Qualcomm\QXDM5\QXDM.exe` 5.2.660，为 Telephony-KB 生成可复用的 Qualcomm 常见业务日志配置包。配置同时覆盖：

- QXDM PC 端实时抓取和离线 Filtered View：`.dmc`。
- 设备端 SD Logging 的 DIAG Mask：`.cfg`。
- 人工可读、可审查的启用项清单：`.items.txt`。

本机用户手册确认：DMC 用于设置需要记录的数据包，并可保存视图；CFG Generator 从 Filtered View 的 logging masks 生成设备端 `.cfg`。两者用途相关，但不能把 `.cfg` 当作普通离线 Filtered View 文件。

## 交付目录

```text
70_Tools-Debug/QXDM/
├─ README.md
├─ profiles/
│  ├─ 00_Common_Balanced/
│  ├─ 01_Network_Registration_LTE_NR/
│  ├─ 02_Data_Session_LTE_NR/
│  ├─ 03_IMS_Registration/
│  ├─ 04_VoLTE_VoNR_CSFB_Call/
│  ├─ 05_VoWiFi_ePDG/
│  ├─ 06_SMS_IMS_NAS/
│  ├─ 07_Mobility_Handover_RLF/
│  ├─ 08_Emergency_Call/
│  ├─ 09_SIM_UIM_MCFG/
│  └─ 10_Stability_SSR_Fatal/
└─ validation/
   ├─ Test-QxdmProfiles.ps1
   └─ QXDM-5.2.660-validation.md
```

每个业务目录固定包含同名 `.dmc`、`.cfg` 和 `.items.txt`。

## 业务范围

| 编号 | 业务包 | 主要覆盖范围 |
|---|---|---|
| 00 | Common Balanced | 注册、数据、IMS、语音、SMS、移动性和稳定性的低速关键控制面项 |
| 01 | Network Registration LTE NR | LTE/NR RRC、LTE NAS、5GMM/5GSM、GSM/WCDMA 回落与注册事件 |
| 02 | Data Session LTE NR | ESM、5GSM、PDN/PDU Session、QMI WDS/DSD/NAS 与数据状态 |
| 03 | IMS Registration | IMS 注册、SIP、P-CSCF、IMS QMI/事件和必要的承载上下文 |
| 04 | VoLTE VoNR CSFB Call | SIP/SDP、IMS 呼叫、VoLTE/VoNR、CSFB、Call Manager 和语音承载控制面 |
| 05 | VoWiFi ePDG | WLAN/IMS、ePDG、IKE/IPsec、IMS SIP 和 Wi-Fi Calling 相关状态 |
| 06 | SMS IMS NAS | IMS SMS、NAS SMS、WMS、CP/RP/TPDU 以及必要的注册上下文 |
| 07 | Mobility Handover RLF | LTE/NR 测量、切换、重建、RLF、TAU/Registration Update 和 Inter-RAT |
| 08 | Emergency Call | IMS emergency、NAS emergency service、E911/ECBM、呼叫控制和定位辅助事件 |
| 09 | SIM UIM MCFG | UIM/MMGSDI、QMI UIM、MCFG/PDC、订阅和 NV/配置激活状态 |
| 10 | Stability SSR Fatal | fatal、assert、SSR、reset、crash、错误事件和低速稳定性 debug message |

## 生成原则

1. 使用本机 QXDM 数据库和原生 Filtered View/Manage Configuration/CFG Generator 链路生成，不直接套用其他版本配置。
2. 每个业务包必须能独立使用，允许重复少量公共控制面项。
3. 默认保留 `Accept Unknowns`，避免目标版本存在本机数据库尚未定义的 item 时被静默丢弃。
4. 优先启用 OTA、NAS/RRC、IMS SIP、QMI 状态、Events 和必要 Message Packets；不默认启用高频 L1、RF IQ、全量 ULog 或吞吐调试项。
5. `00_Common_Balanced` 只提供平衡的快速入口，不替代专项包。QXDM 可同时选择多个 DMC，故不另做全量大包。
6. 文件名只使用 ASCII，中文说明集中在 README 和验证报告中。

## 错误处理与兼容性边界

- 本机数据库中不存在的候选 item 不写入配置，并在 `.items.txt` 中的“未匹配候选”章节记录。
- 某业务无法生成有效 CFG 时，不复制伪造文件；验证报告必须记录 QXDM 返回结果和失败原因。
- DMC/CFG 可在 QXDM 5.2.660 加载只证明本机工具兼容，不能替代连接具体目标后验证 log mask 是否被 modem 接受。
- 高通平台和 modem 分支会改变 item key；README 必须提示在新版本 QXDM/数据库上重新生成或复核。

## 验收标准

1. 11 个业务目录齐全，每目录含非空 `.dmc`、`.cfg`、`.items.txt`。
2. 所有 DMC 可由 QXDM 5.2.660 加载并恢复对应命名的 Filtered View。
3. 所有 CFG 由本机 CFG Generator 或等价 QXDM 原生转换接口生成，并能被本机工具重新读取。
4. `.items.txt` 与 DMC 中启用的 item family 一致，且记录未匹配候选。
5. 自动检查脚本通过，`git diff --check` 通过。
6. 验证报告区分“本机工具已验证”和“连接目标设备待验证”。
