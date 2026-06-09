---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# MTK-META参数导入导出SOP

## 速查结论

MTK META 的 `UpdateParameter Tool` 可用于参数导出、备份和导入。操作重点是：关机连接进入 META MODE，加载当前软件匹配的 BPL DB，读取参数后导出 ini；导入时选择备份 ini 并执行 Write。

## 使用入口

| 项目 | 内容 |
| --- | --- |
| 适用平台 | MTK |
| 适用工具 | META / UpdateParameter Tool |
| 输入 | 当前软件匹配的 BPL DB、待导入的 ini 参数文件 |
| 输出 | 备份 ini 或写入设备的参数 |
| 风险 | DB 与软件版本不匹配会导致读取、解析或写入异常；写入前先备份 |

## 导出流程

1. 安装 META 后，桌面会出现 META 快捷方式，点击运行。

![](../../attachments/outline/b4bba62e-1f0e-4181-bdc6-dbe1a5fb727f.png)

2. 打开 META 后确认主界面正常显示。

![](../../attachments/outline/3f7d08c7-404f-4e6a-8c09-a58b984a7f80.png)

![](../../attachments/outline/f0f78f27-2df3-4857-88dd-af6672e3ba9c.png)

3. 点击界面右下角 `Connect`，设备保持关机状态，通过 USB 连接电脑，等待手机进入 META MODE。

![](../../attachments/outline/4545619a-e5a9-4b86-8a84-bff53bd5a66a.png)

![](../../attachments/outline/72e5f766-43eb-4bc8-80ed-694c2d730804.png)

4. 连接成功后选择左上角 `LOAD DB`，从当前软件版本对应路径选择 BPL 文件。

![](../../attachments/outline/4183ba5c-5e9f-42c9-9f58-2c863d799f0b.png)

5. DB 加载成功后，确认界面进入可操作状态。

![](../../attachments/outline/03a74d33-aed3-4522-a081-073a1e2fd9cb.png)

6. 点击右上角搜索图标，选择 `UpdateParameter Tool`。

![](../../attachments/outline/b9847dae-5db4-452c-8c62-018de49af92c.png)

7. 点击 `Read`，等待进度条到 100%。

![](../../attachments/outline/899b7836-0b1b-4aec-921b-4a9835d61ca2.png)

8. 点击 `Export` 备份参数，选择保存路径，导出 ini 文件。

![](../../attachments/outline/b9ae8a1b-04ed-49c3-b657-e30e59ab8ff3.png)

## 导入流程

1. 按导出流程完成连接、加载 DB、进入 `UpdateParameter Tool`。
2. 选择 `Import`，选择需要导入的 ini 文件。

![](../../attachments/outline/05a812e3-5d79-4a0d-b21a-992eb311b5e2.png)

3. 选择 `Write` 写入设备。

![](../../attachments/outline/c28ac301-eb4a-47c9-b6f9-6a00242adae7.png)

4. 写入完成后断开设备。

![](../../attachments/outline/09b6b744-b0c1-4f30-b04f-41234d1d16e5.png)

## 操作检查

- 写入前先导出备份 ini。
- DB 必须来自当前设备软件匹配版本，临时 DB 要标注来源。
- 记录设备软件版本、META 版本、BPL 文件路径和导入文件名。
- 写入后验证目标业务，不只看工具进度条。

## 来源记录

- [META工具使用](http://192.168.3.94:8888/doc/meta-ETEH4m1Top) (`ETEH4m1Top`)
