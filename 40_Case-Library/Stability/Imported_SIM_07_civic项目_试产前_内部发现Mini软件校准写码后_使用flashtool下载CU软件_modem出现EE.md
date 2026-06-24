---
doc_type: case
quality: imported_reference
domain: Stability
rat: Mixed
feature: 'NVRAM SML LID size'
platform: Mixed
layer: 'RF/Modem'
symptom: 'civic项目，试产前，内部发现Mini软件校准写码后，使用flashtool下载CU软件，modem出现EE'
cause: 'Mini 与 CU 软件 SML LID size 不一致，跨版本下载后 nvram_main.c assert'
source_log: 'Old Outline knowledge base; split from SIM问题案例补充.md'
first_bad_point: 'SML LID 0x0000ef11 size mismatch：para1=0x644，para2=0xa28'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - nvram
  - sml
  - lid-size
search_tier: case_summary
---

# civic项目，试产前，内部发现Mini软件校准写码后，使用flashtool下载CU软件，modem出现EE

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
civic项目，试产前，内部发现Mini软件校准写码后，使用flashtool下载CU软件，modem出现EE

## 结论

首坏点是 Mini 软件与 CU 软件的 SML LID size 不一致。跨版本从 Mini 校准写码后再用 flashtool 下载 CU，modem 读取 SML/NVRAM 时发现 LID size mismatch，于 `nvram_main.c` assert。

## 关键证据

- 原始分类：一、Modem 崩溃
- 来源：SIM问题案例补充.md
- 拆分序号：7
- assert：`mcu/common/service/nvram/src/nvram_main.c line=2362`
- 参数：`para0=0x0000ef11, para1=0x00000644, para2=0x00000a28`
- 修复方向：同步 SML LID patch；必要时通过 LID Verno 处理已出机器兼容。

## 定位口径

| 检查项 | 判断 |
|---|---|
| `0x0000ef11` | SML LID 方向 |
| `para1/para2` 不一致 | LID size mismatch |
| Mini -> CU 下载 | 必须确认 NV layout / LID verno 是否兼容 |
| 已出机器 | 需要迁移策略，不能简单整包覆盖 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：civic项目，试产前，内部发现Mini软件校准写码后，使用flashtool下载CU软件，modem出现EE

分析：0x0000ef11为SML 的lid， 看crash原因为 SML的lid size不匹配导致，

```java
<5>[   18.357838]  (6)[296:ccci_fsm1][ccci1/fsm]filename = mcu/common/service/nvram/src/nvram_main.c
<5>[   18.357850]  (6)[296:ccci_fsm1][ccci1/fsm]line = 2362

<5>[   18.357861]  (6)[296:ccci_fsm1][ccci1/fsm]assert para0 = 0x0000ef11, para1 = 0x00000644, para2 = 0x00000a28
```

根本原因：排查发现mini软件与CU软件的lid size确实不一致

方案： 1.TCL提供同步SML lid的patch给BSP分支 2.BSP分支可以通过调整SML的Lid Verno规避已经出去的机器，涉及mini与CU的Lid Verno控制问题，此方案最终未启用

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
