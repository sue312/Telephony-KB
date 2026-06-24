---
doc_type: index
domain: Configuration
status: active
quality: curated
search_tier: main_entry
---

# 业务配置方法

## 速查结论

这里放按业务或功能域拆出来的配置方法，适合回答“这个业务怎么配、配置从哪里来、怎么验证是否生效”。

核心配置入口仍保留在上一级：

| 类型 | 入口 |
|---|---|
| 配置总览 | [60_Configuration README](../README.md) |
| APN | [APN配置方法](../Core-Config/APN配置方法_重构.md) |
| CarrierConfig | [CarrierConfig配置方法](../Core-Config/CarrierConfig配置方法_重构.md) |
| ECC | [ECC配置方法](../Core-Config/ECC配置方法_重构.md) |
| NV | [NV参数配置](../Core-Config/NV参数配置.md) |
| IMS / VoWiFi / SBP | [IMS配置方法](../IMS配置方法.md) |

## 业务入口

| 业务/功能 | 配置方法 | 适合回答的问题 |
|---|---|---|
| SMS | [SMS配置方法](SMS配置方法.md) | SMSC、FDN、短码、SMS over IMS、Voicemail |
| 补充业务 | [补充业务配置方法](补充业务配置方法.md) | Call Forwarding、Call Barring、USSD、UT/XCAP |
| SIMLock | [SIMLock配置方法](SIMLock配置方法.md) | 锁网规则、白名单、解锁次数、modem 产物、AP UI 同步 |
| User-Agent | [User-Agent配置方法](User-Agent配置方法.md) | IMS/SIP、MMS、Video Streaming UA |
| 网络制式图标 | [网络制式图标配置方法](网络制式图标配置方法.md) | 4G/5G/NR 图标显示、CarrierConfig、MobileMappings |
| 卫星通信 | [卫星通信配置](卫星通信配置.md) | Satellite Telephony feature flag、区域和能力门控 |
| 小区广播 | [小区广播配置方法](小区广播配置方法.md) | CB/CMAS/ETWS 信道、Mainline 限制、紧急广播过滤 |
| 运营商名称 | [运营商名称配置方法](运营商名称配置方法_重构.md) | EONS、SPN、PNN/OPL、NITZ、手动搜网列表名称 |

## 放置规则

| 内容 | 放置位置 |
|---|---|
| 某个业务/功能怎么配置 | `60_Configuration/Business-Config` |
| APN / ECC / CarrierConfig / NV 等核心配置链路 | `60_Configuration` 根目录 |
| 字段级大表、默认值缓存、映射表 | `60_Configuration/References` |
| 运营商需求原始记录或备份资料 | `60_Configuration/OperatorRecords` |
| 配置导致的真实问题证据链 | `40_Case-Library` |
