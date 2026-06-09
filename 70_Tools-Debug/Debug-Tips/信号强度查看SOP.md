---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# 信号强度查看SOP

## 适用场景

用于快速查看 MTK / UNISOC 平台的 LTE / 3G 信号强度、覆盖质量和基础射频状态。弱网、无服务、驻留失败、吞吐低时优先用于补充现场证据。

## UNISOC / Logel

1. 打开 Logel 工具。
2. 根据网络类型打开对应图表。
3. LTE SIM1 示例路径：`View -> LTE -> LTE Serving Cell Chart of SIM1 / Primary`。

![](../../attachments/outline/20fa75b2-5927-4277-a89e-601e20db22b9.png)

4. 打开 log 后，信号强度会加载到图表窗口。

![](../../attachments/outline/21da621b-4fc0-4414-abb3-8da42edfe8b0.png)

## MTK / EMMA

1. 打开 LTE 工具。
2. 打开目标 log。
3. 进入 `EM -> EMMA`。

![](../../attachments/outline/bca3b686-a625-48c1-a3b0-38f07365252c.png)

4. 在浏览器中打开 EMMA 页面。

![](../../attachments/outline/c62d1bc8-9fe2-461f-a74c-3cb1be694bfc.png)

5. 选择要查看的模块，点击 `Add App`。
6. 例如查看 3G 信号强度，可加载 `UMTS UTAS Main RSRP`。

![](../../attachments/outline/07059ebc-7ea3-44d3-9151-8f139b5f638d.png)

## 输出口径

| 信息 | 要求 |
| --- | --- |
| 时间点 | 标出问题发生前后信号变化 |
| 制式 | LTE / NR / UMTS / GSM |
| 小区 | PCI / EARFCN / band / cell id |
| 信号 | RSRP / RSRQ / SINR / RSSI 等 |
| 对比 | DUT / REF 同位置同 SIM 或交换 SIM 后对比 |

## 关联入口

- [UNISOC-Logel工具使用SOP](../Log-Analysis/UNISOC-Logel工具使用SOP.md)
- [无线信号与搜网失败排查](../../30_Troubleshooting/无线信号与搜网失败排查.md)

## 来源记录

- [查看信号强度](http://192.168.3.94:8888/doc/5pl55yl5lh5y35by65bqm-JM11tjGSsg) (`JM11tjGSsg`)
