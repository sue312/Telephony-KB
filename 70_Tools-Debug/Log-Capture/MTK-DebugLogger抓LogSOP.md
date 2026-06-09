---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# MTK-DebugLogger抓LogSOP

## 适用场景

用于 MTK 平台通过 Engineer Mode / DebugLoggerUI 抓取普通问题、网络注册问题、数据业务问题的 AP / modem log。

## 通用现场要求

- 手机和 PC 时间对齐，状态栏尽量显示秒。
- 记录复现步骤、SIM、运营商、地点、时间点、DUT/REF 对照信息。
- 网络、注册、数据业务、IMS/WFC 问题尽量从重启或飞行模式开关开始抓，保留完整入网过程。
- 复现后立即停止日志，避免 DebugLogger 循环覆盖第一坏点。

## 前置准备

1. 进入 `Settings -> About phone`，连续点击 `Build number` 5 次，打开开发者选项。
2. 进入 `Settings -> System -> Developer options`，打开 `USB debugging`。
3. USB 连接 PC，手机侧勾选并确认 `Always allow from this computer`。

## 普通问题抓取

1. 电话拨号进入 Engineer Mode，常见入口：
   - `*#*#9646633#*#*`
   - `*#*#3646633#*#*`
   - `*#*#8646633#*#*`
2. 进入 `Log and Debugging -> DebugLoggerUI`。
3. 点击右上角设置，进入后选择 `Enable Tag Log`。
4. 点击开始按钮，开始抓取 log。
5. 复现问题，记录问题发生的准确时间点、操作步骤和现象。
6. 复现后点击停止按钮。
7. 使用配套脚本拉取日志，例如双击 `02_get-trace.bat`。
8. 压缩 PC 侧生成的 log 文件夹，随问题描述一起提交。

## 网络问题增强抓取

网络注册、数据业务、IMS/WFC、弱网类问题需要打开 Telephony log，并尽量覆盖开机注册或重启后的完整入网过程。

1. 完成普通问题抓取的 Engineer Mode / DebugLoggerUI 入口步骤。
2. 进入 `Dynamic Settings -> TelephonyLog`，选择 `Enable` 并确认。
3. 重启设备，让 log 覆盖完整网络注册流程。
4. 启动 DebugLoggerUI 抓 log。
5. 复现问题；如果问题与开机注册、SIM 识别、IMS 注册有关，保留从重启到问题出现的完整时间段。
6. 停止抓取后使用 `02_get-trace.bat` 拉取日志。

## 数据和吞吐量问题

数据不可用、APN、DNS、TCP timeout、吞吐量低等问题，需要同时保留 AP、modem、netlog 和对照信息。

| 项 | 要求 |
| --- | --- |
| modem log | 容量尽量放大，避免复现后循环覆盖 |
| netlog / pcap | 保留 DNS、TCP、HTTP/HTTPS 关键包，packet size 可限制到 128B |
| DUT / REF | 时间对齐，记录 SIM、位置、server、Speedtest 版本 |
| 吞吐量 | 记录每轮 DUT/REF 测试顺序，中途是否交换 SIM 和位置 |
| APN 问题 | 保留 `SETUP_DATA_CALL`、`DataCallResponse`、DNS query、TCP timeout 证据 |

## 提交检查

| 检查项 | 要求 |
| --- | --- |
| 问题时间点 | 提供精确到分钟的发生时间，最好标注复现动作 |
| 复现路径 | 写清楚开机、飞行模式、手动搜网、移动数据开关、通话等入口 |
| Log 完整性 | 确认 AP log、modem log、DebugLogger 目录都在压缩包内 |
| 网络类问题 | 确认已打开 `TelephonyLog`，并覆盖重启后的入网过程 |

## 提交给分析者的最小信息

```text
项目 / 版本 / 平台：
SIM / 运营商 / 国家：
问题现象：
复现步骤：
复现概率：
复现时间点：
日志目录：
对照机 / 对照版本：
是否重启开始抓：
是否包含 AP / modem / netlog / pcap：
```

## 不合格日志

- 没有复现时间点。
- 只给 AP log，没有 modem log，却要求判断 modem/RRC/NAS。
- 网络注册问题不是从重启或飞行模式开始抓，缺少完整注册链路。
- 数据、MMS、HTTP、TCP 问题没有 netlog / pcap / socket 证据。
- DUT/REF 时间不一致，无法对齐。

## 来源记录

- [Catch Log](http://192.168.3.94:8888/doc/catch-log-wOkSR4iPwh) (`wOkSR4iPwh`)
- 原导入图片为飞书临时链接，当前已过期；原始 URL 记录在 `attachments/external/manifest.json`。
