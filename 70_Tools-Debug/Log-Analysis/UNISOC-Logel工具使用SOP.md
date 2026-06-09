---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# UNISOC-Logel工具使用SOP

## 适用场景

用于展锐 / UNISOC modem log 回放、关键字搜索、场景搜索、DSP log 搜索、信号图表查看，以及 modem blocked / assert 后的 full dump 抓取。

## 工具定位

Logel 是展锐实时诊断和 modem log 分析工具，支持消息过滤、实时抓取、离线回放、场景化搜索和图表展示。

官方资料入口：<https://unisupport.unisoc.com/file/index.do?fileid=32409>

本地附件：[Logel User Guide.pdf](../../attachments/outline/files/f5686886-47ec-43e7-8aee-18b3769af4ce_Logel User Guide.pdf)

![](../../attachments/outline/7696b380-f8ba-4dc8-96cd-08395825d8e1.png)

![](../../attachments/outline/20dfca97-be27-4c05-a3dc-189f2d9d69f5.png)

## 回放 modem log

回放前先确认 log 是否覆盖完整开机流程。网络、IMS、注册类问题建议保留从开机或飞行模式恢复开始的完整时间段。

AP 侧可辅助确认关键服务是否启动：

```text
ImsApp: ImsApp Boot Successfully. version:12
ImsApp: ImsService Boot Successfully!
UniTelephonyApp: Boot Successfully!
```

1. 点击左上角 `Open log file to replay`。
2. 在弹出的 log 选择框中选择目标 log 文件。
3. 点击打开，等待 Logel 完成回放解析。

![](../../attachments/outline/8ce06dbc-4eb6-49ef-a4ac-76ce85a45e9d.png)

![](../../attachments/outline/d548d0ca-ceb5-4a0a-a95b-b1c22b17e800.png)

![](../../attachments/outline/083da041-c1cb-467d-bc17-ca402e0a199b.png)

## Arm log 搜索

1. 点击工具栏左上角 `Find`。
2. 输入要检索的消息名或关键字。
3. 选择搜索窗口和搜索列。
4. 可通过颜色块给不同关键字设置颜色，便于区分流程阶段。
5. 点击 `Find` 查看结果。

![](../../attachments/outline/e41c93bd-9377-45f8-84a5-a0c05b87ac22.png)

![](../../attachments/outline/1a462ae3-578d-4a1c-8a41-6e6158591847.png)

## LTE 注册常用消息

无存储信息的 PLMN 和小区选择：

| 消息名称 | 描述 |
| --- | --- |
| `MSG_ID_CMD_RLM_SELECT_CELL` | NAS / ASM 请求 LRRC 开始 PLMN 和小区选择 |
| `MSG_ID_LTE_CPHY_BAND_SWEEP_REQ` | LRRC 请求 PHY 检测并同步所有支持频段上的小区 |
| `MSG_ID_LTE_CPHY_SUCC_SYNC_CELLS_IND` | PHY 上报 LRRC 小区检测和同步结果 |
| `MSG_ID_LTE_CPHY_IDLE_CONFIG_REQ` | LRRC 请求 PHY 驻留在当前小区 |
| `MSG_ID_LTEAS_NAS_UPDATE_INFO_IND` | LRRC 上报 NAS 当前驻留小区的接入信息 |
| `MSG_ID_LAS_CELL_SELECT_CNF` | LRRC 上报 NAS PLMN 和小区选择结果 |

PLMN 搜索：

| 消息名称 | 描述 |
| --- | --- |
| `MSG_ID_CMD_RLM_SEARCH_REQUEST` | NAS / ASM 请求开始 PLMN 搜索 |
| `MSG_ID_LTEAS_PLMN_LIST_IN_IND` | LRRC 指示 NAS 检测到的小区 PLMN 信息 |
| `MSG_ID_LTEAS_PLMN_LIST_SEARCH_CNF` | LRRC 指示 NAS PLMN 搜索流程结束 |

## 场景化搜索

菜单路径：`Edit -> Scene Search`。

Scene Search 内置部分业务场景，支持新增、修改、删除场景。`type` 可选择 `MSG`、`AIR`、`TRACE`。

![](../../attachments/outline/354b0724-492e-49eb-bf90-a90cac5a9186.png)

## DSP log 搜索

1. 点击工具栏右上角 `LTE`、`TG` 搜索按钮。
2. 对有独立 AG-DSP 模块的芯片，可点击 `AG` 搜索按钮。
3. 输入 DSP Address，点击 `Add`。
4. 通过 `Addr` 后的颜色块设置颜色。
5. 点击 `Start` 开始搜索。

![](../../attachments/outline/8375a06a-67e5-44e3-88da-43a7b7a7b738.png)

![](../../attachments/outline/5ab1e975-b2a8-432c-8325-b60c5c56b349.png)

![](../../attachments/outline/32ed063e-ae64-4120-8dc8-2bcae2d82a72.png)

## 图表功能

菜单路径：`View`，可打开对应图表，例如 `LTE Serving Cell Chart of SIM1 / Primary`。

| 指标 | 含义 | 判断 |
| --- | --- | --- |
| SINR | 信号与干扰加噪声比 | 数值越大，链路质量越好 |
| RSRQ | 参考信号接收质量，反映信噪比和干扰水平 | 取值范围约 `-3` 到 `-19.5`，值越大越好 |
| RSRP | 参考信号接收功率，反映路径损耗和覆盖 | 取值范围约 `-44` 到 `-140 dBm`，值越大越好 |

![](../../attachments/outline/852615f6-ab7a-4dfc-b1f2-414fed5b41a9.png)

## full dump 抓取

modem blocked / assert 问题通常需要提供 full dump。

1. 确认 `Sysdump Enable` 已打开。
   - 路径：`Ylog -> 调试 -> Sysdump Enable`
   - `ud` 软件通常默认打开，`user` 软件需要手动打开。
2. 在 system info dumping 场景完成后，同时按住音量上键和音量下键，再双击电源键。
3. 黑屏进入 dump 界面后，打开 modem Logel 工具。
4. 手机插入 USB。
5. 点击 `Capture log` 开始捕获 dump。
6. 等待 `finish` 提示。
7. 到 Logel 工具 `bin\history` 目录下找到 full dump，将整个 `armlog` 文件夹打包提交。

![](../../attachments/outline/a9de6c7c-9efc-4b05-8384-5790ea3321c6.png)

![](../../attachments/outline/507b8668-7e09-4d6d-9970-46279608ca49.png)

![](../../attachments/outline/eb49c225-4e45-4b8e-9a09-71942ea91457.png)

## 注意事项

- 展锐默认使用 Ylog 抓取；若选择 PC 方式输出 modem log，问题后仍需同时导出 Ylog AP log 和 PC 端 modem log。
- `Modem Reset` 在 user 工程上通常默认开启，必要时按版本路径关闭：
  - Android 8.1 到 11：`YLog -> Settings -> LogSetting -> ModemLogSetting`
  - Android 12 到 14：`YLog -> 更多选项 -> 调试`
- 通过 `Log Lost Statistics` 查看 log 丢失率；丢失率小于等于 5% 通常可接受。

## 来源记录

- [Logel工具使用](http://192.168.3.94:8888/doc/logel-9PX7Jl2Ddm) (`9PX7Jl2Ddm`)
- 本地附件：[Logel User Guide.pdf](../../attachments/outline/files/f5686886-47ec-43e7-8aee-18b3769af4ce_Logel User Guide.pdf)
