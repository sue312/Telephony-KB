---
doc_type: config
domain: Configuration
status: active
quality: curated
search_tier: main_entry
platform: UNISOC, MTK, Qualcomm
---

# ECC配置方法_重构

## 速查结论

- 本文当前覆盖展锐 UNISOC、MTK MP6 与 Qualcomm S1E4ProPlus ECC 配置。
- 本文已结合展锐《紧急呼叫配置及常见问题说明 V1.3》（2025-05-20）补充，V1.3 重点新增 Android 16 路径。
- A16 主配置入口是 `vendor/sprd/platform/packages/services/Telephony/uniecc/input/eccdata.txt`。
- A15 主配置入口是 `vendor/sprd/platform/packages/apps/UniTelephony/uniecc/input/eccdata.txt`。
- MTK MP6 主配置入口是 `vendor/mediatek/proprietary/external/EccList/ecc_list.xml`，OP 定制文件是同目录 `ecc_list_OPxx.xml`，最终复制到 `/vendor/etc/ecc_list*.xml`。
- Qualcomm AP 侧本地数据库入口是 `qssi/packages/services/Telephony/ecc/input/eccdata.txt`，生成 `ecc/output/eccdata` 后作为 `TeleService` assets 加载。
- Qualcomm QCRIL/RIL 侧入口是 `target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/upgrade/other/*.sql`，生成 `qcrilNr.db` 后打包到 `/vendor/etc/qcril_database/qcrilNr.db`；开机 init 先拷贝到 `/data/vendor/radio/qcrilNr_prebuilt.db`，QCRIL 再检查/恢复运行时 active DB `/data/vendor/radio/qcrilNr.db`。
- AOSP / Qualcomm AP OTA DB 路径是 `/data/misc/emergencynumberdb/emergency_number_db`；`EmergencyNumberTracker` 会加载 assets `eccdata`，再尝试加载 OTA DB，并按有效 `revision` 选择版本。
- UNISOC 改完 `input/eccdata.txt` 后必须运行 `gen_eccdata.sh` 生成 `output/unieccdata`，只改 input 不能证明设备会加载新号码库。
- UNISOC / Qualcomm AP `eccdata` 只能配置来源为 `DATABASE` 的紧急号码；MTK `ecc_list*.xml` 与 Qualcomm QCRIL `qcrilNr.db` 经 RIL/native 侧合并后以 `MODEM_CONFIG` 口径上报给 Framework。两条口径不要混用。
- UNISOC A15/A16 运行时不是直接读文本文件，而是 `UniEmergencyNumberTracker` 从 `com.android.phone` 的 assets 中打开 `unieccdata`，按国家 ISO、MNC 和 `card_flag` 过滤；当 OTA DB 版本更高时，还会合并 OTA 与 asset DB。
- 展锐 `mnc` 是可选运营商条件，但它不是简单追加：当前 MNC 命中已配置 MNC 时，会优先使用命中的 MNC 条目列表；当前 MNC 不命中任何已配置 MNC 时，才继续使用未带 `mnc` 的国家通用条目。
- `ecc_fallback` 当前代码证据来自 proto 规则：每个国家必须配置 `112` 或 `911`，当 `EccInfo` 被 `ril.ecclist` 拒绝时可由 fallback 替代；当前 AOSP/Qualcomm/UNISOC Java 加载链路没有把它直接转换成 `EmergencyNumber`，不要把它当成强制拨号改号开关。

## 配置路径

| 分支 / 版本 | 输入文件 | 生成物 | 打包入口 | 备注 |
|---|---|---|---|---|
| Android 4.4 / 7 / 8.1 / 9 | `packages/apps/CarrierConfig/assets/carrier_config_xxxxxx.xml` | CarrierConfig XML | 旧版本 `GlobalConfigManager` / `GlobalConfigController` | 主要字段是 `ecclist_nocard`、`ecclist_withcard`、`fake_ecclist_withcard` |
| Android 10 | `packages/services/Telephony/ecc/input/eccdata.txt` | `packages/services/Telephony/ecc/output/eccdata` | AOSP TeleService assets | Android 10 起引入 `EmergencyNumber` / `EmergencyNumberTracker` 数据库方式 |
| A16 | `/home/wx/Project/Common/SPRDROID16_SYS_MAIN_W25.22.4/alps/vendor/sprd/platform/packages/services/Telephony/uniecc/input/eccdata.txt` | `uniecc/output/unieccdata` | `vendor/sprd/platform/packages/services/Telephony/Android.bp` 中 `:uniecc_asset{assets}` 注入 `TeleService` | 以 `services/Telephony/uniecc` 为准 |
| A15 | `/home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps/vendor/sprd/platform/packages/apps/UniTelephony/uniecc/input/eccdata.txt` | `uniecc/output/unieccdata` | `vendor/sprd/platform/packages/apps/UniTelephony/Android.bp` 中 `asset_dirs: ["uniecc/output"]` | 以 `apps/UniTelephony/uniecc` 为准 |
| MTK MP6 | `/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/vendor/mediatek/proprietary/external/EccList/ecc_list.xml` | `/vendor/etc/ecc_list.xml`、`/vendor/etc/ecc_list_OPxx.xml`、`/vendor/etc/ecc_list_preference.xml` | `vendor/mediatek/proprietary/external/EccList/EccList.mk` 通过 `PRODUCT_COPY_FILES` 复制到 `$(TARGET_COPY_OUT_VENDOR)/etc` | 运行时代码常量写 `/system/vendor/etc/`，设备上通常等价看 `/vendor/etc/` |
| Qualcomm AP database | `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/packages/services/Telephony/ecc/input/eccdata.txt` | `qssi/packages/services/Telephony/ecc/output/eccdata` | `qssi/packages/services/Telephony/Android.bp` 中 `asset_dirs: ["ecc/output"]` 注入 `TeleService` | 影响 Framework `DATABASE` source，格式同 AOSP `eccdata.txt` |
| Qualcomm QCRIL database | `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/upgrade/other/*.sql` | `qcrilNr.db` | `qcril_database/Android.bp` 中 `qcril_config_database` 生成 DB，`qcrilNrDb_vendor` 打包到 `vendor/etc/qcril_database` | 影响 RIL/PBM 上报的 `MODEM_CONFIG` source；按 MCC/MNC、service state 和 source 表匹配 |

注意：`uniecc/README.md` 里仍可能写 `output/eccdata`，但 A15/A16 的 `conversion_toolset_v1/env.sh` 实际定义为 `OUTPUT_DATA="${OUTPUT_DIR}/unieccdata"`，文档和排查时应以脚本变量、生成物和 Android.bp 打包规则为准。

MTK 也有 `vendor/mediatek/proprietary/packages/services/Telephony/ecc/input/eccdata.txt` 和 `ecc/output/eccdata`，这是 Android emergency database 资产库路径；用户日常改 MTK vendor RIL 侧紧急号码时，优先看本节给出的 `external/EccList/ecc_list*.xml`。

Qualcomm 同时存在 AP `eccdata` 和 QCRIL `qcrilNr.db` 两套入口。若需求是“Android Framework 数据库号码、国家 ISO、routing/category”，优先看 `qssi/packages/services/Telephony/ecc/input/eccdata.txt`；若现象来自 radio emergency list、`ril.ecclist`、PBM/QCRIL 或 modem config source，优先看 `qcril_database/upgrade/other/*.sql`。

## AOSP / Qualcomm AP eccdata 配置格式

`eccdata.txt` 是 protobuf text 格式。AOSP Android 10+ 与 Qualcomm AP database 使用这一套 schema，生成物一般是 `ecc/output/eccdata`。核心结构如下：

```text
revision: 1
countries {
  iso_code: "CO"
  eccs {
    phone_number: "123"
    types: POLICE
    types: AMBULANCE
    types: FIRE
  }
  eccs {
    phone_number: "112"
    types: TYPE_UNSPECIFIED
  }
  eccs {
    phone_number: "911"
    routing: NORMAL
    normal_routing_mncs: "101"
  }
  ecc_fallback: "112"
  ignore_modem_config: false
}
```

| 字段 | 含义 | 代码口径 / 风险 |
|---|---|---|
| `revision` | 数据版本 | proto 注释说明该值用于标识内容问题；但当前 AOSP / Qualcomm `EmergencyNumberTracker` 会在 asset DB 和 OTA DB 间比较 `revision`，使用有效且版本更高的一方。目标分支若启用 OTA DB，必须确认版本策略 |
| `countries.iso_code` | 国家/地区 ISO 码，如 `CO` | 运行时按 country ISO 匹配，不是直接写 MCC |
| `eccs.phone_number` | 紧急号码 | 每个 `eccs` 一个号码；同号码多 category 后续会合并 |
| `eccs.types` | 紧急服务类别 | AOSP / Qualcomm proto 使用 `POLICE`、`AMBULANCE`、`FIRE`、`MARINE_GUARD`、`MOUNTAIN_RESCUE`、`MIEC`、`AIEC` |
| `eccs.routing` | 呼叫路由 | proto 枚举：`UNKNOWN=0`、`EMERGENCY=1`、`NORMAL=2`。不配置默认为 `UNKNOWN`；`NORMAL` 是普通路由/假紧急，不等价于“无卡不能拨打” |
| `eccs.normal_routing_mncs` | NORMAL routing 的 MNC 条件 | 仅当 `routing` 为 `NORMAL` 时生效；为空表示所有 MNC 都按 NORMAL routing；这不是运营商专属号码过滤 |
| `ecc_fallback` | fallback 号码 | proto 要求每个国家配置 `112` 或 `911`，注释口径是当 `EccInfo` 被 `ril.ecclist` 拒绝时可替代；当前 Java 加载链路没有直接消费该字段，已有国家通常保留原值，除非有明确需求和实机证据 |
| `ignore_modem_config` | 是否忽略 modem config 来源号码 | `true` 表示该国家更信任 Android database，可能影响 `MODEM_CONFIG` 来源号码合并，落地前必须结合目标分支代码和 log 验证 |

注意：AOSP / Qualcomm AP `eccdata.txt` 不支持 UNISOC 的 `eccs.mnc` 和 `eccs.card_flag` 字段。高通需要运营商级号码时，通常应看 QCRIL `qcril_emergency_source_mcc_mnc_table` / `voice_mcc_mnc_table`，不要把展锐字段直接写到高通 AP `eccdata.txt`。

### AOSP / Qualcomm AP OTA DB 选择

当前 S1E4ProPlus 代码中，`EmergencyNumberTracker` 的数据库选择链路如下：

| 证据点 | 结论 |
|---|---|
| `EMERGENCY_NUMBER_DB_ASSETS_FILE = "eccdata"` | AP assets 数据库文件名是 `eccdata`，由 `TeleService` assets 提供 |
| `EMERGENCY_NUMBER_DB_OTA_FILE_PATH = "misc/emergencynumberdb/emergency_number_db"` | OTA DB 运行时路径是 `/data/misc/emergencynumberdb/emergency_number_db` |
| `cacheEmergencyDatabaseByCountry()` | 先读 assets DB，再调用 `cacheOtaEmergencyNumberDatabase()` |
| `assetsDatabaseVersion > mCurrentOtaDatabaseVersion` | asset 版本更高时用 asset；否则保留 OTA DB 结果 |
| `updateOtaEmergencyNumberListDatabaseAndNotify()` | 收到 OTA DB 更新事件后重新加载 OTA DB、更新列表并通知 |

因此，高通 AP 侧如果只改 `qssi/packages/services/Telephony/ecc/input/eccdata.txt`，但设备上已有更高版本 OTA DB，最终 `DATABASE` source 可能仍来自 OTA DB。验证时要同时看 `getEmergencyNumberDbVersion()` / `getEmergencyNumberOtaDbVersion()`、`EmergencyNumberTracker` dump 和 `/data/misc/emergencynumberdb/emergency_number_db` 是否存在。

## UNISOC uniecc 扩展格式

UNISOC A15/A16 使用 `UniProtobufEccData`，字段与 AOSP 基础结构相近，但展锐扩展了 `mnc` 和 `card_flag`，生成物是 `uniecc/output/unieccdata`：

```text
revision: 1
countries {
  iso_code: "CO"
  eccs {
    phone_number: "112"
    types: POLICE
  }
  eccs {
    phone_number: "911"
    routing: 2
    mnc: "101"
    card_flag: "with_card"
  }
  ecc_fallback: "112"
}
```

| 字段 | 含义 | 代码口径 / 风险 |
|---|---|---|
| `revision` | 数据版本 | `UniEmergencyNumberTracker` 会记录 asset `unieccdata` 的 revision，并调用 OTA DB 加载逻辑；asset 版本高时直接使用 asset，OTA 版本高时进入 asset/OTA 合并逻辑。需要配合目标分支 OTA 策略确认是否递增 |
| `eccs.types` | 紧急服务类别 | UNISOC proto 使用 `POLICE`、`AMBULANCE`、`FIRE`、`MARINE`、`MOUNTAIN`、`MIEC`、`AIEC` |
| `eccs.routing` | 呼叫路由 | UNISOC proto 是 `int32`：`0=unknown`、`1=emergency`、`2=normal`；`2` 只表示普通路由/假紧急，不控制卡状态 |
| `eccs.mnc` | 针对运营商 MNC 配置 | 只写 MNC，不写 MCCMNC；运行时先取驻留网络 MNC，取不到再取 SIM MNC |
| `eccs.card_flag` | 卡状态过滤 | 支持 `no_card` 和 `with_card`；不配置表示有卡/无卡都可用 |
| `ecc_fallback` | fallback 号码 | 新增国家时按展锐资料要求配置 `112` 或 `911`；A16 代码检索只在 proto 和输入数据中找到该字段，未在 `UniEmergencyNumberTracker` 中看到直接转换逻辑，已有国家通常保留原值 |

### UNISOC 运行时加载证据

当前 A16 代码中，`vendor/sprd/platform/frameworks/telephony-injection/uni-telephony-common/src/java/com/android/internal/telephony/emergency/UniEmergencyNumberTracker.java` 是关键运行时入口：

| 代码点 | 结论 |
|---|---|
| `UNI_EMERGENCY_NUMBER_DB_ASSETS_FILE = "unieccdata"` | 运行时加载的是生成物 `unieccdata`，不是 `input/eccdata.txt` |
| `createPackageContext("com.android.phone", ...)` + `remoteContext.getAssets().open(...)` | 从 `com.android.phone` 的 assets 打开 `unieccdata` |
| `cacheEmergencyDatabaseByCountry(countryIso)` | 按 country ISO 过滤国家条目，生成 `mEmergencyNumberListFromAssetDatabase` |
| `getMnc()` | 优先取驻留网络 numeric 的 MNC，取不到再取 SIM numeric 的 MNC |
| `eccInfo.mnc` 分支 | 配置了 MNC 的条目只在当前 MNC 命中时进入 MNC 专属列表；有 MNC 专属列表时会替换国家通用列表 |
| `isValidEccInfo()` | `card_flag` 为空表示有卡/无卡都可用；`no_card` 仅 SIM absent；`with_card` 表示 SIM 非 absent |
| `mergeAssetAndOtaEmergencyNumberList()` | OTA DB 版本高于 asset 时，先保留 OTA 号码，同号合并 category/routing，再补充 OTA 不包含的 asset 号码 |
| `needLoadDataBaseEccList()` | 无卡但其他 slot 有 active subscription 时，可能清空本 slot database list 并跳过加载 |

这几个点决定了展锐 ECC 配置排查顺序：先看生成物是否进入 assets，再看 country ISO、MNC、`card_flag`、active subscription / phoneId，最后看 OTA DB 是否覆盖或合并。

## MTK EccList 配置格式

MTK `ecc_list*.xml` 是 XML 表，核心结构是：

```xml
<EccTable>
    <EccEntry Ecc="999" Category="0" Condition="1" Plmn="234 10"/>
</EccTable>
```

| 字段 | 含义 | 代码口径 / 风险 |
|---|---|---|
| `Ecc` | 紧急号码 | 字符串号码，最终进入 AP ECC list / modem ECC list |
| `Category` | service category bitmask | 取 3GPP TS 24.008 bitmask：`1=Police`、`2=Ambulance`、`4=Fire`、`8=Marine`、`16=Mountain`、`32=MIEC`、`64=AIEC`；`0` 表示未指定 |
| `Condition` | 卡状态 / 真伪紧急策略 | `0=仅无卡为 ECC`、`1=始终为 ECC`、`2=MMI 显示 ECC 但有卡 ready 时按 normal call routing`；代码里无卡遇到 `2` 会转成 no-sim ECC |
| `Plmn` | MCC/MNC 匹配 | 写法是 `"MCC MNC"`，例如 `460 03`；`FFF` 或 `FF` 表示同 MCC 下所有运营商，例如 `460 FFF` |
| `ecc_list_OPxx.xml` | OPTR 定制文件 | 运行时读 `persist.vendor.operator.optr`，优先尝试 `/system/vendor/etc/ecc_list_${optr}.xml`，不存在再回落 `ecc_list.xml` |
| `ecc_list_preference.xml` | RAT 偏好列表 | 配置 `GsmOnly`、`GsmPref`、`CdmaPref`，影响紧急号码优先 RAT，不等同于新增号码 |

MTK 匹配逻辑和 UNISOC 不同：MTK 会把 XML、属性、Framework/Test、modem/MCF 等来源按号码合并。同一个号码下，网络来源优先级最高，其次 SIM；AP XML / property / framework / test 高于 MCF，默认号码优先级最低。相同优先级时，带具体 MNC 的运营商条目优先于国家级 `FFF/FF` 条目。

## Qualcomm QCRIL 配置格式

Qualcomm AP 侧 `eccdata.txt` 使用上面的 AOSP / Qualcomm AP protobuf text，主要差异是生成物叫 `ecc/output/eccdata`，不是 `unieccdata`。

QCRIL 侧是 SQLite SQL 表，常见配置文件位于：

```text
target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/upgrade/other/0_initial_qcrilnr.sql
target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/upgrade/other/*_version_update_ecc_table*.sql
```

核心表结构和用途：

| 表 | 字段 | 用途 |
|---|---|---|
| `qcril_emergency_source_mcc_table` | `MCC, NUMBER, IMS_ADDRESS, SERVICE` | 按 MCC 匹配自定义紧急号码 |
| `qcril_emergency_source_voice_table` | `MCC, NUMBER, IMS_ADDRESS, SERVICE` | 按 MCC 匹配 voice service 口径号码 |
| `qcril_emergency_source_hard_mcc_table` | `MCC, NUMBER, IMS_ADDRESS, SERVICE` | 无卡 / hardcoded 场景按 MCC 匹配 |
| `qcril_emergency_source_nw_table` | `MCC, NUMBER, IMS_ADDRESS, SERVICE` | 网络 MCC 相关的自定义号码 |
| `qcril_emergency_source_mcc_mnc_table` | `MCC, MNC, NUMBER, IMS_ADDRESS, SERVICE` | 按 SIM MCC/MNC 精确匹配 |
| `qcril_emergency_source_voice_mcc_mnc_table` | `MCC, MNC, NUMBER, IMS_ADDRESS, SERVICE` | 按 SIM MCC/MNC 精确匹配 voice service 口径号码 |
| `qcril_emergency_source_escv_iin_table` | `IIN, NUMBER, ESCV, ROAM` | 韩国等场景按 IIN 查询 ESCV 类型 |
| `qcril_emergency_source_escv_nw_table` | `MCC, MNC, NUMBER, ESCV` | 按网络 MCC/MNC 查询 ESCV 类型 |

示例：

```sql
INSERT INTO qcril_emergency_source_mcc_table VALUES('450','112','','');
INSERT INTO qcril_emergency_source_mcc_mnc_table VALUES('405','840','101','','');
INSERT INTO qcril_emergency_source_escv_nw_table VALUES('450', NULL, '112', 1);
```

`SERVICE` 常见值为空、`full`、`limited`。QCRIL 查询时会先查无 service 限制的行，再根据当前 voice/data service confidence 查 `full` 或 `limited` 行。因此新增号码时不能只看 MCC/MNC，还要确认需求是否只在 full service 或 limited service 场景生效。

当前 S1E4ProPlus QCRIL 代码边界：

| 代码点 | 结论 |
|---|---|
| `qcril_db.cpp` 的 `qcril_db_emergency_number_tables` | source enum 到 `qcril_emergency_source_*` 表名一一映射；MCC 表和 MCC/MNC 表的主键不同 |
| `qcril_db_is_mcc_part_of_emergency_numbers_table()` | source 是 `MCC_MNC` / `VOICE_MCC_MNC` 且 MNC 有效时按 MCC+MNC 查，否则按 MCC 查 |
| `qcril_db_is_mcc_part_of_emergency_numbers_table_with_service_state()` | service 参数生效时按 `SERVICE` 再过滤，MCC/MNC 表仍要求 MNC 有效 |
| `qcril_check_mcc_part_of_emergency_numbers_table_with_service_state()` | NAS 先查无 service 限制，再按 full / limited service state 查 |
| `qcril_qmi_nas_add_emergency_numbers()` | 先按 IMSI/SIM MCC 查 MCC / voice MCC，再按 MCC/MNC 命中关系投射 MCC_MNC / VOICE_MCC_MNC；网络 MCC 不同还会追加 NW MCC 号码 |
| `RilPbmFillEccMap` / `PbmModule::handlePbmFillEccMap()` | NAS 查到号码后交给 PBM 填 ECC map，source 设置为 `MODEM_CONFIG` |
| `qcril_pbm.cpp` | PBM 合并 PBM cache、RIL ECC map、network detected ECC 后发送 `RilUnsolEmergencyListIndMessage`，并兼容更新 `ril.ecclist` |
| `qcril_database/Android.bp` | `qcril_config_database` 用 SQL 生成 `qcrilNr.db`，`qcrilNrDb_vendor` 打包到 `vendor/etc/qcril_database` |
| `qcril_db_check_prebuilt_and_wait()` | 首次启动或 data DB 不存在时，从 `/data/vendor/radio/qcrilNr_prebuilt.db` 拷贝生成 `/data/vendor/radio/qcrilNr.db`；active DB 不更新时，源码 SQL 修改不会生效 |

Qualcomm QCRIL 新增号码时先按场景选表：

| 场景 | 优先表 | 判断 |
|---|---|---|
| 国家级号码，随 SIM MCC 生效 | `qcril_emergency_source_mcc_table` / `qcril_emergency_source_voice_table` | 需求只按国家，不区分运营商 |
| 运营商级号码，随 SIM MCC/MNC 生效 | `qcril_emergency_source_mcc_mnc_table` / `qcril_emergency_source_voice_mcc_mnc_table` | 需求明确到 MCC/MNC，且设备能取到 SIM MCC/MNC |
| 无卡 / hardcoded 场景 | `qcril_emergency_source_hard_mcc_table` | 重点验证无卡、SIM absent、默认 MCC 选择 |
| 网络 MCC 相关号码 | `qcril_emergency_source_nw_table` | 现象来自 network emergency list 或网络 MCC，不是普通 SIM MCC/MNC |
| ESCV 分类 | `qcril_emergency_source_escv_iin_table` / `qcril_emergency_source_escv_nw_table` | 只处理 ESCV 类型/分类，不等同于新增 emergency number list 号码 |

编辑文件时也要区分“初始 DB”和“版本迁移”：新平台初建可改 `0_initial_qcrilnr.sql`；已经有量产 DB 或当前分支通过 `*_version_update_ecc_table*.sql` 升级时，应优先补对应 version update SQL，并确认 `Android.bp` / 生成脚本会把该 SQL 纳入 `qcrilNr.db`。

## 需求类型到配置落点

| 需求 / 现象 | 优先落点 | 判断口径 |
|---|---|---|
| 新增某国家本地紧急号码 | 平台对应 AP database：AOSP/Qualcomm `eccdata.txt` 或 UNISOC `uniecc/input/eccdata.txt` | 目标号码 source 应为 `DATABASE`；Qualcomm 生成 `ecc/output/eccdata`，UNISOC 生成 `output/unieccdata` |
| UNISOC 同一国家不同运营商号码不同 | `eccs.mnc` | 只写 MNC；命中 MNC 后需要补齐该运营商仍要保留的通用号码 |
| UNISOC 有卡 / 无卡号码不同 | `eccs.card_flag` | `with_card` 表示非 absent，PIN locked 也可能按有卡处理；`no_card` 只在 absent 场景生效 |
| Qualcomm AP 按 MNC 控制假紧急 routing | `normal_routing_mncs` | 只限制 `routing=NORMAL` 对哪些 MNC 生效，不是运营商专属号码过滤 |
| 号码要按真紧急拨出 | `eccs.routing` 不配置或配置 `0/1` | radio log 典型下发 `ATD<number>@<category>,#` |
| 号码要按假紧急 / 普通路由拨出 | `eccs.routing: 2` | radio log 典型下发 `ATD<number>`；不控制卡状态 |
| 需求表要求紧急号码显示名称 | 平台显示名客制化资源 / Dialer 展示逻辑 | 不属于 emergency number source；先确认目标平台是否有显示名资源链路 |
| 通话记录是否显示紧急号码 | CarrierConfig call-log 相关 key | 不属于号码库配置，只影响 call log 展示 |
| 飞行模式下 ECC 是否受限开协议栈 | `KEY_CARRIER_RADIO_POWER_ON_FOR_ECALL` | `true` 常见 `AT+SFUN=4,1,1`；`false` 常见 `AT+SFUN=4` |
| Android 12 前 VoWiFi ECC 策略 | VoWiFi ECC CarrierConfig key | Android 12 及之后展锐资料说明主要走 CP 侧方案，落地前要查目标分支 |
| FDN 开启时假紧急能否拨出 | RIL 行为 / `AT+SPCALLSETTING=1,0` | fake emergency 是否绕 FDN 取决于 RIL 限制策略，不能只改号码库 |
| MTK 新增/调整 vendor RIL 侧 ECC | `external/EccList/ecc_list.xml` 或 `ecc_list_OPxx.xml` | 运行时按 PLMN、SIM 状态过滤后 sync 到 modem，再通过 radio emergency list 上报 Framework |
| MTK 调整 ECC RAT 偏好 | `external/EccList/ecc_list_preference.xml` | 只影响 `GsmOnly/GsmPref/CdmaPref` 判断，不是号码来源本身 |
| Qualcomm 新增 Framework 数据库号码 | `qssi/packages/services/Telephony/ecc/input/eccdata.txt` | 生成 `ecc/output/eccdata` 并重编 `TeleService`；最终 source 为 `DATABASE` |
| Qualcomm 新增 QCRIL/RIL 侧号码 | `qcril_database/upgrade/other/*_ecc_table*.sql` 或初始 SQL 对应表 | 生成 `qcrilNr.db`；经 NAS 查询、PBM 填 `ril_ecc_map`，最终以 `MODEM_CONFIG` 口径上报 |
| Qualcomm 按运营商 MCC/MNC 精确配置 | `qcril_emergency_source_mcc_mnc_table` / `qcril_emergency_source_voice_mcc_mnc_table` | 代码先取 SIM MCC/MNC，命中后会优先投射 MCC/MNC 表号码 |
| Qualcomm 按网络 MCC / 无卡场景配置 | `qcril_emergency_source_nw_table` / `qcril_emergency_source_hard_mcc_table` | 网络 MCC 或无卡 hardcoded 场景使用；需结合卡状态和 `custom_emergency_numbers_enabled_for_nw` |
| Qualcomm ESCV 类型 | `qcril_emergency_source_escv_iin_table` / `qcril_emergency_source_escv_nw_table` | 只解决 ESCV 分类，不等同于新增普通 ECC 号码 |

## 需求表读取规则

旧 ECC 需求表通常会把号码、国家、运营商、显示名和拨打条件放在同一张表里。落地前先把它拆成不同控制点，不要直接把整行内容塞进号码库。

| 需求字段 | 先转成什么问题 | 配置/验证口径 |
|---|---|---|
| `Country MCC` / 国家 | 号码按国家生效，还是按运营商生效 | AOSP / UNISOC `eccdata` 先转国家 ISO；MTK `ecc_list*.xml` 用 `MCC FFF/FF` 表示国家级；Qualcomm QCRIL 国家级优先看 MCC 表 |
| `MCC/MNC` / 运营商 | 是否需要运营商级覆盖 | UNISOC 只写 `mnc` 且会覆盖国家通用列表；MTK 写 `MCC MNC`；Qualcomm QCRIL 写 MCC/MNC 表 |
| `Number` | 新增/修改的 emergency number | 需要确认 source 是 `DATABASE`、`MODEM_CONFIG`、`SIM` 还是 `NETWORK_SIGNALING` |
| `English display` / `Local Language Display` | 显示名称需求 | 多数平台不是号码库字段；要查显示名资源、Dialer/TeleService 显示逻辑和语言资源 |
| `Without SIM Can Call = Yes` | 无卡也应按 ECC 识别/拨出 | UNISOC 看 `card_flag`；MTK 不要简单等同 `Condition=1`，还要看 no-sim 过滤和最终 `ril.ecclist` |
| `Without SIM Can Call = No` | 仅插卡可用，或插卡时按 normal call | UNISOC 优先看 `card_flag=with_card`；MTK 原生 `Condition=2` 是 SIM ready normal routing、无卡 no-sim ECC，不完全等价于“无卡禁止” |
| `Category` / `Type` | service category / SIP URN | 多类型 category 可能影响 `urn:service:sos.*`，需要结合 IMS/运营商要求确认是否改成 generic SOS |

白卡只能覆盖显示名、UI 识别和部分本地列表场景，不能证明目标国家实网一定能拨通。涉及“国外能否接通”“网络是否接受”“无卡 emergency camping”等问题时，必须补现场 fail/pass 对比 log 或仪表环境复现证据。

## 紧急号码来源

最终号码池不是只来自本地配置文件。展锐资料和 MTK 代码里都能看到多来源合并逻辑，常见来源如下：

| 来源 | source 位图（binary / decimal） | 说明 | 优先级 | 配置/验证口径 |
|---|---|---|---|---|
| `NETWORK_SIGNALING` | `1` / `1` | 网络侧经 modem 上报的紧急号码，例如 AT `+CEN1/+CEN2`，RIL 侧 `UNSOL_ECC_NETWORKLIST_CHANGED` | 1 | 看 modem/RIL 上报，不能通过本地 `eccdata.txt` 修改 |
| `SIM` | `10` / `2` | USIM/SIM 文件中的 EF_ECC | 2 | 看 SIM 读取和 Framework 合并，不能通过本地 `eccdata.txt` 修改 |
| `DATABASE` | `10000` / `16` | 本地国家/运营商紧急号码库 | 3 | 本文 `eccdata.txt` / `unieccdata` 的主要控制点 |
| `MODEM_CONFIG` | `100` / `4` | modem 配置来源 | 4 | UNISOC 资料标注当前平台未使用；MTK `ecc_list*.xml` / property / framework / test / MCF、Qualcomm QCRIL `qcrilNr.db` 投射号码会按此类口径上报 |
| `DEFAULT` | `1000` / `8` | 3GPP 默认号码 | 5 | 无卡默认 `112/911/000/08/110/118/119/999`，有卡默认 `112/911` |

排查时先确认目标号码来自哪一类 source。若 log 里号码来自网络或 SIM，本地 `unieccdata` 改对了也可能不是最终第一坏点。

## Category 与真假紧急

`types` 对应 Android `EmergencyNumber` 的 service category。常见映射如下：

| 配置值 | category 含义 |
|---|---|
| `TYPE_UNSPECIFIED` / 不配置 | 一般紧急呼叫，所有类别 |
| `POLICE` | 匪警 |
| `AMBULANCE` | 急救 |
| `FIRE` | 火警 |
| `MARINE` / `MARINE_GUARD` | 海事；UNISOC 使用 `MARINE`，AOSP/Qualcomm 使用 `MARINE_GUARD` |
| `MOUNTAIN` / `MOUNTAIN_RESCUE` | 高山救援；UNISOC 使用 `MOUNTAIN`，AOSP/Qualcomm 使用 `MOUNTAIN_RESCUE` |
| `MIEC` | 手动 eCall |
| `AIEC` | 自动 eCall |

真假紧急主要看 `routing`：

| routing   | 含义         | 典型下发                       |
| --------- | ---------- | -------------------------- |
| `0` / 不配置 | 真紧急        | `ATD<number>@<category>,#` |
| `1`       | 真紧急        | `ATD<number>@<category>,#` |
| `2`       | 假紧急 / 普通路由 | `ATD<number>`              |

因此，`routing: 2` 只控制“界面按紧急显示但按普通呼叫拨出”，不能用来表示“无卡不能拨打”。无卡/有卡过滤要看 `card_flag` 或具体平台代码。

## UNISOC MNC 匹配注意

展锐代码里 MNC 匹配有一个容易踩坑的点：

```text
国家通用 eccs -> updatedAssetEmergencyNumberList
当前 MNC 命中的 eccs -> updatedAssetEmergencyNumberListWithMnc
如果当前 MNC 命中已配置 MNC，则最终使用 MNC 列表替换国家通用列表
如果当前 MNC 不命中任何已配置 MNC，则继续使用未带 mnc 的国家通用列表
```

因此，给某个运营商加 `mnc` 条目时要确认两件事：

1. 该运营商还需要的通用号码是否也要复制到同一个 MNC 条件下；否则当前 MNC 命中后，这些未带 `mnc` 的通用号码不会自动叠加进最终列表。
2. `mnc` 与 `card_flag` 同时使用时，某个卡状态下如果没有有效条目，可能导致该 MNC 下列表为空或缺号码。

简单理解：展锐这套配置主要按国家维护，MNC 是国家内的特例覆盖，不是全量列表之外的简单增量。若某国家只给部分号码配置了 MNC，则要特别验证“当前 MNC 命中”和“当前 MNC 不命中”两种场景的最终号码池。

## 编译生成

A10 示例：

```bash
cd <android10_alps_root>
source build/envsetup.sh
lunch <target>
m aprotoc
cd packages/services/Telephony/ecc
bash gen_eccdata.sh
m TeleService
```

A16 示例：

```bash
cd /home/wx/Project/Common/SPRDROID16_SYS_MAIN_W25.22.4/alps
source build/envsetup.sh
lunch <target>
m aprotoc
cd vendor/sprd/platform/packages/services/Telephony/uniecc
bash gen_eccdata.sh
m TeleService
```

A15 示例：

```bash
cd /home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps
source build/envsetup.sh
lunch <target>
m aprotoc
cd vendor/sprd/platform/packages/apps/UniTelephony/uniecc
bash gen_eccdata.sh
m UniTelephony
```

编译后至少按平台确认：

| 平台 / 链路 | 检查项 | 预期 |
|---|---|---|
| UNISOC AP database | `input/eccdata.txt`、`output/unieccdata`、APK assets | input 包含修改；`unieccdata` 重新生成；`com.android.phone` 对应 APK assets 内能看到 `unieccdata` |
| Qualcomm AP database | `input/eccdata.txt`、`ecc/output/eccdata`、APK assets | input 包含修改；`eccdata` 重新生成；`TeleService.apk` assets 内能看到 `eccdata` |
| Qualcomm QCRIL database | SQL 文件、`qcrilNr.db`、设备侧 `/vendor/etc/qcril_database/qcrilNr.db` 与 `/data/vendor/radio/qcrilNr*` | SQL 被纳入生成；vendor DB 更新；data 分区 prebuilt/active DB 与本次构建一致 |
| MTK EccList | `ecc_list*.xml`、`EccList.mk` 打包、设备侧 `/vendor/etc/ecc_list*` | XML 包含修改；目标 OPTR 文件被打入 vendor；运行时能按 PLMN/SIM 状态命中 |

`gen_eccdata.sh` 依赖 `ANDROID_BUILD_TOP` 和 `aprotoc`。如果脚本提示 `You need to source and lunch`，先回到源码根目录执行 `source build/envsetup.sh` 和 `lunch`；如果提示缺 `aprotoc`，先编译 `m aprotoc`。

A15/A16 的最终编译目标以当前项目 `Android.bp`、产品打包规则和实际 APK assets 为准。如果官方脚本或分支文档提示的目标与本文示例不一致，以“`output/unieccdata` 已生成，并被 `com.android.phone` 对应 APK 打入 assets”为验收标准。

Qualcomm AP database 示例：

```bash
cd /home/wx/Project/QCOM/qcom4490/S1E4ProPlus
source build/envsetup.sh
lunch <target>
m aprotoc
cd qssi/packages/services/Telephony/ecc
bash gen_eccdata.sh
m TeleService
```

Qualcomm QCRIL database 生成口径：

```bash
cd /home/wx/Project/QCOM/qcom4490/S1E4ProPlus
source build/envsetup.sh
lunch <target>
m qcrilNrDb_vendor
```

源码证据显示 `qcril_database/Android.bp` 会把 `upgrade/other/*.sql` 和 `upgrade/config/*.sql` 输入 `tools/gen_db.sh`，通过 `sqlite3` 生成 `qcrilNr.db`。如果当前产品编译目标不接受 `qcrilNrDb_vendor`，以整机/产品构建中实际包含的 `qcrilNr.db` 模块为准。验收时先确认 vendor DB `/vendor/etc/qcril_database/qcrilNr.db` 更新；开机 init 会把它复制到 `/data/vendor/radio/qcrilNr_prebuilt.db`，QCRIL 再通过 `qcril_db_check_prebuilt_and_wait()` / recovery 逻辑创建或恢复 active DB `/data/vendor/radio/qcrilNr.db`。查询以 active DB 为主，排查不生效时同时对比 vendor DB、prebuilt DB 和 active DB。

## 加载链路

### UNISOC uniecc

```text
GsmCdmaPhone 初始化
-> TelephonyComponentFactory.inject(EmergencyNumberTracker)
-> UniTelephonyComponentFactory.makeEmergencyNumberTracker()
-> new UniEmergencyNumberTracker()
-> 监听 SIM 状态、飞行模式、网络国家变化
-> cacheEmergencyDatabaseByCountry(countryIso)
-> createPackageContext("com.android.phone")
-> assets.open("unieccdata")
-> gzip 解压 + UniProtobufEccData.AllInfo.parseFrom()
-> countries.iso_code 匹配当前 countryIso
-> isValidEccInfo() 按 card_flag / SIM 状态过滤
-> MNC 条目按当前 network/sim MNC 覆盖国家通用列表
-> merge asset DB、OTA DB、Radio/SIM/TestMode 列表
-> Dialer/Telecom/Telephony 使用最终 EmergencyNumber list 判断拨号
```

关键代码证据：

| 代码位置 | 结论 |
|---|---|
| `vendor/sprd/platform/packages/services/Telephony/uniecc/conversion_toolset_v1/env.sh` | A16 生成 `output/unieccdata` |
| `vendor/sprd/platform/packages/apps/UniTelephony/uniecc/conversion_toolset_v1/env.sh` | A15 生成 `output/unieccdata` |
| `vendor/sprd/platform/packages/services/Telephony/Android.bp` | A16 把 `uniecc/output/*` 作为 TeleService assets |
| `vendor/sprd/platform/packages/apps/UniTelephony/Android.bp` | A15 把 `uniecc/output` 作为 UniTelephony assets |
| `vendor/sprd/platform/frameworks/telephony-injection/uni-telephony-common/.../UniTelephonyComponentFactory.java` | `makeEmergencyNumberTracker()` 返回 `UniEmergencyNumberTracker` |
| `vendor/sprd/platform/frameworks/telephony-injection/uni-telephony-common/.../UniEmergencyNumberTracker.java` | 读取 `unieccdata`、按 country/MNC/card_flag 过滤并合并 |
| `frameworks/opt/telephony/src/java/com/android/internal/telephony/GsmCdmaPhone.java` | Phone 初始化时创建 EmergencyNumberTracker |

### MTK EccList

```text
vendor/mediatek/proprietary/external/EccList/ecc_list*.xml
-> EccList.mk 复制到 /vendor/etc/ecc_list*.xml
-> RtmEccNumberController.onInit()
-> initEmergencyNumberSource()
-> XmlEccNumberSource 读取 /system/vendor/etc/ecc_list_${persist.vendor.operator.optr}.xml
   不存在则回落 /system/vendor/etc/ecc_list.xml
-> 监听 PLMN / SIM / UICC MCCMNC / capability switch / screen state
-> XmlEccNumberSource.update(plmn, isSimInsert) 解析 EccEntry
-> 按 PLMN、FFF/FF MCC 通配、卡状态 Condition 过滤
-> syncEccToModem()
-> RFX_MSG_REQUEST_LOCAL_SYNC_ECC_NUM_TO_MD
-> MIPC_CALL_SET_ECC_LIST_REQ 下发 modem
-> modem ECC list change / get ECC list
-> RFX_MSG_URC_EMERGENCY_NUMBER_LIST 上报 RILJ
-> EmergencyNumberTracker 合并 radio list、database、test list
-> Dialer/Telecom/Telephony 使用最终 EmergencyNumber list 判断拨号
```

MTK 关键代码证据：

| 代码位置 | 结论 |
|---|---|
| `vendor/mediatek/proprietary/external/EccList/EccList.mk` | `ecc_list*.xml` 通过 `PRODUCT_COPY_FILES` 复制到 vendor etc |
| `device/mediatek/vendor/common/device.mk` / `device/mediatek/common/device.mk` | include `EccList.mk`，确保产品继承 ECC List Customization |
| `vendor/mediatek/proprietary/hardware/ril/fusion/mtk-ril/telcore_mipc/cc/EccNumberSource.h` | 定义运行时路径 `/system/vendor/etc/ecc_list.xml`、OPTR 属性、`Condition` 和 source 枚举 |
| `.../telcore_mipc/cc/EccNumberSource.cpp` | `XmlEccNumberSource` 选择 OPTR 文件、解析 `EccEntry`、按 PLMN/SIM 状态过滤 |
| `.../telcore_mipc/cc/RtmEccNumberController.cpp` | 注册 PLMN/SIM/UICC/连接状态回调，合并 AP ECC list，sync 到 modem，再回报 Framework |
| `.../mdcomm_mipc/cc/RmmEccNumberRequestHandler.cpp` | AP ECC list 转成 `MIPC_CALL_SET_ECC_LIST_REQ`，modem ECC list 转成 `RFX_MSG_URC_EMERGENCY_NUMBER_LIST` |
| `vendor/mediatek/proprietary/packages/services/Telephony/src/com/mediatek/services/telephony/EmergencyNumberUtils.java` | AP 侧读取 `ecc_list_preference.xml`，判断 GSM/CDMA emergency RAT 偏好 |
| `frameworks/opt/telephony/src/java/com/android/internal/telephony/emergency/EmergencyNumberTracker.java` | 注册 radio emergency number list；`updateEmergencyNumberList()` 合并 database/radio/prefix/test，`getEmergencyNumberList()` 在 radio list 非空时返回合并后的 `mEmergencyNumberList`，radio list 为空时才回落到 legacy `ril.ecclist` + database/test |

### Qualcomm AP eccdata 与 QCRIL qcrilNr.db

AP database 链路：

```text
qssi/packages/services/Telephony/ecc/input/eccdata.txt
-> gen_eccdata.sh
-> ecc/output/eccdata
-> qssi/packages/services/Telephony/Android.bp asset_dirs: ["ecc/output"]
-> TeleService assets
-> GsmCdmaPhone 初始化 EmergencyNumberTracker
-> EmergencyNumberTracker assets.open("eccdata")
-> gzip 解压 + ProtobufEccData.AllInfo.parseFrom()
-> 按 countryIso 读取本地 database 号码
-> merge radio/database/prefix/test list
-> Dialer/Telecom/Telephony 使用最终 EmergencyNumber list 判断拨号
```

QCRIL database / radio list 链路：

```text
qcril_database/upgrade/other/*.sql
-> qcril_database/tools/gen_db.sh
-> qcrilNr.db
-> vendor/etc/qcril_database/qcrilNr.db
-> init.qcom.rc 拷贝到 /data/vendor/radio/qcrilNr_prebuilt.db
-> qcril_db_check_prebuilt_and_wait() / recovery 检查或恢复 /data/vendor/radio/qcrilNr.db
-> qcril_db_init() 建表/打开 DB
-> NAS 根据 SIM MCC/MNC、IMSI MCC、网络 MCC、service state 查询 qcril_emergency_source_* 表
-> RilPbmFillEccMap 填充 RIL ECC map，source = MODEM_CONFIG / DEFAULT
-> PbmModule / qmi_ril_send_ecc_list_indication()
-> 合并 PBM cache、RIL ECC map、network detected ECC
-> RilUnsolEmergencyListIndMessage
-> HIDL currentEmergencyNumberList 或 socket RIL_UNSOL_EMERGENCY_NUMBERS_LIST
-> EmergencyNumberTracker EVENT_UNSOL_EMERGENCY_NUMBER_LIST
-> Framework 合并 radio/database/test list
```

Qualcomm 关键代码证据：

| 代码位置 | 结论 |
|---|---|
| `qssi/packages/services/Telephony/Android.bp` | `asset_dirs` 包含 `ecc/output`，`TeleService` 会打入 AP emergency database |
| `qssi/packages/services/Telephony/ecc/conversion_toolset_v1/env.sh` | AP 侧输入 `input/eccdata.txt`，输出 `output/eccdata` |
| `qssi/frameworks/opt/telephony/.../EmergencyNumberTracker.java` | 从 assets 打开 `eccdata`；注册 `mCi.registerForEmergencyNumberList`；合并 radio/database/prefix/test list |
| `qssi/vendor/qcom/proprietary/commonsys/telephony-fwk/.../QtiEmergencyCallHelper.java` | Qualcomm 定制 emergency call 选 phoneId / stack，不是号码库配置入口 |
| `target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/Android.bp` | SQL 文件生成 `qcrilNr.db`，`qcrilNrDb_vendor` 打包到 vendor etc |
| `target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/src/qcril_db.cpp` | 定义 `qcril_emergency_source_*` 表，并根据 MCC/MNC 查询号码 |
| `target/vendor/qcom/proprietary/qcril-nr/modules/nas/src/qcril_qmi_nas.cpp` | 根据卡状态、SIM MCC/MNC、IMSI MCC、网络 MCC、service state 选择表并填 `RilPbmFillEccMap` |
| `target/vendor/qcom/proprietary/qcril-nr/modules/pbm/src/PbmModule.cpp` | 处理 `RilPbmFillEccMap` / `RilPbmSendEccListInd` |
| `target/vendor/qcom/proprietary/qcril-nr/modules/pbm/src/qcril_pbm.cpp` | 合并 PBM cache、RIL ECC map、network detected ECC，发 `RilUnsolEmergencyListIndMessage` 并兼容设置 `ril.ecclist` |
| `target/vendor/qcom/proprietary/qcril-nr/qcrild/libril/RilSocketIndicationModule.cpp` | socket RIL 路径发送 `RIL_UNSOL_EMERGENCY_NUMBERS_LIST` |
| `target/vendor/qcom/proprietary/qcril-nr/qcrild/libril/hidl_impl/1.4/radio_service_1_4.h` | HIDL 路径发送 `currentEmergencyNumberList` |

## 验证命令与 log

| 目标 | 命令 / 关键字 | 预期 |
|---|---|---|
| 确认 APK 内有生成物 | `adb shell pm path com.android.phone` 后 pull APK，再 `unzip -l <apk> | grep unieccdata` | APK assets 中存在 `unieccdata` |
| 确认运行时加载 asset DB | `adb logcat -b main -b radio`，过滤 `UniEmergencyNumberTracker` / `asset emergency database` / `cacheEmergencyDatabaseByCountry` | 看到加载版本、phoneId、countryIso |
| 确认 MNC 匹配 | log 关键字 `getMnc`、`updatedAssetEmergencyNumberListWithMnc` | 当前 MNC 与配置一致，且最终列表没有丢通用号码 |
| 确认卡状态过滤 | log 关键字 `isValidEccInfo: eccInfoCardFlag`，分别测有卡/无卡 | `with_card` 仅非 absent 生效，`no_card` 仅 absent 生效 |
| 确认最终号码池 | `adb shell dumpsys phone` 中查 `EmergencyNumberTracker` / `mEmergencyNumberList` | 最终列表包含预期号码、category、routing、source |
| 确认拨号路径 | AP log / radio log 查拨号号码、emergency routing、RIL 下发 | UI 识别、AP 判定、RIL/Modem 下发一致 |
| 区分真/假紧急 | radio log 查 `ATD<number>@<category>,#` 或 `ATD<number>` | 真紧急带 `@category,#`，假紧急按普通 ATD 拨出 |
| 确认 CS emergency setup | CS 通话 log 查 `EMERGENCY_SETUP` | 证明已经走 CS emergency call setup，不是普通 CS call |
| 确认 VoLTE ECC 网络能力 | Attach Accept / NAS / AS log 查 `ims_vops`、`emc_bs`、`isImsEmergencySupport` | 当前 LTE/IMS 环境具备 VoLTE emergency 条件，再继续看域选和 NV |
| 确认 N3GPP / VoWiFi ECC 条件 | IMS / IKE / Wi-Fi / WFC log 查 N3GPP 注册、WFC 开关、白名单、Wi-Fi 链路 | 不要把 N3GPP 注册失败误判为 ECC 号码库问题 |
| 网络下发号码 | radio log 查 `+CEN1/+CEN2`、`UNSOL_ECC_NETWORKLIST_CHANGED` | 证明号码来自网络，不应继续只改 `unieccdata` |
| FDN 场景假紧急 | log 查 `AT+SPCALLSETTING=1,0` | 若 RIL 支持假紧急绕 FDN，会先下发 fake emergency 标志再普通拨号 |
| MTK 确认 vendor XML 已入机 | `adb shell ls -l /vendor/etc/ecc_list* /system/vendor/etc/ecc_list*` | 目标 `ecc_list.xml` / `ecc_list_OPxx.xml` 存在 |
| MTK 确认 OPTR 文件选择 | `adb shell getprop persist.vendor.operator.optr` | 有值时优先尝试 `ecc_list_${optr}.xml`；文件不存在回落 `ecc_list.xml` |
| MTK 确认 RIL 属性和特殊 ECC | `adb shell getprop ril.ecclist`、`adb shell getprop vendor.ril.special.ecclist` | `ril.ecclist` 包含最终号码；`Condition=2` 且 SIM ready 时进入 special list |
| MTK 确认 sync 到 modem / 回报 Framework | radio log 关键字 `RtmEccNumberController`、`EccNumberSource`、`RmmEccNumber`、`MIPC_CALL_SET_ECC_LIST_REQ`、`RFX_MSG_URC_EMERGENCY_NUMBER_LIST` | 能看到 AP ECC list、MD ECC list、URC 上报 |
| Qualcomm 确认 AP DB 已入 APK | `unzip -l <TeleService.apk> | grep eccdata` | APK assets 中存在 `eccdata` |
| Qualcomm 确认 QCRIL DB 已入机 | `adb shell ls -l /vendor/etc/qcril_database/qcrilNr.db /data/vendor/radio/qcrilNr*` | vendor DB、prebuilt DB 和 active DB 存在，时间或 hash 符合本次构建 |
| Qualcomm 查询 QCRIL 表 | `adb shell sqlite3 /data/vendor/radio/qcrilNr.db "select * from qcril_emergency_source_mcc_table where MCC='450';"` | active DB 能查到目标 MCC/MNC/NUMBER 行；若查不到，再对比 `/data/vendor/radio/qcrilNr_prebuilt.db` 和 vendor DB |
| Qualcomm 确认 PBM/RIL 上报 | radio log 关键字 `qcril_db_is_mcc_part_of_emergency_numbers_table`、`RilPbmFillEccMap`、`QCRIL_SEND_ECC_LIST_IND`、`RIL_UNSOL_EMERGENCY_NUMBERS_LIST`、`currentEmergencyNumberList` | 能看到查库、填 map、发送 emergency list |
| Qualcomm 确认 legacy 属性 | `adb shell getprop ril.ecclist` | PBM 发送列表后兼容写入 `ril.ecclist`，可作为辅助证据 |

常用过滤命令：

```bash
adb logcat -b main -b radio | grep -iE "UniEmergencyNumberTracker|asset emergency database|cacheEmergencyDatabaseByCountry"
adb shell dumpsys phone | grep -iE "EmergencyNumberTracker|mEmergencyNumberList|EmergencyNumber"
adb logcat -b main -b radio | grep -iE "RtmEccNumberController|EccNumberSource|RmmEccNumber|MIPC_CALL_SET_ECC_LIST_REQ|RFX_MSG_URC_EMERGENCY_NUMBER_LIST"
adb logcat -b main -b radio | grep -iE "qcril_db_is_mcc_part_of_emergency_numbers_table|RilPbmFillEccMap|QCRIL_SEND_ECC_LIST_IND|RIL_UNSOL_EMERGENCY|currentEmergencyNumberList"
adb shell sqlite3 /data/vendor/radio/qcrilNr.db "select * from qcril_emergency_source_mcc_table where MCC='<mcc>';"
```

如果只看到源码已修改，但没有运行时 `UniEmergencyNumberTracker` 加载、没有最终号码池 dump，不能认为 ECC 配置已经生效。

### 配置不生效自查清单

旧导入资料里多次出现“源文件已改但设备不生效”的问题。遇到这类现象时，先按下面顺序切，不要先猜是网络侧或 Dialer 问题。

| 检查点 | 判断方法 |
|---|---|
| 改的是当前分支实际编译路径 | 同时搜索 AOSP `packages/services/Telephony/ecc`、UNISOC `apps/UniTelephony/uniecc`、`services/Telephony/uniecc`、MTK `external/EccList`、Qualcomm QCRIL SQL，确认 Android.bp / makefile 实际打包哪一份 |
| 生成物是否同步 | UNISOC 要有 `output/unieccdata`，AOSP / Qualcomm AP 要有 `ecc/output/eccdata`，Qualcomm QCRIL 要重新生成 `qcrilNr.db`，MTK 要确认 `/vendor/etc/ecc_list*.xml` |
| 模块是否重新打包 | 只 push 单个 APK / DB / XML 时要确认设备端实际替换成功并重启；量产分支优先看整机构建产物 |
| 字段是否被当前分支解析 | `card_flag`、`normal_routing_mncs`、MTK `Condition`、Qualcomm `SERVICE` 等字段要在目标分支代码里能找到解析链路 |
| 国家/PLMN 是否匹配 | `iso_code`、MCC/MNC、MNC、OPTR、network MCC、SIM MCC/MNC 都可能是不同匹配维度 |
| 运行时列表是否更新 | 看 `EmergencyNumberTracker` / `UniEmergencyNumberTracker` dump、RIL emergency list、PBM/QCRIL map、`ril.ecclist` 和拨号前最终判定 |

结论模板：

```text
当前只能证明配置文件已修改/生成物已更新，不能证明运行时已加载。
需要补充：设备端产物校验、EmergencyNumberTracker 最终号码列表、拨号前 AP 判定、RIL/Modem 下发命令和对应通话域证据。
```

## 非号码库配置项

下面这些配置会影响紧急呼叫行为，但不属于 AP emergency database（`eccdata` / `unieccdata`）或 vendor/RIL 号码表（MTK `ecc_list*.xml`、Qualcomm `qcrilNr.db`）本身，排查时不要混在一起改：

| 场景 | 配置项 / 关键字 | 版本边界 | 说明 |
|---|---|---|---|
| 紧急号码显示名称 | MTK / 项目客制化显示名资源，例如 `ecc_config_list.xml` / `config.xml`、`strings.xml`、`values-xx/strings.xml` | 路径强依赖项目客制化，必须以目标分支代码为准 | 只影响 UI 显示文案，不证明号码是否是 ECC，也不影响网络是否接通 |
| 通话记录显示紧急号码 | `allow_emergency_numbers_in_call_log_bool` | Android 12+ 可随卡配置 | CarrierConfig 随卡开关 |
| 通话记录显示紧急号码 | `allow_emergency_numbers_in_call_log` | Android 10/11 主要随版本，Android 12+ 也可随版本 | 任一开关满足时可显示 emergency call log |
| VoWiFi 下拨 ECC | `support_vowifi_ecall`、`ecall_on_vowifi_first`、`dial_ecall_vowifi_when_airplane_mode`、`retry_ecall_vowifi`、`retry_ecall_cellualr_network`、`deregister_vowifi_before_ecall`、`deregister_vowifi_when_cellular_preffered` | Android 12 之前 AP 侧方案相关 | Android 12 及之后展锐资料说明使用 CP 侧方案，不再走这些 Telephony key；其中 `cellualr`、`preffered` 按资料原文记录，落地前必须在目标分支搜索确认 key 名 |
| N3GPP / VoWiFi ECC 域选 | `OPERATOR_NV_MN\mn_vowifi_ecc\vowifi_ecc\vowifi_ecc[0]`、N3GPP 注册、WFC 白名单、Wi-Fi 链路 | CP / NV / IMS 方案相关 | 先证明 N3GPP 注册和 VoWiFi 能力成立，再判断 ECC 域选；这不是号码库新增/删除问题 |
| VoLTE ECC 域选 | `OPERATOR_NV_MN\mn_ecc_cs_only\ecc_cs_only\ecc_cs_only[0]`、`OPERATOR_NV_MN\mn_emc_need_csfb_when_roaming\emc_need_csfb_when_roaming\emc_need_csfb_when_roaming[0]`、`ims_vops`、`emc_bs`、`isImsEmergencySupport` | NV 随当前驻留 PLMN 或 SIM PLMN 生效，需按平台确认 | 控制是否允许 ECC over LTE/IMS 或漫游时是否回 CS；不要和号码是否存在混在一起 |
| 普通通话中拨 ECC | `allow_hold_call_during_emergency_bool` | `false` 全分支生效；`true` 只在部分 Android 11 分支生效 | `false` 先挂断普通电话再拨 ECC；`true` 保持普通电话同时拨 ECC |
| FDN 开启时拨假紧急 | `AT+SPCALLSETTING=1,0` | RIL 行为相关 | RIL 若加限制，只能拨 FDN 列表和真紧急；RIL 无限制时假紧急也可拨 |
| 飞行模式拨 ECC | `KEY_CARRIER_RADIO_POWER_ON_FOR_ECALL` | CarrierConfig 随 SIM 卡配置 | `true` 受限开协议栈，典型 `AT+SFUN=4,1,1`；`false` 正常开协议栈，典型 `AT+SFUN=4` |

这些 key 更适合放在 CarrierConfig / IMS / Call 专项里展开。本文只保留 ECC 排查时需要知道的边界和关键字。

## 常见失败模式

| 现象 | 优先检查 | 判断 |
|---|---|---|
| 修改后不生效 | A15/A16 路径是否改错、`output/unieccdata` 是否同步生成、APK 是否重编 | 第一坏点常在路径/生成物/打包 |
| 白卡验证通过但现场失败 | 白卡只验证 UI/本地列表，不能证明实网接通 | 国外紧急号码接通、无卡驻留、网络接受/拒绝必须靠现场或仪表证据 |
| 国家通用号码丢失 | 是否新增了当前 MNC 条目 | MNC 命中后会优先用 MNC 列表，需补齐该 MNC 下仍需保留的号码 |
| 无卡/有卡行为不符合预期 | `card_flag` 是否配置，SIM 状态是否真是 `ABSENT` | `with_card` 是非 absent，不只 SIM READY；PIN locked 也可能按有卡处理 |
| 把 `routing: 2` 当成无卡禁止 | routing 语义 | `routing: 2` 是 normal routing/假紧急，控制真/假紧急路由，不控制卡状态 |
| 把需求表显示名当号码配置 | 显示名资源和号码库是否分离 | UI 文案、通话记录、号码 source 是三条链路，必须分别验证 |
| 插卡拨 `110/120/119` 无法进入人工台 | source 优先级、真假紧急、category、对比机配置 | 优先确认是否应配置成假紧急或调整 category，而不是只判断号码是否存在 |
| SIM EF_ECC 号码未入池 | SIM 读取日志、EF_ECC category、source 是否为 `SIM` | 展锐资料提到 category `0xff` 也可能是合法 SIM 类别；若号码被过滤，优先确认合并逻辑是否排除了 `0xff` |
| MTK 改 `ecc_list.xml` 后不生效 | 是否打入 `/vendor/etc`、`persist.vendor.operator.optr` 是否选中了 OP 文件、PLMN 是否命中、是否触发 sync | 旧 XML 源码改了不等于运行时生效；先看 `AP ECC` / `MD ECC` log 和 `ril.ecclist` |
| MTK 国家级号码被运营商覆盖 | 同号是否有具体 `MCC MNC` 与 `MCC FFF/FF` 条目 | 同优先级下具体 MNC 条目会覆盖国家级条目的 category/condition |
| MTK `Condition=2` 行为误判 | SIM 状态、`vendor.ril.special.ecclist`、拨号 routing | SIM ready 时 special ECC 按 normal routing；无 SIM 时会转成 no-sim ECC |
| Qualcomm 改了 AP `eccdata` 但最终结果不符合预期 | `mEmergencyNumberListFromRadio` 是否非空、QCRIL/PBM 是否上报了同号、合并后 category/routing/source 是否被调整 | radio list 非空时 `getEmergencyNumberList()` 返回 database/radio/prefix/test 合并结果，不是简单“radio 覆盖 DB”；同号合并后需要查最终 `EmergencyNumber` 字段 |
| Qualcomm 改了 QCRIL SQL 但不生效 | `qcrilNr.db` 是否重新生成/打包，`qcrilNr_prebuilt.db` 和 active `qcrilNr.db` 是否更新 | 只改 SQL 不等于运行时 DB 更新；先查设备侧 active DB 内容，再对比 prebuilt/vendor DB |
| Qualcomm MCC/MNC 表配置错位 | 需求是国家级还是运营商级、SIM MCC/MNC 是否可取到、service state 是否 full/limited | `MCC_MNC` 表需要 SIM MCC/MNC 命中；`SERVICE` 为空/full/limited 生效条件不同 |
| Qualcomm 无卡或网络 MCC 场景缺号 | `qcril_emergency_source_hard_mcc_table`、`qcril_emergency_source_nw_table`、卡状态 | 无卡/hardcoded 与网络 MCC 不是普通 AP database 路径 |
| Qualcomm ESCV 配了但号码仍不出现 | 是否只改了 `escv_*` 表 | ESCV 表只给号码分类/类型，不一定新增 emergency number list 号码 |
| 飞行模式 ECC 失败 | `KEY_CARRIER_RADIO_POWER_ON_FOR_ECALL`、`AT+SFUN=4,1,1` / `AT+SFUN=4`、CP/AP 挂断方 | 受限开协议栈失败时可尝试正常开协议栈，再按 log 判断 CP 上报挂断还是 AP 主动挂断 |
| VoLTE / VoWiFi ECC 失败 | Android 版本边界、AP/CP 域选方案、挂断原因上报 | Android 12 前 AP 侧会处理重拨和域选择；Android 12 后展锐资料说明主要由 CP 控制 |
| 紧急通话界面显示其他号码 | `ImsPhoneConnection` / `GsmCdmaConnection` 的号码更新、底层 `CLCC/DSCI` 上报 | UI 显示可能跟随底层上报号码更新，不一定是 ECC 号码库配置错误 |
| 紧急电话结束后拨号器进程退出 | Google Dialer 位置权限回收、`am_kill ... permissions revoked` | 可能是权限撤销导致进程被系统结束，不一定是 telephony 崩溃 |
| 现场国家不匹配 | country ISO 来源、驻留网络、SIM MCC、最后一次 countryIso | `iso_code` 按 country 匹配，不是直接按 MCC/MNC 全量匹配 |
| 双卡/eSIM 无卡场景异常 | `needLoadDataBaseEccList()`、active subscription 数量、选中的 phoneId | 某些场景可能不加载本地 DB，需结合 phoneId 和 active subscription 判断 |
| 网络下发覆盖预期 | Radio emergency list、SIM EF_ECC、OTA DB 版本 | 最终号码池来自多来源合并，不只看本地 uniecc |

## 待补证据

- A15/A16 实机验证：需要一份改号后 log，确认 `UniEmergencyNumberTracker` 加载、MNC/card_flag 匹配、最终 `mEmergencyNumberList`。
- MTK 实机验证：需要一份改 `ecc_list.xml` 后的 AP/radio log，确认 `/vendor/etc/ecc_list*.xml`、OPTR 选择、`AP ECC` / `MD ECC`、`RFX_MSG_URC_EMERGENCY_NUMBER_LIST` 和最终 `EmergencyNumberTracker`。
- Qualcomm 实机验证：需要一份改 `qcrilNr.db` 后的 AP/radio log，确认设备侧 DB 内容、NAS 查表、`RilPbmFillEccMap`、`RIL_UNSOL_EMERGENCY_NUMBERS_LIST/currentEmergencyNumberList` 和最终 `EmergencyNumberTracker`。
- Qualcomm 官方配置文档：当前代码已能证明路径、表结构和加载链路；各 `qcril_emergency_source_*` 表在具体运营商需求中的官方推荐边界仍可后续用 Qualcomm 文档补强。
- OTA DB 刷写/触发来源：当前已确认 AOSP / Qualcomm AP 路径、版本选择和 UNISOC asset/OTA 合并逻辑；OTA 文件由谁下发、何时写入、项目是否启用仍需要目标项目证据。
- `ecc_fallback` 实机触发场景：proto 规则已确认，但当前本地代码只证明字段约束，未证明具体拨号场景一定会触发替换；需要后续真实案例或专项 log 验证。

## 来源记录

- `F:\展锐\102154__紧急呼叫配置及常见问题说明V1.3.pdf`：展锐紧急呼叫配置官方说明，文档版本 V1.3，发布日期 2025-05-20。当前仅记录本机来源路径，未作为可迁移附件入库；若后续需要共享知识库，应确认资料权限后再归档到附件目录。
- 旧 `ECC配置方法.md`：Outline / CQ 导入资料；已删除旧文件。本页已抽取需求表读法、显示名边界、配置不生效自查、域选证据和测试边界，未整段搬运旧图片/教程。
- `/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/vendor/mediatek/proprietary/external/EccList/ecc_list.xml`：MTK MP6 vendor RIL 侧 ECC List 配置入口。
- `/home/wx/Project/MP6/alps-release-b0.mp1.rc-tb-default/alps/vendor/mediatek/proprietary/hardware/ril/fusion/mtk-ril/telcore_mipc/cc/`：MTK ECC List 解析、合并、sync modem 和 Framework 回报代码来源。
- `/home/wx/Project/Common/SPRDROID16_SYS_MAIN_W25.22.4/alps/vendor/sprd/platform/frameworks/telephony-injection/uni-telephony-common/src/java/com/android/internal/telephony/emergency/UniEmergencyNumberTracker.java`：UNISOC A16 runtime 加载 `unieccdata`、MNC/card_flag 过滤、asset/OTA 合并和 phoneId / subscription 边界来源。
- `/home/wx/Project/Common/SPRDROID15_SYS_MAIN_W24.37.2_P1/alps/vendor/sprd/platform/frameworks/telephony-injection/uni-telephony-common/src/java/com/android/internal/telephony/emergency/UniEmergencyNumberTracker.java`：UNISOC A15 runtime 同名入口；路径已确认，细节按目标分支复查。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/emergency/EmergencyNumberTracker.java`：AOSP / Qualcomm AP `eccdata` asset 加载、OTA DB 路径、版本选择和 Framework emergency list 合并来源。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/qssi/packages/services/Telephony/ecc/input/eccdata.txt`：Qualcomm AP / AOSP emergency database 配置入口。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/`：Qualcomm QCRIL database、ECC SQL、`qcrilNr.db` 生成和打包来源。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/qcril-nr/qcril-common/qcril_database/src/qcril_db.cpp`：Qualcomm QCRIL ECC 表定义、source 到表名映射、MCC/MNC/service 查表和 prebuilt/active DB 恢复来源。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/qcril-nr/modules/nas/src/qcril_qmi_nas.cpp`：Qualcomm NAS 查 ECC 表、按 MCC/MNC/service state 投射号码的代码来源。
- `/home/wx/Project/QCOM/qcom4490/S1E4ProPlus/target/vendor/qcom/proprietary/qcril-nr/modules/pbm/src/`：Qualcomm PBM 合并 ECC map 并上报 RIL emergency list 的代码来源。

## 关联案例

| Case | 复用点 |
|---|---|
| [ECC_UNISOC_routing不控制无卡禁止_card_flag](../../40_Case-Library/Call/2022-07-30_ECC_UNISOC_routing不控制无卡禁止_card_flag.md) | 区分 `routing` 与 `card_flag` |
| [ECC_UNISOC_PIN未解锁EF_ECC与无卡ECC分类](../../40_Case-Library/Call/2021-06-04_ECC_UNISOC_PIN未解锁EF_ECC与无卡ECC分类.md) | PIN locked 不等同无卡 |
| [ECC_UNISOC_无卡紧急呼叫选到eSIM卡槽失败](../../40_Case-Library/Call/2025-12-10_ECC_UNISOC_无卡紧急呼叫选到eSIM卡槽失败.md) | 无卡 ECC 还要看 phoneId / slot 选择 |
| [LA Réunion重定向](../../40_Case-Library/Call/Imported_Call_03_LA_Réunion重定向.md) | 本地 ECC 配置和 fallback 导致号码重定向 |

## 维护要求

- UNISOC / MTK / Qualcomm 配置方法以后优先维护本文；旧 `ECC配置方法.md` 已删除，不再作为入口维护。
- 每次补配置值时同时写清：输入文件、生成物、编译目标、运行时 dump/log 证据。
- 没有代码证据或实机证据的行为只写“待确认”，不要写成配置结论。
