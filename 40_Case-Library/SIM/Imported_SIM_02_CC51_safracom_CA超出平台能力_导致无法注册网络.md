---
doc_type: case
quality: imported_reference
domain: SIM
rat: LTE
feature: 'CA capability / Modem Assert'
platform: Mixed
layer: 'Modem/LTE PHY/CA capability'
symptom: 'CC51 safracom，CA超出平台能力，导致无法注册网络'
cause: 'UE 上报了平台不支持的 CA 组合，网络按该能力配置超出平台能力的 CA，导致 LTE PHY assert 并引发 SIM 状态异常/无法注册'
source_log: 'Old Outline knowledge base; split from SIM问题案例补充.md'
first_bad_point: 'RIL 上报 LTE_DL_SCH0_TASK PHY CP assert，assert 点在 AFC_mainLccAdjVcoNcoProcess'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - modem-assert
  - ca-capability
  - registration
search_tier: case_summary
---

# CC51 safracom，CA超出平台能力，导致无法注册网络

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
CC51 safracom，CA超出平台能力，导致无法注册网络

## 结论

这是 CA 能力配置导致的 modem assert，并连带表现为 SIM 状态异常和无法注册。根因不是 SIM 卡本身，而是 UE 上报了平台不支持的 CA 组合，网络按错误能力下发配置后触发 LTE PHY assert。

## 关键证据

- 原始分类：一、Modem 崩溃
- 来源：SIM问题案例补充.md
- 拆分序号：2
- RIL log：`Modem Assert: LTE_DL_SCH0_TASK Task PHY CP assert in file afc_aaal.c line 1567`。
- assert 信息包含 `AFC_mainLccAdjVcoNcoProcess`、`lcc_idx` 等 CA / LCC 相关字段。
- 原始根因：组合流数超出平台能力，网络配置了 UE 不支持的 CA。

## 定位口径

| 检查项 | 判断 |
|---|---|
| SIM unknown | 先看是否由 modem assert 连带造成，不要直接按卡异常处理 |
| UE capability | 核对上报的 CA band combo / layer / LCC 是否符合平台能力 |
| 网络配置 | 网络是否按 UE 上报能力配置了超限 CA |
| 修复动作 | 按平台能力收敛 CA 组合上报或配置 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：CC51 safracom，CA超出平台能力，导致无法注册网络

分析：开始有注册上网络，但是后面SIM卡状态变成UNKNOW了，继续分析发现Modem Assert了

```javascript
R007B04  06-18 08:41:42.362   681   748 E RIL     : Modem Assert: LTE_DL_SCH0_TASK Task  PHY CP assert in file afc_aaal.c line 1567 exp=0 info=[AFC_mainLccAdjVcoNcoProcess ch_idx=0,lcc_idx=0, cep_cfg_to_adjFoe_step = 0,ts=0x1ef35271 afcSwFsm = 15], [dfs=6]
```

根本原因：组合流数超出了平台能力。UE上报了不支持的CA组合，网络根据UE上报支持的CA 能力，配置了UE不支持的CA配置，导致底层ASSERT。

方案：按照平台能力配置CA组合

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
