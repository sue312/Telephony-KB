---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# IMS Cases

## 快速定位

- 先按现象、第一坏点、平台、配置项四个维度归类，再回看截图和关键 log。
- 复用案例时不要只套结论，需要确认版本、运营商、卡类型、开关默认值和最终生效配置。
- 案例里的图片已本地化，适合直接在 HTML 中对照字段和流程位置。

IMS、VoLTE、VoWiFi、VoNR、SMS over IMS、UT、视频通话相关 case 放这里。

## 已整理案例

| Case | 场景 | 用途 |
|---|---|---|
| [[Imported_IMS_01_HMD场测反馈_VoLTE_注册_403]] | VoLTE 注册返回 403 `IMEI check failed` | 区分运营商 IMEI 备案拒绝和本地 IMS 配置问题 |
| [[Imported_IMS_02_Iran_无法注册IMS问题]] | LTE 正常但 MTK 不发起 IMS PDN | 按 IMC 条件、SBP/DSBP/CXP 和 MNCMCC whitelist 定位 |
| [[Imported_IMS_03_6032+_Spark反馈WFC注册有问题]] | VoWiFi IKE 建链失败 | 用 `unsupported integ algo` 定位 IKE 配置错误 |
| [[2026-09-03_VoWiFi_UNISOC_41903_PRF密钥展开截断导致IKE_AUTH解密失败]] | 41903 VoWiFi 首个 IKE_AUTH 解密失败 | 区分网络报文异常与终端 PRF+ 密钥展开截断 |
| [[2025-07-29_IMS_SMS-over-IP配置缺失]] | 运营商要求 SMS over IP，但域选择或 IMS profile 未打开 | SMS over IP 配置和域选择闭环 |
| [[2025-W20_IMS_SMS短码CTS配置不匹配]] | CTS 短码分类和项目 XML 不匹配 | 对齐 `sms_short_codes.xml` 与 CTS 版本 |
| [[Imported_Call_05_RTT_通话]] | RTT over VoWiFi | 区分 Dialer RTT 入口能力和底层 IMS/VoWiFi RTT 承载 |
| [[Imported_Call_10_DUT视频通话闪退]] | ViLTE 视频通话闪退 | QCI2 dedicated bearer、video resolution 和 AP 崩溃补证模板 |
| [[Imported_Call_11_DUT视频通话卡死]] | ViLTE 视频通话卡死 | modem 媒体流正常时转 AP media/render/UI 补证 |


## 已拆分旧 Outline 案例

| Case | 原始分类 | 用途 |
|---|---|---|
| [[Imported_IMS_01_HMD场测反馈_VoLTE_注册_403]] | IMS 注册 403 | 已精修为 SIP 403 / IMEI check failed 样例 |
| [[Imported_IMS_02_Iran_无法注册IMS问题]] | IMS 注册问题 | 已精修为 MTK SBP / MNCMCC whitelist 样例 |
| [[Imported_IMS_03_6032+_Spark反馈WFC注册有问题]] | VoWiFi 注册问题 | 已精修为 IKE 完整性算法配置样例 |
| [[../Registration/2025-07-16_Registration_UNISOC_UECapability缺少2G能力_网络模式客制化]] | 能力上报问题 | 已迁入 Registration / 网络模式客制化 |

建议命名：

```text
YYYY-MM-DD_IMS_现象_根因.md
YYYY-MM-DD_VoLTE_现象_根因.md
YYYY-MM-DD_VoWiFi_现象_根因.md
```


## 外部检索资料

- [[2026-05-27_BEEONE_External-Cases_Summary|BEEONE/ALPS 案例汇总（外部可检索片段）]] - 待登录 eService 后补齐原始 case 链路
