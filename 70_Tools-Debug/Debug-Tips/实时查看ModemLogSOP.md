---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# 实时查看ModemLogSOP

## 适用场景

用于 PC 侧实时查看 modem log，适合现场边复现边确认 modem 侧状态、信号、AT 指令和关键 trace。

## UNISOC 手机端设置

1. 拨号输入 `*#*#83781#*#*` 进入 Engineer Mode。

![](../../attachments/outline/e2c6a231-4148-4461-b229-ce547fcd4b87.png)

2. 路径：`DEBUG&LOG -> YLog -> Setting`。
3. 打开 `CP log to pc`。
4. 将 `Log Storage Location` 设置为 `Data`。

![](../../attachments/outline/d286d0cb-b59f-43ab-a566-c4ed1f78ebc8.png)

5. USB 连接手机，路径：`Settings -> Connected devices -> USB`。
6. 打开 `File transfer`。

![](../../attachments/outline/329b90fe-7bae-496a-be3f-57604dd4e15e.png)

## UNISOC Logel 设置

1. 打开 Logel 工具。
2. 按工具界面选择端口、配置并开始实时捕获。

![](../../attachments/outline/5bbc422e-90a2-46e4-a6d3-b3e0dbbad686.png)

![](../../attachments/outline/ef1c323d-f2b3-48cd-81df-57091799e35e.png)

## UNISOC 通过 Logel 测试 AT

1. 打开 Logel 工具。
2. 按工具界面进入 AT 指令测试入口。
3. 输入目标 AT 指令并查看返回。

![](../../attachments/outline/1e81b7b1-e592-433d-8b92-46fdac9ce7df.png)

## MTK 手机端设置

1. 进入 Engineer Mode。
2. 进入 `DebugLoggerUI`。
3. 关闭当前 Log。
4. 点击右上角设置。
5. 选择 `ModemLog`。
6. 将日志模式改为 USB 模式。
7. 重新打开 Log。

![](../../attachments/outline/40515611-4009-4c1b-9a78-df67e121b59a.png)

## MTK ELT 设置

1. 打开 ELT 工具连接手机。

![](../../attachments/outline/73ded2bc-070e-473a-a204-357d02760c00.png)

![](../../attachments/outline/71522b14-dbd9-4722-8f92-e8edd89f3f16.png)

2. 连接后如果显示信息较少，按工具配置打开更多显示项。

![](../../attachments/outline/9c1ab9ec-b606-4d55-82d2-8be4060da49b.png)

![](../../attachments/outline/6a62adcb-5054-4954-9200-6c8dfafe4665.png)

3. 例如可显示信号强度等实时信息。

![](../../attachments/outline/9468c698-b2d3-49e7-b5e4-a2354f33cb4f.png)

## 输出口径

- 记录工具名、版本、端口、开始时间和复现时间点。
- 实时查看不能替代完整 log 包；问题复现后仍需保存并提交完整 AP / modem log。
- 如果使用 USB 输出 modem log，仍要保留端侧 AP log，避免只看到 modem 侧事实。

## 来源记录

- [实时查看modem log](http://192.168.3.94:8888/doc/modem-log-DQ0rwDRU4N) (`DQ0rwDRU4N`)
