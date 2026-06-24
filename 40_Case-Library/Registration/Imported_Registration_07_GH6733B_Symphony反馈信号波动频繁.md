---
doc_type: case
quality: imported_reference
domain: Registration
rat: LTE
feature: 'Cell reselection / SINR optimization'
platform: UNISOC
layer: 'Modem/LRRC/RF'
symptom: 'GH6733B_Symphony反馈信号波动频繁'
cause: 'SINR 优化触发异频测量和小区重选，终端重选到 B40/39248 后因动态场景信号变差又回到 1800，导致信号显示波动'
source_log: 'Old Outline knowledge base; split from 注网问题案例补充.md'
first_bad_point: 'LRRC 根据 SINR 触发 non-intra search，并从 arfcn 1800 重选到 39248 后又回到 1800'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - cell-reselection
  - sinr
  - lrrc
search_tier: case_summary
---

# GH6733B_Symphony反馈信号波动频繁

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
GH6733B_Symphony反馈信号波动频繁

## 结论

这是小区重选策略导致的信号波动样例。DUT 启动 SINR 优化后起测异频，满足条件重选到高优先级频点 `39248`，但动态测试中该小区信号很快变差，于是又回到 `1800`，用户侧表现为信号频繁波动。

处理方向不是简单“禁止重选”，而是调整 SINR 优化阈值，避免在动态弱覆盖下过于频繁触发异频重选。

## 关键证据

- 原始分类：四、小区选择
- 来源：注网问题案例补充.md
- 拆分序号：7
- `is_measure_should_active_according_sinr = 1`，说明 SINR 触发了测量。
- `UE is going to Reselect Cell=443 on Frequency=39248` 后，39248 上 RSRP 继续下降。
- 随后 `UE is going to Reselect Cell=171 on Frequency=1800`，形成来回波动。

## 定位口径

| 检查项 | 判断 |
|---|---|
| RSRP / RSRQ / SINR | 不只看 RSRP；SINR 会影响是否触发测量和重选 |
| 频点优先级 | 结合 `freqPriorityListEUTRA` 判断为何起测异频 |
| 动态场景 | 动态测试中目标小区质量变化快，容易出现重选后又回退 |
| 配置项 | 原始修复调整 `cus_meas_sinr_threshold`，降低 SINR 优化触发强度 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：GH6733B_Symphony反馈信号波动频繁

Actual result: Banglalink Network Fluctuates in comparison with MAX60. Both devices were at the same place at a same time. Please play both videos side by side.

Expected Result: No network fluctuation should come.

**问题分析：**

Log显示测试机小区切换频繁，切到B40后，rsrp就很低了，对比机没有切到B40。

需要知道测试机为什么小区切换这么频繁，以及为什么会切到信号质量很差的B40的小区上

CQ:SPCSS01590953

```java
9386933-1    15:41:08.131    --    Time: 1313072 LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -8531 , rsrq = -1603 , sinr = -1 , arfcn = 1800 , cell_id = 0 , is_signal_report = 1
9397898-1    15:41:17.091    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -9713 , rsrq = -2201 , sinr = -10 , arfcn = 1800 , cell_id = 0 , is_signal_report = 1
9399538-1    15:41:18.371    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -10015 , rsrq = -2369 , sinr = -12 , arfcn = 1800 , cell_id = 0 , is_signal_report = 1
9404097-1      15:41:19.651     Time: 1314297 LRRC:TCM_RMH:Sserving = 2766, Squalserving = 507, s_NonIntraSearchP = 800, s_NonIntraSearchQ = 400, is_measure_should_active_according_sinr = 1        LRRC           3:39:03.798      2651
9407087-1    15:41:22.211    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -9255 , rsrq = -1774 , sinr = -9 , arfcn = 1800 , cell_id = 0 , is_signal_report = 1
9408224-1    15:41:23.491    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -8965 , rsrq = -1677 , sinr = -5 , arfcn = 1800 , cell_id = 0 , is_signal_report = 1
9410248-1    15:41:24.771    --    LRRC:TCM_RMH:cardId 0,UE is going to Reselect Cell=443 on Frequency=39248 And the Serving Cell was EUTRA Cell=0 on Frequency=1800
9413697-1    15:41:26.567    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -11157 , rsrq = -1332 , sinr = 1 , arfcn = 39248 , cell_id = 443 , is_signal_report = 1
9417377-1    15:41:34.246    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -11730 , rsrq = -999 , sinr = -1 , arfcn = 39248 , cell_id = 443 , is_signal_report = 1
9421305-1    15:41:39.366    --    LRRC:RMH_TCM:ASM signal information : cardId = 0 rsrp = -12139 , rsrq = -1726 , sinr = -2 , arfcn = 39248 , cell_id = 443 , is_signal_report = 1
9421550-1    15:41:39.366    --    LRRC:TCM_RMH:cardId 0,UE is going to Reselect Cell=171 on Frequency=1800 And the Serving Cell was EUTRA Cell=443 on Frequency=39248

428443-1       15:35:22.688     SIM1      LTE                                                            <- RRCCONNECTIONRELEASE                          0:05:53.097

                                freqPriorityListEUTRA

                                        carrierFreq = 50
                                        cellReselectionPriority = 7

                                        carrierFreq = 1800
                                        cellReselectionPriority = 6

                                        carrierFreq = 39050
                                        cellReselectionPriority = 5

                                        carrierFreq = 39248
                                        cellReselectionPriority = 5

                                        carrierFreq = 75
                                        cellReselectionPriority = 4

                                        carrierFreq = 3626
                                        cellReselectionPriority = 3
                                freqPriorityListGERAN
                                t320 = min10
```

**根本原因：**

测试机终端启动了sinr优化，起测了异频，39248是高优先级频点，重选门限是-112，满足重选条件重选过去了
但由于动态测试，这个小区信号会变很差，所以又起测了异频，低优先级重选回1800，所以看到了信号波动较大的现象。小区信号情况不能只关注rsrp，sinr对终端行为影响更大，所以为了防止终端在sinr不好的小区上做业务受到影响，才有该sinr的优化。
对比机这段时间受专有优先级影响，没有起测异频，测试机是通过sinr优化重选过去的，是为了保业务质量的。

网络环境差，开启了SINR优化，导致小区切换频繁，网络波动大

**解决方案：**

降低SINR优化，小区切换阈值

<http://192.168.3.81:8085/c/SPRD_U/SPRDROID13_VND_RLS_23A/+/117219>

```java
//Redmine 380003 Modify for the issue of network fluctuations in 6733B by wangxin 2025/11/28 begin
PS_NV_PARAMS\LTE_NV_EUTRA_CUSTOMER_SETTINGS\cus_meas_sinr_threshold\sinr_threshold=0xFFF1
//Redmine 380003 Modify for the issue of network fluctuations in 6733B by wangxin 2025/11/28 end
```

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
