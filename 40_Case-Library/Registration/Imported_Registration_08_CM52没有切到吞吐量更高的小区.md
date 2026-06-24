---
doc_type: case
quality: imported_reference
domain: Registration
rat: Mixed
feature: 'CellSelection'
platform: Mixed
layer: 'Mixed'
symptom: 'CM52没有切到吞吐量更高的小区'
cause: '原始资料只有现象，缺少测量、重选、负载或策略证据，暂不能判断为何优先驻留 n78 20MHz 而非 n78 60MHz'
source_log: 'Old Outline knowledge base; split from 注网问题案例补充.md'
first_bad_point: '证据缺口：缺少 NR 小区测量、重选/切换策略、SIB 优先级和吞吐量对比 log'
confidence: low
status: summarized_with_log_gap
tags:
  - imported
  - split_from_bucket
  - evidence-gap
  - nr-cell-selection
search_tier: case_summary
---

# CM52没有切到吞吐量更高的小区

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
CM52没有切到吞吐量更高的小区

## 结论

当前只能作为“证据不足样例”。原始资料描述 DUT 间歇性优先使用 n78 20 MHz 小区而不是 n78 60 MHz 小区，导致吞吐低，但没有保留测量值、优先级、负载、NR RRC/测量报告或切换/重选决策 log。

后续复现时应先补齐证据，再判断是小区选择策略、负载均衡、CA/ENDC 能力、网络配置还是测试环境问题。

## 关键证据

- 原始分类：四、小区选择
- 来源：注网问题案例补充.md
- 拆分序号：8
- 现象：`n78 20MHz Cell 905` 与 `n78 60MHz Cell 192` 同时可用时，设备间歇性优先驻留 20 MHz 小区。
- 缺口：原始“问题分析 / 根本原因 / 解决方案”为空。

## 下次复现补证清单

| 必抓证据 | 具体内容 | 能证明什么 |
|---|---|
| NR serving/neighbor measurement | n78 20 MHz 与 n78 60 MHz 的 PCI/NRARFCN/SSB、RSRP/RSRQ/SINR | 60 MHz 小区是否真的比当前小区更适合 |
| SIB / cell restriction | cell barred、intra/inter frequency priority、thresh、qRxLevMin、qQualMin | 网络是否限制或引导 UE 不选目标小区 |
| RRC measurement / reselection log | 测量报告、重选/切换事件、失败 cause | UE 是否测到目标小区以及为何未切换 |
| 吞吐时间线 | iperf/Speedtest 开始结束、小区变化、吞吐下降点 | 吞吐低是否与驻留 20 MHz 小区同步 |
| ENDC/CA/band combo | UE capability、当前 CA/DC 组合、调度带宽 | 是否受终端能力、组合或网络调度限制 |
| 对比机同场景 | 同卡、同点位、同方向、同测试 server | 区分网络负载/策略和 DUT 行为差异 |

判定口径：

- 没有 NR 测量和 SIB 信息时，不能直接判“应切到 60 MHz”。
- 吞吐低不等于小区选择错，还要排除网络负载、server、CA/DC 组合和调度。
- 如果网络没有下发目标小区可选条件，问题归网络配置或覆盖，不归 UE 重选策略。

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：CM52没有切到吞吐量更高的小区

Intermittently, device prioritizing n78 20Mhz (Cell id 905) instead of N78 60Mhz (Cell id 192) when both cells are available which resulting in poor throughput

**问题分析：**


**根本原因：**


**解决方案：**
