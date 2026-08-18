下面按调用链列出。你在其他 Android/QCOM 代码中，优先搜索右侧的方法名或常量，文件名可能随 Android 版本变化。

## 1. Settings 一级“SIM 卡”入口

源码根：

```
qssi/packages/apps/Settings/
```

| 作用                  | 本项目路径                                                                                              | 关键字                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| “网络和互联网”页面定义 SIM 入口 | `qssi/packages/apps/Settings/res/xml/network_provider_internet.xml`                                | `mobile_network_list`                                              |
| 控制 SIM 入口显示、启用和跳转   | `qssi/packages/apps/Settings/src/com/android/settings/network/MobileNetworkSummaryController.java` | `isAvailable()`、`showEuiccSettingsDetecting()`、`startAddSimFlow()` |
| 判断是否显示所有 SIM 相关 UI  | `qssi/packages/apps/Settings/src/com/android/settings/network/SubscriptionUtil.java`               | `isSimHardwareVisible()`                                           |
| SIM UI 总开关          | `qssi/packages/apps/Settings/res/values/config.xml`                                                | `config_show_sim_info`                                             |

本项目配置：

```
<bool name="config_show_sim_info">true</bool>
```

一级入口的主要条件在：

```
MobileNetworkSummaryController.isAvailable()
```

包含：

```
config_show_sim_info=true
非 Wi-Fi-only 设备
当前用户为 Admin User
```

---

## 2. “添加 SIM 卡”菜单

|作用|路径|关键字|
|---|---|---|
|“添加 SIM 卡”菜单 XML|`qssi/packages/apps/Settings/res/xml/network_provider_sims_list.xml`|`add_sim`|
|控制“添加 SIM 卡”是否可见|`qssi/packages/apps/Settings/src/com/android/settings/network/MobileNetworkListFragment.java`|`KEY_ADD_SIM`、`showEuiccSettings()`|
|Android 老版本的列表控制器|`qssi/packages/apps/Settings/src/com/android/settings/network/MobileNetworkListController.java`|`KEY_ADD_MORE`、`showEuiccSettings()`|
|eSIM Settings 核心显示判断|`qssi/packages/apps/Settings/src/com/android/settings/network/telephony/MobileNetworkUtils.java`|`showEuiccSettings()`、`showEuiccSettingsDetecting()`|
|当前国家是否支持 eSIM|同一个 `MobileNetworkUtils.java`|`isCurrentCountrySupported()`|

最核心的是：

```
qssi/packages/apps/Settings/src/com/android/settings/network/telephony/MobileNetworkUtils.java
```

需要重点搜索：

```
showEuiccSettings()
showEuiccSettingsDetecting()
isCurrentCountrySupported()
```

以及这些常量：

```
Settings.Global.EUICC_PROVISIONED
DevelopmentSettingsEnabler.isDevelopmentSettingsEnabled()
ro.boot.cid
ro.setupwizard.esim_cid_ignore
esim.enable_esim_system_ui_by_default
```

“添加 SIM 卡”点击后发送：

```
EuiccManager.ACTION_PROVISION_EMBEDDED_SUBSCRIPTION
```

对应 XML：

```
<intent android:action=
    "android.telephony.euicc.action.PROVISION_EMBEDDED_SUBSCRIPTION"/>
```

---

## 3. `EuiccManager.isEnabled()` 判断

源码根：

```
qssi/frameworks/base/
qssi/frameworks/opt/telephony/
```

|作用|路径|关键字|
|---|---|---|
|Android eSIM 公共接口|`qssi/frameworks/base/telephony/java/android/telephony/euicc/EuiccManager.java`|`isEnabled()`|
|刷新默认 eUICC cardId|同一个文件|`refreshCardIdIfUninitialized()`|
|获取 eUICC Controller Binder|同一个文件|`getIEuiccController()`|
|TelephonyManager 获取默认 eUICC cardId|`qssi/frameworks/base/telephony/java/android/telephony/TelephonyManager.java`|`getCardIdForDefaultEuicc()`|
|Framework 内部维护默认 eUICC cardId|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/uicc/UiccController.java`|`getCardIdForDefaultEuicc()`、`mDefaultEuiccCardId`|

核心判断：

```
return getIEuiccController() != null
        && refreshCardIdIfUninitialized();
```

对应路径：

```
qssi/frameworks/base/telephony/java/android/telephony/euicc/EuiccManager.java
```

注意：

```
UNINITIALIZED_CARD_ID
```

会导致 `isEnabled()` 返回 false。

但：

```
UNSUPPORTED_CARD_ID
```

出于旧 HAL 兼容性，不一定导致 `isEnabled()` 返回 false。

---

## 4. eUICC Framework 服务初始化

|作用|路径|关键字|
|---|---|---|
|根据 Feature 初始化 EuiccController|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/PhoneFactory.java`|`FEATURE_TELEPHONY_EUICC`、`EuiccController.init()`|
|Framework eSIM 控制器|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/euicc/EuiccController.java`|`init()`、`register(this)`|
|eUICC 卡级接口|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/euicc/EuiccCardController.java`|`init()`|
|Subscription 与 eSIM Profile 回流|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/subscription/SubscriptionManagerService.java`|`FEATURE_TELEPHONY_EUICC`、`updateEmbeddedSubscriptions()`|

入口在：

```
qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/PhoneFactory.java
```

判断逻辑：

```
if (hasSystemFeature(PackageManager.FEATURE_TELEPHONY_EUICC)) {
    EuiccController.init(context);
    EuiccCardController.init(context);
}
```

所以没有：

```
android.hardware.telephony.euicc
```

就不会注册 `EuiccController` Binder。

---

## 5. eUICC Feature 和 SKU 判断

|作用|路径|关键字|
|---|---|---|
|eUICC Feature XML|`qssi/frameworks/native/data/etc/android.hardware.telephony.euicc.xml`|`android.hardware.telephony.euicc`|
|MEP Feature XML|`qssi/frameworks/native/data/etc/android.hardware.telephony.euicc.mep.xml`|`android.hardware.telephony.euicc.mep`|
|本项目拷贝配置|`target/device/castles/qdt676/qdt676.mk`|`sku_qdt676_sku1`|
|Framework 读取 SKU 专用目录|`qssi/frameworks/base/services/core/java/com/android/server/SystemConfig.java`|`SKU_PROPERTY`、`skuDir`|
|Feature 对外常量|`qssi/frameworks/base/core/java/android/content/pm/PackageManager.java`|`FEATURE_TELEPHONY_EUICC`|

本项目配置：

```
target/device/castles/qdt676/qdt676.mk
```

目标位置：

```
/odm/etc/permissions/sku_qdt676_sku1/
    android.hardware.telephony.euicc.xml
```

Framework 使用的属性：

```
ro.boot.product.hardware.sku
```

对应源码：

```
qssi/frameworks/base/services/core/java/com/android/server/SystemConfig.java
```

搜索：

```
private static final String SKU_PROPERTY =
        "ro.boot.product.hardware.sku";
```

---

## 6. LPA 后台服务选择

|作用|路径|关键字|
|---|---|---|
|查找和绑定 EuiccService|`qssi/frameworks/opt/telephony/src/java/com/android/internal/telephony/euicc/EuiccConnector.java`|`findBestComponent()`|
|检查 LPA 合法性|同一个文件|`isValidEuiccComponent()`|
|查看实际选中的 LPA|同一个文件|`mSelectedComponent`|
|Android LPA 服务接口定义|`qssi/frameworks/base/telephony/java/android/service/euicc/EuiccService.java`|`EUICC_SERVICE_INTERFACE`|

`EuiccConnector` 会检查：

```
LPA 拥有 WRITE_EMBEDDED_SUBSCRIPTIONS
EuiccService 要求 BIND_EUICC_SERVICE
intent-filter priority 不得为 0
选择 priority 最大的服务
```

关键方法：

```
findBestComponent()
isValidEuiccComponent()
createBinding()
```

运行时通过：

```
adb shell dumpsys euicc
```

查看：

```
mSelectedComponent=
mEuiccService=
```

---

## 7. 本项目 LinksField LPA 配置

|作用|路径|
|---|---|
|将 LinksFieldLPA 加入 QSSI 产品|`qssi/vendor/mobiiot/system_device.mk`|
|LinksFieldLPA APK 编译定义|`qssi/vendor/mobiiot/apps/LinksFieldLPA/Android.mk`|
|LinksFieldLPA APK|`qssi/vendor/mobiiot/apps/LinksFieldLPA/LinksFieldLPA.apk`|
|QSSI 引入 Mobiiot 产品配置|`qssi/device/qcom/qssi/qssi.mk`|

模块定义：

```
PRODUCT_PACKAGES += LinksFieldLPA
```

APK 内对应类：

```
后台：
com.linksfield.android.euicc.impl.EuiccServiceImpl

管理/下载界面：
com.linksfield.android.euicc.activity.lui.LUIActivity
```

APK Manifest 中建议搜索：

```
android.service.euicc.EuiccService
android.service.euicc.action.MANAGE_EMBEDDED_SUBSCRIPTIONS
android.service.euicc.action.PROVISION_EMBEDDED_SUBSCRIPTION
android.service.euicc.category.EUICC_UI
```

---

## 8. Qualcomm LPA 服务

|作用|路径|
|---|---|
|Qualcomm LPA 产品包声明|`qssi/vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/prebuilt.mk`|
|Qualcomm LPA APK 编译定义|`qssi/vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/Android.mk`|
|Qualcomm LPA APK|`qssi/vendor/qcom/proprietary/prebuilt_HY11/target/product/qssi/product/app/uimlpaservice/uimlpaservice.apk`|
|LPA Framework HIDL 接口|`qssi/vendor/qcom/proprietary/commonsys-intf/telephony/interfaces/hal/lpa/`|
|LPA Framework AIDL 接口|`qssi/vendor/qcom/proprietary/commonsys-intf/telephony/interfaces/aidl/lpa/`|

Qualcomm APK 的包名：

```
com.qualcomm.qti.lpa
```

EuiccService：

```
com.qualcomm.qti.lpa.QtiEuiccServiceImpl
```

本项目 LinksField 和 Qualcomm `EuiccService` 都声明了 priority 100，需要运行时确认最终选择。

---

## 9. LPA UI Intent 转发

Settings 发出的 public action 不会直接启动 LinksField，而是先进入 Telephony：

|作用|路径|关键字|
|---|---|---|
|Public eSIM Action 注册|`qssi/packages/services/Telephony/AndroidManifest.xml`|`PROVISION_EMBEDDED_SUBSCRIPTION`|
|转发到实际 LPA UI|`qssi/packages/services/Telephony/src/com/android/phone/euicc/EuiccUiDispatcherActivity.java`|`createLuiIntent()`|
|eSIM 错误解决界面转发|`qssi/packages/services/Telephony/src/com/android/phone/euicc/EuiccResolutionUiDispatcherActivity.java`|`EuiccService.ACTION_RESOLVE`|

调用链是：

```
Settings
→ EuiccManager public action
→ com.android.phone.EuiccUiDispatcherActivity
→ EuiccService internal action
→ LinksField LUIActivity
```

---

## 10. 有 Profile 后的显示与管理

|作用|路径|关键字|
|---|---|---|
|SIM/eSIM 列表构造|`qssi/packages/apps/Settings/src/com/android/settings/network/NetworkProviderSimsCategoryController.java`|`SubscriptionInfo`|
|获取可显示 Subscription|`qssi/packages/apps/Settings/src/com/android/settings/network/SubscriptionUtil.java`|`getAvailableSubscriptions()`|
|eSIM Profile 判断|`qssi/frameworks/base/telephony/java/android/telephony/SubscriptionInfo.java`|`isEmbedded()`|
|单个 Profile 设置页面|`qssi/packages/apps/Settings/src/com/android/settings/network/telephony/MobileNetworkSettings.java`|`mSubId`|
|Profile 设置页面 XML|`qssi/packages/apps/Settings/res/xml/mobile_network_settings.xml`|`erase_sim`|
|删除 eSIM Profile 的显示条件|`qssi/packages/apps/Settings/src/com/android/settings/network/telephony/DeleteSimProfilePreferenceController.java`|`info.isEmbedded()`|
|删除 Profile 操作|`qssi/packages/apps/Settings/src/com/android/settings/network/telephony/DeleteEuiccSubscriptionSidecar.java`|`deleteSubscription()`|

关键判断：

```
if (info.getSubscriptionId() == subscriptionId
        && info.isEmbedded()) {
    // 显示 eSIM 删除/管理项
}
```

---

## 11. “清除 eSIM”菜单

这不是 Profile 管理入口，而是恢复设置入口：

|作用|路径|
|---|---|
|“清除 eSIM”菜单 XML|`qssi/packages/apps/Settings/res/xml/reset_dashboard_fragment.xml`|
|显示条件|`qssi/packages/apps/Settings/src/com/android/settings/network/EraseEuiccDataController.java`|
|确认和执行|`qssi/packages/apps/Settings/src/com/android/settings/network/EraseEuiccDataDialogFragment.java`|

主要条件：

```
config_show_sim_info=true
用户没有移动网络管理限制
存在 android.hardware.telephony.euicc Feature
```

## 在其他代码中快速搜索

进入其他 Android 源码根目录后执行：

```
rg -n \
  "showEuiccSettings|showEuiccSettingsDetecting|isCurrentCountrySupported" \
  packages/apps/Settings
```

```
rg -n \
  "ACTION_PROVISION_EMBEDDED_SUBSCRIPTION|ACTION_MANAGE_EMBEDDED_SUBSCRIPTIONS" \
  packages frameworks
```

```
rg -n \
  "FEATURE_TELEPHONY_EUICC|android.hardware.telephony.euicc" \
  frameworks packages device vendor
```

```
rg -n \
  "EUICC_PROVISIONED|enable_esim_system_ui_by_default|esim_cid_ignore" \
  frameworks packages device vendor
```

```
rg -n \
  "getCardIdForDefaultEuicc|mDefaultEuiccCardId|UNINITIALIZED_CARD_ID" \
  frameworks
```

```
rg -n \
  "findBestComponent|mSelectedComponent|BIND_EUICC_SERVICE" \
  frameworks packages vendor
```

对比其他平台时，建议依次追：

```
Settings 菜单
→ EuiccManager.isEnabled()
→ FEATURE_TELEPHONY_EUICC
→ EuiccController
→ UiccController/default cardId
→ EuiccConnector/LPA
→ SubscriptionInfo.isEmbedded()
```