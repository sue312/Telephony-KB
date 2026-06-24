---
doc_type: case
quality: imported_reference
domain: SIM
rat: Mixed
feature: 'SIM power / regulator late cleanup'
platform: Mixed
layer: 'Kernel/DTS/DWS/SIM power'
symptom: 'VINCA SIM PIN掉卡问题'
cause: 'kernel regulator late cleanup 将 AP 侧无 user 使用的 VSIM regulator 关闭，导致 PIN/Meta 等场景下 VSIM 掉电并掉卡'
source_log: 'Old Outline knowledge base; split from SIM问题案例补充.md'
first_bad_point: 'kernel time 约 31s 出现 vsim1/vsim2 disabling，随后 RIL 上报 ESIMS 事件'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - regulator
  - vsim
  - pin
search_tier: case_summary
---

# VINCA SIM PIN掉卡问题

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
VINCA SIM PIN掉卡问题

## 结论

这是 kernel regulator late cleanup 造成的 VSIM 掉电问题。VSIM 电源在 kernel 对应时间点前被 enable，但 AP 侧没有 user 持有，late cleanup 会把 regulator off 掉，PIN 解锁或 Meta 测试场景因此掉卡。

## 关键证据

- 原始分类：三、驱动配置问题
- 来源：SIM问题案例补充.md
- 拆分序号：18
- kernel log 出现 `vsim1: disabling`、`vsim2: disabling`。
- RIL 随后上报 `+ESIMS` 相关 SIM 事件。
- 原始方案：去掉 DWS / DTS 中 VSIM 相关节点，避免被 regulator late cleanup 误关。

## 定位口径

| 检查项 | 判断 |
|---|---|
| 时间点 | 关注 kernel time 30s 左右是否有 regulator cleanup |
| 电源 log | 搜 `vsim1: disabling`、`vsim2: disabling` |
| 场景 | PIN 解锁、Meta 测试、开机后固定时间掉卡优先查 regulator |
| 配置 | 检查 DWS / DTS 中 VSIM regulator 节点和 user 持有关系 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：VINCA SIM PIN掉卡问题

分析：FAQ35132
kernel原生会有regulator late cleanup的机制，没有user使用的regulator会被off掉，时间点大约在kernel time 30s，经常遇到在进行一些meta测试或者一些sim卡解锁的场景，会有vpa掉电或vsim掉电，影响功能。原因是这路power在kernel该时间点之前被enable了，但ap侧无user使用它，因此被off下电。
碰到这种情况，一般可以查阅开机kernel log看是否有类似如下disabling的打印，会有如下log：
\[   31.743968\]\[T1600743\] vpa: disabling
或者
\[   31.745900\]\[T1600061\] vsim1: disabling
\[   31.746013\]\[T1600061\] vsim2: disabling
如有遇到这种情况，请先盘点一下项目中是否在AP侧用到这些power，如由md全权控制的话，可以在dts中使用

```java
<6>[   31.713056][   T57] vsim1: disabling
<6>[   31.713176][   T57] va09: disabling
 06-27 10:28:01.323236  1606  1631 I AT      : [0] AT< +ESIMS: 0,13 (RIL_URC_READER, tid:516195208176)
 06-27 10:28:03.595023  1606  1631 I AT      : [0] AT< +ESIMS: 1,14 (RIL_URC_READER, tid:516195208176)
```

根本原因：由于 kernel原生的 regulator late cleanup 机制导致的每次开机掉卡

解决方案：去掉DWS文件和DTS文件中,vsim相关的节点
