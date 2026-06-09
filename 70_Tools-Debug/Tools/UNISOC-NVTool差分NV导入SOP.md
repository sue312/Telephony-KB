---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# UNISOC-NVTool差分NV导入SOP

## 速查结论

展锐差分 NV 导入流程分两段：先用 Pandora 让关机设备进入校准模式并读取端口，再用 NVTool 打开 RD NV 工程、从手机读取 NV、导入差分 NV、保存到手机。

## 使用入口

| 项目 | 内容 |
| --- | --- |
| 适用平台 | UNISOC / 展锐 |
| 适用工具 | Pandora、NVTool |
| 输入 | RD NV 工程 `rd_nvitem.xprj`、差分 NV 文件 |
| 输出 | 写入设备的差分 NV |
| 高风险点 | fixnv、IMEI、RF 校准参数、AP/CP 版本匹配 |

涉及 fixnv、fastboot、OTA nvmerge 或现场机个体化 NV 时，不在本 SOP 展开；回到 [NV参数配置](../../60_Configuration/Core-Config/NV参数配置.md) 和相关稳定性案例确认风险边界。

## 连接 Pandora 并读取端口

1. 将手机关机。
2. 打开 Pandora 工具，点击 `connect`。

![](../../attachments/outline/7e23464e-b6d5-4e11-957d-07ba988bbbfa.png)

3. 样机通过 USB 连接 PC。
4. 等待 Pandora 右侧窗口提示 `Entermode success`，记录上一行端口信息，例如 `Port134 plug in`。

![](../../attachments/outline/09b3a73a-1cb3-4fb1-833f-f90d40c38e8c.png)

5. 点击 `disconnect` 断开 Pandora。

![](../../attachments/outline/e7ef67e9-2d91-4696-a716-2a6d6a85f2d1.png)

## NVTool 读取 NV

1. 打开 NVTool，选择 `File -> Open Project`，加载基础 RD NV 工程。

![](../../attachments/outline/185f698a-294e-47a7-a933-6879caa8b434.png)

2. 选择类似 `Legend_A14_modem_20251203\RDNV\rd_nvitem.xprj` 的工程文件。

![](../../attachments/outline/3f6171f0-401c-49cb-9ec8-ad288cd43548.png)

3. 等待工程加载完成。

![](../../attachments/outline/e22124fa-c92c-4e1e-9d71-e5032b5efe61.png)

4. 选择 `File -> Port setting`，选择 Pandora 中记录的端口。

![](../../attachments/outline/00fcd28f-514a-4653-bf7a-b0e45c1e6638.png)

![](../../attachments/outline/200c67bb-7029-480f-8789-ead5fbcc717b.png)

5. 选择 `File -> Load from Phone（running）` 或按 `F7`，从样机读取 NV。

![](../../attachments/outline/36b74416-6edc-4766-93f6-552b62f46794.png)

6. 等待进度条加载完成，点击确认。

![](../../attachments/outline/a004ed7e-7906-4972-aec6-9b905f5cb00a.png)

![](../../attachments/outline/141b9930-8d04-48f8-b585-7c0be8c43026.png)

## 导入差分 NV

1. 选择 `Facility -> Import`。

![](../../attachments/outline/2fae577a-ee2f-4155-b639-ce98640ae368.png)

2. 选择目标差分 NV 文件，例如 `LTE B4 66降1dB.nv`。

![](../../attachments/outline/48171e52-9ed0-4e6f-b5e2-fdf677646f00.png)

3. 导入完成后，选择 `File -> Save To Phone(Normal Mode)`。

![](../../attachments/outline/63f16b44-9739-4b29-95ff-ddae0ba31d68.png)

4. 等待进度条完成。

![](../../attachments/outline/0ea63259-9742-413a-8406-f5132caf6b04.png)

5. 点击确认，完成差分 NV 导入。

![](../../attachments/outline/ad5fc650-f41d-4a18-b28c-a6be007717bd.png)

6. 读取或修改 NV 后退出 NVTool 时选择“否”。

![](../../attachments/outline/14018a07-ebd5-4a1d-b8fe-aeaeabaf0b75.png)

## 操作检查

- 导入差分 NV 前先从手机读取并保存当前 NV 状态。
- 记录 Pandora 端口、NVTool 版本、RD NV 工程路径、差分 NV 文件名。
- 写入后验证目标频段、射频参数、SIM 识别、IMEI、紧急呼叫等依赖 NV 的业务。
- 现场机、售后机、量产机不要直接按研发样机流程刷 fixnv。

## 来源记录

- [射频参数导入与导出](http://192.168.3.94:8888/doc/5bce6akr5yc5pww5a85ywl5lio5a85ye6-GUyV8waR5H) (`GUyV8waR5H`)
