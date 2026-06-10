---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
platform: MTK
source: Notion MTK 网络通信模块知识库 / MediaTek Online Telephony Common
source_url: https://www.notion.so/35df72d579ba817eb528d6f08a68e6f8
search_tier: supplemental
---

# MTK网络通信问题抓Log与提交模板

<!-- SUPPLEMENTAL_BOUNDARY_START -->
## 使用边界

- 本页是补充资料或短专题，适合查局部步骤、旧来源和零散技巧。
- 若需要直接定位问题，优先回到对应主流程、配置方法、排障流程或 Case。
- 后续新增结论应沉淀到主文档，本页只保留来源和辅助说明。
<!-- SUPPLEMENTAL_BOUNDARY_END -->


## 使用入口

这篇用于提交 MTK 网络通信问题前准备证据包。适用范围：注册/驻网、IMS/VoLTE/VoWiFi/VoNR、Data/APN/PDU、吞吐、SMS/MMS/CB、Call/Emergency、RRC/切换、SIM/AT、三方应用上网。

目标不是多抓 log，而是保证复现窗口、问题时间点、DUT/REF 对比和第一手分析足够明确。

## 速查结论

- 通信问题基础 log 包按 `AP/Mobile log + MD/Modem log + Telephony log` 起步。
- 开机即失败、首次注册失败、首次 attach/registration 异常时补 BOOT log。
- Data / HTTP / TCP / MMS / 三方应用问题补 Netlog / tcpdump / pcap / socket log。
- IMS / WFC 类问题必须确认 IMS/SIP/IWLAN/ePDG trace 可用。
- RRC / 驻网 / 切换问题要保证 NAS/RRC/RF 信息完整。
- 提交时必须标明 issue time，不能只写“看 log”。

## 复现前固定信息

| 字段 | 要填什么 |
|---|---|
| Project / Load | 项目名、版本、branch、build time |
| DUT | 芯片、平台、硬件版本、SIM slot、是否双卡 |
| SIM / Operator | 运营商、国家/城市、是否 roaming、套餐状态 |
| 网络环境 | RAT、PLMN、band、cell/PCI、Wi-Fi SSID、ePDG/IMS 场景 |
| 复现步骤 | 从开机/插卡/飞行模式/拨号/上网到失败的步骤 |
| 发生时间点 | 精确到秒，最好列 2-3 个关键时间 |
| DUT 现象 | UI、状态栏、toast、错误码、拨号失败原因 |
| REF 对比 | 对比机型号、平台、同 SIM/同地点行为 |
| 客制化信息 | CarrierConfig、SBP、NVRAM、APN、IMS config 改动 |
| 初步分析 | 已排除什么、怀疑什么、希望 MTK 看哪个时间点 |

## 打开 Telephony Log

Android S 之前：

```text
EngineerMode -> Log and Debugging -> Telephony Log Setting -> Enable -> reboot
```

Android S 及之后：

```text
DebugLoggerUI / MTK Log APK -> Setting -> Dynamic settings -> TelephonyLog -> Enable -> reboot
```

ADB：

```bash
adb root
adb shell setprop persist.vendor.log.tel_dbg 1
adb shell setprop persist.vendor.log.tel_log_ctrl 1
adb reboot
```

必须打开的场景：IMS / VoLTE / VoWiFi / VoNR / ViLTE / IMS SS、Call / Emergency、CarrierConfig、SIM/RAT、APN、MMS、CB、Dialer、外场和协议测试。

## 按问题类型抓什么

| 问题类型 | 必抓 log | 第一手检查点 |
|---|---|---|
| 注册 / 驻网 / 搜网 | AP + MD + Telephony，开机问题加 BOOT | NAS reject、PLMN search、camp-on、RRC connection、forbidden list |
| 5G 注册 / PDU Session | AP + MD + Telephony | 5GMM/5GSM cause、T3502/T3346、PDU session establishment |
| RRC / 切换 / RLF / paging | MD/RRC/RF + AP + Telephony | system info、measurement report、handover command、RLF cause |
| IMS / VoLTE / VoNR | AP + MD + Telephony + IMS/SIP trace | IMS PDN、SIP REGISTER、401/403/timeout、INVITE/183/200 OK |
| VoWiFi / WFC / ePDG | AP + MD + Telephony + IWLAN/ePDG + Wi-Fi/netlog | ePDG DNS、IKE_AUTH、IMS over Wi-Fi、W2L/L2W handover |
| Data / APN | AP + MD + Telephony + Netlog | PDN/PDU、IP、DNS、route、UL/DL packet flow |
| 吞吐低 | AP + MD + RF/RRC + Netlog + speed report | RF、CA/NR capability、scheduler、TCP/window、server |
| 三方应用上网 | Mtklog + Netlog + socket/tcpdump | 单 App 失败还是全局失败、socket error、Stream ID |
| SMS | AP + MD + Telephony | SMS submit/deliver/report、domain、IMS/WiFi 注册状态 |
| MMS | Mobile log + Netlog + MD log | MMS PDN、Mms/Txn、MMS APN、UA |
| Cell Broadcast / PWS | AP + MD + Telephony | `cb_data_ind`、`cb_update`、channel 配置 |
| CS / Emergency Call | AP + MD + Telephony | local emergency rule、选卡逻辑、domain selection、call setup |
| SIM / SAT / BIP / AT | AP + MD + Telephony + SIM/UIM | SIM refresh、service table、AT routing、BIP session |

## eService / issue描述模板

Title 建议：

```text
[Customer][Project][TestType][Country/City][Operator][Module] short English issue summary
```

Description 建议：

```text
1. Build / Load / Branch:
2. DUT / REF:
3. SIM / Operator / Country / City:
4. Test type: FT / Lab / CTA / Operator official / Internal
5. Problem summary:
6. Reproduce steps:
7. Expected result:
8. Actual result:
9. Issue time in log:
10. Logs attached: AP / MD / Telephony / BOOT / Netlog / pcap / video
11. First analysis:
12. Customization involved: CarrierConfig / SBP / NVRAM / APN / IMS config / app changes
13. Related FAQ / DCC checked:
14. Need MTK help on:
```

## 提交前自检

- [ ] Title 里有项目、测试类型、国家/城市、operator、module。
- [ ] 复现步骤清楚，DUT/REF 行为对比清楚。
- [ ] log 包含 AP + MD + Telephony；必要时包含 BOOT / Netlog / pcap / video。
- [ ] 标出 issue time，且 log 覆盖 issue 前后。
- [ ] 已做第一手分析，说明希望继续看哪个时间点和哪类问题。
- [ ] 若涉及客制化，附 CarrierConfig / SBP / NVRAM / APN / IMS config / app 改动说明。
- [ ] 若是 Question 类，先查过 FAQ / DCC；提交时附已查 FAQ ID。

## 常见无效log

- 只给截图，不给 log。
- 只给 AP log，没有 MD / Telephony log。
- IMS / Call 问题没有打开 Telephony log。
- log 从失败之后才开始抓，看不到触发条件。
- 没有 issue time，只说“看 log”。
- 没有 REF 对比，无法判断网络侧还是 DUT 侧。
- MMS / HTTP / TCP 问题没有 Netlog / socket 信息。
- 外场问题没有地点、operator、RAT、band/cell 信息。
- 客制化问题没有附配置改动。

## 本地关联

- [MTK-DebugLogger抓LogSOP](MTK-DebugLogger抓LogSOP.md)
- [Log分析方法](../Log-Analysis/Log分析方法.md)
- [MTK-WFC-ePDG配置与排查索引](../../60_Configuration/MTK-WFC-ePDG配置与排查索引.md)
- [MTK-5G注册与PDU排障入口](../../30_Troubleshooting/MTK-5G注册与PDU排障入口.md)
