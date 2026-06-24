---
doc_type: case
quality: imported_reference
domain: SIM
rat: 3G
feature: 'Modem Assert / RF TAS'
platform: Mixed
layer: 'Modem/RF/NV'
symptom: 'WM28+ 连不上Meta'
cause: 'ul1d_custom_rf_tas.h 存在未定义设置，触发 WCDMA RF error check 相关 modem assert，导致 Meta 无法连接'
source_log: 'Old Outline knowledge base; split from SIM问题案例补充.md'
first_bad_point: 'ccci_fsm 上报 modem assert，需按 WCDMA RF Error Check 指南检查 RF TAS 配置'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - modem-assert
  - rf-tas
  - meta
search_tier: case_summary
---

# WM28+ 连不上Meta

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
WM28+ 连不上Meta

## 结论

首坏点不是 Meta 工具本身，而是 modem assert。原始结论指向 `ul1d_custom_rf_tas.h` 中存在未定义设置，触发 WCDMA RF Error Check 相关 assert；处理方式是修改 3G 未使用频段的 index 值。

## 关键证据

- 原始分类：一、Modem 崩溃
- 来源：SIM问题案例补充.md
- 拆分序号：1
- kernel / CCCI log 中出现 `ccci_fsm` assert。
- 原始分析要求参考 `CS0050-GAL2C-AND-V1.0EN_Platform_System_RF_WCDMA_RF_Error_Check_Application_Note`。
- 原始根因：`ul1d_custom_rf_tas.h` 有未定义设置。

## 定位口径

| 检查项 | 判断 |
|---|---|
| Meta 连接失败 | 先确认 modem 是否已 assert；modem 崩溃时 Meta 失败只是结果 |
| RF TAS 配置 | 查 `ul1d_custom_rf_tas.h` 和未使用 3G band index |
| 指南依据 | 对照 WCDMA RF Error Check application note 的 line / error code |
| 修复验证 | 修改 RF 配置后确认 modem 不 assert，Meta 可连接 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：WM28+ 连不上Meta

```java
<5>[   11.409652][T00700000584] ccci_fsm: [ccci1/fsm]filename = mcu/l1/ul1/ul1d_public/ul1d_rf_error_check.c
<5>[   11.409656][T00700000584] ccci_fsm: [ccci1/fsm]line = 330
<5>[   11.409660][T00700000584] ccci_fsm: [ccci1/fsm]assert para0 = 0x00000000, para1 = 0x00000000, para2 = 0x00000000
```

分析：参考DCC上对应的说明文档CS0050-GAL2C-AND-V1.0EN_Platform_System_RF_WCDMA_RF_Error_Check_Application_Note LINE330报错指导检查对应的配置

[CS0050-GAL2C-AND-V1.0EN_Platform_System_RF_WCDMA_RF_Error_Check_Application_Note.pdf 1240167](..\..\attachments\outline\files\21c29016-9183-45b5-9c75-5023160cd61c_CS0050-GAL2C-AND-V1.0EN_Platform_System_RF_WCDMA_RF_Error_Check_Application_Note.pdf)

根本原因：ul1d_custom_rf_tas.h 存在一个未定义的设置，该设置触发了此断言

解决方案：修改3G几个没用到的频段的index值

<http://192.168.3.81:8085/c/S0_MP1/alps-release-s0.mp1.rc-tb-default_modem/+/124533>

## 复用边界

- 本 case 来自旧 Outline 迁入资料，状态为 partial。
- 复用时需要重新核对平台、项目、运营商、版本、log 时间窗和第一坏点。
- 如果后续补齐完整证据链，再把 status 改为 summarized 或 closed。
