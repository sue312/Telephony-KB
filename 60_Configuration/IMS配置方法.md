---
doc_type: config
domain: Configuration
status: active
quality: curated
---

# IMS配置方法

## 速查结论

- IMS 注册问题先分清：没有发起 IMS PDN、IMS PDN 建立失败、SIP REGISTER 被拒、SIP 成功但 AP 回调异常。
- AP 侧 VoLTE/VoWiFi 开关为 true，只代表能力门控允许，不代表 modem IMC 条件、SBP、IMS profile 或网络签约满足。
- MTK 项目遇到“LTE 正常但无 IMS PDN”时，重点查 `IMC_REG_CHECK_*`、SBP ID、DSBP/CXP mapping 和运营商支持状态。
- VoWiFi 注册失败如果卡在 IKE/ePDG，不要继续追 SIP；先看 IKE proposal、完整性算法、ePDG 地址和网络环境。
- SIP 403 要看响应文本。`IMEI check failed` 这类字段优先按运营商侧 IMEI 备案/白名单处理。


<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| CarrierConfig / IMS profile | VoLTE/VoWiFi/VoNR/SMS over IMS 开关 | `dumpsys carrier_config`、IMS service log |
| MTK SBP / DSBP / CXP | 运营商支持状态、IMC 条件 | `AT+EIMSCFG`、IMC / SBP log |
| modem / IMS APN | P-CSCF、IMS PDN、IKE/ePDG、SIP | modem IMS/SIP/IWLAN trace |
| AP IMS service | 注册状态、MMTel capability、feature update | `dumpsys ims`、radio/IMS log |

### 匹配与生效链路

```text
运营商 / SIM / CarrierConfig / IMS profile
-> AP IMS service 和 modem IMC 判定能力
-> 建 IMS PDN 或 IWLAN/ePDG
-> SIP REGISTER
-> MMTel / SMS / VoWiFi / ViLTE capability
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
| 源配置存在 | CarrierConfig / SBP/DSBP/CXP / IMS profile / UA | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | dumpsys ims、ImsService log、AT+EIMSCFG | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | SIP、IKE、IMS bearer、IMS modem trace | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

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
| LTE 正常但不发 IMS PDN | SBP/DSBP/CXP、allow_ims、MCCMNC whitelist | IMS 配置门控早于 SIP |
| SIP 403 | IMEI/签约/P-CSCF/realm/profile | 网络拒绝和本地配置要用 SIP response 区分 |
| VoWiFi 不注册 | IKE/ePDG、Wi-Fi 网络、IMS profile | 没有 IKE 证据时不直接判 SIP |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 专题定位

IMS 文档主线只回答四件事：能力门控是否放行、IMS PDN 是否建立、SIP / IKE 是否成功、失败时先查哪一层。

本文保留 MTK SBP / CXP、VoWiFi IKE、SIP 403 等历史证据；可复用结论优先沉淀到 `40_Case-Library`、平台代码入口或专题下的常见失败模式。

## 主线速查

| 问题 | 优先入口 |
|---|---|
| 能力是否放行 | CarrierConfig、IMS profile、Settings 开关 |
| IMS PDN 是否起来 | APN、P-CSCF、IMC 条件、SBP / DSBP / CXP |
| SIP / IKE 是否成功 | SIP REGISTER、IKE/ePDG、IMS trace |
| 失败先查哪层 | 网络签约、运营商支持状态、modem profile、AP 日志 |

## 迁入资料

以下内容保留平台差异、关键日志和操作边界，适合追溯和复核。

## IMS注册配置分层

| 层级 | 检查项 | 典型证据 |
|---|---|---|
| AP 能力门控 | CarrierConfig、Settings 开关、IMS service 能力 | `carrier_volte_available_bool`、`config_device_volte_available`、IMS callback |
| IMS APN / PDU | IMS APN、P-CSCF、IP、DNS | PDN connectivity request、PCO、P-CSCF |
| Modem IMS profile | VoLTE/VoWiFi/ViLTE/SMS/UT profile | `AT+EIMSCFG`、profile/NV/MDDB |
| MTK SBP / DSBP | operator code、SBP ID、CXP/OPDB mapping | `ccci_mdinit`、`L4BSBP`、`PROTOCOL_2 SBP ID` |
| IMC 注册条件 | MCC/MNC whitelist、VOPS、SIM/ISIM | `IMC_REG_CHECK_*` |
| IMS Core | SIP REGISTER、401、403、408、503 | SIP response、Warning、Reason |

## MTK SBP / DSBP / CXP

### 概念边界

| 概念 | 作用 | 常见来源 |
|---|---|---|
| CCCI SBP ID | AP 在 modem 启动阶段传给 modem 的项目级 SBP ID | `MTK_MD_SBP_CUSTOM_VALUE`、`ro.vendor.mtk_md_sbp_custom_value` |
| SIM SBP ID / DSBP | 根据插入 SIM 的 PLMN / OPDB / CXP 动态匹配运营商 SBP | `AT+EDSBP`、`L4BSBP`、CXP operator map |
| OP load / OM load | 运营商定制版本或公开市场版本 | `OPTR_SPEC_SEG_DEF`、`MTK_MD_SBP_CUSTOM_VALUE` |
| CXP | AP 侧 Carrier Express 运营商包 / mapping | `CarrierExpress/res/values/strings.xml` |

判断模板：

```text
LTE 注册正常，但 IMS PDN 没有发起。
AP IMS 能力已打开，IMC 检查失败于 MNCMCC whitelist。
当前 SBP ID 为 0，目标 PLMN 未匹配到支持 IMS 的 SBP。
第一坏点在 MTK SBP/运营商支持状态，不在 LTE 注册。
```

### 关键日志

```text
ccci_mdinit: PRJ_SBP_ID ... using default value
ccci_mdinit: Get: usp_sbp=-1, cip_sbp=0, project_sbp=0, nvram_sbp=0, set sbp=0
AT+EDSBP=2
[L4BSBP] PLMN ID=43211
[L4BSBP] PLMN ID (43211) not matched!
[L4BSBP] OPDB PLMN ID(43211) => SBP ID(0, SBP_ID_OM)
PROTOCOL_2 SBP ID = 0
```

IMC 条件失败：

```text
[IMC-REG] ims_support:1
[IMC-REG] sim->priv.nw_ims_vops: (1)
[IMC-REG] Operator code = 0, IMSI-MNC:11, IMSI-MCC:432
[IMC-REG] imc_check_mncmcc_whitelist()
[IMC-REG] Normal REG condition check result: IMC_REG_CHECK_MNCMCC_FAILED
```

项目固定 SBP 的验证日志：

```text
ccci_mdinit: PRJ_SBP_ID value: 147 for md1
ccci_mdinit: Get: usp_sbp=-1, cip_sbp=0, project_sbp=147, nvram_sbp=0, set sbp=147
PROTOCOL_2 SBP ID = 147
```

### 配置风险

| 方案 | 适用性 | 风险 |
|---|---|---|
| `AT+ECFGSET` / `AT+ESBP` 手动设置 | 实验室快速验证 | 插拔卡后可能被覆盖；商用风险高 |
| 固定 `MTK_MD_SBP_CUSTOM_VALUE` | 单运营商或专用项目 | 其他 SIM 的 IMS、会议、补充业务可能异常 |
| SBP custom mapping NV | 取决于 modem baseline | LR12A / LR13 等版本支持差异需实测 |
| CXP / DSBP mapping | 更接近量产方案 | 需要 AP/operator package 和 modem 支持一致 |
| MTK patch / eService | 正式方案 | 依赖 MTK 支持状态、项目基线和交付周期 |

## VoWiFi IKE配置

VoWiFi 注册链路中，IKE/ePDG 在 SIP REGISTER 之前。IKE 失败时不应继续追 IMS Core。

关键日志：

```text
MSG_ID_CMCP_HANDOVER_TO_VOWIFI_REQ
MSG_ID_IKE_ATTACH_REQ
IKE: nv: ike_intg = 18
IKE: cfg: ike_integ_alg=18
IKE_SessCheckAlgorithms unsupported integ algo:18
IKE: Session start failed!
MSG_ID_IKE_ATTACH_FAILED
```

检查项：

| 检查项 | 说明 |
|---|---|
| IKE 完整性算法 | `ike_intg` / `ike_integ_alg` 是否为平台支持值 |
| IKE 加密算法 | proposal 是否与网络 / ePDG 匹配 |
| ePDG 地址 | DNS / FQDN / 国家和 PLMN 选择是否正确 |
| Wi-Fi 网络 | 是否阻断 UDP 500/4500、NAT-T、DNS |
| IMS over IWLAN | IKE 成功后再看 IMS REGISTER |

## SIP 403判断

SIP 403 不能只写“网络拒绝”，要保留响应文本。

| 403 文本 | 优先方向 |
|---|---|
| `IMEI check failed` | 运营商 IMEI 备案 / 白名单 |
| `Forbidden` 无更多字段 | 签约、IMS profile、IMPI/IMPU、运营商策略 |
| USSD / USSI 403 | 运营商是否支持 IMS USSD，必要时回 CS |

## 最小证据包

```text
AP radio/main log
CarrierConfig dump
IMS APN / P-CSCF / PDN log
AT+EIMSCFG 或平台 IMS profile
MTK ccci_mdinit / L4BSBP / IMC-REG log
SIP REGISTER / 401 / 403 / 200
VoWiFi: IKE / ePDG / Wi-Fi 环境
对比机或运营商支持状态
```

## 关联案例

- [[../40_Case-Library/IMS/Imported_IMS_01_HMD场测反馈_VoLTE_注册_403]]
- [[../40_Case-Library/IMS/Imported_IMS_02_Iran_无法注册IMS问题]]
- [[../40_Case-Library/IMS/Imported_IMS_03_6032+_Spark反馈WFC注册有问题]]
- [[../40_Case-Library/IMS/2025-07-29_IMS_SMS-over-IP配置缺失]]
