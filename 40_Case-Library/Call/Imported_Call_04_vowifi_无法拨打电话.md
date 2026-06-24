---
doc_type: case
quality: imported_reference
domain: Call
rat: IWLAN
feature: 'ECC'
platform: Mixed
layer: 'IMS/IWLAN/ECC'
symptom: 'vowifi 无法拨打电话'
cause: '当前只保留 VoWiFi ECC 复盘附件，缺少正文证据；应迁入 IMS 专项后按 IWLAN/ePDG/IMS emergency 域选补齐'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: '证据缺口在 VoWiFi ECC 域选与 IMS emergency 建呼链路，当前 markdown 只有 PPT 附件'
confidence: low
status: summarized_with_log_gap
tags:
  - imported
  - split_from_bucket
  - vowifi
  - ecc
  - ims-deferred
search_tier: case_summary
---

# vowifi 无法拨打电话

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，目前只保留 VoWiFi ECC 复盘附件入口。正文证据不足，后续应在 IMS 专项中补齐 IWLAN / ePDG / SIP emergency 链路。

## 用户现象
vowifi 无法拨打电话

## 结论

当前 markdown 只有 `Vanilla VoWiFi ECC问题复盘总结.pptx` 附件，没有足够正文证据，不能沉淀成确定 root cause。它的复用方式是作为 VoWiFi emergency 专项的资料入口，而不是放在普通 LTE 注册或 CS Call 排障中扩散。

后续 IMS 专项处理时，需要从附件中补齐：WFC 开关 / IWLAN 注册 / ePDG / IMS emergency registration / SIP INVITE / domain selection / CS retry 的完整链路。

## 关键证据

- 原始分类：一、紧急通话
- 来源：通话问题案例补充.md
- 拆分序号：4
- 附件：`attachments/outline/files/e3b69f59-0e2a-4fde-8454-de3e745d1048_Vanilla VoWiFi ECC问题复盘总结.pptx`

## 下次复现补证清单

| 必抓证据 | 具体内容 | 能证明什么 |
|---|---|
| AP main/radio log + bugreport | WFC 开关、飞行模式、拨号入口、EmergencyNumberTracker、domain selection、失败弹框时间 | AP 是否允许 emergency over Wi-Fi，以及实际选择了哪个 phoneId/domain |
| CarrierConfig dump | WFC、IMS emergency、ECC、roaming、carrier privilege 相关 key | 是否被配置门控拦截 |
| modem IMS/IWLAN log | IKE/ePDG、IMS over IWLAN REGISTER、P-CSCF、IMS emergency capability | 问题卡在 ePDG、IMS 注册还是 emergency 建呼 |
| SIP log | emergency INVITE、Request-URI/URN、P-Access-Network-Info、SIP response | emergency call 是否真正发到 IMS core，以及网络拒绝原因 |
| retry / fallback log | CS retry、LTE/CS domain retry、slot/subId 切换、radio power state | 失败后是否按策略回退到蜂窝或 CS |
| Wi-Fi 环境证据 | SSID、DNS、UDP 500/4500、tcpdump/ISAKMP、公司/公共 Wi-Fi | 区分 Wi-Fi/ePDG 基础链路失败和 emergency 业务失败 |

判定口径：

- 飞行模式下提示“需关闭飞行模式”时，先查 AP domain selection 是否认为 Wi-Fi emergency 不可用。
- IKE/ePDG 未建立时，不要继续归因 SIP 或 ECC 号码配置。
- IMS over IWLAN 已注册但 INVITE 被拒时，再看 URN、号码映射、签约和网络策略。

## 归属规则

- VoWiFi ECC 的“紧急号码识别、域选择入口”可在 Call/ECC 索引中保留入口。
- IMS 注册、ePDG、SIP、媒体和 WFC 能力问题应放入 IMS 专项，不混入 LTE 注册文档。

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例4：vowifi 无法拨打电话

[Vanilla VoWiFi ECC问题复盘总结.pptx 1059246](..\..\attachments\outline\files\e3b69f59-0e2a-4fde-8454-de3e745d1048_Vanilla VoWiFi ECC问题复盘总结.pptx)
