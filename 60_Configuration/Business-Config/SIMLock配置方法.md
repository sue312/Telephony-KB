---
doc_type: config
domain: Configuration
status: active
quality: curated
search_tier: supplemental
feature: SIMLock
layer: AP/Modem/Build/NV
---

# SIMLock配置方法

## 阅读入口

这篇回答 SIMLock / 锁网怎么配置、怎么确认生效、第一坏点怎么切。真实问题样例看 [SIMLock锁网不生效：产物错误](../../40_Case-Library/Registration/2025-W21_Registration_SIMLock锁网不生效_产物错误.md) 和 [SimLock锁卡状态MCCMNC为空](../../40_Case-Library/SIM/2024-04-12_SIM_UNISOC_SimLock锁卡状态MCCMNC为空.md)。


<!-- CONFIG_TEMPLATE_BLOCK_START -->
## 模板化定位

### 配置来源

| 来源 | 本文落点 | 运行时验证 |
|---|---|---|
| modem SIMLock 配置 | 白名单、锁类型、剩余次数、锁卡策略 | modem log、锁卡状态、AT/NV 读取 |
| AP UI / Telephony | 锁卡弹框、SubInfo、MCC/MNC 显示 | radio log、Settings/Telephony log |
| 编译产物 | modem image、operator NV、市场版本 | PAC/out 对比、产物时间戳 |

### 匹配与生效链路

```text
锁网白名单 / modem profile
-> 编译或下载进入 modem 产物
-> 插卡后 modem 判锁
-> AP 同步锁卡状态和 UI
-> 注册允许或拒绝
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
| 源配置存在 | modem SIMLock 配置 / 白名单 / 解锁策略 / AP UI | 能定位到需求字段、默认值和项目覆盖值 |
| 运行时 dump 生效 | SIMLock service log、锁网状态、卡槽状态 | 设备当前值与预期配置一致 |
| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |
| modem/协议侧采用 | modem lock result、PLMN allow/deny、NV readback | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |

### 关联入口

| 入口 | 用途 |
|---|---|
| [配置目录 README](../README.md) | 回到配置分类和放置规则 |
| [Case横向索引](../../40_Case-Library/Case横向索引.md) | 查历史同类问题和第一坏点 |
| [平台代码入口](../../50_Platform-Code/README.md) | 查厂商代码读取位置 |
| [常用命令](../../70_Tools-Debug/Commands/常用命令.md) | 查 dumpsys、logcat 和 adb 命令 |

### 常见失败模式

| 现象 | 优先检查 | 第一坏点判断 |
|---|---|---|
| 非白名单卡仍可驻网 | modem 产物是否含锁网配置 | 第一坏点通常在产物链路，不是 AP UI |
| AP 显示 MCC/MNC 为空 | 锁卡状态下是否允许读卡 | 不等于 SIM 读卡失败 |
| 升级后锁网失效 | modem image / NV 是否被替换 | 先查版本和产物一致性 |
<!-- CONFIG_TEMPLATE_BLOCK_END -->
## 一句话

锁网问题既可能是 SIM/网络策略，也可能是 modem 产物或编译流水线问题。现象是“不弹锁网界面、非白名单卡可驻网”时，不能只查 AP UI。

## 定位链路

| 阶段 | 关键问题 |
|---|---|
| 需求 | 白名单/黑名单、运营商、地区、卡类型规则是否明确 |
| 配置 | SIMLock 配置是否进入目标项目/运营商版本 |
| 产物 | 市场 modem 和基础版本 modem 是否应该不同 |
| 编译 | 服务器是否生成并拷贝正确 modem image |
| 运行 | 插入非白名单卡后 modem/AP 是否识别锁网状态 |
| UI | 锁网界面是否由 AP 正确弹出 |

## 编译产物检查

| 字段 | 说明 |
|---|---|
| `MTK_TARGET_PROJECT` | 主设备型号和基础配置，例如 `km5_xk67j` |
| `VEXT_TARGET_PROJECT` | 扩展定制版本，例如 `km5_xk67j_Claro` |
| modem image | 基础版本和市场/运营商版本应按需求区分 |
| Jenkins 参数 | 参数缺失会导致拷贝脚本取错产物 |

## MTK配置速查

| 目标 | 路径/字段 | 检查点 |
|---|---|---|
| 判断锁网实现类型 | `mcu/make/project` | 确认项目是 SML 还是 SMB 口径 |
| 白名单和锁状态 | `mcu/pcore/custom/service/nvram/custom_nvram_sec.c` / `NVRAM_EF_SML_S_DEFAULT` | 对应 category 是否 `LOCK`，白名单个数是否正确 |
| 白名单容量 | `mcu/pcore/interface/modem/general/sml_public_def.h` | `SML_MAX_SUPPORT_CAT_*` 是否覆盖运营商数量 |
| 解锁码 | `custom_nvram_sec.c` 中对应 category key | 固定解锁码安全性低，量产需求需确认算法方案 |
| 解锁次数 | `sml_public_def.h` / `SML_RETRY_COUNT_*` | 0 可能表现为弹窗后立刻提示无剩余次数 |
| 锁网规则 | `mcu/pcore/custom/service/nvram/l4_nvram_def.c` / `NVRAM_EF_SML_GBLOB_DEFAULT` | 单卡、双卡、卡槽依赖、过期卡规则 |
| 升级生效 | `NVRAM_EF_SML_GBLOB_LID_VERNO`、`NVRAM_EF_SML_S_LID_VERNO` | 从无锁网升级到有锁网时通常两个 VERNO 都要变化 |

MTK 上如果锁网数据变化但 VERNO 未变化，可能被判断为 NVRAM 数据异常并触发 modem assert。不要直接屏蔽 assert，先确认升级策略和数据版本设计。

## UNISOC配置速查

| 目标 | NV/字段 | 典型值或说明 |
|---|---|---|
| 锁卡范围 | `PS_NV_PARAMS -> NV_PARAM_TYPE_SIM_CFG1 -> is_support_gsm_only` | 低 4 bit 按卡槽控制，单卡常见 `1`，双卡常见 `3` |
| 锁网类型 | `PS_NV_PARAMS -> NV_SIM_LOCK_CUSTOMIZE_DATA_ID -> sim_lock_status` | bit0 network lock，bit1 network subset，bit2 SP，bit3 corporate，bit4 user |
| 解锁次数 | `max_num_trials` | 常规需求常见 255，特殊需求按客户定义 |
| 白名单个数 | `network_locks -> numLocks` | 必须和实际 locks 数量一致 |
| 白名单内容 | `locks[i] -> mcc/mnc/mnc_digit_num` | MNC 位数要按 2/3 位准确配置 |
| 锁网依赖 | `dummy2` | One SimLock、卡槽依赖、Any SimLock、过期卡组合规则 |
| 解锁码类型 | `NV_SIM_LOCK_NV_CONTROL_KEY_ID -> control_key_type` | 可按固定码、IMEI 计算、server 侧 key 等方案 |

## 锁卡状态下 MCC/MNC 读取边界

从 CQWeb 历史问题 `SPCSS01329406` 看，卡仍处于 `NETWORK_LOCKED` / `PH-NET PIN` 时，AP 侧 SubInfo 中 `mcc/mnc` 为空通常是预期行为。只有解锁后 SIM 进入 READY，才会继续读取 IMSI、MCC/MNC、SPN 等卡信息。

关键证据：

```text
updateSimState: slot 1 NETWORK_LOCKED
updateSubscription: phoneId=1, simState=NETWORK_LOCKED
+CPIN: PH-NET PIN
SubscriptionInfoInternal ... mcc= mnc= ...
```

定位边界：

- `iccid` 存在不代表 `mcc/mnc` 应该存在；锁卡状态下可能只完成了卡存在性和 ICCID 更新。
- 白名单/黑名单判断不能依赖锁卡状态下的 AP SubInfo MCC/MNC，应回到 modem 锁网判定结果、SIMLock NV/配置和解锁流程。
- 若先插卡读到 READY 后再做安全部署，历史订阅缓存可能掩盖冷启动锁卡行为，复测时要清缓存或走完整冷启动流程。

## 第一坏点

| 现象 | 优先方向 |
|---|---|
| 非白名单卡可驻网 | modem 锁网产物/配置未生效 |
| 本地替换 modem 后有效 | 服务器编译或拷贝链路问题 |
| modem 镜像和基础版本一致 | 市场定制 modem 未生成或未拷贝 |
| modem 已拦截但 UI 不弹 | AP 锁网状态同步或 UI 逻辑 |

## 自检清单

1. 需求里的白名单、锁网类型、卡槽依赖、解锁次数是否明确。
2. 目标项目和运营商扩展项目参数是否进入编译。
3. 基础版本与市场版本 modem image 是否按预期不同。
4. 刷入设备的 PAC/modem image 是否来自正确产物。
5. 插入非白名单卡后 modem 是否已经给出锁网状态。
6. AP 是否收到锁网状态并弹出 UI。

