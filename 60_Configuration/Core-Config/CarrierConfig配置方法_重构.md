---
doc_type: config
domain: Configuration
status: active
quality: curated
search_tier: main_entry
---

# CarrierConfig配置方法_重构

## 使用入口

这篇用于回答 CarrierConfig / CarrierSettings 怎么配、配到哪个文件、怎么按 SIM 命中、为什么源码改了但 `dumpsys carrier_config` 不变、以及业务失败时怎么补证据。

当前版本先固化已验证的 UNISOC / SPRDROID15、MTK / MP6、Qualcomm / S1E4ProPlus CarrierConfig 主路径和加载机制。

## 速查结论

- 展锐 SPRDROID15 日常配置优先改 `vendor/sprd/platform/packages/apps/CarrierConfig/res/xml/vendor_ex.xml`。
- `vendor_ex.xml` 在 `DefaultCarrierConfigService` 中最后读取，`config.putAll(vendorConfigEx)` 会覆盖 assets 和 `vendor.xml` 中同名 key，因此它是当前维护口径里的最高优先级入口。
- 如果不放 `vendor_ex.xml`，再看 `vendor/sprd/platform/packages/apps/CarrierConfig/assets` 下的运营商 XML。
- MTK MP6 日常配置优先改 `packages/apps/CarrierConfig/res/xml/vendor_ex.xml`。
- MTK 这棵树里 `vendor_ex.xml` 也是 `DefaultCarrierConfigService` 最后合并的 SWIFT 修改，最终优先级同样高于 assets 和 `vendor.xml`。
- MTK 备选入口包括 `packages/apps/CarrierConfig/assets`、`packages/apps/CarrierConfig/res/xml/vendor.xml`，以及可能被 `PRODUCT_PACKAGE_OVERLAYS` 引入的 `device/mediatek/system/common/overlay/CarrierConfig/packages/apps/CarrierConfig/res/xml/vendor.xml`。
- Qualcomm S1E4ProPlus 当前没有 `vendor_ex.xml`。日常优先看静态 RRO `CarrierConfigResCommon_Sys` 覆盖的 `vendor.xml`。
- QCOM QSSI 侧主入口：`qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml`。
- QCOM target 侧也有一份：`target/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml`，且与 qssi 侧内容不同；落地前要按当前编译目标 / merged image 复核最终使用哪一份。
- QCOM `packages/apps/CarrierConfig/res/xml/vendor.xml` 是空的 `<carrier_config_list />`，一般不是日常运营商配置主入口。
- assets 中 carrier id 文件优先于 MCC/MNC 文件：`specific carrier id > carrier id > MCC/MNC fallback carrier id > carrier_config_mccmnc_<mcc><mnc>.xml`。
- carrier id 来源看 `packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb`，但最终运行时 id 仍要用设备 dump / log 确认。
- MTK carrier id 查询优先看 `vendor/mediatek/proprietary/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb`，因为 `MtkTelephonyProvider` 会覆盖 AOSP `TelephonyProvider`；但 `textpb` 只是可读参考，真正编入的是 `carrier_list.pb`。
- QCOM carrier id 查询看 `qssi/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb`，target 侧也有镜像文件且可能不同，最终以实际编译侧和运行时 carrier id dump 为准。
- `vendor_ex.xml`、`vendor.xml`、`carrier_config_mccmnc_*.xml` 可以包含多个 `<carrier_config>` 片段并用过滤条件命中；`carrier_config_carrierid_*.xml` 一般按“一 carrier id 一文件”维护。
- CarrierConfig 修改不能只看源码 XML。完成判断至少需要：源 XML、运行时 `dumpsys carrier_config`、消费者模块 log / 业务结果。

## UNISOC配置入口

### 首选入口：vendor_ex.xml

当前维护路径：

```text
/home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps/vendor/sprd/platform/packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

相对 Android 源码根目录：

```text
vendor/sprd/platform/packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

`vendor_ex.xml` 的根节点是：

```xml
<carrier_config_list>
    <carrier_config mcc="259" mnc="15">
        <boolean name="carrier_volte_available_bool" value="true" />
        <int name="carrier_default_wfc_ims_mode_int" value="1" />
    </carrier_config>
</carrier_config_list>
```

维护口径：

- 日常新增或覆盖运营商配置，优先在 `vendor_ex.xml` 中新增带过滤条件的 `<carrier_config>`。
- 因为 `vendor_ex.xml` 最后合并，必须尽量写明确过滤条件，避免只按 MCC 或无过滤条件覆盖过大范围。
- 同一个 key 如果同时出现在 assets、`vendor.xml`、`vendor_ex.xml`，以 `vendor_ex.xml` 最后合并的值为准。

### 备选入口：assets

当前维护路径：

```text
/home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps/vendor/sprd/platform/packages/apps/CarrierConfig/assets
```

相对 Android 源码根目录：

```text
vendor/sprd/platform/packages/apps/CarrierConfig/assets
```

常见文件名：

```text
carrier_config_carrierid_<carrier_id>_<carrier_name>.xml
carrier_config_mccmnc_<mcc><mnc>.xml
carrier_config_no_sim.xml
```

例如：

```text
carrier_config_carrierid_1345_Telstra.xml
carrier_config_carrierid_1839_Verizon-Wireless.xml
carrier_config_mccmnc_50507.xml
```

维护口径：

- 如果目标运营商已有 carrier id 文件，优先改对应 `carrier_config_carrierid_<id>_*.xml`。
- 如果没有 carrier id，或者确实只想按 MCC/MNC 兜底，才考虑 `carrier_config_mccmnc_<mcc><mnc>.xml`。
- 文件名中的 carrier name 只是可读性辅助，代码匹配靠 `carrier_config_carrierid_<id>_` 前缀。
- 如果同一个 SIM 能命中 carrier id 文件，MCC/MNC 文件通常不会作为主配置被采用。

### carrier id查询入口

carrier id 定义文件：

```text
/home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

相对 Android 源码根目录：

```text
packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

查询方式：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

注意：

- `canonical_id` 是 carrier id。
- `carrier_attribute` 中的 `mccmnc_tuple`、`gid1`、`spn`、`imsi_prefix_xpattern` 等会影响 TelephonyProvider / CarrierId 识别。
- 源码定义不等于当前 SIM 运行时一定命中。排查时还要保存设备侧 `carrier id` / `specific carrier id` dump。

## MTK配置入口

### 首选入口：vendor_ex.xml

当前维护路径：

```text
/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

相对 Android 源码根目录：

```text
packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

维护口径：

- 日常新增或覆盖 MTK 运营商 CarrierConfig，优先在 `vendor_ex.xml` 中新增带过滤条件的 `<carrier_config>`。
- 这棵 MP6 树里的 `vendor_ex.xml` 是 `DefaultCarrierConfigService.java` 中的 SWIFT-383 修改，代码在读取 assets 和 `vendor.xml` 后再读取 `R.xml.vendor_ex`。
- `vendor_ex.xml` 最后 `config.putAll(vendorConfigEx)`，同名 key 会覆盖前面 assets / `vendor.xml` 的结果，因此必须写清楚 `mcc`、`mnc`、`gid1`、`spn`、`cid` 等过滤条件。
- 当前文件头注释里提到 `vendor/sprd/carriers/cucc/...` 是复用来的示例路径，不是 MP6 这棵 MTK 树的日常维护入口。

### 备选入口：assets和vendor.xml

MTK AOSP CarrierConfig app 自带入口：

```text
packages/apps/CarrierConfig/assets
packages/apps/CarrierConfig/res/xml/vendor.xml
packages/apps/CarrierConfig/res/xml/vendor_no_sim.xml
```

MTK common overlay 中还存在一份 `vendor.xml`：

```text
device/mediatek/system/common/overlay/CarrierConfig/packages/apps/CarrierConfig/res/xml/vendor.xml
```

维护口径：

- 如果不走 `vendor_ex.xml`，再看 `packages/apps/CarrierConfig/assets` 下的 `carrier_config_carrierid_<id>_*.xml` 或 `carrier_config_mccmnc_<mcc><mnc>.xml`。
- `packages/apps/CarrierConfig/res/xml/vendor.xml` 会在 assets 后合并，适合平台公共默认覆盖，不适合作为日常单运营商最高优先级入口。
- `device/mediatek/system/common/overlay/CarrierConfig/.../vendor.xml` 是资源 overlay 入口。当前 `device/mediatek/system/common/device.mk` 会在 `MSSI_MTK_TELEPHONY_ADD_ON_POLICY=0` 且非 `MTK_BASIC_PACKAGE` 时把 `overlay/CarrierConfig` 加到 `PRODUCT_PACKAGE_OVERLAYS`。
- 当前 MP6 树里没有 `vendor/mediatek/proprietary/packages/apps/CarrierConfig/Android.bp`，所以没有实际编入 `MtkCarrierConfig` 包；运行入口仍是 `packages/apps/CarrierConfig` 的 `CarrierConfig` app。

### carrier id查询入口

MTK carrier id 优先查询：

```text
/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/vendor/mediatek/proprietary/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

相对 Android 源码根目录：

```text
vendor/mediatek/proprietary/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

查询方式：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  vendor/mediatek/proprietary/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

注意：

- `MtkTelephonyProvider` 的 `Android.bp` 声明 `overrides: ["TelephonyProvider"]`，并使用 `asset_dirs: ["assets/latest_carrier_id"]`。
- AOSP `packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb` 也存在，但 MTK 产品要优先看 MTK provider 的这份。
- `carrier_list.textpb` 主要用于可读性；MTK README 明确说明直接改 `textpb` 不会生效，真正编入 / 加载的是 `carrier_list.pb`。如果要改 carrier id，需要同步生成 PB 或按 README 的测试覆盖流程验证。
- CarrierConfig assets 命中仍依赖运行时 `carrier id` / `specific carrier id`，不能只凭 `textpb` 静态定义判断。

## Qualcomm配置入口

### 首选入口：CarrierConfigResCommon_Sys RRO

S1E4ProPlus 当前 QSSI 侧维护路径：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml
```

相对 Android 源码根目录：

```text
qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml
```

target 侧也存在一份：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml
```

维护口径：

- 这棵 QCOM 树没有 `vendor_ex.xml`。`DefaultCarrierConfigService` 只会在 assets 之后读取 `R.xml.vendor`。
- `qssi/packages/apps/CarrierConfig/res/xml/vendor.xml` 和 `target/packages/apps/CarrierConfig/res/xml/vendor.xml` 当前都是空的 `<carrier_config_list />`，不是主要运营商配置入口。
- Qualcomm 把大量公共 carrier 覆盖放在 `CarrierConfigResCommon_Sys` 静态 RRO 中。该 RRO 的 manifest 里 `targetPackage="com.android.carrierconfig"`，`android:priority="100"`，会覆盖 CarrierConfig app 的 `R.xml.vendor`。
- `qssi/device/qcom/qssi/qssi.mk` 和 `target/device/castles/qdt676/qdt676.mk` 都设置 `TARGET_USES_RRO := true`，因此当前产品优先按 RRO 路径判断；传统 `device/qcom/common/device/overlay` 只在 `TARGET_USES_RRO` 不为 true 时启用。
- qssi 侧和 target 侧的 RRO `vendor.xml` 内容不同。落地前必须结合当前编译目标、最终 merged image 和设备侧 overlay 包确认实际生效来源，不要只改其中一份后假设一定进版本。
- QCOM RRO `vendor.xml` 里存在无过滤条件的全局 `<carrier_config>`，会对所有 SIM 生效；单运营商修改必须写明确过滤条件，避免覆盖面过大。

### 备选入口：assets和传统overlay

QSSI CarrierConfig app 自带 assets：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/packages/apps/CarrierConfig/assets
```

相对 Android 源码根目录：

```text
qssi/packages/apps/CarrierConfig/assets
```

target 侧镜像：

```text
target/packages/apps/CarrierConfig/assets
```

如果当前分支没有启用 RRO，传统 overlay 路径是：

```text
target/device/qcom/common/device/overlay/packages/apps/CarrierConfig/res/xml/vendor.xml
target/device/qcom/common/automotive/device/overlay/packages/apps/CarrierConfig/res/xml/vendor.xml
```

维护口径：

- 如果目标运营商已经有 `carrier_config_carrierid_<id>_*.xml`，可以改 assets 里的 carrier id 文件；但 QCOM RRO `vendor.xml` 会在 assets 后合并，并覆盖同名 key。
- 如果要按 MCC/MNC fallback 文件落地，当前代码读取的是 `carrier_config_mccmnc_<mcc><mnc>.xml`。
- 当前 assets 里能看到一些老式 `carrier_config_<mccmnc>.xml` 文件，例如 `carrier_config_46002.xml`。当前 `DefaultCarrierConfigService` 的 MCC/MNC fallback 前缀是 `carrier_config_mccmnc_`，这类老式文件名不要直接当作当前代码一定会读取的入口。
- `target/device/generic/goldfish/.../CarrierConfig/res/xml/vendor.xml` 属于 emulator / goldfish 路径，不是 S1E4ProPlus 真机日常配置入口。

### carrier id查询入口

QSSI 侧 carrier id 定义文件：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

相对 Android 源码根目录：

```text
qssi/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

target 侧镜像：

```text
target/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

查询方式：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  qssi/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb \
  target/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

注意：

- 当前未看到 Qualcomm 专门覆盖 `TelephonyProvider` 的 provider 包；qssi / target 都是 AOSP `TelephonyProvider`，并使用 `asset_dirs: ["assets/latest_carrier_id"]`。
- qssi 与 target 的 `carrier_list.textpb` 内容可能不同。分析时先按 QSSI 侧查，最终用运行时 `carrier id` / `specific carrier id` dump 兜底确认。
- CarrierConfig assets 的 carrier id 文件命中仍取决于运行时 CarrierIdProvider 识别结果，静态 textpb 只是候选证据。

## 加载与覆盖链路

展锐当前默认 CarrierConfig app 由 vendor 侧 `UnisocCarrierConfig` 覆盖 AOSP `CarrierConfig`：

```text
vendor/sprd/platform/packages/apps/CarrierConfig/Android.bp
-> android_app name: UnisocCarrierConfig
-> overrides: CarrierConfig
-> system_ext_specific: true
```

运行时服务入口仍是：

```text
packages/apps/CarrierConfig/src/com/android/carrierconfig/DefaultCarrierConfigService.java
```

加载主链路：

```text
CarrierConfigLoader.updateConfigForPhoneId
-> bind DefaultCarrierConfigService
-> DefaultCarrierConfigService.onLoadConfig(CarrierIdentifier)
-> loadConfig()
-> readConfigFromXml()
-> PersistableBundle
-> dumpsys carrier_config
-> Telephony / IMS / Data / Settings / vendor logic 读取
```

`loadConfig()` 的有效合并顺序：

```text
1. assets 中按 carrier id / MCCMNC 找到的配置
2. res/xml/vendor.xml
3. res/xml/vendor_ex.xml
```

最终覆盖关系：

```text
vendor_ex.xml
> vendor.xml
> assets carrier_config_carrierid_*.xml / carrier_config_mccmnc_*.xml
> CarrierConfigManager 默认值
```

如果是无 SIM 场景，代码会加载：

```text
carrier_config_no_sim.xml
-> vendor_no_sim.xml
```

MTK MP6 当前 CarrierConfig app 仍是 AOSP 包名：

```text
packages/apps/CarrierConfig/Android.bp
-> android_app name: CarrierConfig
-> system_ext_specific: true
-> privileged: true
```

运行时服务入口：

```text
packages/apps/CarrierConfig/src/com/android/carrierconfig/DefaultCarrierConfigService.java
```

MTK `loadConfig()` 的有效合并顺序：

```text
1. assets 中按 carrier id / MCCMNC 找到的配置
2. res/xml/vendor.xml
3. res/xml/vendor_ex.xml
```

最终覆盖关系：

```text
vendor_ex.xml
> vendor.xml
> assets carrier_config_carrierid_*.xml / carrier_config_mccmnc_*.xml
> CarrierConfigManager 默认值
```

因此 MTK 和当前展锐分支在 CarrierConfig 运行时覆盖顺序上基本一致；差异主要是源码落点和 provider 包名不同。

Qualcomm S1E4ProPlus 当前 CarrierConfig app 入口：

```text
qssi/packages/apps/CarrierConfig/Android.bp
-> android_app name: CarrierConfig
-> system_ext_specific: true
-> privileged: true
```

运行时服务入口：

```text
qssi/packages/apps/CarrierConfig/src/com/android/carrierconfig/DefaultCarrierConfigService.java
```

QCOM `loadConfig()` 的有效合并顺序：

```text
1. assets 中按 carrier id / MCCMNC 找到的配置
2. R.xml.vendor
```

由于当前产品 `TARGET_USES_RRO := true`，`R.xml.vendor` 通常由静态 RRO 覆盖：

```text
CarrierConfigResCommon_Sys
-> targetPackage: com.android.carrierconfig
-> resource: res/xml/vendor.xml
```

最终覆盖关系：

```text
CarrierConfigResCommon_Sys 的 vendor.xml
> packages/apps/CarrierConfig/res/xml/vendor.xml
> assets carrier_config_carrierid_*.xml / carrier_config_mccmnc_*.xml
> CarrierConfigManager 默认值
```

如果 `TARGET_USES_RRO` 不为 true，才回到传统 `DEVICE_PACKAGE_OVERLAYS` / `PRODUCT_PACKAGE_OVERLAYS` 的 overlay 路径。

## assets匹配优先级

当 `CarrierIdentifier.getCarrierId()` 不是 unknown 时，代码会遍历 assets：

```text
carrier_config_carrierid_<specificCarrierId>_*
> carrier_config_carrierid_<carrierId>_*
> carrier_config_carrierid_<getCarrierIdFromMccMnc(mcc+mnc)>_*
```

如果以上都没有命中，才回退：

```text
carrier_config_mccmnc_<mcc><mnc>.xml
```

因此“carrier id 优先级比 MCC/MNC 高”的具体含义是：

- 只要 carrier id 文件被读到并产生非空配置，MCC/MNC 文件不会作为主配置继续加载。
- `vendor.xml` 和 `vendor_ex.xml` 仍会在 carrier id 文件后继续合并，并可能覆盖同名 key。
- `specific carrier id` 比普通 `carrier id` 更高，适合 MVNO / 子运营商。

## 过滤条件

`vendor_ex.xml`、`vendor.xml` 和 `carrier_config_mccmnc_*.xml` 中的每个 `<carrier_config>` 都会走 `checkFilters()`。UNISOC / MTK / QCOM 的过滤逻辑大体一致，但平台扩展属性有差异：UNISOC 分支额外支持 `ecid`，QCOM 分支额外支持 `iccid`，MTK MP6 当前代码未支持这两个扩展。

| 属性            | 匹配对象                             | 说明                              |
| ------------- | -------------------------------- | ------------------------------- |
| `mcc`         | SIM MCC                          | 精确匹配                            |
| `mnc`         | SIM MNC                          | 精确匹配，保留两位 / 三位精度                |
| `gid1`        | SIM GID1                         | 大小写忽略匹配                         |
| `gid2`        | SIM GID2                         | 大小写忽略匹配                         |
| `spn`         | SIM SPN                          | 支持正则；`null` 可匹配空 SPN            |
| `imsi`        | IMSI                             | 支持 `x` 通配，代码会按配置长度截取当前 IMSI 再匹配 |
| `cid`         | carrier id / specific carrier id | 任一匹配即可                          |
| `sku`         | `R.string.sku_filter`            | OEM 自定义过滤                       |
| `ecid`        | `ro.boot.ecid`                   | UNISOC 扩展，支持 `x` 通配；MTK MP6 当前未支持 |
| `iccid`       | ICCID                            | QCOM 扩展，支持逗号分隔前缀匹配            |
| `device`      | `Build.DEVICE`                   | 设备名过滤                           |
| `vendorSku`   | `ro.boot.product.vendor.sku`     | vendor SKU 过滤                   |
| `hardwareSku` | `ro.boot.product.hardware.sku`   | hardware SKU 过滤                 |
| `board`       | `Build.BOARD`                    | board 过滤                        |

过滤规则：

- 一个 `<carrier_config>` 上写了多个属性时，必须全部匹配才会合并。
- 未写属性的片段会被认为匹配所有 SIM，`vendor_ex.xml` 中不要轻易这样写。
- 同一个 XML 中可以有多个匹配片段；后匹配片段里的同名 key 会覆盖前面片段。
- 未知属性会导致该片段不匹配，并在 log 中打印 `Unknown attribute`。

## 字段配置规则

### 先确认 key 是否存在

配置前先确认 key 存在于目标分支 `CarrierConfigManager.java` 或确有平台私有消费者：

```bash
rg -n 'KEY_HIDE_IMS_APN_BOOL|hide_ims_apn_bool|key_oem_pref_network_mode' \
  frameworks/base/telephony/java/android/telephony/CarrierConfigManager.java \
  packages vendor/sprd vendor/mediatek qssi target
```

日常默认值优先查：

```text
60_Configuration/References/CarrierConfig/CarrierConfig参数映射.md
60_Configuration/References/CarrierConfig/*.md
```

如果映射表缺失、默认值冲突、平台大版本不同，或者准备给出直接可落地补丁，再回目标分支源码复核。

### 按 delta 配置

- 需求值等于默认值时，通常不要新增 carrier 覆盖。
- 需求值不同于默认值时，再写入 `vendor_ex.xml` 或 assets。
- 只改一个运营商时，必须带足够过滤条件，不要改全局 `vendor.xml` 或无过滤片段。
- 如果是厂商私有 key，要同时记录消费者代码位置，例如 Settings、IMS service、DataProfile、RILJ 或 vendor service。

### XML值类型

常见写法：

```xml
<boolean name="carrier_volte_available_bool" value="true" />
<int name="carrier_default_wfc_ims_mode_int" value="1" />
<string name="default_vm_number_string">+61101</string>
<string-array name="read_only_apn_types_string_array" num="1">
    <item value="ims" />
</string-array>
<int-array name="lte_rsrp_thresholds_int_array" num="4">
    <item value="-126" />
    <item value="-115" />
    <item value="-105" />
    <item value="-97" />
</int-array>
```

不要把 XML 字段名、Java 常量名和运营商需求表字段混用。最终入库到 `PersistableBundle` 的 key 通常是不带 `KEY_` 前缀的字符串名。

## 配置作业流

1. 明确运营商和匹配条件：
   - MCC / MNC
   - carrier id / specific carrier id
   - GID1 / GID2
   - SPN / IMSI
   - ECID（UNISOC）/ ICCID（QCOM）/ SKU / board 是否相关
2. 查 `carrier_list.textpb`，确认该 SIM 是否有 carrier id 定义。
3. 查现有配置：
   - `vendor_ex.xml` 是否已有同 MCC/MNC 或更宽泛片段
   - assets 是否已有 `carrier_config_carrierid_<id>_*.xml`
   - assets 是否已有 `carrier_config_mccmnc_<mcc><mnc>.xml`
   - MTK 是否存在 `device/mediatek/system/common/overlay/CarrierConfig/.../vendor.xml` 资源覆盖
   - QCOM 是否启用 `TARGET_USES_RRO`，最终 `R.xml.vendor` 来自 RRO 还是传统 overlay
4. 查 key 默认值和消费者：
   - `References/CarrierConfig/CarrierConfig参数映射.md`
   - `CarrierConfigManager.java`
   - 目标模块代码 / log
5. 选择配置落点：
   - UNISOC / MTK 日常优先 `vendor_ex.xml`
   - QCOM 日常优先 `CarrierConfigResCommon_Sys` 的 `vendor.xml`
   - 不走高优先级 `vendor_ex.xml` / RRO 时，carrier id 文件优先于 MCC/MNC 文件
6. 写入最小 delta，只配置需要覆盖的 key。
7. 编译后验证设备侧 app / resource 是否更新。
8. 插卡或触发 reload 后验证 `dumpsys carrier_config`。
9. 用业务 log 验证消费者确实读取并采用该值。

## 验证证据链

### 源码侧

确认 `vendor_ex.xml`：

```bash
rg -n 'mcc="748"|mnc="01"|carrier_volte_available_bool|carrier_wfc_ims_available_bool' \
  vendor/sprd/platform/packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

确认 assets：

```bash
find vendor/sprd/platform/packages/apps/CarrierConfig/assets -maxdepth 1 -type f \
  \( -name 'carrier_config_carrierid_1345_*' -o -name 'carrier_config_mccmnc_50501.xml' \)
```

确认 carrier id：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

确认加载代码：

```bash
rg -n 'vendor_ex|priority: specific carrier id|MCCMNC_PREFIX|getCarrierIdFromMccMnc|checkFilters' \
  packages/apps/CarrierConfig/src/com/android/carrierconfig/DefaultCarrierConfigService.java
```

MTK 确认 `vendor_ex.xml`：

```bash
rg -n 'mcc="748"|mnc="01"|carrier_volte_available_bool|carrier_wfc_ims_available_bool' \
  packages/apps/CarrierConfig/res/xml/vendor_ex.xml
```

MTK 确认 assets 和 `vendor.xml`：

```bash
find packages/apps/CarrierConfig/assets -maxdepth 1 -type f \
  \( -name 'carrier_config_carrierid_1345_*' -o -name 'carrier_config_mccmnc_50501.xml' \)
rg -n 'mcc="505"|mnc="01"|carrier_volte_available_bool|carrier_wfc_ims_available_bool' \
  packages/apps/CarrierConfig/res/xml/vendor.xml \
  device/mediatek/system/common/overlay/CarrierConfig/packages/apps/CarrierConfig/res/xml/vendor.xml
```

MTK 确认 carrier id：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  vendor/mediatek/proprietary/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

MTK 确认包和 overlay 是否参与构建：

```bash
rg -n 'PRODUCT_PACKAGE_OVERLAYS.*overlay/CarrierConfig|PRODUCT_PACKAGES.*CarrierConfig|MtkCarrierConfig|MtkTelephonyProvider' \
  device/mediatek/system/common/device.mk \
  device/mediatek/common/device.mk \
  packages/apps/CarrierConfig/Android.bp \
  vendor/mediatek/proprietary/packages/providers/TelephonyProvider/Android.bp
```

QCOM 确认 RRO `vendor.xml`：

```bash
rg -n 'mcc="505"|mnc="01"|carrier_volte_available_bool|carrier_wfc_ims_available_bool|iccid=' \
  qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml \
  target/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/res/xml/vendor.xml
```

QCOM 确认 CarrierConfig app 和加载代码：

```bash
rg -n 'config.putAll|R.xml.vendor|priority: specific carrier id|MCCMNC_PREFIX|getCarrierIdFromMccMnc|checkFilters|iccid' \
  qssi/packages/apps/CarrierConfig/src/com/android/carrierconfig/DefaultCarrierConfigService.java
```

QCOM 确认 RRO 是否参与构建：

```bash
rg -n 'TARGET_USES_RRO|CarrierConfigResCommon_Sys|commonsys/resource-overlay/overlay.mk|targetPackage="com.android.carrierconfig"' \
  qssi/device/qcom/qssi/qssi.mk \
  target/device/castles/qdt676/qdt676.mk \
  qssi/vendor/qcom/proprietary/common/config/device-vendor-qssi.mk \
  qssi/vendor/qcom/proprietary/commonsys/resource-overlay/overlay.mk \
  qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/AndroidManifest.xml \
  qssi/vendor/qcom/proprietary/commonsys/resource-overlay/common/CarrierConfig/Android.mk
```

QCOM 确认 carrier id：

```bash
rg -n 'canonical_id: 1345|carrier_name: "Telstra"|mccmnc_tuple: "50501"' \
  qssi/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb \
  target/packages/providers/TelephonyProvider/assets/latest_carrier_id/carrier_list.textpb
```

### 设备侧

确认当前 CarrierConfig app：

```bash
adb shell pm path com.android.carrierconfig
adb shell dumpsys package com.android.carrierconfig | grep -E 'CarrierConfig|DefaultCarrierConfigService|system_ext|version'
```

QCOM 还要确认 overlay 包：

```bash
adb shell cmd overlay list | grep -i carrierconfig
adb shell pm path com.android.carrierconfig.overlay.common
adb shell dumpsys package com.android.carrierconfig.overlay.common | grep -E 'targetPackage|priority|static|path|version'
```

确认运行时 bundle：

```bash
adb shell dumpsys carrier_config
adb shell dumpsys carrier_config | grep -E 'carrier_volte_available_bool|carrier_wfc_ims_available_bool|key_oem_pref_network_mode'
```

确认当前 SIM / carrier id：

```bash
adb shell dumpsys telephony.registry
adb shell dumpsys isub
adb shell dumpsys carrier_config | grep -E 'phoneId|subId|mcc|mnc|carrierId|specific'
```

确认加载 log：

```bash
adb logcat -b main -b radio -s CarrierConfigLoader CarrierSvcBindHelper CarrierService DefaultCarrierConfigService CarrierPrivilegesTracker UiccController
```

关键 log：

```text
Config being fetched
vendor ex for feature config
CarrierConfigLoader
CarrierSvcBindHelper
onLoadConfig
```

### 业务侧

`dumpsys carrier_config` 正确只说明运行时 bundle 正确，不代表业务已经采用。还要按业务继续看：

| 业务 | 消费方证据 |
|---|---|
| VoLTE / VoWiFi / ViLTE | IMS service / ImsManager / Settings log |
| APN UI 隐藏 | Settings APN 列表过滤、`KEY_HIDE_APN_TYPE_STRING_ARRAY` |
| MMS 大小 / proxy / retry | MmsService / TelephonyProvider / DataProfile |
| 网络模式 | Settings / PhoneInterfaceManager / RILJ / modem AT |
| 运营商名 / voicemail | Telephony framework / Dialer / Contacts |

## 常见失败模式

| 现象 | 优先检查 | 不要误判为 |
|---|---|---|
| 改 assets 后 `dumpsys` 仍是旧值 | `vendor_ex.xml` 是否最后覆盖了同名 key | assets 没编进去 |
| 改 MCC/MNC 文件不生效 | 是否已命中 carrier id 文件 | key 不支持 |
| MTK 改 `vendor.xml` 后不生效 | 是否被 `vendor_ex.xml` 最后覆盖，或是否改的是未参与构建的 overlay | CarrierConfig app 没启动 |
| MTK carrier id 静态查询和运行时不一致 | 当前产品是否编入 `MtkTelephonyProvider`，运行时 carrier id dump 是否命中 | 只看 AOSP `packages/providers` |
| QCOM 改 `packages/apps/CarrierConfig/res/xml/vendor.xml` 不生效 | 当前是否由 `CarrierConfigResCommon_Sys` 静态 RRO 覆盖 `R.xml.vendor` | XML 格式错 |
| QCOM 改传统 `device/qcom/common/device/overlay` 不生效 | `TARGET_USES_RRO` 是否为 true；true 时传统 overlay 不走 | CarrierConfig 不读 vendor.xml |
| QCOM 改 qssi RRO 后 target 侧仍不同 | qssi / target 两份 RRO 是否需要同步，最终 merged image 用哪一份 | 代码加载顺序错 |
| QCOM `carrier_config_<mccmnc>.xml` 不生效 | 当前代码 MCC/MNC fallback 文件名前缀是 `carrier_config_mccmnc_` | carrier id 识别失败 |
| 只换 SIM 不重启配置不刷新 | SIM state、subId/phoneId、CarrierConfigLoader reload | XML 格式错 |
| `vendor_ex.xml` 一改影响多个运营商 | 过滤条件是否只写 MCC 或没写 MNC/GID/SPN | 平台随机错误 |
| `dumpsys` 正确但业务不变 | 消费方是否读这个 key，是否还有私有开关或 NV | CarrierConfig 未生效 |
| carrier id 查不到 | `carrier_list.textpb` 是否已有定义、SIM 是否满足 GID/SPN/IMSI 条件 | MCC/MNC 写错 |
| MVNO 没命中预期配置 | specific carrier id、GID/SPN/IMSI 是否与白卡一致 | 普通 carrier id 文件一定优先 |
| XML 片段完全不生效 | 是否用了未知过滤属性、MNC 位数是否正确 | key 默认值问题 |

## 结论边界

- 看到源码 XML 正确，不代表运行时 bundle 正确。
- 看到 `dumpsys carrier_config` 正确，不代表业务模块已经读取。
- 看到 Settings 菜单变化，不代表 IMS / Data / Call 协议侧成功。
- 看到 carrier id 定义文件里有 `canonical_id`，不代表当前 SIM 运行时一定命中该 id。
- 展锐 `vendor_ex.xml` 是当前最高优先级配置入口，但也正因为它最后覆盖，必须控制匹配范围。
- MTK MP6 的 `vendor_ex.xml` 也是当前最高优先级配置入口；`device/mediatek/system/common/overlay/CarrierConfig/.../vendor.xml` 属于资源覆盖入口，是否生效要结合产品 make 条件和最终 APK 资源确认。
- MTK 的 `carrier_list.textpb` 是可读参考，直接改 textpb 不会生效；需要确认 `carrier_list.pb`、provider 包和运行时数据库。
- QCOM S1E4ProPlus 没有 `vendor_ex.xml`，最高优先级通常来自静态 RRO `CarrierConfigResCommon_Sys` 覆盖的 `vendor.xml`。
- QCOM 的 qssi / target 侧 CarrierConfig RRO 和 carrier id 文件可能不同；结论必须落到最终编译产物和设备侧 overlay / dump。
- QCOM 的 CarrierConfig 是 AP/framework 侧配置，不等于 MCFG / QCRIL NV 已生效。IMS、VoWiFi、ViLTE 等问题还要继续看 Qualcomm IMS service、QCRIL、MCFG/NV 和 modem log。

## 后续待补

- `overrideConfig()` / 测试命令的稳定验证方法。
- CarrierConfig 常用 key 到消费者代码的速查表。

## 关联入口

- [配置目录 README](../README.md)
- [CarrierConfig参数映射](../References/CarrierConfig/CarrierConfig参数映射.md)
- [UNISOC-CarrierService启动与CarrierConfig加载流程](../../50_Platform-Code/UNISOC/UNISOC-CarrierService启动与CarrierConfig加载流程.md)
- [APN配置方法](APN配置方法_重构.md)
- [运营商需求表配置作业流](../运营商需求表配置作业流.md)
