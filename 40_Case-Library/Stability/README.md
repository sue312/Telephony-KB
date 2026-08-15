---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# Stability Cases

Modem assert、SSR、radio restart、稳定性、长稳、弱网触发崩溃相关 case 放这里。

## 已整理案例

| Case | 场景 | 用途 |
|---|---|---|
| [[NVRAM与产物链路问题索引]] | 写码 / 升级 / IMEI unknown / Meta / RF 参数链路 | 从旧 SIM 导入内容归并出的 Stability 总入口 |
| [[2021-01-12_Stability_UNISOC_RDNV保存后双卡Modem崩溃_CustNV差异]] | RDNV 保存后双卡 modem 崩溃 | 用保存前后 bin 差异和 CustNV 对比定位第一坏点 |
| [[2022-03-04_Stability_UNISOC_fastboot刷fixnv导致IMEI校准丢失]] | fastboot 直接刷 fixnv 后 IMEI/校准参数丢失 | 识别刷机流程覆盖个体化 NV 的第一坏点 |
| [[2022-04-05_Stability_UNISOC_fixnv损坏IMEI校准丢失_回读证据包]] | 售后 IMEI/校准参数丢失怀疑 fixnv 损坏 | fixnv 主备分区回读证据包模板 |
| [[2023-09-18_Stability_UNISOC_AB_OTA_nvmerge前中断fixnv风险]] | A/B OTA 在 nvmerge 前中断 | 定位 fixnv 写入后、个体化参数合并前的风险窗口 |
| [[2024-01-25_Stability_UNISOC_RFIC读取失败Modem不起]] | 售后单机不识卡、modem not alive | 用 sysdump assert 将 AP radio unavailable 追到 RFIC 读取失败 |
| [[2024-07-31_Stability_UNISOC_fixnv双备损坏Modem不起]] | fixnv 主备损坏导致 modem boot fail | 把不识卡/IMEI 丢失/radio unavailable 归到 modem 启动第一坏点 |
| [[2024-08-05_Stability_UNISOC_售后IMEI丢失WSRCH校准NV损坏]] | 售后无信号、IMEI null、WSRCH assert | 通过 RF calibration assert 识别校准 NV/分区损坏 |
| [[2025-06-27_Stability_MTK_Patch导致ModemEE]] | MTK patch 引入 IMS call retry 崩溃 | patch 回归和 CR 依赖排查样例 |
| [[2025-06-25_Stability_UNISOC_CA能力上报异常导致ModemAssert]] | 注册后无法上网并 modem assert | 检查 UE capability 上报 CA 组合是否超平台能力 |
| [[2025-08-01_Stability_UNISOC_ModemBlocked]] | 展锐 modem blocked 现场 | blocked 问题证据保全和规避边界 |
| [[2026-07-28_Stability_MTK_RFIC版本读取失败Modem不起_3DXray确认虚焊]] | 售后两台 Modem 反复 Assert、不识卡 | 从 line 156 RFIC version 回读失败追到 3D X-ray 确认 RFIC 虚焊 |
| [[Imported_Stability_G100_通话过程中ModemAssert_PWM32K时钟源]] | G100 通话过程中 modem assert | BSP 灯环 PWM 32K clock source 占用总线诱发 modem assert |

建议命名：

```text
YYYY-MM-DD_Stability_现象_模块.md
```
