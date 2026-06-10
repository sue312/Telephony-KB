---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# 70_Tools-Debug

## 使用入口

- 先确认目标：抓 log、解 log、写卡、导入参数、射频/校准、专项验证。
- 操作类内容优先看截图；遇到版本差异时检查工具菜单、依赖环境和输入文件格式。
- 本文图片已转成本地附件；非图片附件仍保留原 Outline 链接作为资料索引。

这里放工具、命令、log 抓取、解码方法、维护脚本。业务结论不放这里，工具只回答“怎么拿证据、怎么看字段”。

## 抓取

| 文档 | 用途 |
|---|---|
| [常用命令](Commands/常用命令.md) | adb、logcat、dumpsys、telephony / phone / ims / carrier_config 状态 |
| [MTK网络通信问题抓Log与提交模板](Log-Capture/MTK-网络通信问题抓Log与提交模板.md) | MTK 注册、IMS/WFC、Data、MMS/CB、Call、RRC、SIM/AT 等问题的 log 包和 eService 描述模板 |
| [MTK-DebugLogger抓LogSOP](Log-Capture/MTK-DebugLogger抓LogSOP.md) | MTK DebugLoggerUI 普通问题和网络问题抓 log 步骤 |
| [UNISOC-Ylog抓LogSOP](Log-Capture/UNISOC-Ylog抓LogSOP.md) | 展锐 Ylog AP / Modem / Connectivity log 抓取步骤 |
| [Kali-WiFi-Sniffer抓包SOP](Log-Capture/Kali-WiFi-Sniffer抓包SOP.md) | Kali + Wireshark 抓 Wi-Fi / Wi-Fi 6E 空口包 |

## 分析

| 文档 | 用途 |
|---|---|
| [Log分析方法](Log-Analysis/Log分析方法.md) | Android AP 侧 log 和 modem trace 通用分析方法 |
| [LTE注册-平台Log速查](Log-Analysis/LTE注册-平台Log速查.md) | LTE 注册平台 log 字段和关键模块 |
| [UNISOC-Logel日志分析SOP](Log-Analysis/UNISOC-Logel日志分析SOP.md) | 展锐 Logel 回放 modem log、搜索、图表、parser 和 full dump |
| [MTK-ELT日志分析SOP](Log-Analysis/MTK-ELT日志分析SOP.md) | MTK ELT 打开 `.muxz` / `.elg`、匹配 EDB、过滤和导出证据 |
| [Qualcomm-QXDM5日志分析SOP](Log-Analysis/Qualcomm-QXDM5日志分析SOP.md) | 高通 QXDM5 打开 HDF/ISF/DLF、加载 QShrink 数据库、筛选 DIAG 证据 |
| [Wireshark-SIP与抓包分析SOP](Log-Analysis/Wireshark-SIP与抓包分析SOP.md) | Wireshark 打开 cap、查看 SIP 和基础抓包分析 |

## 工具

| 文档 | 用途 |
|---|---|
| [SpeechAnalyzer音频日志分析SOP](Tools/SpeechAnalyzer音频日志分析SOP.md) | MTK 通话 VM 音频文件解析和 UL/DL 第一坏点判断 |
| [MTK-META参数导入导出SOP](Tools/MTK-META参数导入导出SOP.md) | MTK META UpdateParameter Tool 参数备份、导出、导入 |
| [UNISOC-NVTool差分NV导入SOP](Tools/UNISOC-NVTool差分NV导入SOP.md) | 展锐 Pandora 进校准模式、NVTool 读取和导入差分 NV |
| [GRSIMWrite白卡工具使用SOP](Tools/GRSIMWrite白卡工具使用SOP.md) | 白卡写卡、MCCMNC / IMSI / SPN / ECC / SIM Lock 场景构造 |

## 专项调试

| 文档 | 用途 |
|---|---|
| [专项调试技巧](Debug-Tips/README.md) | 刷机、锁小区、信号强度、实时 modem log、校准参数、IKE 解密、FCC B40 验证 |

## 维护

| 文档 | 用途 |
|---|---|
| [[知识库维护工具]] | Case 横向索引、配置文档模板化、导入资料治理、Markdown 健康检查脚本和 HTML 同步导出 |

## 目录说明

| 目录 | 用途 |
|---|---|
| `Commands` | adb、dumpsys、shell、logcat |
| `Log-Capture` | 抓 log SOP、复现记录、证据包规范 |
| `Log-Analysis` | AP / modem / 平台 log 字段解释 |
| `Tools` | 专用通信工具使用说明 |
| `Debug-Tips` | 现场调试技巧和专项验证 |
| 根目录脚本 | 知识库维护脚本 |
