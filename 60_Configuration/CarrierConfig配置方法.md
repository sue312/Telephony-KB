---
doc_type: config
domain: Configuration
status: active
quality: imported_reference
---

# CarrierConfig配置方法

## 速查结论

- 配置问题先确认落点：AOSP 公共配置、厂商私有配置、MCC/MNC 运营商配置、SIM/卡槽维度、NV/系统属性/CarrierConfig。
- 定位时必须同时保留三类证据：配置文件、运行时 dump、log 中最终生效值。
- 本文图片已转成本地附件；非图片附件仍保留原 Outline 链接作为资料索引。

CarrierConfig / CarrierSettings 配置和架构资料。

> 图片已保存为本地附件；非图片附件仍保留原 Outline 链接作为资料索引。

参数映射入口：[[CarrierConfig参数映射]]

相关流程：[[UNISOC-CarrierService启动与CarrierConfig加载流程]]


<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| AOSP 默认配置 | `packages/apps/CarrierConfig` 默认 XML | `dumpsys carrier_config` 默认值 |
| 厂商 / 项目 overlay | `vendor/*/overlays/packages/apps/CarrierConfig` | 产物中 XML、overlay 是否打入 |
| CarrierService | `CarrierConfigLoader` 绑定默认包或 carrier app | `CarrierConfigLoader` log、bind/fetch 结果 |
| 临时 override | `overrideConfig()`、测试命令 | `dumpsys carrier_config` 是否出现 override 值 |

### 匹配与生效链路

```text
SIM / carrier id / MCCMNC / GID / SPN
-> CarrierConfigLoader.updateConfigForPhoneId
-> bindToConfigPackage / CarrierService.onLoadConfig
-> PersistableBundle 合并
-> Telephony / Data / IMS / UI 模块读取
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
| 源配置存在 | CarrierConfig XML / overlay / CarrierService | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | dumpsys carrier_config、CarrierConfigLoader log | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | 读取方业务 log，必要时结合 IMS/Data/Call trace | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

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
| XML 已改但 dump 不变 | overlay 是否进产物、carrier id 是否命中、是否被 override 覆盖 | 源配置未进入运行时 bundle |
| dump 正确但业务不变 | 消费方是否读取该 key，是否还有厂商私有开关 | 第一坏点在读取链路或私有配置优先级 |
| 换卡后仍旧值 | SIM 状态触发、缓存、subId/phoneId 映射 | 配置刷新或卡槽映射问题 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 专题定位

CarrierConfig / CarrierSettings 只回答一件事: 某个 key 如何被匹配、覆盖并最终生效。

本文不再承载完整需求搬运或长篇平台说明。参数含义、默认值和平台覆盖情况统一看 [CarrierConfig参数映射](CarrierConfig参数映射.md)，原始资料入口看 [运营商应答资料索引](运营商应答资料索引.md)。

## 配置来源与优先级

| 来源 | 常见落点 | 说明 |
|---|---|---|
| AOSP 默认配置 | `packages/apps/CarrierConfig` 或平台默认 XML | 提供基线默认值 |
| 运营商覆盖 | `carrier_config_carrierid_*.xml` / `carrier_config_mccmnc_*.xml` | 按 Carrier ID、MCC/MNC 命中 |
| 厂商覆盖 | `vendor.xml` / `vendor_ex.xml` / 项目 overlay | 后加载者覆盖同名 key |
| CarrierService 动态加载 | `CarrierConfigLoader` / `DefaultCarrierConfigService` | 以运行时 bundle 为准 |

### 常见目录

| 平台 | 常见目录 |
|---|---|
| MTK | `vendor/mediatek/proprietary/packages/apps/CarrierConfig/assets`、`.../res/xml` |
| UNISOC | `vendor/sprd/platform/packages/apps/CarrierConfig/assets`、`.../res/xml` |

## 匹配与生效链路

```text
SIM / carrier id / MCCMNC / GID / SPN / IMSI
-> CarrierConfigLoader / DefaultCarrierConfigService
-> 选择 carrierid 或 mccmnc 配置
-> 合并 vendor / vendor_ex / overlay
-> framework / IMS / Data / UI 读取
-> dumpsys carrier_config 验证
```

## 配置写法

```xml
<carrier_config>
  <boolean name="carrier_wfc_ims_available_bool" value="true"/>
  <int name="carrier_default_wfc_ims_mode_int" value="1"/>
  <string name="key_oem_pref_network_mode">1,0,0,1,1,1</string>
</carrier_config>
```

同一 key 的目标值如果与当前分支默认值一致，通常不写入运营商 XML，避免无意义覆盖。

## `key_oem_pref_network_mode`

这个 key 不只是控制 Settings 里可见的网络模式。部分项目会在插卡或 CarrierConfig 更新后触发 `updateOemAllowedNetworkMode()`，再调用 `setPreferredNetworkType()`，最终影响 modem workmode 和 UE Capability 上报。

典型链路：

```text
key_oem_pref_network_mode
-> updateOemAllowedNetworkMode()
-> setPreferredNetworkType()
-> modem workmode
-> UECapabilityInformation
```

遇到“UI 看起来对了，但空口能力不对”的问题，要同时查 CarrierConfig、AP 日志和 modem trace。

## 新建配置文件

- MTK: 优先用 MCF Tool 生成，再按项目目录补充。
- UNISOC: 参考同类运营商文件命名和结构，新建 XML 后按 carrier id / mccmnc 放入对应目录。

## 验证方式

1. 确认 key 存在于目标分支 `CarrierConfigManager.java`。
2. 确认 SIM 的 MCC/MNC、Carrier ID、GID、SPN、IMSI 命中预期配置。
3. 查看 `adb shell dumpsys carrier_config`。
4. 对照 Telephony / IMS / Data 日志确认消费方已读取。
5. 必要时回看 [CarrierConfig参数映射](CarrierConfig参数映射.md) 的平台覆盖和默认值。

## 历史问题速查

| 场景 | 关键配置/代码 | 排查点 |
|---|---|---|
| 手动选网成功后是否回自动模式 | `oem_key_restore_auto_mode` | `false` 保持手动；`true` 成功后返回自动模式 |
| 手动选网失败后是否回自动模式 | `oem_key_permanent_auto_sel_mode_bool` | `true` 失败后返回自动模式；`false` 失败后保持手动 |
| 手动选网失败弹框 | `mShowNetworkSelectionFailed` | 可能拦截自动回网分支，需结合 `NetworkSelectSettings.java` 验证 |
| APN type 不显示 | `KEY_HIDE_APN_TYPE_STRING_ARRAY` | APN XML 已写入也可能被隐藏列表过滤 |
| MMS 大小限制 | `KEY_MMS_MAX_MESSAGE_SIZE_INT` | 优先按 MCC/MNC 在 CarrierConfig 覆盖，不建议改全局默认值 |

相关案例：

- [[../40_Case-Library/Registration/2024-06-24_Registration_UNISOC_手动选网CarrierConfig策略]]
- [[../40_Case-Library/Data/2022-10-31_Data_UNISOC_APN_XCAP类型被隐藏]]
- [[../40_Case-Library/Data/2024-11-13_Data_UNISOC_MMS大小限制CarrierConfig]]

## 资料索引

| 资料 | 用途 |
|---|---|
| [CC键值对逻辑整理](http://192.168.3.94:8888/doc/cc-wzlRpYy4TR) | 旧逻辑整理入口，结论需要回填到参数映射或案例 |
| [CarrierConfig参数映射](CarrierConfig参数映射.md) | key、默认值、平台覆盖和分组索引 |
| [UNISOC-CarrierService启动与CarrierConfig加载流程](UNISOC-CarrierService启动与CarrierConfig加载流程.md) | UNISOC 加载链路和日志断点 |

## 来源记录

本节只保留来源入口；可复用结论应回填到参数映射、资料索引或 Case。

- [CarrierConfig配置](http://192.168.3.94:8888/doc/carrierconfig-Q1I6HioHAA) (`Q1I6HioHAA`)
- [CarrierConfig架构](http://192.168.3.94:8888/doc/carrierconfig-O1eCwlVdF9) (`O1eCwlVdF9`)
- [CarrierSettings的配置](http://192.168.3.94:8888/doc/carriersettings-RD3NZCYel6) (`RD3NZCYel6`)
- [CC键值对逻辑整理](http://192.168.3.94:8888/doc/cc-wzlRpYy4TR) (`wzlRpYy4TR`)
