---
doc_type: triage
domain: Troubleshooting
status: active
quality: curated
search_tier: main_entry
---

# SIM与运营商名排障流程

## 阅读入口

SIM 初始化主流程看 [SIM业务流程](../20_Service-Flows/SIM/SIM业务流程.md)，EF 文件含义看 [SIM-USIM-EF文件速查](../10_Basics/SIM-USIM-EF文件速查.md)，运营商名称配置看 [运营商名称配置方法](../60_Configuration/Business-Config/运营商名称配置方法.md)。

## SIM 不识别

| 顺序 | 判断点 | 关键证据 |
|---:|---|---|
| 1 | 卡槽是否上电 | slot state、ATR、中断、卡座硬件 |
| 2 | 卡应用是否选择成功 | USIM/SIM/ISIM app state、PIN/PUK |
| 3 | 基础 EF 是否读取 | IMSI、ICCID、SPN、PNN/OPL、ECC |
| 4 | AP 状态是否同步 | `UiccController`、`IccCardProxy`、SubscriptionInfo |
| 5 | 是否平台/配置差异 | 双卡单软多硬、eSIM、VSIM、SIMLock |

常见首坏点样例：

| 样例 | 首坏点 | 复用口径 |
|---|---|---|
| [SIM 热插拔无中断](../40_Case-Library/SIM/2024-09-26_SIM_UNISOC_热插拔无中断与NV路径.md) | 插拔时间点 modem 无 SIM interrupt / plug-in 流程 | 优先查热插拔 NV、GPIO/中断触发、硬件 detect，不先查 AP subscription |
| [VSIM 退出后物理卡不显示](../40_Case-Library/SIM/2023-11-21_SIM_UNISOC_VSIM退出后物理卡不显示.md) | `vsim_set_nv` 返回 `CME ERROR` | 先确认 VSIM 退出和 slot mapping 恢复，不按 ATR 硬件问题处理 |
| [No ATR 售后不识卡](../40_Case-Library/SIM/Imported_SIM_17_6601_蓝鸟售后反馈不识卡.md) | 无 ATR，贴纸垫高仍不识卡 | 按卡座/电气波形/卡片交叉补证，未补证前不写最终根因 |
| [VSIM regulator late cleanup 掉卡](../40_Case-Library/SIM/Imported_SIM_18_VINCA_SIM_PIN掉卡问题.md) | kernel time 约 31s 出现 `vsim1/vsim2 disabling` | PIN / Meta / 开机固定时间掉卡先查 regulator user 和 DTS/DWS |
| [卡托 AT 命令导致 modem assert](../40_Case-Library/SIM/Imported_SIM_12_WM58卡托检查代码修改问题_导致Modem_Assert.md) | AP 下发 `AT+ESIMTRAY`，modem 缺少支持宏 | AP 新增 AT 能力前必须确认 modem feature 和宏已合入 |
| [SIM2 NFC UICC 供电掉卡](../40_Case-Library/SIM/Imported_SIM_16_Dahlia_451H_卡二识卡后_会自动掉卡.md) | SIM2 电源/IO/RST/CLK 波形异常 | 卡二特有掉卡优先查 NFC/UICC 共用链路和硬件 BOM |

## 运营商名显示异常

| 判断点 | 先看 |
|---|---|
| 当前注册 PLMN | RPLMN、registered PLMN、漫游状态 |
| SIM 文件 | EFSPN、EFPNN、EFOPL、IMSI MCC/MNC |
| AP 配置 | CarrierConfig、运营商名称 overlay / database |
| 网络下发 | NITZ、EONS、PLMN long/short name |
| 缓存问题 | 飞行模式、换卡、重启 phone 进程后的状态 |

## 结论边界

- 运营商名显示问题不等于注册失败，要先确认注册态和当前 PLMN。
- 手动搜网列表名称和状态栏名称来源可能不同，不能直接互相证明。
- MVNO 名称需要同时看 IMSI/GID/SPN/PNN/OPL 命中条件。
