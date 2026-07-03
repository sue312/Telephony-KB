---
doc_type: triage
domain: Troubleshooting
status: active
quality: curated
search_tier: main_entry
---

# Modem稳定性排障流程

## 阅读入口

这篇用于 modem assert、blocked、radio unavailable、modem 不起等稳定性问题第一轮分诊。真实历史问题看 [Stability Cases](../40_Case-Library/Stability/README.md)，业务背景看 [Modem稳定性与Assert](../20_Service-Flows/Stability/Modem稳定性与Assert.md)。

写码、升级、IMEI unknown、Meta 连接和 RF 参数类历史问题统一看 [NVRAM与产物链路问题索引](../40_Case-Library/Stability/NVRAM与产物链路问题索引.md)。

## 分诊顺序

|  顺序 | 判断点                | 关键证据                                      |
| --: | ------------------ | ----------------------------------------- |
|   1 | 是 modem 重启还是 AP 误判 | radio unavailable、modem reset、assert dump |
|   2 | 是否有 assert 信息      | assert reason、file/line、task、stack        |
|   3 | 触发业务是什么            | 注册、数据、通话、SIM、NV、OTA、开关机                   |
|   4 | 是否与 NV/校准相关        | fixnv、rfnv、IMEI、校准区、NV merge              |
|   5 | 是否版本/patch 相关      | modem image、patch list、编译产物、刷机包           |
|   6 | 是否可复现              | 同机同卡、不同卡、对比版本、最小复现步骤                      |

## 最小证据包

- AP：radio log、kernel log、bugreport、触发时间点。
- Modem：assert dump、trace、版本号、modem image 信息。
- 产物：刷机包、modem patch、NV 分区备份或回读结果。
- 复现：触发动作、概率、对比版本、是否恢复出厂或格式化 NV。

## 结论边界

- `RADIO_NOT_AVAILABLE` 不等于 modem assert，可能只是 radio service 重启或飞行模式切换。
- IMEI 丢失、校准丢失、fixnv 损坏类问题必须保留分区证据，不能只用 AP 现象下结论。
- OTA / A/B 升级相关问题要看升级日志和分区处理顺序，不只看升级后现象。
- 通话中 modem assert 不一定是通话协议根因，也可能由 AP/BSP 外设访问诱发。历史 case [G100 通话过程中 modem assert](../40_Case-Library/Stability/Imported_Stability_G100_通话过程中ModemAssert_PWM32K时钟源.md) 的第一坏点是灯环 PWM 32K clock source 占用总线。

## 常见首坏点样例

| 样例 | 首坏点 | 复用口径 |
|---|---|---|
| [G100 通话过程中 modem assert](../40_Case-Library/Stability/Imported_Stability_G100_通话过程中ModemAssert_PWM32K时钟源.md) | BSP 灯环 PWM 32K clock source 访问寄存器耗时长、占用总线 | 业务触发 modem assert 时要查 AP/BSP 外设改动和二分结果 |
| [NVRAM与产物链路问题](../40_Case-Library/Stability/NVRAM与产物链路问题索引.md) | LID size、加密宏控、modem image、RF 参数不一致 | IMEI unknown / META 失败 / modem EE 先查产物和 NV 链路 |
| [MTK Patch 导致 ModemEE](../40_Case-Library/Stability/2025-06-27_Stability_MTK_Patch导致ModemEE.md) | patch 引入固定场景 EE | 查 patch list、CR 依赖和 modem 产物 |
| [CA 能力上报异常导致 assert](../40_Case-Library/Stability/2025-06-25_Stability_UNISOC_CA能力上报异常导致ModemAssert.md) | UE capability 上报超平台能力 | 注册/数据异常伴随 assert 时查能力矩阵 |
