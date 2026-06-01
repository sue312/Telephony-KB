---
doc_type: config
domain: Configuration
status: active
quality: imported_reference
feature: User-Agent
layer: AP/IMS/MMS/Media/NV
search_tier: supplemental
---

# User-Agent配置方法

<!-- SUPPLEMENTAL_BOUNDARY_START -->
## 使用边界

- 本页是补充资料或短专题，适合查局部步骤、旧来源和零散技巧。
- 若需要直接定位问题，优先回到对应主流程、配置方法、排障流程或 Case。
- 后续新增结论应沉淀到主文档，本页只保留来源和辅助说明。
<!-- SUPPLEMENTAL_BOUNDARY_END -->


## 阅读入口

这篇记录 IMS / SIP、MMS、Video Streaming User-Agent 客制化入口。修改前必须同时确认配置来源、运行时 log 中最终 UA，以及是否影响多个运营商共用格式。


<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| IMS / SIP UA | IMS profile、CarrierConfig、vendor IMS 配置 | SIP REGISTER/INVITE header |
| MMS UA | MMS CarrierConfig、MmsService 配置 | HTTP UA、MMS send log |
| Video Streaming UA | 浏览器/媒体/运营商 profile | HTTP header、业务抓包 |

### 匹配与生效链路

```text
运营商 UA 需求
-> 对应业务配置源
-> AP/IMS/MMS 模块读取
-> HTTP 或 SIP header 出现在网络侧
```

### 平台差异

| 平台 | 重点看点 | 验证口径 |
|---|---|---|
| Android common | AOSP 公共 XML、Provider、framework 读取点 | 先证明 common 默认值和运行时 dump 是否一致 |
| UNISOC | carrier overlay、CarrierService、Operator NV、modem profile | 同时看 AP log、产物配置、NV/readback 和 modem trace |
| MTK | vendor/mediatek 私有配置、SBP/DSBP/CXP、NVRAM | 结合 debuglogger、ELT/MD log、AP dump 验证最终值 |
| Qualcomm | CarrierConfig overlay、MCFG/QCRIL、modem profile | 结合 dumpsys、QXDM/QCAT、MCFG 产物确认 |

### 验证命令与 log

| 目标 | 证据入口 | 预期结论 |
|---|---|---|
| 源配置存在 | IMS/MMS/HTTP User-Agent 配置和运营商要求 | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | SIP REGISTER、MMS HTTP、streaming request log | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | SIP/HTTP 报文中的最终 UA 字段 | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

### 关联入口

| 入口 | 用途 |
|---|---|
| [配置目录 README](README.md) | 回到配置分类和放置规则 |
| [Case横向索引](../40_Case-Library/Case横向索引.md) | 查历史同类问题和第一坏点 |
| [平台代码入口](../50_Platform-Code/README.md) | 查厂商代码读取位置 |
| [常用命令](../70_Tools-Debug/Commands/常用命令.md) | 查 dumpsys、logcat 和 adb 命令 |

### 常见失败模式

| 现象 | 优先检查 | 第一坏点判断 |
|---|---|---|
| dump 正确但 header 不变 | 业务模块是否读取该字段 | 配置未被消费 |
| 只有某业务 UA 错 | 区分 IMS / MMS / streaming 三套来源 | 不跨业务套用同一配置 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 专题定位

User-Agent 文档主线只回答三件事：目标业务是哪一类 UA、配置从哪里来、最终报文里是否带出了预期字段。

本文是短专题和补充资料，真实业务失败应回到 IMS / MMS / Data / Media 对应流程或 Case。

## 主线速查

| UA 类型 | 优先证据 |
|---|---|
| IMS / SIP UA | SIP REGISTER / INVITE header |
| MMS UA | MMS HTTP request header |
| Video Streaming UA | 媒体业务 HTTP request header |

## 迁入资料

以下内容保留具体代码入口和历史定制写法。

## IMS / SIP UA

UNISOC 参考入口：

```text
alps/vendor/sprd/modules/rild/impl-ril/impl_ril.c
OPERATOR_NV_IMS\ims_ua_name_type\sip_uaNameType\sip_uaNameType[0]
```

常见 SIP UA 组成：

```text
operator name + brand + model + operating system + firmware version + ims version
```

示例：

```text
Telstra TCL T450H Android15 450HDS1L IMS2.0
```

注意事项：

- `sip_uaNameType` 控制 UA 格式类型，不能只改字符串模板。
- 不要随意改公共 `snprintf()` 格式；多个运营商可能共用同一格式。
- 如果必须新增格式，建议新增自定义 type，再通过 NV 按运营商选择。
- IMS UA 属于 IMS/SIP 行为，真实问题 case 应放 `40_Case-Library/IMS` 或 Call/IMS 对应 case。

## MMS UA

AOSP/UNISOC 常见入口：

```text
alps/packages/services/Telephony/src/com/android/phone/PhoneInterfaceManager.java
```

默认 MMS UA 常见格式：

```text
<model>-MMS/2.0
```

客户定制时常见做法是按厂商或项目条件拼接 brand，例如：

```text
TCL T450H-MMS/2.0
```

验证时看 MMS HTTP 请求头，不要只看配置文件。

## Video Streaming UA

常见入口：

```text
alps/frameworks/av/media/module/foundation/FoundationUtils.cpp
```

原生默认值常见为：

```text
stagefright/1.2
```

客户定制可能按 `ro.product.model` 或厂商字段生成 UA，并新增 `x-wap-profile`。验证时以实际 HTTP 请求和媒体业务 log 为准。

## 来源记录

本节只保留来源入口；可复用结论应回填到 IMS / MMS / Data / Media 对应专题或 Case。

- [User Agent配置](http://192.168.3.94:8888/doc/user-agent-MtPEx09ncp) (`MtPEx09ncp`)
