---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# Call Cases

## 阅读入口

- 本页是当前目录入口，优先按表格进入已整理主题；来源记录只用于回溯。
- 可复用结论应沉淀到主流程/配置/排障/case；本文只保留溯源材料和操作细节。

CS call、VoLTE call、VoNR call、MO/MT call fail、call drop、SRVCC、EPSFB、ECC 相关 case 放这里。Call Forwarding、Call Barring、USSD、UT/XCAP 等补充业务 case 放 [Supplementary-Service Cases](../Supplementary-Service/README.md)。

## 已整理案例

| Case | 场景 | 用途 |
|---|---|---|
| [[2022-07-30_ECC_UNISOC_routing不控制无卡禁止_card_flag]] | ECC `routing=2` 后无卡仍可拨 | 区分 routing、真/假紧急拨号和 card_flag 卡状态条件 |
| [[2021-06-04_ECC_UNISOC_PIN未解锁EF_ECC与无卡ECC分类]] | SIM PIN 未解锁时 EF_ECC 与无卡 ECC 分类错误 | 区分 PIN locked、Without SIM ECC 和 SIM EF_ECC |
| [[2024-05-27_ECC_UNISOC_PUK锁卡紧急呼叫误走PS域无声]] | PUK 锁卡拨 112/911 一直紧急呼叫且无声 | 区分音频问题和 ECC 域选择第一坏点 |
| [[2025-12-10_ECC_UNISOC_无卡紧急呼叫选到eSIM卡槽失败]] | 无实体卡拨 112/911 失败，飞行模式后正常 | 用 AP 选卡、eUICC 过滤和 modem ATD 下发栈定位第一坏点 |
| [[2025-07-30_ECC_无卡紧急呼叫回退超时]] | IMS emergency 失败后 CS 回退超时 | 紧急呼叫域选择和 retry 第一坏点 |
| [[2025-06-23_ECC_双卡紧急号码共享]] | 双卡紧急号码池共享 | 判断 emergency number 是否按设备级缓存 |
| [[2026-06-05_ECC_UNISOC_喀麦隆113缺少routing2误走EMERGENCY_SETUP]] | 喀麦隆 113 缺少 `routing:2` 无法呼出 | 区分未配 fake/normal routing 导致的真紧急 `EMERGENCY_SETUP` |
| [[2025-W22_Call_SRVCC_Claro切换掉话]] | VoLTE 通话 SRVCC 后掉话 | SRVCC 能力协商、Feature-Caps、切换执行排查口径 |
| [[2026-06-25_Call_SRVCC_405854_RJIO_srvcc_cap为0导致BYE]] | 405854/RJIO 仪表 SRVCC 到 3G 被 BYE 释放 | 用 `srvcc_cap=0x00` 和 RJIO 源码 profile 区分运行时覆盖与静态默认 |
| [[Imported_Call_01_urnservicesos.police问题]] | 多类型 ECC 被映射为 `urn:service:sos.police` | 区分网络 category、SIP emergency URN 和 generic URN 配置 |
| [[Imported_Call_02_ECC_csfb_cs后重回LTE时间过长问题]] | ECC 后长时间停留 3G | 区分 CSFB 与 ECC 选网入 3G，核对 `ecc_cs_prefer` / `ecc_cs_only` |
| [[Imported_Call_03_LA_Réunion重定向]] | RE 15/17/18 被重定向到 112 | 本地 `eccdata` / fallback 与运营商需求不一致 |
| [[Imported_Call_04_vowifi_无法拨打电话]] | VoWiFi ECC 复盘附件入口 | 后续 IMS 专项补 IWLAN/ePDG/SIP 证据 |
| [[Imported_Call_05_RTT_通话]] | RTT over VoWiFi | 区分 Dialer RTT 入口能力和底层 IMS/VoWiFi RTT 承载 |
| [[Imported_Call_06_会议通话无法合并]] | IMS 会议通话无法合并 | 按 SIP REFER/202、conf_uri、confRefer/confSubscribe NV 分诊 |
| [[Imported_Call_07_一台DUT插联通卡通话正常_其它DUT_fail_插移动卡问题不复现]] | CSFB 后 3G 承接失败 | 用同卡对比和 RF 校准缺失定位第一坏点 |
| [[Imported_Call_08_5G_to_2G_GPRS_Fallback_Delay_After_Video_Call]] | LTE/5G 回落到 3G/2G 延迟 | 判断 3G 重定向目标不可用和 PLMN 不匹配 |
| [[Imported_Call_09_CS通话杂音]] | CSFB 后 3G 通话杂音 | 结合 ECNO/RSCP 判断 3G 弱场通话质量 |


## 已拆分旧 Outline 案例

| Case | 原始分类 | 用途 |
|---|---|---|
| [[Imported_Call_10_DUT视频通话闪退]] | 五、视频通话 | 通话类旧 Outline case 拆分项 |
| [[Imported_Call_11_DUT视频通话卡死]] | 五、视频通话 | 通话类旧 Outline case 拆分项 |

建议命名：

```text
YYYY-MM-DD_Call_现象_根因.md
```
