---
doc_type: index
domain: Meta
status: active
quality: generated
generated: true
search_tier: main_entry
---

# Case横向索引

> 由 `70_Tools-Debug/generate-case-index.ps1` 生成。不要手工改表格；新增或修改 case 后重新运行脚本。

## 统计

| 维度 | 值 | 数量 |
|---|---|---:|
| Domain | Call | 17 |
| Domain | Data | 13 |
| Domain | IMS | 10 |
| Domain | Registration | 23 |
| Domain | Signal | 3 |
| Domain | SIM | 24 |
| Domain | SMS | 4 |
| Domain | Stability | 21 |
| Domain | Supplementary-Service | 2 |
| Platform | Android | 1 |
| Platform | Mixed | 29 |
| Platform | MTK | 20 |
| Platform | MTK/UNISOC | 1 |
| Platform | UNISOC | 66 |
| 第一坏点分类 | Call / SS / ECC | 20 |
| 第一坏点分类 | Data / APN / ESM | 17 |
| 第一坏点分类 | EMM / PLMN / Registration | 18 |
| 第一坏点分类 | IMS / SIP | 10 |
| 第一坏点分类 | RRC / RF / Cell | 3 |
| 第一坏点分类 | SIM / EF / Card | 24 |
| 第一坏点分类 | SMS / CB / FDN | 4 |
| 第一坏点分类 | Stability / NV / Modem | 21 |
| Status | closed | 4 |
| Status | open | 2 |
| Status | summarized | 99 |
| Status | summarized_with_log_gap | 12 |
| SearchTier | case_summary | 113 |
| SearchTier | supplemental | 4 |

## 全量索引

| Case | Domain | 平台 | 第一坏点分类 | 层级 | 置信度 | 状态 | Source | 第一坏点 |
|---|---|---|---|---|---|---|---|---|
| [5G to 2G (GPRS) Fallback Delay After Video Call](Call/Imported_Call_08_5G_to_2G_GPRS_Fallback_Delay_After_Video_Call.md) | Call | Mixed | Call / SS / ECC | 'RRC/Modem/Network' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'RRC release 指向 utra-FDD 10738 后测量结果为 0；可测 10763 小区 PLMN 不匹配' |
| [CS通话杂音](Call/Imported_Call_09_CS通话杂音.md) | Call | Mixed | Call / SS / ECC | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'CSFB 后 3G serving cell 质量差：ECNO=-21、RSCP=-63' |
| [vowifi 无法拨打电话](Call/Imported_Call_04_vowifi_无法拨打电话.md) | Call | Mixed | Call / SS / ECC | 'IMS/IWLAN/ECC' | low | summarized_with_log_gap | 'Old Outline knowledge base; split from 通话问题案例补充.md' | '证据缺口在 VoWiFi ECC 域选与 IMS emergency 建呼链路，当前 markdown 只有 PPT 附件' |
| [一台DUT插联通卡通话正常，其它DUT fail；插移动卡问题不复现](Call/Imported_Call_07_一台DUT插联通卡通话正常_其它DUT_fail_插移动卡问题不复现.md) | Call | Mixed | Call / SS / ECC | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'Fail DUT log 提示 no RF calibration data，随后 MT CSFB 到 3G 扫频但未完成 3G 驻留' |
| [405854/RJIO SRVCC 过程中 srvcc_cap=0 导致 BYE](Call/2026-06-25_Call_SRVCC_405854_RJIO_srvcc_cap为0导致BYE.md) | Call | MTK | Call / SS / ECC | IMS/Modem/OperatorProfile | high | summarized | F:\\Log\\SRVCC\\debuglogger; F:\\Log\\SRVCC\\62130\\debuglogger | SRVCC 开始时 VoLTE UA 打印 srvcc cap: 0x00，随后立即释放 IMS session 并发送 BYE |
| [LA Réunion重定向](Call/Imported_Call_03_LA_Réunion重定向.md) | Call | MTK | Call / SS / ECC | 'Config/Modem/AP' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'eccdata / EccList 中 RE 的 15、17、18 本地配置与运营商期望不一致' |
| [SRVCC Claro切换掉话](Call/2025-W22_Call_SRVCC_Claro切换掉话.md) | Call | MTK | Call / SS / ECC | IMS/Modem/Network | medium | summarized_with_log_gap | internal weekly technical case | 证据缺口在 SRVCC 切换阶段：需要先确认能力协商是否匹配，再看 mobility / CS 承接 / release cause |
| [urn:service:sos.police问题](Call/Imported_Call_01_urnservicesos.police问题.md) | Call | MTK | Call / SS / ECC | 'Network/Modem' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'RIL 上报 network ECC category:31 后，SIP emergency URN 映射成 urn:service:sos.police' |
| [无卡紧急呼叫回退超时](Call/2025-07-30_ECC_无卡紧急呼叫回退超时.md) | Call | MTK | Call / SS / ECC | AP/Modem/IMS/CS | medium | summarized | internal weekly technical case | IMS emergency 失败后进入 CS domain，EMM_T_CSFB 内未找到可用 CS PLMN |
| [ECC `routing=2` 不等于无卡禁止](Call/2022-07-30_ECC_UNISOC_routing不控制无卡禁止_card_flag.md) | Call | UNISOC | Call / SS / ECC | Framework/Telephony/EmergencyNumberTracker | high | summarized | CQWeb SPCSS01017433 | 把 routing=2 误理解为 Without SIM 不能拨打 |
| [ECC csfb cs后重回LTE时间过长问题](Call/Imported_Call_02_ECC_csfb_cs后重回LTE时间过长问题.md) | Call | UNISOC | Call / SS / ECC | 'Network/Modem' | high | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'MSG_ID_MNM_PHONE_ECC_STATUS_SET 后 forbidden_rat_list 包含 LTE，随后 LTE RAT TO 3G RAT 是选网进入而不是 CSFB' |
| [PIN未解锁时 EF_ECC 与无卡 ECC 分类](Call/2021-06-04_ECC_UNISOC_PIN未解锁EF_ECC与无卡ECC分类.md) | Call | UNISOC | Call / SS / ECC | Modem/L4/MMI/ECC | high | summarized | CQWeb SPCSS00841322 | MMIAPIPHONE_GetSimExistedStatusEx 将 PIN 未解锁状态判为无卡，后续 MMIAPICC_IsEccByLocalConfig 走 Without SIM ECC |
| [PUK 锁卡紧急呼叫误走 PS 域无声](Call/2024-05-27_ECC_UNISOC_PUK锁卡紧急呼叫误走PS域无声.md) | Call | UNISOC | Call / SS / ECC | RTOS MMI / MN_CALL / ATC | medium | summarized | CQWeb SPCSS01344396 | MSG_ID_MN_CALL_VOICE_CALL_SETUP_REQ 后 mncall_volte 显示 MO call domain 走失败域，而对比机同场景走 CS 域 |
| [会议通话无法合并](Call/Imported_Call_06_会议通话无法合并.md) | Call | UNISOC | Call / SS / ECC | 'IMS/SIP/NV/Network' | medium | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'SIP REFER 后是否收到 202 Accepted；若收到 486 Busy Here 或无 202，再分支查网络/订阅/NV' |
| [喀麦隆 113 缺少 `routing:2` 导致误走 `EMERGENCY_SETUP`](Call/2026-06-05_ECC_UNISOC_喀麦隆113缺少routing2误走EMERGENCY_SETUP.md) | Call | UNISOC | Call / SS / ECC | UNISOC ECC config / Modem Call Control / CS domain selection | high | summarized | F:\\Log\\ECC\\20260602 Ylog\\md_20260602-100945_armlog\\md_20260602-100945.logel | 失败版本 113 缺少 routing:2，拨号链路按真紧急建立，MNCALL 下发 emergency call 并发送 EMERGENCY_SETUP |
| [双卡紧急号码共享](Call/2025-06-23_ECC_双卡紧急号码共享.md) | Call | UNISOC | Call / SS / ECC | AP/Framework/RIL | high | summarized | internal weekly technical case | 号码识别阶段命中 mEmergencyNumberList |
| [无卡紧急呼叫选到 eSIM 卡槽失败](Call/2025-12-10_ECC_UNISOC_无卡紧急呼叫选到eSIM卡槽失败.md) | Call | UNISOC | Call / SS / ECC | AP Telephony / UnisocCallManager / RIL / Modem ATC | high | summarized | CQWeb SPCSS01593707 | Modem 侧看到无卡紧急呼叫 ATD112/ATD911 被下发到 sim:1，AP 侧 getProperPhoneForEcc 需要区分实体 SIM 与 eUICC |
| [APN IPv6代理不支持](Data/Case_Data_APN_IPV6代理不支持.md) | Data | MTK | Data / APN / ESM | AP/Modem/Network | medium | summarized | internal technical case | IPv6-only APN 下 TCP SYN 访问由 proxy 派生的 NAT64 地址无响应，删除 proxy 后恢复 |
| [快速回4G与吞吐量KPI](Data/Case_Data_快速回4G与吞吐量KPI.md) | Data | MTK/UNISOC | Data / APN / ESM | AP/Modem/RAN | medium | summarized | internal project summary | 2/3G 场景下无 LTE 邻区或无回 LTE 触发；吞吐量场景下 DUT/REF 小区、能力、测试手法未统一 |
| [APN `type=wap` 显示为空](Data/2025-02-06_Data_UNISOC_APN_WAP类型显示为空.md) | Data | UNISOC | Data / APN / ESM | Framework/Settings/APN | high | summarized | CQWeb SPCSS01460052 | APN editor/display 枚举标准 APN type 时无法匹配 wap |
| [APN xcap 类型被隐藏](Data/2022-10-31_Data_UNISOC_APN_XCAP类型被隐藏.md) | Data | UNISOC | Data / APN / ESM | Framework/Telephony/CarrierConfig/APN | high | summarized | CQWeb SPCSS01052197 search summary | ApnSettings/ApnEditor 显示 APN type 前被 CarrierConfig 隐藏列表过滤 |
| [CGDCONT 修改 APN 不会自动触发 PDN 重建](Data/2026-05-08_Data_UNISOC_CGDCONT修改APN不触发PDN重建.md) | Data | UNISOC | Data / APN / ESM | Modem/AT/NAS | high | summarized | CQWeb SPCSS01656937 | 直接 AT+CGDCONT 后期望 modem 自动重建已有 PDN，流程假设不符合 AT/PDN 标准拆分 |
| [India 注册 4G 后 DNS 超时无法上网](Data/2026-01-20_Data_UNISOC_India注册4G但DNS超时无法上网.md) | Data | UNISOC | Data / APN / ESM | AP/NetworkMonitor/Netlog | medium | summarized | CQWeb SPCSS01607450 | NetworkMonitor PROBE_DNS 多域名 6s timeout，netlog 中 DNS query 发出后无响应 |
| [MMS size limit 调整为 600KB](Data/2024-11-13_Data_UNISOC_MMS大小限制CarrierConfig.md) | Data | UNISOC | Data / APN / ESM | Framework/CarrierConfig/MMS | high | summarized | CQWeb SPCSS01427933 search summary | CarrierConfig 未按目标 MCC/MNC 覆盖 KEY_MMS_MAX_MESSAGE_SIZE_INT |
| [MMS 发送失败：彩信 PDP 使用错误 APN](Data/2023-09-13_Data_UNISOC_MMS发送失败_APN使用错误.md) | Data | UNISOC | Data / APN / ESM | RTOS MMS / PDP / APN config | medium | summarized | CQWeb SPCSS01232418 | MMIAPIPDP_Active 使用的 APN 与目标 MCC/MNC 的 MMS APN 配置不匹配 |
| [MTN弱网DNS超时与TCP重传](Data/2023-09-28_Data_UNISOC_MTN弱网DNS超时与TCP重传.md) | Data | UNISOC | Data / APN / ESM | AP/Modem/Network | medium | summarized | CQWeb SPCSS01238438 | NetworkMonitor PROBE_DNS 多域名 timeout；netlog 可见 DNS/TCP 流量但存在响应迟滞和重传 |
| [Phoenix视频加载失败DNS无响应](Data/2023-12-04_Data_UNISOC_Phoenix视频加载失败DNS无响应.md) | Data | UNISOC | Data / APN / ESM | AP/Modem/Network | medium | summarized | CQWeb SPCSS01265370 | 14:19~14:20 DNS 解析无响应，随后 CELLULAR validation failed |
| [RTOS Data PDN按需激活后主动释放](Data/2026-04-24_Data_UNISOC_RTOS_DataPDN按需激活后主动释放.md) | Data | UNISOC | Data / APN / ESM | Modem/L4/PDP Manager/Application | high | summarized | CQWeb SPCSS01652533 | PDP Manager 收到 MMIAPIPDP_Deactive/app_handler 请求，传导到协议层 PDN disconnect |
| [Safaricom Wi-Fi切蜂窝被重定向](Data/2023-10-27_Data_UNISOC_Safaricom_WiFi切蜂窝被重定向.md) | Data | UNISOC | Data / APN / ESM | AP/NetworkMonitor/Network | medium | summarized | CQWeb SPCSS01246382 | ConnectivityService validation failed with redirect to safaricom.zerod.live；APN 配置成功/失败前后无差异 |
| [白卡 `EF_AD` 测试模式导致 XCAP 复用默认承载](Data/2026-09-03_Data_UNISOC_白卡EF_AD测试模式导致XCAP复用默认承载.md) | Data | UNISOC | Data / APN / ESM | SIM EF / Operator NV / Modem SS / Data bearer | high | open | F:/Log/A01/A01_XCAP/2026-09-03-16-45-38_42004_XCAP | SIM 初始化读到 EF_AD=80000002，首字节 0x80 触发 UNISOC 测试卡判定 |
| [SMS短码CTS配置不匹配](IMS/2025-W20_IMS_SMS短码CTS配置不匹配.md) | IMS | Android | IMS / SIP | Framework/Telephony | medium | summarized | internal weekly technical case | `SmsUsageMonitorShortCodeTest#testSmsShortCodeDestination` 报 expected:<1> but was:<3> |
| [DUT视频通话闪退](Call/Imported_Call_10_DUT视频通话闪退.md) | IMS | Mixed | IMS / SIP | 'IMS/ESM/AP/Modem' | medium | summarized_with_log_gap | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'ViLTE 建呼中缺少 QCI2 dedicated bearer，AP 侧 `RIL_IMS_REQUEST_SET_VIDEO_RESOLUTION` 返回 RADIO_NOT_AVAILABLE' |
| [HMD VoLTE 注册 403：网络 IMEI 校验失败](IMS/Imported_IMS_01_HMD场测反馈_VoLTE_注册_403.md) | IMS | Mixed | IMS / SIP | IMS/Modem/Network | high | summarized | Old Outline knowledge base; split from IMS问题案例补充.md | SIP/IMS 注册阶段网络返回 403 Forbidden: IMEI check failed |
| [Spark VoWiFi 注册失败：IKE 完整性算法配置错误](IMS/Imported_IMS_03_6032+_Spark反馈WFC注册有问题.md) | IMS | Mixed | IMS / SIP | Modem/IKE/IMS | high | summarized | Old Outline knowledge base; split from IMS问题案例补充.md | IKE_SessCheckAlgorithms unsupported integ algo:18，导致 IKE_ATTACH_FAILED |
| [Case: MTK 46001/CU DSBP 未打开导致 SMS over IMS 不注册](IMS/2026-07-02_IMS_MTK_CU_DSBP未打开导致SMS-over-IMS不注册.md) | IMS | MTK | IMS / SIP | AP vendor property / RIL / Modem DSBP / IMSM / ImsSmsDispatcher | high | summarized | F:\\Log\\WM18短信无法发送\\debuglogger; F:\\Log\\WM18短信无法发送\\pass\\debuglogger; F:\\Log\\WM18短信无法发送\\MP6debuglogger\\debuglogger; F:\\Log\\WM18短信无法发送\\SMSOIP\\debuglogger | RIL 下发 AT+EDSBP=0，modem 侧 DSBP disable / SIM_SBP_ID:-1，导致没有 +ESBPID:0,2 和 IMSM sbp_id[2] |
| [Iran 43211 IMS 不注册：MTK SBP / MNCMCC whitelist 未命中](IMS/Imported_IMS_02_Iran_无法注册IMS问题.md) | IMS | MTK | IMS / SIP | AP/CCCI/Modem/IMC/SBP | high | summarized | Old Outline knowledge base; split from IMS问题案例补充.md | IMC_REG condition check failed: IMC_REG_CHECK_MNCMCC_FAILED before IMS PDN connectivity request |
| [SMS over IP / SMS over IMS 配置缺失](IMS/2025-07-29_IMS_SMS-over-IP配置缺失.md) | IMS | MTK | IMS / SIP | IMS/SDM/Modem/Network | medium | summarized | internal technical case and imported SMS Outline notes | 未同时满足 IMS 注册可用、SMS over IP allowed、SGs 不优先、IMS profile sms_support/sms_network_types 打开 |
| [DUT视频通话卡死](Call/Imported_Call_11_DUT视频通话卡死.md) | IMS | UNISOC | IMS / SIP | 'IMS/RTP/AP/Modem' | medium | summarized_with_log_gap | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'modem/TCPIP 可见 audio/video 数据交互正常，缺少 AP media/render/UI 卡死证据' |
| [RTT 通话](Call/Imported_Call_05_RTT_通话.md) | IMS | UNISOC | IMS / SIP | 'Dialer/IMS/IWLAN/Modem' | medium | summarized | 'Old Outline knowledge base; split from 通话问题案例补充.md' | 'AP Dialer RTT 能力/入口限制，而不是 VoWiFi 注册或 modem RTT 承载失败' |
| [UNISOC 41903 VoWiFi 注册失败：IKE PRF+ 密钥展开在 200 字节处截断](IMS/2026-09-03_VoWiFi_UNISOC_41903_PRF密钥展开截断导致IKE_AUTH解密失败.md) | IMS | UNISOC | IMS / SIP | Modem/IKE/Crypto/IMS | high | open | F:/Log/A01/A01_VOWIFI/2026-09-03-10-47-15_41903 VOWIFI; F:/Log/A01/A01_VOWIFI/2026-09-03-17-33-50_REF_41903 VOWIFI | IKE_SA_INIT 后生成的 SK_er 仅前 20/32 字节有效，后 12 字节为 0；SK_pi/SK_pr 全 0，密钥展开恰在累计 200 字节处停止 |
| [CM52在宁波实验室测试，待机功耗高](Registration/Imported_Registration_09_CM52在宁波实验室测试_待机功耗高.md) | Registration | MTK | Call / SS / ECC | 'Modem/NWSEL/Power' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | '无支持 ECC 小区时 modem 持续搜网，合入降低紧急搜网频率 patch 后功耗下降' |
| [2026-05-14 MTK LTE开机注册成功](Registration/2026-05-14_Registration_MTK_LTE开机注册成功.md) | Registration | MTK | Data / APN / ESM | AP/Modem/Network | high | closed | 'F:\Log\流程Log\MTKLte注册流程\debuglogger' | none |
| [MP6漫游失败](Registration/Imported_Registration_05_MP6漫游失败.md) | Registration | MTK | Data / APN / ESM | APN/Modem/Network | medium | summarized | Old Outline knowledge base; split from 注网问题案例补充.md | AT +EGREG 已显示 roaming 注册成功，但打开漫游后仍无 PDP 请求，首坏点转为 APN 匹配 |
| [Case: UNISOC LTE开机注册成功样例](Registration/2026-05-14_Registration_UNISOC_LTE开机注册成功.md) | Registration | UNISOC | Data / APN / ESM | AP/Modem/Network | high | closed | 'F:\Log\流程Log\展锐Lte注册流程\ylog\poweron\modem\md_20260514-091138_armlog', 'F:\Log\流程Log\展锐Lte注册流程\ylog\ap\001-0514_091134--0514_091333_poweron' | none |
| [Verizon 未认证 IMEI 后 Attach / PDN 拒绝](Registration/2025-10-15_Registration_UNISOC_Verizon未认证IMEI后Attach_PDN拒绝.md) | Registration | UNISOC | Data / APN / ESM | Modem/NAS/ESM | medium | summarized | CQWeb SPCSS01550358 / SPCSS01607196 | ATTACH_REQUEST 后收到 ATTACH_REJECT，同时 PDN_CONNECTIVITY_REJECT 携带 REQ_SERV_OPT_NOT_SUBSCRIBED |
| [BB印度实网反馈，无法注册网络](Registration/Imported_Registration_02_BB印度实网反馈_无法注册网络.md) | Registration | Mixed | EMM / PLMN / Registration | 'Network/Modem' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'NAS Attach Reject，EMM cause 指向 Illegal ME / unauthorized ME' |
| [CM52没有切到吞吐量更高的小区](Registration/Imported_Registration_08_CM52没有切到吞吐量更高的小区.md) | Registration | Mixed | EMM / PLMN / Registration | 'Mixed' | low | summarized_with_log_gap | 'Old Outline knowledge base; split from 注网问题案例补充.md' | '证据缺口：缺少 NR 小区测量、重选/切换策略、SIB 优先级和吞吐量对比 log' |
| [DAHLIA 450A软件刷在450H手机上，能搜到网络，但是注册不上网络](Registration/Imported_Registration_01_DAHLIA_450A软件刷在450H手机上_能搜到网络_但是注册不上网络.md) | Registration | Mixed | EMM / PLMN / Registration | 'RF/NV/Modem' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'ATTACH_REQUEST / RRCCONNECTIONREQUEST 已发出，首坏点回到 RF 参数/硬件版本错配' |
| [GH67M1_OMEGA无法注册网络](Registration/Imported_Registration_04_GH67M1_OMEGA无法注册网络.md) | Registration | Mixed | EMM / PLMN / Registration | 'Network/Modem' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'LTE/3G 注册 reject cause 6: Illegal ME' |
| [MTN Uganda售后反馈，无法注册网络](Registration/Imported_Registration_03_MTN_Uganda售后反馈_无法注册网络.md) | Registration | Mixed | EMM / PLMN / Registration | 'Network/Modem' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | '注册失败原因值 0x06 / Illegal ME' |
| [WM58 使用物联网卡，无法注册上网络](Registration/Imported_Registration_06_WM58_使用物联网卡_无法注册上网络.md) | Registration | Mixed | EMM / PLMN / Registration | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'Cellular 搜不到小区，且 RF 校准参数显示未校准' |
| [SIMLock锁网不生效：产物错误](Registration/2025-W21_Registration_SIMLock锁网不生效_产物错误.md) | Registration | MTK | EMM / PLMN / Registration | Build/Modem/AP | medium | summarized | internal weekly technical case | 产物检查发现基础版本和市场软件 modem image 一致，本地替换单编 modem 后锁网生效 |
| [Steering of Roaming Cause17](Registration/Imported_Registration_10_Steering_of_Roaming_Cause17.md) | Registration | MTK | EMM / PLMN / Registration | 'Modem/NWSEL/MM/SBP' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'NWSEL SBP dump 中 SBP_MM_PERFORM_PLMN_SEARCH_AFTER_LU_ABNORMAL = KAL_FALSE' |
| [3G only 联通弱场无法驻网：全 Band 测量与历史频点差异](Registration/2024-03-27_Registration_UNISOC_3GOnly联通弱场无法驻网.md) | Registration | UNISOC | EMM / PLMN / Registration | Modem/WPHY/WAS | high | summarized | CQWeb SPCSS01316717 | WRRC_MM_PLMN_CAMPING_REQ 后全 Band 测量未获得可驻留小区，随后 WRRC_MM_NO_CELL_IN_PLMN_IND / PLMN_SEL_FAILURE |
| [Case: UNISOC LTE飞行模式开关回网成功](Registration/2026-05-14_Registration_UNISOC_LTE飞行模式开关回网成功.md) | Registration | UNISOC | EMM / PLMN / Registration | AP/Modem | high | closed | 'F:\Log\流程Log\展锐飞行模式开关注册\ylog', 'F:\Log\流程Log\展锐飞行模式开关注册\ylog\modem\md_20260514-104312_armlog' | none |
| [Case: UNISOC LTE手动搜网选网成功](Registration/2026-05-14_Registration_UNISOC_LTE手动搜网选网成功.md) | Registration | UNISOC | EMM / PLMN / Registration | AP/Modem/Network | high | closed | 'F:\Log\流程Log\展锐手动搜网\ylog', 'F:\Log\流程Log\展锐手动搜网\ylog\modem\md_20260514-104542_armlog' | none |
| [GH6733B_Symphony反馈信号波动频繁](Registration/Imported_Registration_07_GH6733B_Symphony反馈信号波动频繁.md) | Registration | UNISOC | EMM / PLMN / Registration | 'Modem/LRRC/RF' | high | summarized | 'Old Outline knowledge base; split from 注网问题案例补充.md' | 'LRRC 根据 SINR 触发 non-intra search，并从 arfcn 1800 重选到 39248 后又回到 1800' |
| [Kenya Safaricom LTE 拒绝后 3G 建链失败](Registration/2026-03-06_Registration_UNISOC_Kenya_Safaricom_LTE拒绝后3G建链失败.md) | Registration | UNISOC | EMM / PLMN / Registration | Modem/NAS/3G AS | high | summarized | CQWeb SPCSS01629027 | LTE ATTACH_REJECT cause 15 后，3G WRRC/MM signalling establish 失败，重复 RRCConnectionRequest |
| [Spectranet 无信号：Band 40 不支持导致无法驻网](Registration/2024-05-16_Registration_UNISOC_Spectranet_B40不支持无信号.md) | Registration | UNISOC | EMM / PLMN / Registration | Modem/RRC/NAS/RF capability | high | summarized | CQWeb SPCSS01345057 | LTE cell select 后 Attach Reject: EMM_CAUSE_NO_SUIT_CELLS_IN_TA，并进入 LIMITED_SERVICE |
| [UECapability 不带 2G 能力：网络模式客制化影响能力上报](Registration/2025-07-16_Registration_UNISOC_UECapability缺少2G能力_网络模式客制化.md) | Registration | UNISOC | EMM / PLMN / Registration | AP/CarrierConfig/RIL/Modem/RRC | high | summarized | Old Outline knowledge base; split from IMS问题案例补充.md and CQWeb SPCSS01532727 | CarrierConfig 客制化网络模式触发 updateOemAllowedNetworkMode -> setPreferredNetworkType -> AT+SPTESTMODEM=24,6 |
| [弱场移动后无法回 4G：先补齐 DSP/ARM 对齐证据](Registration/2025-05-18_Registration_UNISOC_弱场移动后无法回4G_Log证据不足.md) | Registration | UNISOC | EMM / PLMN / Registration | Modem/LRRC/DSP | medium | summarized_with_log_gap | CQWeb SPCSS01497276 | 目标 LTE 频点测量值极弱，后续卡在 2G 后未及时回 LTE；但 DSP 与 ARM 时间点未完全对齐 |
| [手动选网 CarrierConfig：成功/失败后是否返回自动模式](Registration/2024-06-24_Registration_UNISOC_手动选网CarrierConfig策略.md) | Registration | UNISOC | EMM / PLMN / Registration | Framework/Telephony/CarrierConfig | high | summarized | CQWeb SPCSS01362804 | NetworkSelectSettings.java EVENT_SET_NETWORK_SELECTION_MANUALLY_DONE 分支决定 UI 返回值和网络选择模式 |
| [赞比亚双卡全制式无信号：RF 接收掉底](Registration/2026-04-01_Registration_UNISOC_赞比亚双卡全制式无信号_RF掉底.md) | Registration | UNISOC | EMM / PLMN / Registration | Modem/RF/L1 | high | summarized | CQWeb SPCSS01643005 | ASM select cell 后 LTE/3G/GPRS 搜网均失败，RSSI 主辅通路持续异常低 |
| [3G RACH Preamble 最大发射仍失败：疑似 PA / RF 单机异常](Signal/2026-02-25_Signal_UNISOC_3G_RACH_Preamble最大功率失败疑似PA异常.md) | Signal | UNISOC | RRC / RF / Cell | Modem/WPHY/RF | high | summarized | CQWeb, see related Registration case | WRRC_MM_SIGNALLING_ESTABLISH_CNF est_success=0，WPHY 显示 TX_RACH_Preamble 多次发送且功率达到网络/硬件上限 |
| [弱场 RSRP 低触发 2G 重定向](Signal/2025-05-07_Signal_UNISOC_弱场RSRP低触发2G重定向.md) | Signal | UNISOC | RRC / RF / Cell | Modem/LRRC/L1/RF | high | summarized | CQWeb SPCSS01502273 | DUT 在 LTE 小区上报测量后收到 RRCConnectionRelease redirectedCarrierInfo=GERAN，同时同时间 RSRP 约 -123 dBm，明显差于对比机约 -114 dBm |
| [搜网失败：前端射频能量低样例](Signal/2024-07-12_Signal_UNISOC_搜网失败前端射频能量低.md) | Signal | UNISOC | RRC / RF / Cell | Modem/RF/L1 | medium | summarized | CQWeb SPCSS01363092 search summary | MSG_ID_LTEAS_CELL_SELECT_CNF status=0x3 后上报 PLMN_SEL_FAILURE_IND |
| [6601 蓝鸟售后反馈不识卡](SIM/Imported_SIM_17_6601_蓝鸟售后反馈不识卡.md) | SIM | Mixed | SIM / EF / Card | 'SIM/HW/ATR' | low | summarized_with_log_gap | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'No ATR；贴纸垫高后仍不识卡，需测量 VSIM/RST/IO 波形' |
| [CC51 safracom，CA超出平台能力，导致无法注册网络](SIM/Imported_SIM_02_CC51_safracom_CA超出平台能力_导致无法注册网络.md) | SIM | Mixed | SIM / EF / Card | 'Modem/LTE PHY/CA capability' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'RIL 上报 LTE_DL_SCH0_TASK PHY CP assert，assert 点在 AFC_mainLccAdjVcoNcoProcess' |
| [Dahlia 451H，卡二识卡后，会自动掉卡](SIM/Imported_SIM_16_Dahlia_451H_卡二识卡后_会自动掉卡.md) | SIM | Mixed | SIM / EF / Card | 'SIM power / NFC UICC / HW' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | '卡二识别后 SIM 电源/IO/RST/CLK 波形异常并掉卡' |
| [GH6683 sunking sim pin issue report](SIM/Imported_SIM_19_GH6683_sunking_sim_pin_issue_report.md) | SIM | Mixed | SIM / EF / Card | 'AP/Data/RIL/SIM' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'DataStallRecoveryManager 从 GET_DATA_CALL_LIST/CLEANUP/RADIO_RESTART 升级到 RESET_MODEM' |
| [GH66B2Astech售后反馈不识卡](SIM/Imported_SIM_05_GH66B2Astech售后反馈不识卡.md) | SIM | Mixed | SIM / EF / Card | 'Modem/RFIC/HW' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'ccci1/fsm 上报 modem assert，原始根因为 RF 芯片版本检查失败' |
| [VINCA SIM PIN掉卡问题](SIM/Imported_SIM_18_VINCA_SIM_PIN掉卡问题.md) | SIM | Mixed | SIM / EF / Card | 'Kernel/DTS/DWS/SIM power' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'kernel time 约 31s 出现 vsim1/vsim2 disabling，随后 RIL 上报 ESIMS 事件' |
| [WM28+ 连不上Meta](SIM/Imported_SIM_01_WM28+_连不上Meta.md) | SIM | Mixed | SIM / EF / Card | 'Modem/RF/NV' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'ccci_fsm 上报 modem assert，需按 WCDMA RF Error Check 指南检查 RF TAS 配置' |
| [WM58使用工厂工具刷机后，不识卡](SIM/Imported_SIM_04_WM58使用工厂工具刷机后_不识卡.md) | SIM | Mixed | SIM / EF / Card | 'Modem/NVRAM/Flash tool' | low | summarized_with_log_gap | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'ccci1/fsm 上报 mcu/service/nvram/src/nvram_main.c assert，para1 = 0x20' |
| [SIM不识卡：No ATR或无插卡中断](SIM/2025-05-19_SIM_不识卡_NO_ATR或无中断.md) | SIM | MTK | SIM / EF / Card | SIM/Modem/HW | medium | summarized | internal case summary | 插卡时 SIM driver 未收到 ATR，或插卡后完全没有 SIM driver 流程 |
| [WM58卡托检查代码修改问题，导致Modem Assert](SIM/Imported_SIM_12_WM58卡托检查代码修改问题_导致Modem_Assert.md) | SIM | MTK | SIM / EF / Card | 'AP/SystemUI/AT/Modem SIM' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'mcu/protocol/layer4/sim/src/sim_handler.c assert，触发点为 AP 下发 AT+ESIMTRAY' |
| [Dahlia singlesim 插卡无 ATR 后掉卡](SIM/2026-05-27_SIM_UNISOC_Dahlia插卡无ATR后掉卡.md) | SIM | UNISOC | SIM / EF / Card | SIM/Modem/HW | high | summarized | F:\\Log\\NOSIM\\ylog; F:\\Log\\NOSIM\\OK\\ylog | 10:05:47 插卡后 CARDSTATE_PRESENT 但 ATR/ICCID 为空，AT+SPATR? 返回空，约 1 秒后回落到 ABSENT/ERROR |
| [eSIM 空卡与 AP euicc 配置：卡2不识别](SIM/2024-08-14_SIM_UNISOC_eSIM空卡与euicc配置.md) | SIM | UNISOC | SIM / EF / Card | SIM/Modem/RIL/Framework | medium | summarized | CQWeb SPCSS01386630 | USIMDRV[1] 收到 ATR，但 EF/应用读取为空；AP GET_SIM_STATUS 显示 APPTYPE_UNKNOWN、ICCID/EID 为空 |
| [Idea漫游显示Airtel与漫游图标配置](SIM/2025-08-22_SIM_UNISOC_Idea漫游显示Airtel与漫游图标配置.md) | SIM | UNISOC | SIM / EF / Card | AP/Framework/CarrierConfig | high | summarized | CQWeb SPCSS01545940 | updateSpnDisplay 中 simNumeric=405799、operatorNumeric=40492，rawPlmn 从 XML 命中 Airtel，showPlmn=true、showSpn=false |
| [MVNO EF_PNN 读取与 pnn_len 为 0](SIM/2023-03-08_SIM_UNISOC_MVNO_EFPNN读取与pnn_len为0.md) | SIM | UNISOC | SIM / EF / Card | Modem/MMI phone / SIM records | high | summarized | CQWeb SPCSS01132047 | GetPNNIndexByOPL / SetPNNWithLac 与 GetNetworkNameString 中 pnn_len 不一致 |
| [MVNO 名称 SPN/PNN 未命中回退本地 PLMN](SIM/2023-02-24_SIM_UNISOC_MVNO名称SPN_PNN未命中回退本地PLMN.md) | SIM | UNISOC | SIM / EF / Card | Modem/MMI phone / Framework operator display | high | summarized | CQWeb SPCSS01124358 | GetNetworkNameString 中 spn_len、pnn_len、ons_len、opn_len 均为 0 |
| [NITZ 名称：飞行模式后缓存失效](SIM/2025-11-06_SIM_UNISOC_NITZ名称飞行模式后缓存失效.md) | SIM | UNISOC | SIM / EF / Card | AP/Framework/Telephony/RIL | medium | summarized | CQWeb index SPCSS01575486; related NITZ config cases SPCSS01266529/SPCSS01638776 | radio off / out of service 后 updateSpnDisplayLegacy 是否继续使用 s_nitzOperatorInfo 缓存未先确认 |
| [PLMN 列表与 SIM 短信参数能力确认](SIM/2026-02-27_SIM_UNISOC_PLMN列表与SIM短信参数能力确认.md) | SIM | UNISOC | SIM / EF / Card | SIM/UICC/AP/Modem | high | summarized | CQWeb SPCSS01630213 | 需要先拆清 EF 文件、平台能力和当前 SIM 实际写入内容，避免把容量支持误解为当前卡内容或 UI 列表数量 |
| [PLMN 名称：ONS 空值与 numeric_operator 双来源](SIM/2024-12-10_SIM_UNISOC_PLMN名称ONS空值与numeric_operator双来源.md) | SIM | UNISOC | SIM / EF / Card | Framework/Telephony/RIL/operator XML | high | summarized | CQWeb SPCSS01440031 | getSimOns() 返回空值后未做 TextUtils.isEmpty 判断，导致高优先级名称链路异常返回 |
| [SIM 热插拔无中断：先确认 NV 路径和硬件触发](SIM/2024-09-26_SIM_UNISOC_热插拔无中断与NV路径.md) | SIM | UNISOC | SIM / EF / Card | SIM/Modem/NV/HW | medium | summarized | CQWeb SPCSS01407737 | 热插拔时间点 modem log 未出现 SIM interrupt / plug-in 相关流程 |
| [SimLock 锁卡状态下 MCC/MNC 为空](SIM/2024-04-12_SIM_UNISOC_SimLock锁卡状态MCCMNC为空.md) | SIM | UNISOC | SIM / EF / Card | Framework/Subscription / RIL / SIMLock | high | summarized | CQWeb SPCSS01329406 | AP 在 NETWORK_LOCKED 状态下期望读取完整 SubInfo MCC/MNC |
| [VSIM 退出后物理卡不显示](SIM/2023-11-21_SIM_UNISOC_VSIM退出后物理卡不显示.md) | SIM | UNISOC | SIM / EF / Card | Framework/Telephony/VSIM/SIM | high | summarized | CQWeb SPCSS01257378 search summary | ATCI_VSIM: vsim_set_nv 返回 CME ERROR，随后物理卡未显示 |
| [单双卡单软多硬：NV 卡槽配置不匹配导致不识卡](SIM/2024-02-05_SIM_UNISOC_单双卡单软多硬NV卡槽配置不匹配.md) | SIM | UNISOC | SIM / EF / Card | Modem/NV/SIM | high | summarized | CQWeb SPCSS01287405 | ro.boot.product.hardware.sku=singlesim，但 NV 卡槽配置仍按旧接反项目处理 |
| [手动搜网列表运营商名与 MNC 位数不匹配](SIM/2022-06-20_SIM_UNISOC_手动搜网列表运营商名MNC位数不匹配.md) | SIM | UNISOC | SIM / EF / Card | Framework/Telephony/RIL | high | summarized | CQWeb SPCSS01007822 | processNetworkName 拼出的 PLMN key 未命中 numeric_operator.xml |
| [手动搜网名称：未注册 5G 时误用 EFOPL5G](SIM/2024-05-17_SIM_UNISOC_手动搜网名称PNN_OPL5G误用.md) | SIM | UNISOC | SIM / EF / Card | Framework/Telephony/RIL/SIMRecords | high | summarized | CQWeb SPCSS01345931 | UniOperatorNameHandler 取 PNN record 时未按当前注册 RAT 区分 EFOPL/EFOPL5G |
| [CB 信道配置受 full/Mainline 版本限制](SMS/2023-01-24_SMS_UNISOC_CB_Full版本信道配置受Mainline限制.md) | SMS | UNISOC | SMS / CB / FDN | CellBroadcastReceiver / Mainline / AP config | high | summarized | CQWeb SPCSS01099451 | 把旧平台源码修改方案套到 full/Mainline CellBroadcastReceiver，并用 00101 白卡测试目标地区信道 |
| [FDN 发送短信：SMSC 和收件人都要在 FDN 列表](SMS/2024-03-11_SMS_UNISOC_FDN发送短信需同时放行SMSC和收件人.md) | SMS | UNISOC | SMS / CB / FDN | Framework/Telephony/SIM FDN | high | summarized | CQWeb SPCSS01310994 | SMS FDN check 中 SMSC 未加入 FDN list |
| [短码短信未到 RILJ `SEND_SMS`](SMS/2025-03-22_SMS_UNISOC_短码发送未到RILJ_SEND_SMS.md) | SMS | UNISOC | SMS / CB / FDN | Framework/Telephony/SMSDispatcher | medium | summarized | CQWeb SPCSS01484963 | SMSDispatcher premium short code 分支处理对象类型错误，导致发送流程在 AP 侧中断 |
| [关闭 CB 菜单仍收到 LTE 紧急广播 4370](SMS/2026-04-12_SMS_UNISOC_CB关闭菜单仍收LTE紧急广播4370.md) | SMS | UNISOC | SMS / CB / FDN | RTOS MMI / L4 / ETWS-CMAS | high | summarized | CQWeb SPCSS01634532 | 把普通 CB 菜单开关等同于底层紧急广播接收开关 |
| [Civic Plus VK7L版本升级Vk1J版本后，IMEI显示unknown](Stability/Imported_SIM_09_Civic_Plus_VK7L版本升级Vk1J版本后_IMEI显示unknown.md) | Stability | Mixed | Stability / NV / Modem | 'Config/Modem/AP' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'md1img build 时间戳与编译产物不一致，反查 custom_modem 指到 civic modem' |
| [civic项目，CU刷回Mini软件，IMEI显示unknown](Stability/Imported_SIM_08_civic项目_CU刷回Mini软件_IMEI显示unknown.md) | Stability | Mixed | Stability / NV / Modem | 'Config/Modem/AP' | medium | summarized_with_log_gap | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'nvram_main.c line 2206，para0=0x0000ef11，分析指向 SML file 丢失' |
| [civic项目，试产前，内部发现Mini软件校准写码后，使用flashtool下载CU软件，modem出现EE](Stability/Imported_SIM_07_civic项目_试产前_内部发现Mini软件校准写码后_使用flashtool下载CU软件_modem出现EE.md) | Stability | Mixed | Stability / NV / Modem | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'SML LID 0x0000ef11 size mismatch：para1=0x644，para2=0xa28' |
| [civic项目BSP生成的Mini软件使用MBW开发的工具写入IMEI后，升级到CU软件，IMEI无法显示](Stability/Imported_SIM_06_civic项目BSP生成的Mini软件使用MBW开发的工具写入IMEI后_升级到CU软件_IMEI无法显示.md) | Stability | Mixed | Stability / NV / Modem | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'CU 开启 NVRAM_BIND_TO_CHIP_CIPHER，Mini 未开启，跨版本升级后 NV 数据无法按新策略解密' |
| [Model3 Proto试产，出现E配置机器meta无法连接](Stability/Imported_SIM_10_Model3_Proto试产_出现E配置机器meta无法连接.md) | Stability | Mixed | Stability / NV / Modem | 'Config/Modem/AP' | medium | summarized_with_log_gap | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'custom_nvram_extra.c line 11520，SML data 为空导致 META 连接失败' |
| [Model3 生产，出现音频无声及卡logo问题](Stability/Imported_SIM_11_Model3_生产_出现音频无声及卡logo问题.md) | Stability | Mixed | Stability / NV / Modem | 'Config/Modem/AP' | medium | summarized_with_log_gap | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'current status 为 nvram_main.c line 2520，para0=0x0000ef31' |
| [NUU单机出现Modem Assert](Stability/Imported_SIM_15_NUU单机出现Modem_Assert.md) | Stability | Mixed | Stability / NV / Modem | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'el1d_rf_error_check.c line 238，para1=0x0d/para2=0x14，指向 RF band/硬件版本不匹配' |
| [WM58 OTA跨版本升级，出现Modem Assert](Stability/Imported_SIM_13_WM58_OTA跨版本升级_出现Modem_Assert.md) | Stability | Mixed | Stability / NV / Modem | 'RF/Modem' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | '升级后版本的 RF_PARA_CUSTOM 指向错误 RF parameter' |
| [G100 通话过程中，出现Modem Assert](Stability/Imported_Stability_G100_通话过程中ModemAssert_PWM32K时钟源.md) | Stability | MTK | Stability / NV / Modem | 'BSP/PWM/Modem' | high | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'ccci modem assert 指向 lte_scheduler.c，同时二分定位到灯环 PWM 32K clock source' |
| [MTK Patch导致ModemEE](Stability/2025-06-27_Stability_MTK_Patch导致ModemEE.md) | Stability | MTK | Stability / NV / Modem | Modem/IMS | medium | summarized | internal weekly technical case | VDM 在 IMS call retry 期间访问 call_id，错误取值 255 后触发 crash |
| [MTK RFIC 版本读取失败导致 Modem 反复 Assert（3D X-ray 确认虚焊）](Stability/2026-07-28_Stability_MTK_RFIC版本读取失败Modem不起_3DXray确认虚焊.md) | Stability | MTK | Stability / NV / Modem | Modem/MML1/MMRF/RFIC/HW | high | summarized | 售后 DebugLogger AP kernel log / MTK FAQ33228 / 3D X-ray | mml1_rf_error_check.c line 156，期望 RFIC 版本 0x02，RFIC1/RFIC2 回读均为 0x00 |
| [WM58从有锁网升级下载到无锁网，Modem Assert](Stability/Imported_SIM_03_WM58从有锁网升级下载到无锁网_Modem_Assert.md) | Stability | MTK | Stability / NV / Modem | 'Config/Modem/AP' | medium | summarized | 'Old Outline knowledge base; split from SIM问题案例补充.md' | 'nvram_main.c line 2192，para0=0x0000ef11 指向 SML/NVRAM 数据保护' |
| [A/B OTA 在 nvmerge 前中断的 fixnv 风险](Stability/2023-09-18_Stability_UNISOC_AB_OTA_nvmerge前中断fixnv风险.md) | Stability | UNISOC | Stability / NV / Modem | update_engine / postinstall / NV partition | high | summarized | CQWeb SPCSS01234705 | update_engine 写入 l_fixnv1/l_fixnv2 后，在 Running /postinstall/bin/nvmerge 之前被打断 |
| [CA 能力上报异常导致 Modem Assert](Stability/2025-06-25_Stability_UNISOC_CA能力上报异常导致ModemAssert.md) | Stability | UNISOC | Stability / NV / Modem | Modem/LTE PHY/UE capability | high | summarized | CQWeb SPCSS01521496 | LTE_DL_SCH0_TASK PHY CP assert in afc_aaal.c after unsupported CA configuration |
| [fastboot 刷 fixnv 导致 IMEI/校准参数丢失](Stability/2022-03-04_Stability_UNISOC_fastboot刷fixnv导致IMEI校准丢失.md) | Stability | UNISOC | Stability / NV / Modem | Bootloader fastboot / NV partition / Field flashing | high | summarized | CQWeb SPCSS00766912 / SPCSS00967511 | fastboot flash fixnv 分区前未备份并合并原机 IMEI/校准 NV |
| [fixnv 双备损坏导致 modem 起不来](Stability/2024-07-31_Stability_UNISOC_fixnv双备损坏Modem不起.md) | Stability | UNISOC | Stability / NV / Modem | AP MODEM_CTRL / NV / Modem boot | high | summarized | CQWeb SPCSS01379846 | MODEM_CTRL: NV_READ calc_checksum fail，both org and bak partition are damaged |
| [fixnv 损坏怀疑：必须回读主备分区](Stability/2022-04-05_Stability_UNISOC_fixnv损坏IMEI校准丢失_回读证据包.md) | Stability | UNISOC | Stability / NV / Modem | NV / Download tool / Field return | medium | summarized_with_log_gap | CQWeb SPCSS00977064 | IMEI 回到展锐原始值、工模校准参数丢失，但缺少 fixnv 分区回读证据 |
| [RDNV 保存后双卡 Modem 崩溃与 CustNV 差异](Stability/2021-01-12_Stability_UNISOC_RDNV保存后双卡Modem崩溃_CustNV差异.md) | Stability | UNISOC | Stability / NV / Modem | Modem NV / NVTool | high | summarized | CQWeb SPCSS00783213 | sharkl3_pubcp_customer_nvitem.bin 与原始/基线 NV 工程差异过大 |
| [RFIC 读取失败导致 modem 起不来](Stability/2024-01-25_Stability_UNISOC_RFIC读取失败Modem不起.md) | Stability | UNISOC | Stability / NV / Modem | MODEM_CTRL / RF driver / hardware | high | summarized | CQWeb SPCSS01290608 | Modem assert in drv_rf_iram.c when Get RFIC type, g_rfic_type=-1 |
| [UNISOC Modem Blocked现场](Stability/2025-08-01_Stability_UNISOC_ModemBlocked.md) | Stability | UNISOC | Stability / NV / Modem | Modem/HW/AP | low | summarized | internal project summary | 拔卡瞬间 modem 挂住，无后续 modem log 输出 |
| [售后 IMEI 丢失与 WSRCH 校准 NV 损坏](Stability/2024-08-05_Stability_UNISOC_售后IMEI丢失WSRCH校准NV损坏.md) | Stability | UNISOC | Stability / NV / Modem | Modem/RF/NV | medium | summarized | CQWeb SPCSS01379783 | Modem Assert WSRCH Task in drv_rf_nv_comanche_calibration_wcdma_iram.c while read rssi |
| [CF 执行 XCAP 失败后 CSFB：`ss_XcapAuid` 误配](Supplementary-Service/2025-09-09_SS_UNISOC_CF_XCAP_AUID误配导致HTTP400后CSFB.md) | Supplementary-Service | UNISOC | Call / SS / ECC | Modem SS / XCAP / Operator NV | high | summarized | CQWeb index SPCSS01552839 and imported supplementary-service notes | OPERATOR_NV_IMS ims_ss_param ss_XcapAuid 被手动配置为 simserv.ngn.etsi.org |
| [USSD 域选：运营商只支持 CS 时不要强走 IMS/USSI](Supplementary-Service/2024-07-19_SS_UNISOC_USSD域选需按运营商走CS.md) | Supplementary-Service | UNISOC | Call / SS / ECC | Modem SS / IMS USSI / CS CISS | medium | summarized | Imported supplementary-service notes and CQWeb xcap/USSD index | USSD domain selection 配置与运营商支持域不一致 |

## 使用建议

- 按现象先看 `30_Troubleshooting`，再用本索引按平台、第一坏点分类和 source 反查历史 case。
- 如果一个 CQ ID 或 log 结论只出现在配置/流程文档中，没有独立 case，说明它更适合做规则沉淀，不一定需要 case 化。
- 新 case 应补齐 `domain`、`platform`、`layer`、`first_bad_point`、`confidence`、`status`、`search_tier`，否则横向索引和 HTML 搜索价值会下降。

