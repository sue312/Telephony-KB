---
doc_type: index
domain: Configuration
status: active
quality: curated
search_tier: main_entry
---

# Core-Config

## 速查结论

这里放高频核心配置方法：APN、CarrierConfig、ECC、NV。业务配置方法放在 `Business-Config`，字段级映射和资料索引放在 `References`。

## 使用入口

| 文档 | 用途 |
| --- | --- |
| [APN配置方法](APN配置方法_重构.md) | APN 配置字段、MTK / UNISOC / Qualcomm 路径和生效验证 |
| [CarrierConfig配置方法](CarrierConfig配置方法_重构.md) | CarrierConfig / CarrierSettings 配置、匹配、生效和运行时 dump |
| [ECC配置方法](ECC配置方法_重构.md) | 有卡 / 无卡紧急号码、EF_ECC、EmergencyNumberTracker 和厂商 ECC 数据 |
| [NV参数配置](NV参数配置.md) | NV 参数配置、NVTool、展锐 NV 参数、版本、生效、回退和验证清单 |

## 放置边界

| 内容 | 放置位置 |
| --- | --- |
| APN / CarrierConfig / ECC / NV 配置方法 | `60_Configuration/Core-Config` |
| 运营商名称、SMS、SIMLock、User-Agent、网络制式图标等业务配置 | `60_Configuration/Business-Config` |
| CarrierConfig key、Modem NV 字段级映射 | `60_Configuration/References` |
| 配置引发的历史问题证据链 | `40_Case-Library` |
