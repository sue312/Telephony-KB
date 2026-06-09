---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# UNISOC-Ylog抓LogSOP

## 适用场景

用于展锐 / UNISOC 平台通过 Engineer Mode 的 Ylog 抓取 AP、Modem、Connectivity 和其他系统日志。

## 通用现场要求

- 手机和 PC 时间对齐，状态栏尽量显示秒。
- 记录复现步骤、SIM、运营商、地点、时间点、DUT/REF 对照信息。
- 网络、注册、数据业务、IMS/WFC 问题尽量从重启或飞行模式开关开始抓，保留完整入网过程。
- 复现后立即停止日志，避免 Ylog 循环覆盖第一坏点。

## 前置准备

1. 进入 `Settings -> About phone`，连续点击 `Build number` 5 次，打开开发者选项。
2. 进入 `Settings -> System -> Developer options`，打开 `USB debugging`。
3. USB 连接 PC，手机侧勾选并确认 `Always allow from this computer`。

## Ylog 抓取流程

1. 电话拨号进入 Engineer Mode，常见入口：
   - `*#*#9646633#*#*`
   - `*#*#83781#*#*`
   - `*#*#8646633#*#*`
2. 切换到 `DEBUG&LOG` 页签，进入 `Ylog`。
3. 点击右上角设置，选择 `Clear` 清理历史 log，确认出现 `Clear log successfully`。
4. 进入 Ylog `Settings`。
5. 在 `Ap Logs Settings`、`Modem Logs Settings`、`Connectivity Log Settings` 中关闭 `Log Cycle Cover`，避免循环覆盖关键时间段。
6. 回到 Ylog 设置，进入 `Custom`，勾选需要的子项；常规排查建议勾选全部子项。
7. 在 `Template settings` 中选择 `Normal`。
8. 启动 Ylog，确认顶部 AP / Modem / Connectivity / Others 等 log tag 信息不为空。
9. 开始复现问题，记录问题发生时间点和操作路径。
10. 复现完成后停止抓取。
11. 使用配套脚本拉取日志，例如双击 `02_get-trace.bat`。
12. 压缩 PC 侧生成的 log 文件夹，随问题描述一起提交。

## 网络问题注意事项

- 注册、搜网、数据业务、IMS/WFC 问题，建议重启设备后抓取完整入网流程。
- 如果顶部 AP / Modem / Connectivity / Others 任一信息为空，先回头检查模板、Custom 子项和 log tag 设置。
- 长时间复现问题时要确认 `Log Cycle Cover` 已关闭，否则第一坏点可能被覆盖。

## 常见日志类型

| 日志 | 用途 |
| --- | --- |
| Ylog AP | framework、RIL、AP 侧状态同步 |
| Ylog modem / armlog | NAS/RRC/SIM/IMS/modem trace |
| Logel systemdump | modem blocked / assert 现场 |
| memdump / ETB | 平台要求时用于底层定位 |
| netlog / pcap | DNS、TCP、HTTP/HTTPS、数据业务链路 |

## 数据和吞吐量问题

数据不可用、APN、DNS、TCP timeout、吞吐量低等问题，需要同时保留 AP、modem、netlog 和对照信息。

| 项 | 要求 |
| --- | --- |
| modem log | 容量尽量放大，避免复现后循环覆盖 |
| netlog / pcap | 保留 DNS、TCP、HTTP/HTTPS 关键包，packet size 可限制到 128B |
| DUT / REF | 时间对齐，记录 SIM、位置、server、Speedtest 版本 |
| 吞吐量 | 记录每轮 DUT/REF 测试顺序，中途是否交换 SIM 和位置 |
| APN 问题 | 保留数据拨号、DNS query、TCP timeout 证据 |

## 提交检查

| 检查项 | 要求 |
| --- | --- |
| Ylog 标签 | AP / Modem / Connectivity / Others 信息不为空 |
| 覆盖范围 | 网络类问题覆盖重启到问题出现的完整过程 |
| 覆盖策略 | `Log Cycle Cover` 已关闭 |
| 证据说明 | 附问题时间点、操作路径、SIM/运营商、网络制式和是否可复现 |

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
是否包含 AP / modem / connectivity / dump：
```

## 不合格日志

- 没有复现时间点。
- 只给 AP log，没有 modem log，却要求判断 modem/RRC/NAS。
- 网络注册问题不是从重启或飞行模式开始抓，缺少完整注册链路。
- modem blocked / assert 只有 AP 表现，没有 systemdump / memdump。
- 数据、MMS、HTTP、TCP 问题没有 netlog / pcap / socket 证据。
- DUT/REF 时间不一致，无法对齐。

## 来源记录

- [Catch Log](http://192.168.3.94:8888/doc/catch-log-wOkSR4iPwh) (`wOkSR4iPwh`)
- 原导入图片为飞书临时链接，当前已过期；原始 URL 记录在 `attachments/external/manifest.json`。
