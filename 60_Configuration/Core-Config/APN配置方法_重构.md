---
doc_type: config
domain: Configuration
status: draft
quality: curated
search_tier: main_entry
---

# APN配置方法_重构

## 使用入口

这篇用于回答 APN 怎么配、怎么匹配 SIM、怎么入库、怎么下发到 modem、失败时怎么补证据。

当前版本先固化已验证的 UNISOC / SPRDROID16、MTK / MP6、Qualcomm / S1E4ProPlus APN 主路径；MTK RIL 侧 `vendor-apns-conf.xml` 仅作为 emergency / ePDG APN 补充入口记录，不等同于普通 APN 日常配置入口。

## 速查结论

- UNISOC SPRDROID16 / Android T 及之后，日常 APN 只改 `vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml`。
- 编译时 `apns-conf_8_v3.xml` 会复制成设备侧 `/product/etc/apns-conf.xml` 和 `/product/etc/old-apns-conf.xml`。
- MTK MP6 日常 APN 主入口是 `device/mediatek/config/apns-conf.xml`，当前分支编译到设备侧 `/system/etc/apns-conf.xml`。
- Qualcomm S1E4ProPlus 当前是 QSSI / target 分裂构建；APN 主入口优先看 `qssi/vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml`，编译到 `/product/etc/apns-conf.xml`。
- `target/device/generic/goldfish/data/etc/apns-conf.xml` 是 goldfish / emulator 文件，会被 generic goldfish 规则复制到 `/data/misc/apns/apns-conf.xml`，不是 S1E4ProPlus 真实设备的日常 APN 主入口。
- 运行时 `TelephonyProvider` 读取 APN XML 后写入 `telephony.db` 的 `carriers` 表；业务侧不直接读源码 XML。
- APN 匹配以 `mcc/mnc` 为主；虚拟运营商用 `mvno_type` + `mvno_match_data` 区分。命中 MVNO APN 时优先使用 MVNO APN，未命中才回退普通 MCC/MNC APN。
- 展锐 APN 日常配置不使用 `carrier_id` 作为区分入口，即使 Android common 代码支持该字段；MTK 主 APN XML 当前也未见 `carrier_id` 配置；Qualcomm 主 APN XML 可解析且已有少量 `carrier_id`，但日常仍先按目标 MCC/MNC / MVNO 条件确认入口。
- 运营商需求如果写 `network_type_bitmask`，在 UNISOC / MTK / Qualcomm 主 APN XML 中优先按 `bearer_bitmask` 配置；入库时会同步转换成 `network_type_bitmask`。
- MTK 另有 `/vendor/etc/vendor-apns-conf.xml` 被 RIL 读取，用于补 emergency APN 或给已有 APN 增加 emergency type，普通 default / ims / mms / xcap APN 不优先走这个入口。
- MTK legacy RILD / 旧 HAL 场景可能把 DataProfile 数量限制到 16 条，新增大量非 default APN 时要额外确认是否被裁剪。
- Qualcomm `QtiDataProfileManager` 可能按 CarrierConfig 的 `KEY_MULTI_APN_ARRAY_FOR_SAME_GID` 对同 GID 的多 APN 做 radio capability 过滤。
- APN 结论必须同时看三类证据：源 XML、运行时数据库 / dump、AP 下发和 modem 协议侧实际使用值。

## UNISOC配置入口

### 源码路径

```text
/home/wx/Project/Common/SPRDROID16_SYS_MAIN_W25.22.4/alps/vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml
```

相对 Android 源码根目录：

```text
vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml
```

同目录可能还有：

```text
vendor/sprd/telephony-res/apn/apns-conf_8.xml
vendor/sprd/telephony-res/apn/apns-conf_8_v2.xml
vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml
```

当前维护口径：SPRDROID16 只改 `apns-conf_8_v3.xml`，不要同步改 `v2` 或无后缀版本，除非目标分支或项目构建规则另有要求。

### 编译复制路径

构建规则位于：

```text
device/sprd/sys_mpool/module/product/telephony/uni_tele_res_product.mk
```

关键链路：

```text
APN_VERSION <- frameworks/base/core/res/res/xml/apns.xml
apn_src_file_v3 = vendor/sprd/telephony-res/apn/apns-conf_$(APN_VERSION)_v3.xml
apn_src_file_v3 -> product/etc/apns-conf.xml
apn_src_file_v3 -> product/etc/old-apns-conf.xml
```

所以修改源码 XML 后，设备侧验证重点不是源码路径，而是产物里的：

```text
/product/etc/apns-conf.xml
/product/etc/old-apns-conf.xml
```

### 运行时读取优先级

`TelephonyProvider` 的 `getApnConfFile()` 会选择实际读取的 APN 文件，优先级是：

```text
/data/misc/apns/apns-conf.xml
> /product/etc/apns-conf.xml
> /oem/telephony/apns-conf.xml
> /system/etc/apns-conf.xml
```

如果设备上存在 `/data/misc/apns/apns-conf.xml`，它会覆盖产品内置 APN。排查“源码已改但设备不生效”时，必须先确认是否有 data 侧覆盖文件。

## MTK配置入口

### 源码路径

当前 MTK MP6 分支的 APN 主配置文件：

```text
/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/device/mediatek/config/apns-conf.xml
```

相对 Android 源码根目录：

```text
device/mediatek/config/apns-conf.xml
```

当前文件根节点为：

```xml
<apns version="8">
    ...
</apns>
```

当前分支主 APN XML 中常见字段包括 `carrier`、`mcc`、`mnc`、`apn`、`type`、`protocol`、`roaming_protocol`、`bearer_bitmask`、`mvno_type`、`mvno_match_data`、`user_visible`、`user_editable`、`mtu` 等；未见 `carrier_id` 和 `network_type_bitmask` 作为主 APN 日常配置字段。

### 编译复制路径

MTK 构建规则中，主 APN XML 会复制到：

```text
device/mediatek/config/apns-conf.xml
-> /system/etc/apns-conf.xml
```

已确认的构建规则入口包括：

```text
device/mediatek/system/common/device.mk
device/mediatek/common/device.mk
```

所以 MTK 日常修改源码后，设备侧主验证点是：

```text
/system/etc/apns-conf.xml
```

### 运行时读取优先级

MTK `TelephonyProvider` 使用的路径常量和读取逻辑与 Android APN provider 主链路一致：

```text
PARTNER_APNS_PATH     = etc/apns-conf.xml
OEM_APNS_PATH         = telephony/apns-conf.xml
OTA_UPDATED_APNS_PATH = misc/apns/apns-conf.xml
```

`getApnConfFile()` 的实际覆盖顺序仍然是：

```text
/data/misc/apns/apns-conf.xml
> /product/etc/apns-conf.xml
> /oem/telephony/apns-conf.xml
> /system/etc/apns-conf.xml
```

当前 MTK 源码主 APN 编译在 `/system/etc/apns-conf.xml`，因此如果设备上存在 `/product/etc/apns-conf.xml` 或 `/data/misc/apns/apns-conf.xml`，会覆盖你从 `device/mediatek/config/apns-conf.xml` 编进去的结果。排查 MTK APN 不生效时，必须先确认设备侧实际被 provider 读取的是哪一个文件。

### MTK vendor emergency APN补充入口

MTK 还会把 RIL 侧补充 APN 文件复制到 vendor 分区：

```text
vendor/mediatek/proprietary/hardware/ril/fusion/mtk-ril/mdcomm/data/vendor-apns-conf.xml
-> /vendor/etc/vendor-apns-conf.xml
```

这个文件不是普通 APN 的主配置入口。RIL 侧 `RmcDcCommonReqHandler::insertExtraApns()` 会读取 `/vendor/etc/vendor-apns-conf.xml`，用于处理 `type=emergency` 的补充场景：

```text
主 APN 列表里已有相同 APN -> 给已有 APN 增加 emergency type / IWLAN bearer
主 APN 列表里没有相同 APN -> 插入一条 emergency APN
```

`vendor-apns-conf.xml` 中可见 `network_type_bitmask="18"` 这类 Wi-Fi / ePDG emergency APN。RIL 解析时会把 `network_type_bitmask` 转成内部 `bearerBitmask`，再通过 `AT+EAPNSET` 同步 emergency profile 给 modem。

维护口径：

| 场景 | 优先入口 |
|---|---|
| default / mms / ims / xcap / supl / dun APN | `device/mediatek/config/apns-conf.xml` |
| 普通 emergency APN 已在主 APN XML 中维护 | 先看 `device/mediatek/config/apns-conf.xml` |
| emergency / ePDG APN 需要 RIL 补齐或同步给 modem 默认 emergency profile | 再看 `vendor-apns-conf.xml` 和 `RmcDcCommonReqHandler` |

## Qualcomm配置入口

### 源码路径

当前 Qualcomm S1E4ProPlus 分支采用 QSSI / target 分裂构建。`build/env_info.sh` 中的默认项目是 `qdt676`，`build_qssi.sh` 会进入 `qssi` 并 lunch `qssi-userdebug`；`build_vendor.sh` 会进入 `target` 并 lunch `qdt676-userdebug`。

APN 属于 product / system 侧产物，当前日常主入口优先看 QSSI 侧：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml
```

相对 QSSI 源码根目录：

```text
vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml
```

target 侧也有同类文件：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml
```

但当前 `target/device/castles/qdt676/qdt676.mk` 是 vendor-side target，配置里 `PRODUCT_BUILD_PRODUCT_IMAGE := false`。所以只改 target 侧同名文件，不一定会进入最终 `/product/etc/apns-conf.xml`。除非项目构建说明明确要求 target 侧维护 APN，否则 S1E4ProPlus 日常 APN 修改优先放 QSSI 侧。

### 编译复制路径

QSSI 侧构建规则位于：

```text
qssi/vendor/qcom/proprietary/commonsys/telephony-build/build/telephony_system_product.mk
```

关键链路：

```text
XML_CONF_PATH := $(QCPATH_COMMONSYS)/telephony-apps/etc
$(XML_CONF_PATH)/apns-conf.xml
-> $(TARGET_COPY_OUT_PRODUCT)/etc/apns-conf.xml
```

设备侧主验证点：

```text
/product/etc/apns-conf.xml
```

同一个构建规则里还有 HY22 prebuilt 优先路径：

```text
$(QC_PROP_ROOT)/prebuilt_HY22/target/product/$(PREBUILT_BOARD_PLATFORM_DIR)/product/etc/apns-conf.xml
-> /product/etc/apns-conf.xml
```

如果项目启用了 HY22 prebuilt 且该目录存在，prebuilt APN 可能先被加入 `PRODUCT_COPY_FILES`。排查“源码改了但产物没变”时，要同时确认最终 product 镜像里实际取的是 commonsys APN 还是 prebuilt APN。

### 运行时读取优先级

QSSI `TelephonyProvider` 使用同一套 APN provider 主链路：

```text
PARTNER_APNS_PATH     = etc/apns-conf.xml
OEM_APNS_PATH         = telephony/apns-conf.xml
OTA_UPDATED_APNS_PATH = misc/apns/apns-conf.xml
```

源码里先取 `/system/etc/apns-conf.xml`，再依次用 `/oem/telephony/apns-conf.xml`、`/product/etc/apns-conf.xml`、`/data/misc/apns/apns-conf.xml` 覆盖；最终效果是：

```text
/data/misc/apns/apns-conf.xml
> /product/etc/apns-conf.xml
> /oem/telephony/apns-conf.xml
> /system/etc/apns-conf.xml
```

所以 QCOM APN 源码修改后的验证顺序是：

```text
QSSI source apns-conf.xml
-> product image /product/etc/apns-conf.xml
-> device runtime getApnConfFile() 实际读取文件
-> telephony.db carriers 入库值
-> DataProfile / modem 下发值
```

### Qualcomm DataProfile差异

QSSI `TelephonyProvider` 的 APN 入库会解析 `carrier_id`、`network_type_bitmask`、`bearer_bitmask`、legacy `bearer`、`mvno_type`、`mvno_match_data` 等字段。

查询当前 SIM APN 时，QSSI provider 会按：

```text
numeric = 当前 SIM MCCMNC OR carrier_id = 当前 SIM specific carrier id
```

一次查出候选 APN，再分成 MVNO APN、MNO APN、carrier id APN。返回优先级是：

```text
MVNO APN
> 普通 MCC/MNC APN
> 非同 MCC/MNC 但 carrier_id 匹配的 APN
```

最后还会追加只按 carrier id 命中的 APN。因此 QCOM APN 排查时，除了 `mcc/mnc + mvno_type/mvno_match_data`，还要看当前 SIM 的 `carrier_id` / `specific carrier id` 是否参与了 APN 候选。

QTI data 层通过 `QtiTelephonyComponentFactory` 创建 `QtiDataProfileManager`。它继承 AOSP `DataProfileManager`，仍从：

```text
Telephony.Carriers.SIM_APN_URI/filtered/subId/<subId>
```

查询 APN 并下发：

```text
setInitialAttachApn
setDataProfile
```

QTI 额外逻辑是 `filterApnSettingsWithRadioCapability()`：如果 CarrierConfig 中配置了 `KEY_MULTI_APN_ARRAY_FOR_SAME_GID`，会按 GID、APN type、设备 radio capability 过滤同 GID 的多 APN。数组项格式是：

```text
GID数据:APN type列表:device capability:APN name
例如：52FF:mms,supl,hipri,default,fota:SA:nrphone
```

这不是需求表里的 `Account Type` 数字，也不是单纯的 APN 名称列表。只有 APN 自身是 `mvno_type=gid`，且 `mvno_match_data`、APN type 和设备 capability 命中该 CarrierConfig 项时，才会保留对应 APN。遇到“同一 GID 下多个 APN，数据库有但 DataProfile 少了一条”的问题，要检查这条 QTI 过滤链路。

## APN XML结构

根节点：

```xml
<apns version="8">
    ...
</apns>
```

单条 APN：

```xml
<apn carrier="Example Internet"
    mcc="001"
    mnc="01"
    apn="internet"
    protocol="IPV4V6"
    roaming_protocol="IPV4V6"
    type="default,supl,xcap"
/>
```

常用字段：

| 字段 | 用途 | 注意点 |
|---|---|---|
| `carrier` | APN 显示名 / profile 名 | 只用于显示和识别，不等于 APN 接入点名称 |
| `mcc` / `mnc` | PLMN 匹配 | MNC 要保持两位 / 三位精度，不要自动补错 |
| `apn` | 网络接入点名称 / DNN | 运营商分配的实际 APN 名称 |
| `type` | 业务类型 | 常见为 `default`、`mms`、`ims`、`xcap`、`supl`、`dun`、`emergency` |
| `protocol` | 非漫游 PDN/PDP 协议 | 常见 `IP`、`IPV6`、`IPV4V6` |
| `roaming_protocol` | 漫游 PDN/PDP 协议 | 不要默认等同 `protocol`，以需求为准 |
| `authtype` | 认证方式 | `0` none、`1` PAP、`2` CHAP、`3` PAP or CHAP |
| `user` / `password` | APN 认证账号密码 | 有些运营商 MMS / data APN 需要 |
| `mmsc` / `mmsproxy` / `mmsport` | MMS 参数 | MMS 失败时必须验证实际 MMS APN 是否被选中 |
| `mvno_type` / `mvno_match_data` | MVNO 匹配 | 用于同 MCC/MNC 下区分 SPN / IMSI / GID / ICCID / PNN；MTK 主 APN XML 中还可见少量 `ecid`，实际匹配以目标分支代码为准 |
| `carrier_id` | Android carrier id 匹配 | Qualcomm 主 APN XML 可解析且已有少量配置；UNISOC / MTK 日常不优先使用 |
| `user_visible` | Settings 是否显示 | `0` / `false` 通常会在 Settings APN 列表侧隐藏；仍要看 Settings / CarrierConfig 过滤逻辑 |
| `user_editable` | Settings 是否允许编辑 | `0` / `false` 通常禁止用户编辑；仍要看 CarrierConfig 只读 APN type |
| `bearer_bitmask` | RAT 限制 | UNISOC / MTK / Qualcomm 主 APN XML 中用它承接 `network_type_bitmask` 类需求 |
| `bearer` | legacy RAT 限制 | Qualcomm provider 会把 legacy `bearer` 追加转换进 `network_type_bitmask`，旧条目仍可能出现 |
| `network_type_bitmask` | RAT 限制 | 主 APN XML 日常不优先写；MTK `vendor-apns-conf.xml` 的 emergency / ePDG APN 可见该字段；Qualcomm provider 支持解析 |
| `profile_id` | modem profile id | Qualcomm XML 中常见；它是写入 modem profile 的 id，不等于 Android `type` 或需求表 `Account Type` |
| `modem_cognitive` | modem 持久化标志 | `true` 表示该 APN setting 可持久化到 modem；不是 APN 候选选择条件 |
| `max_conns` | APN 最大连接数元数据 | Qualcomm / AOSP provider 可解析；通常不是 APN 名称、type、PDP type 类问题的第一检查点 |
| `max_conns_time` | 最大连接数持续时间 | 单位是秒，和 `max_conns` 配套 |
| `wait_time` | APN retry 等待时间 | 单位是毫秒；用于 retry 元数据，和 `max_conns_time` 不是同一个字段 |
| `mtu` / `mtu_v4` / `mtu_v6` | MTU | `v3` 文件支持该字段；是否已有配置要以目标 XML 为准 |
| `spn` / `imsi` / `pnn` / `ppp` | MTK provider 扩展字段 | MTK `TelephonyProvider` 会入库这些字段，但日常 MVNO 仍优先按 `mvno_type` / `mvno_match_data` 判断 |

## 匹配与生效链路

```text
平台 APN 源 XML
-> UNISOC: vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml
-> MTK: device/mediatek/config/apns-conf.xml
-> Qualcomm: vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml
-> 编译复制到设备侧 apns-conf.xml
   UNISOC: /product/etc/apns-conf.xml
   MTK: /system/etc/apns-conf.xml
   Qualcomm: /product/etc/apns-conf.xml
-> TelephonyProvider 按覆盖优先级选择实际 XML
   /data/misc/apns/apns-conf.xml > /product/etc/apns-conf.xml > /oem/telephony/apns-conf.xml > /system/etc/apns-conf.xml
-> TelephonyProvider 解析 XML
-> 写入 telephony.db carriers 表
-> 按当前 SIM 的 MCC/MNC + MVNO 条件查询 APN
-> DataProfileManager 生成 DataProfile
-> setInitialAttachApn / setDataProfile 下发 modem
-> setupDataCall 发起业务 PDN/PDP
-> modem NAS/SM/ESM 中体现 APN、PDP type 和 reject cause
```

### 入库解析

`TelephonyProvider` 的 APN 入库关键点：

```text
initDatabase()
-> getApnConfFile()
-> loadApns()
-> getRow()
-> insertAddingDefaults()
```

`getRow()` 会解析 XML 中的 `mcc`、`mnc`、`carrier`、`apn`、`type`、`protocol`、`roaming_protocol`、`authtype`、`bearer_bitmask`、`network_type_bitmask`、`mvno_type`、`mvno_match_data`、`user_visible`、`user_editable` 等字段。MTK provider 还会解析 `spn`、`imsi`、`pnn`、`ppp` 等扩展字段；Qualcomm / QSSI provider 会解析 `carrier_id`，并兼容 legacy `bearer`。

注意：源码 XML 中配置的是字符串，真正参与业务选择的是入库后的 `Telephony.Carriers` 字段和后续构造出的 `ApnSetting` / `DataProfile`。

### MVNO匹配优先级

查询当前 SIM APN 时，`TelephonyProvider` 会：

1. 先按当前 SIM 的 `MCCMNC` 查询候选 APN。
2. 对带 `mvno_type` / `mvno_match_data` 的条目调用当前 SIM 匹配逻辑。
3. 如果存在匹配的 MVNO APN，返回 MVNO APN。
4. 如果没有匹配的 MVNO APN，返回普通 MCC/MNC APN。

支持的 MVNO 类型：

| `mvno_type` | 匹配对象 | 说明 |
|---|---|---|
| `spn` | SIM SPN | 大小写忽略匹配 |
| `imsi` | IMSI | 支持 `x` / `X` 通配 |
| `gid` | GID1 | 按前缀匹配 |
| `iccid` | ICCID | 按平台 ICCID 匹配规则 |
| `pnn` | PNN home name | UNISOC 扩展 |

不要把 MVNO APN 和普通 MCC/MNC APN 写成两个互相独立的运营商。它们是同一 MCC/MNC 下的优先级关系。

MTK 分支需要额外注意两点：

- `TelephonyProvider` 查询当前 SIM APN 时，会先通过 MTK 自己的 `getSimOperatorNumeric()` 修正 SIM operator numeric，再按 `numeric = MCCMNC` 和 `carrier_id` 查询候选 APN；返回顺序仍是 MVNO APN 优先、MNO APN 回退，最后再追加 carrier id APN。
- `MtkDataProfileManager` 在 framework APN 查询条件未完全就绪时，会用 RIL 上报的 MCC/MNC 和本地缓存的 SPN / IMSI / GID / ICCID 做早期过滤；这段逻辑明确不依赖 carrier id，因为触发时 carrier id 可能还没有有效值。

因此 MTK APN 日常排查时，不要只看 AOSP `tm.getSimOperator()` 和 carrier id。要同时看 MTK log 中 provider / DataProfileManager 实际使用的 MCCMNC、MVNO 数据，以及最终返回的是 MVNO cursor 还是 MNO cursor。

Qualcomm / QSSI 分支需要额外注意两点：

- `TelephonyProvider` 会用 `tm.getSimOperator()` 和 `tm.getSimSpecificCarrierId()` 同时查候选 APN。返回时 MVNO APN 优先，其次普通 MCC/MNC APN，再处理 carrier id APN。
- `carrier_id` APN 可以不依赖同一个 `numeric` 命中，因此排查 QCOM APN 时要同时保存 `mcc/mnc`、`mvno_type/mvno_match_data`、`carrier_id`、`specific carrier id` 和最终返回 cursor 类型。

QCOM 主 APN 日常仍应先按 MCC/MNC 和 MVNO 定位现有条目；只有当目标条目确实通过 `carrier_id` 区分，或 CarrierConfig / CarrierId 数据库明确要求时，才把 `carrier_id` 当作主要修改条件。

## 字段配置规则

### `type`

`type` 表示 APN 支持的业务类型。常见组合：

| 业务 | 常见 `type` |
|---|---|
| 普通上网 / 默认承载 | `default` |
| SUPL | `supl` |
| MMS | `mms` |
| IMS / VoLTE | `ims` |
| XCAP / UT | `xcap` |
| DUN / tethering | `dun` |
| 紧急业务 | `emergency` |

`ApnSetting.getApnTypesBitmaskFromString()` 中，空 `type` 会被解析成 `TYPE_ALL`。这说明空值在 Android 解析上可以承载全部类型，但配置评审时不建议主动依赖空 `type`；运营商需求明确时应显式写出业务类型。

`wap` 不是 Android 标准 APN type。若需求表写 WAP，要先确认它是 APN 名称、profile 名称，还是业务类型。不要把 `apn="wap"` 和 `type="wap"` 混用。

部分运营商需求表或功能机平台会用 `Account Type` 数字描述业务类型。这个数字不是 Android XML 的 `type` 字符串，评审时必须先转换语义，再决定 XML 字段。

| `Account Type` | 常见业务 | Android APN `type` |
|---:|---|---|
| `0` | 普通数据 / 默认承载 | `default` |
| `1` | 彩信 | `mms` |
| `5` | IMS / VoLTE | `ims` |

不要把 Qualcomm XML 的 `profile_id` 当成这张表里的 `Account Type`。当前 QCOM APN XML 中可见 `profile_id="3"` 配在 `type="fota"` 条目上，IMS 条目也可见其他 `profile_id`；评审时仍以 XML `type`、入库值、DataProfile 和 modem dump 为准。

记录结论时要分清四层：需求表 `Account Type`、Android XML / 数据库 `type`、AP 下发的 DataProfile / initial attach APN、modem NAS 里实际发起的 default / IMS / MMS / XCAP PDN。

### `protocol` / `roaming_protocol`

常见值：

```text
IP
IPV6
IPV4V6
```

验证时要区分：

| 字段 | 验证点 |
|---|---|
| `protocol` | 非漫游时 PDN/PDP type |
| `roaming_protocol` | 漫游时 PDN/PDP type |

如果网络返回 `missing or unknown APN`、`requested service option not subscribed` 或 IPv6/IPv4 建链异常，不要只看 APN 名称，还要同时核对 PDP type / PDN type。

### `authtype`

| 值 | 含义 |
|---|---|
| `0` | none |
| `1` | PAP |
| `2` | CHAP |
| `3` | PAP or CHAP |

认证失败类问题需要同时保存 `user`、`password`、`authtype`、modem reject cause 和对比机结果。

### `bearer_bitmask`

UNISOC / MTK / Qualcomm 主 APN XML 中，运营商需求若写 `network_type_bitmask`，日常按 `bearer_bitmask` 转换配置。

入库逻辑：

```text
XML 有 network_type_bitmask -> 转换并同步 bearer_bitmask
XML 无 network_type_bitmask 但有 bearer_bitmask -> 转换并同步 network_type_bitmask
```

MTK 主 APN XML 当前未见 `network_type_bitmask`，大量条目直接使用 `bearer_bitmask`。MTK `vendor-apns-conf.xml` 的 emergency / ePDG APN 则可见 `network_type_bitmask="18"`，RIL 侧会按 radio technology 编号转换成内部 bearer bitmask。

Qualcomm / QSSI provider 也支持 `network_type_bitmask` 和 `bearer_bitmask` 同步转换；旧 APN 条目里还可能出现 legacy `bearer` 字段。遇到 QCOM 老条目时，不要只查 `bearer_bitmask`，也要看是否存在 `bearer="13"` 这类配置。

如果 `bearer_bitmask` / `network_type_bitmask` 未配置，数据库值可能为 `0`。Android `ServiceState.bitmaskHasTech()` 对 bitmask 为 `0` 的处理是“不限制具体 RAT”。因此不要把未配置理解为“不支持任何 RAT”。

常见 RIL radio technology 编号：

| 编号 | RAT |
|---:|---|
| `13` | LTE |
| `18` | IWLAN |
| `19` | LTE_CA |
| `20` | NR |

具体 bitmask 组合要按目标需求和平台代码转换，不要手算后不验证。

### `user_visible` / `user_editable`

Settings APN 列表会过滤：

```text
user_visible != 0
NOT (type='ia' AND apn is empty)
NOT type='emergency'
如 CarrierConfig KEY_HIDE_IMS_APN_BOOL=true，则隐藏 type='ims'
```

Settings 还会受 CarrierConfig 和厂商扩展控制：

- `KEY_ALLOW_ADDING_APNS_BOOL` 决定是否允许新增 APN。
- `KEY_READ_ONLY_APN_TYPES_STRING_ARRAY` 会让指定 type 只读；如果所有 type 都只读，Settings 可能禁止新增。
- `KEY_HIDE_PRESET_APN_DETAILS_BOOL` 可隐藏未编辑预置 APN 的详情，只显示 profile 名。
- UNISOC 扩展隐藏列表如 `KEY_HIDE_APN_TYPE_STRING_ARRAY` 可能过滤 `xcap` 等 type，所以“type 已入库但 UI 不显示”要同时看 CarrierConfig / UniCarrierConfig。
- Settings 默认 APN 单选项通常只对 `type` 为空、包含 `default`、为 `*` 或空字符串的 profile 可选；`mms`、`ims`、`xcap` 等非 default profile 显示出来也不等于会成为默认数据 APN。

因此：

| 现象 | 优先检查 |
|---|---|
| XML 有 APN，但 Settings 不显示 | `telephony.db` 是否入库、`user_visible`、`type=emergency`、`KEY_HIDE_IMS_APN_BOOL` |
| APN 能显示但不能编辑 | `user_editable`、CarrierConfig 只读 APN type |
| APN type 加了 `xcap` 但 UI 不显示 | APN XML、数据库、CarrierConfig 隐藏列表 |

Settings 显示问题不等于业务不可用。业务失败仍要继续看 APN 是否被 DataProfile 选中并下发 modem。

## 配置作业流

### 新增或修改一条 APN

1. 明确运营商条件：
   - MCC / MNC
   - 是否 MVNO
   - MVNO 类型和值：SPN / IMSI / GID / ICCID / PNN
2. 明确业务类型：
   - default / mms / ims / xcap / supl / dun / emergency
3. 明确 APN 参数：
   - `apn`
   - `protocol`
   - `roaming_protocol`
   - `user` / `password` / `authtype`
   - MMS 参数
   - RAT 限制 / `bearer_bitmask`
4. 在目标平台主 APN XML 中查找同 MCC/MNC 现有条目：
   - UNISOC: `vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml`
   - MTK: `device/mediatek/config/apns-conf.xml`
   - Qualcomm: `vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml`
5. 判断是修改现有 profile，还是新增独立 profile。
6. 保持同一运营商的 default / MMS / IMS / XCAP / emergency profile 分工清楚。
7. 构建后验证设备侧 APN XML：
   - UNISOC: `/product/etc/apns-conf.xml`
   - MTK: `/system/etc/apns-conf.xml`
   - Qualcomm: `/product/etc/apns-conf.xml`
8. 开机或恢复默认 APN 后验证 `telephony.db` 和业务建链。

### 修改现有 APN 时先问的问题

| 问题 | 原因 |
|---|---|
| 是普通 MCC/MNC 还是 MVNO？ | 决定是否需要 `mvno_type` / `mvno_match_data` |
| 改的是 APN 名称还是业务 type？ | 避免把 `apn="wap"` 写成 `type="wap"` |
| 需求写的是 `Account Type` 数字还是 Android `type` 字符串？ | 避免把表格枚举值直接写进 XML |
| 是 default APN、IMS APN、MMS APN 还是 XCAP APN？ | 不同业务看不同 PDN/PDP 和 log |
| 是否只影响 Settings 显示？ | UI 可见性和业务建链不是同一层 |
| 是否涉及漫游？ | 需要看 `roaming_protocol` 和漫游网络 reject |
| 是否涉及 RAT 限制？ | 需要把需求中的 `network_type_bitmask` 转成 `bearer_bitmask` |
| QCOM 是否涉及 carrier id？ | 需要确认 APN XML 是否配置 `carrier_id`，以及当前 SIM specific carrier id |

## 验证证据链

### 源配置

确认 UNISOC 源码 XML：

```bash
rg -n 'mcc="460"|mnc="00"|apn="ims"|mvno_type' \
  vendor/sprd/telephony-res/apn/apns-conf_8_v3.xml
```

确认 MTK 源码 XML：

```bash
rg -n 'mcc="460"|mnc="00"|apn="ims"|mvno_type' \
  device/mediatek/config/apns-conf.xml
```

确认 Qualcomm / QSSI 源码 XML：

```bash
rg -n 'mcc="505"|mnc="01"|carrier_id|apn="ims"|mvno_type|bearer=' \
  vendor/qcom/proprietary/commonsys/telephony-apps/etc/apns-conf.xml
```

确认 UNISOC 产物：

```bash
adb shell ls -l /product/etc/apns-conf.xml /product/etc/old-apns-conf.xml
adb pull /product/etc/apns-conf.xml .
```

确认 MTK 产物：

```bash
adb shell ls -l /system/etc/apns-conf.xml /product/etc/apns-conf.xml /data/misc/apns/apns-conf.xml
adb pull /system/etc/apns-conf.xml .
```

确认 Qualcomm 产物：

```bash
adb shell ls -l /product/etc/apns-conf.xml /data/misc/apns/apns-conf.xml
adb pull /product/etc/apns-conf.xml .
```

如果怀疑 data 或 product 覆盖：

```bash
adb shell ls -l /data/misc/apns/apns-conf.xml
adb shell ls -l /product/etc/apns-conf.xml
```

MTK emergency / ePDG APN 还要额外确认 vendor 补充文件：

```bash
adb shell ls -l /vendor/etc/vendor-apns-conf.xml
adb pull /vendor/etc/vendor-apns-conf.xml .
```

Qualcomm 如果看到 `/data/misc/apns/apns-conf.xml`，要特别区分它是 OTA / 用户覆盖文件，还是 goldfish / emulator 规则带来的测试文件。真实设备 APN 修改一般不从 `device/generic/goldfish/data/etc/apns-conf.xml` 入手。

### 运行时数据库

APN XML 入库后要查 `telephony.db` 或通过 content provider / bugreport 验证。

重点字段：

```text
numeric
mcc
mnc
name / carrier
apn
type
protocol
roaming_protocol
authtype
user
password
mmsc / mmsproxy / mmsport
mvno_type
mvno_match_data
carrier_id
specific carrier id
bearer_bitmask
network_type_bitmask
user_visible
user_editable
edited
current
preferred APN / apn_id
```

建议同时保存：

```bash
adb pull /data/user_de/0/com.android.providers.telephony/databases/telephony.db
adb shell dumpsys telephony.registry
adb shell dumpsys carrier_config
```

具体数据库路径可能随 Android 版本和加密用户目录变化，以设备实际路径为准。

### AP下发

DataProfileManager 从 `Telephony.Carriers.SIM_APN_URI/filtered/subId` 查询当前 SIM 可用 APN，然后构造 `DataProfile`。

MTK 分支在 framework APN 查询尚不可用时，`MtkDataProfileManager` 可先用 RIL 上报的 operator numeric 查询 `Telephony.Carriers.CONTENT_URI/filtered`，再按本地 SPN / IMSI / GID / ICCID 过滤 MVNO。最终 DataProfile 下发仍会走 `setInitialAttachApn` / `setDataProfile`，但早期查询阶段的候选 APN 可能不是 AOSP 标准路径产生的结果。

MTK legacy RILD / 旧 HAL 场景还可能执行 `sortAndLimitDataProfiles()`，把 APN / DataProfile 数量限制到 `MAX_COUNT_DATA_PROFILE = 16`。如果同一 MCC/MNC 下新增了很多 IMS / emergency / MMS / SUPL / XCAP / CBS / RCS 等非 default APN，必须确认目标 profile 没有在这个阶段被裁剪。

Qualcomm / QSSI 分支会通过 `QtiTelephonyComponentFactory` 创建 `QtiDataProfileManager`。它继承 AOSP `DataProfileManager`，但可能执行 `filterApnSettingsWithRadioCapability()`，按 CarrierConfig 的 `KEY_MULTI_APN_ARRAY_FOR_SAME_GID` 过滤同 GID、多 APN、不同 radio capability 的候选。若数据库中有 APN，但 DataProfile 列表缺少某条同 GID APN，要检查这个 QTI 过滤逻辑。

重点 log / dump：

```text
DataProfileManager
MtkDataProfileManager
QtiDataProfileManager
Added DataProfile
Initial attach data profile updated
SETUP_DATA_CALL
DataCallResponse
setInitialAttachApn
setDataProfile
setupDataCall
sortAndLimitDataProfiles Too many APNs
filterApnSettingsWithRadioCapability
KEY_MULTI_APN_ARRAY_FOR_SAME_GID
```

判断点：

| 证据 | 能证明什么 |
|---|---|
| DataProfile 列表包含目标 APN | 数据库匹配和 DataProfile 构造成功 |
| Initial attach profile 是预期 APN | IA / default 选择正确 |
| setupDataCall 使用目标 APN | AP 已下发到数据建链 |
| preferred APN 指向目标 APN | 默认数据 profile 选择正确 |

### AT命令验证边界

`AT+CGDCONT` 只定义 PDP context / APN 参数，不会自动释放并重建已有 PDN。如果测试要求“APN 改完后按新 APN 建链”，脚本需要显式断开再激活：

```text
AT+CGACT?          // 查询当前激活 cid
AT+CGACT=0,<cid>   // 去激活当前数据连接
AT+CGDCONT=<cid>,"IP","APN_2"
AT+CGACT=1,<cid>   // 重新激活，建立新 PDN
```

如果测试规范要求 detach / attach，而不是单独 PDN disconnect，可在去激活后执行 `AT+CFUN=0` / `AT+CFUN=1`。不要把 `CGDCONT` 解释成隐式断链重连，否则会混淆 APN 定义、PDN disconnect 和 detach 三种验证目标。

### modem / 协议侧

AP 已下发不代表网络接受。需要继续看 modem NAS / SM / ESM：

```text
PDN Connectivity Request
PDN Connectivity Reject
Activate Default EPS Bearer
Activate PDP Context Request
Activate PDP Context Reject
ESM cause / SM cause
APN / DNN
PDN type / PDP type
```

常见 reject cause：

| cause | 常见含义 | APN侧检查 |
|---|---|---|
| `#27 missing or unknown APN` | 网络不认识该 APN | APN 名称 / DNN / 运营商签约 |
| `#29 user authentication failed` | 认证失败 | `user`、`password`、`authtype` |
| `#33 requested service option not subscribed` | 业务未签约 | APN type、测试卡签约、网络 profile |

## 常见失败模式

| 现象 | 第一检查点 | 不要误判为 |
|---|---|---|
| 数据无法上网 | default APN 是否匹配、是否下发、ESM cause | LTE 注册失败 |
| IMS 不注册 | `type=ims` APN、IMS PDN 是否建立、P-CSCF | SIP 根因 |
| MMS 失败 | MMS APN 是否被选中、MMSC/proxy/port | 短信或联系人问题 |
| XCAP/UT 失败 | `type=xcap` APN、XCAP APN 是否建链、URL/GBA/BSF | 补充业务代码问题 |
| Settings 不显示 APN | `user_visible`、`type=emergency`、CarrierConfig 隐藏策略 | APN 未入库 |
| APN 修改后不生效 | 是否有 data APN 覆盖、是否恢复默认 APN、telephony.db 是否旧数据 | 源码没编进去 |
| RAT 上不可用 | `bearer_bitmask` / `network_type_bitmask`、当前 RAT、DataProfile 过滤 | 网络侧拒绝 |
| `AT+CGDCONT` 改 APN 后仍走旧链路 | 是否执行 `CGACT` 去激活 / 重新激活，或 detach / attach | `CGDCONT` 会自动重建 PDN |
| MMS 界面报发送失败或地址解析异常 | MMS APN 是否被选中、`mmsc` / `mmsproxy` / `mmsport`、PDP 激活 APN | 联系人或短信应用问题 |
| Attach 成功后 IMS PDN 被拒 | `type=ims` APN、IMS APN 名称 / DNN、ESM cause、测试卡签约 | LTE 注册失败 |
| MTK APN 编进源码但不生效 | provider 实际读取的是 `/data`、`/product`、`/oem` 还是 `/system` APN XML | `device/mediatek/config/apns-conf.xml` 一定优先 |
| MTK 某些业务 APN 缺失 | `MtkDataProfileManager` 是否触发 16 条 DataProfile 裁剪 | XML 未入库 |
| MTK emergency / ePDG APN 异常 | `/vendor/etc/vendor-apns-conf.xml`、`insertExtraApns()`、`AT+EAPNSET` | 只改主 APN XML 就够 |
| QCOM 改了 goldfish APN 但真机不生效 | 是否误改 `device/generic/goldfish/data/etc/apns-conf.xml` | QCOM APN 主文件已修改 |
| QCOM APN 编进 QSSI 但设备不生效 | `/data/misc/apns/apns-conf.xml` 是否覆盖 `/product/etc/apns-conf.xml` | product 产物错误 |
| QCOM 同 GID APN 入库但 DataProfile 缺失 | `KEY_MULTI_APN_ARRAY_FOR_SAME_GID` 和 `QtiDataProfileManager` radio capability 过滤 | APN XML 未入库 |
| QCOM carrier id APN 匹配异常 | `carrier_id`、specific carrier id、MCC/MNC / MVNO 返回 cursor | 只看 MCC/MNC 足够 |
| OMA-CP 后默认 APN 异常 | `edited/current/preferred apn`、用户 APN 与预置 APN 合并 | XML 字段错误 |

## 结论边界

- 只看到 APN XML 正确，不能证明业务会成功。
- 只看到 Settings APN 显示正确，不能证明 DataProfile 会选中。
- 只看到 `setupDataCall` 下发正确，不能证明网络会接受。
- 只看到 PDN reject，不能直接归因 APN 错；还要看 reject cause、签约、漫游、PDP type 和对比机。
- `summarized_with_log_gap` 的 APN case 可以用作抓证据模板，但不能当最终 root cause 复用。

## 后续待补

- Qualcomm `carrier_id`、CarrierConfig 和 MCFG / modem profile 的跨层边界。
- `bearer_bitmask` 与 `network_type_bitmask` 的常用转换表。
- `telephony.db` 查询命令模板。
- APN 相关 log 关键字速查表。

## 关联入口

- [配置目录 README](../README.md)
- [Data Cases](../../40_Case-Library/Data/README.md)
- [IMS配置方法](../IMS配置方法.md)
- [CarrierConfig配置方法_重构](CarrierConfig配置方法_重构.md)
- [常用命令](../../70_Tools-Debug/Commands/常用命令.md)
