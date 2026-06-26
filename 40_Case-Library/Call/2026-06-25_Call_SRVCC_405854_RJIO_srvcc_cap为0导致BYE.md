---
quality: curated
doc_type: case
domain: Call
rat: LTE/UTRAN
feature: SRVCC
platform: MTK
layer: IMS/Modem/OperatorProfile
symptom: "仪表模拟 405854/RJIO SRVCC 到 3G 时，VoLTE 通话被 IMS UA 主动 BYE 释放"
cause: "运行时 IMS UA 看到 srvcc_cap=0x00，判定通话不会在 SRVCC 中转移，触发 call_session_release_session_not_transferred_in_srvcc；静态 modem RJIO profile 默认并未关闭 SRVCC"
operator: "RJIO/RJIL, MCCMNC 405854"
source_log: "F:\\Log\\SRVCC\\debuglogger; F:\\Log\\SRVCC\\62130\\debuglogger"
first_bad_point: "SRVCC 开始时 VoLTE UA 打印 srvcc cap: 0x00，随后立即释放 IMS session 并发送 BYE"
confidence: high
status: summarized
search_tier: case_summary
tags:
  - srvcc
  - ims
  - mtk
  - rjio
  - 405854
  - operator-profile
---

# 405854/RJIO SRVCC 过程中 srvcc_cap=0 导致 BYE

## 基本信息

| 项目 | 内容 |
|---|---|
| 日期 | 2026-06-25 |
| 平台 | MTK |
| 芯片/基线 | `alps-release-s0.mp1.rc-tb-default_modem` |
| 厂商客制化 | modem IMS profile / MCF OTA / NVRAM / RJIO operator policy |
| 原始log | `F:\Log\SRVCC\debuglogger`；对比 log：`F:\Log\SRVCC\62130\debuglogger` |
| 第一坏点 | SRVCC start 时 IMS UA 的 `srvcc cap: 0x00` |
| SIM/运营商 | 失败：`405854`，RJIO/RJIL；正常对比：`62130` |
| RAT | LTE -> 3G |
| 场景 | VoLTE 通话中，仪表触发 SRVCC 到 3G |
| 复现概率 | 405854 在多项目机器上复现；其他运营商卡可呼出/可 SRVCC |

## 用户现象

通话过程中切换到 3G，期望平稳 SRVCC 承接，但 405854/RJIO 场景下通话被挂断。AP 层出现 `IMS_CALL_STATUS_END` / `DMF_CALL_EVENT_CALL_END`，AT 查询释放原因显示 `+CEER: 31,CM_NORMAL_UNSPECIFIED`。

## 结论

首坏点在 IMS UA 的运行时 SRVCC 能力：失败 log 中 `srvcc cap: 0x00`，UA 认为当前 call 不会在 SRVCC 中被转移，于是调用 `call_session_release_session_not_transferred_in_srvcc` 并发送 BYE。`+CEER: 31,CM_NORMAL_UNSPECIFIED` 是后续正常释放口径，不是能解释根因的第一坏点。

MTK modem 静态源码中，`405854` 会映射到 `op_id/SBPID=18` 的 RJIO/RJIL；该 profile 默认 `srvcc_feature_enable=0x0007`，即开启 SRVCC/aSRVCC/midSRVCC。因此当前证据不支持“modem 静态默认关闭 405854 SRVCC”。更可能是运行时 IMS profile、NVRAM、OTA 或 AP/IMS account 更新链路把 `srvcc_feature_enable` 覆盖成 0，或者仪表 405854/3G SRVCC 模型与 RJIO LTE-only 策略冲突。

## 输入材料

- AP log：`F:\Log\SRVCC\debuglogger\mobilelog\APLog_2026_0623_125327__1\main_log_1__2026_0623_125413`
- radio log：`F:\Log\SRVCC\debuglogger\mobilelog\APLog_2026_0623_125327__1\radio_log_2__2026_0623_125413`
- 正常对比：`F:\Log\SRVCC\62130\debuglogger`
- MTK modem 源码：`/home/wx/Modem/alps-release-s0.mp1.rc-tb-default_modem/modem`

## 时间线

| 时间 | 来源 | 事件 | 含义 | 重要性 |
|---|---|---|---|---|
| 2026-06-23 12:54:00.865 | AP main | `srvcc cap: 0x00, force transfer: 0x07` | IMS UA 运行时认为 SRVCC 能力为 0 | 第一坏点 |
| 2026-06-23 12:54:00.865 | AP main | `call_session_release_session_not_transferred_in_srvcc` | UA 判定 session 未在 SRVCC 中转移，主动释放 | 高 |
| 2026-06-23 12:54:00.867 | AP main | `SRVCC: call [1] send BYE` | BYE 是前一条释放决策的结果 | 高 |
| 2026-06-23 12:54:00.895 | radio | `+CEER: 31,CM_NORMAL_UNSPECIFIED` | 后续释放原因为 normal unspecified | 中 |
| 2026-06-24 02:20:34.977 | 对比 AP main | `force_srvcc_transfer=7, srvcc_cap=f` | 正常运营商 profile 会把 SRVCC 能力传到 UA | 高 |
| 2026-06-24 02:21:00.443 | 对比 AP main | `srvcc cap: 0x0f, force transfer: 0x07` | 正常流程 SRVCC start 时能力非 0 | 高 |

## 正常流程对比

正常对比 log 中，IMS account 更新阶段已经带出：

```text
Update acct[0] ... force_srvcc_transfer=7, srvcc_cap=f
srvcc cap: 0x0f, force transfer: 0x07
```

失败 log 中，`force transfer` 仍是 `0x07`，但 `srvcc cap` 变成 `0x00`。这说明问题不在 “SRVCC 触发事件是否到 UA”，而在 UA 最终拿到的 SRVCC capability 为 0。

## 第一个异常点

```text
第一个坏点：
06-23 12:54:00.865 VoLTE UA: srvcc cap: 0x00, force transfer: 0x07

上一条正常证据：
SRVCC 过程已进入 UA 处理；force transfer 已配置为 0x07

下一条异常证据：
VoLTE UA: call_session_release_session_not_transferred_in_srvcc
VoLTE UA: SRVCC: call [1] send BYE

影响层级：
IMS UA / IMS profile runtime config
```

## 关键证据

失败 log：

```text
VoLTE UA: srvcc cap: 0x00, force transfer: 0x07, decouple conf: 0, 1to1 conf: 0
VoLTE UA: call_session_release_session_not_transferred_in_srvcc: release the session, call_id=[1]
VoLTE UA: SRVCC: call [1] send BYE, res=[0]
AT< +CEER: 31,CM_NORMAL_UNSPECIFIED
```

正常对比：

```text
VoLTE UA: Update acct[0] ... force_srvcc_transfer=7, srvcc_cap=f
VoLTE UA: srvcc cap: 0x0f, force transfer: 0x07, decouple conf: 0, 1to1 conf: 1
```

MTK modem 源码：

```c
// custom_l4_utility.c
else if ((mcc == 405) && ((mnc == 840) || (mnc >= 854 && mnc <= 874))) {
    return 18; // RJIO
}

// custom_imc_config.c, case 18: RJIL
nvram_ims_profile_ptr->ua_config.dereg_send_bye = 1;
nvram_ims_profile_ptr->ua_config.srvcc_feature_enable = 0x0007; // enable SRVCC, aSRVCC, midSRVCC
nvram_ims_profile_ptr->ua_config.transfer_conf_call_as_1to1 = 0;
```

OPOTA 检查：

```text
mcu/custom/service/mcf/ota_files/MTK_OPOTA_SBPID_18.xml:
<MCFNVRam Version="1.0" IsOperator="1" Name="MTK_OPOTA_SBPID_18" SBPID="18" MCC="" MNC=""/>

MTK_OPOTA_SBPID_18.mcfopota 只有 TLV-OTA 头和版本串，未看到 IMS/SRVCC override 内容。
```

## 异常分析

### 事实

- 405854 在源码中归属 RJIO/RJIL，`op_id/SBPID=18`。
- RJIO 静态 IMS profile 默认开启 `srvcc_feature_enable=0x0007`。
- 失败时 UA 运行时打印 `srvcc cap: 0x00`，随后主动释放 session 并发送 BYE。
- 正常对比运营商 account 更新为 `srvcc_cap=f`，SRVCC start 时能力为 `0x0f`。
- `+CEER: 31,CM_NORMAL_UNSPECIFIED` 出现在 BYE/释放之后，只能说明最终释放类型偏 normal unspecified。

### 推断

- 直接挂断原因是 IMS UA 在 SRVCC 过程中认为 call 未被转移，主动 BYE。
- 根因候选优先级最高的是运行时 IMS profile 覆盖：`NVRAM_EF_IMS_PROFILE_LID`、MCF OTA、AP/IMS account 转换或项目侧 profile provisioning。
- 405854/RJIO 的 LTE-only/PS-only 策略可能放大仪表 3G SRVCC 测试风险，但现有证据仍先指向 `srvcc_cap=0x00`。

### 待确认

- 失败机插 405854 后，最终生效的 `NVRAM_EF_IMS_PROFILE_LID.ua_config.srvcc_feature_enable` 是否为 0。
- AP/IMS account 更新阶段是否曾打印 405854 的 `force_srvcc_transfer` 和 `srvcc_cap` 完整 profile。
- 仪表 405854 是否宣称/模拟了 RJIO 可 SRVCC 到 3G；如果网络侧模型与 RJIO LTE-only 策略冲突，需要单独确认测试配置。

## 405854 源码特殊性

| 检查项 | 结果 |
|---|---|
| 运营商映射 | `405840`、`405854` 到 `405874` 映射为 `op_id=18/RJIO` |
| IMS SRVCC 默认 | RJIO `srvcc_feature_enable=0x0007`，未默认关闭 |
| OPOTA | `MTK_OPOTA_SBPID_18.xml` 为空 operator 节点，`.mcfopota` 无可见 IMS override |
| LTE-only/PS-only | `CUSTOM_PS_ONLY_PLMN[]` 包含 `405854` |
| 23G 搜索限制 | `SBP_DO_NOT_SEARCH_23G_LTE_ONLY_NETWORK` 编译打开时，不为 RJIO LTE-only SIM 搜 2/3G normal service |
| CSFB 策略 | `custom_ssds.c` 对 RJIL 默认 no CSFB，国际漫游才可能 CSFB once |

## 平台差异检查

| 检查项 | 结果 |
|---|---|
| 是否只在单一平台复现 | 用户反馈换其他项目机器，405854 SRVCC 也失败 |
| 是否涉及 NV 或 modem 配置 | 高度相关，重点是 IMS profile / `NVRAM_EF_IMS_PROFILE_LID` |
| 是否涉及 vendor RIL/IMS service 实现 | 相关，UA account 更新把 `srvcc_feature_enable` 转成 `srvcc_cap` |
| 是否涉及 CarrierConfig | 当前无直接证据 |
| 是否需要平台侧工具解析 | 需要 ELT/MACE 或 NVRAM dump 解析 IMS profile |

## 可能原因排序

| 排名 | 可能原因 | 证据 | 置信度 |
|---|---|---|---|
| 1 | 运行时 IMS profile/NVRAM 把 `srvcc_feature_enable` 覆盖为 0 | 失败 log `srvcc cap: 0x00`；静态源码默认是 `0x0007` | 高 |
| 2 | AP/IMS account 更新链路对 405854 profile 转换错误 | 正常卡有 `srvcc_cap=f`，失败卡缺完整 account dump，需要补证 | 中 |
| 3 | 仪表 RJIO/405854 的 LTE-only/3G SRVCC 模型与源码策略冲突 | RJIO 源码有 PS-only/LTE-only/不搜 23G normal service 特例 | 中 |

## 处理方案

- 临时验证：
  - 清 modem NVRAM 或重置 IMS profile 后复测 405854。
  - 临时强制 RJIO `srvcc_feature_enable=0x0007` 或 `0x000F`，`force_srvcc_transfer=0x07`，确认 SRVCC 是否恢复。
- 正式修复：
  - 如果 dump 证明运行时为 0，修 IMS profile/NVRAM/OTA/provisioning 覆盖链路，不优先改 RRC/SRVCC mobility。
  - 如果运行时 profile 正确但 UA 仍为 `srvcc_cap=0x00`，继续查 AP/IMS account 参数转换。
- 需要供应商/运营商确认：
  - RJIO 405854 是否应支持 SRVCC 到 3G。
  - 仪表配置是否按 RJIO LTE-only 策略建模，还是误用了一个可 3G SRVCC 的通用印度卡模型。

## 复盘

下次遇到 SRVCC 掉话，优先检查：

- 不要从 `+CEER` 末端原因直接定根因；先找第一条 release 决策。
- 对比 pass/fail 的 `Update acct` 中 `force_srvcc_transfer`、`srvcc_cap`。
- 看到 `call_session_release_session_not_transferred_in_srvcc` 时，优先回查 UA 运行时 SRVCC capability。
- 对 MTK 运营商卡，必须区分静态 `custom_imc_config.c` 默认值、MCF OTA、NVRAM 和 AP/IMS account 生效值。
- 对 RJIO/405854，额外检查 LTE-only/PS-only 策略是否与仪表 SRVCC 到 3G 场景冲突。
