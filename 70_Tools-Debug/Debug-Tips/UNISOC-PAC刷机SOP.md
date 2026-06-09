---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# UNISOC-PAC刷机SOP

## 适用场景

用于展锐 PAC 包基础刷机。原始资料只给出通用界面步骤，未明确工具版本；现场以项目指定刷机工具和 PAC 包为准。

## 前置检查

- PC 已安装对应平台 USB 驱动。
- PAC 包版本、项目名、分支和测试目的已确认。
- 刷机前已备份需要保留的 NV、IMEI、校准参数或用户数据。
- 电池电量足够，USB 线和接口稳定。

## 操作步骤

1. 启动刷机工具。
2. 如弹窗提示加载最新 PAC 文件，点击 `Yes`。

![](../../attachments/outline/02971ece-af2e-4f89-9d06-f4ebba7b9c31.png)

3. 点击开始 / 播放按钮。

![](../../attachments/outline/323db157-7b12-47b2-95b4-21c0c92c9fad.png)

4. 手机关机。
5. 按住音量下键并连接 USB。

![](../../attachments/outline/9af4eed7-10ad-4005-92bc-d99aa1a8ee6b.png)

6. 等待工具提示刷机完成。

![](../../attachments/outline/77c4f211-ceb8-46bd-a0d9-f7dfead7896d.png)

## 风险边界

- 不确认 NV / 校准参数备份时，不要把刷机作为第一修复动作。
- 版本验证要记录 PAC 文件名、刷机时间、是否保留用户数据、是否刷 modem / vendor / product 分区。
- 刷机后出现 IMEI、校准、入网异常，先回查刷机模式、PAC 内 NV 产物和是否覆盖个体化数据。

## 来源记录

- [Satellite communication debugging](http://192.168.3.94:8888/doc/satellite-communication-debugging-uOoRcFRiag) (`uOoRcFRiag`)
