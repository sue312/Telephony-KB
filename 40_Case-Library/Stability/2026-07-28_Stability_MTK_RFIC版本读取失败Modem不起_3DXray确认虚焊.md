---
quality: curated
doc_type: case
domain: Stability
rat: Mixed
feature: modem boot / RFIC version check / 3D X-ray
platform: MTK
layer: Modem/MML1/MMRF/RFIC/HW
symptom: "售后两台设备不识卡或 Modem 起不来，MD1 进入 READY 后约 1 秒触发 RF check assert 并反复重启"
cause: "目标 RFIC 焊点虚焊，导致 RFIC1/RFIC2 版本均读取为 0x00；3D X-ray 已确认虚焊"
project: "GH66B2 / Astech IRIS"
chipset: "MT6789"
source_log: "售后 DebugLogger AP kernel log / MTK FAQ33228 / 3D X-ray"
first_bad_point: "mml1_rf_error_check.c line 156，期望 RFIC 版本 0x02，RFIC1/RFIC2 回读均为 0x00"
confidence: high
search_tier: case_summary
status: summarized
tags:
  - stability
  - modem-boot
  - modem-assert
  - rfic
  - x-ray
  - soldering
  - hardware
---

# MTK RFIC 版本读取失败导致 Modem 反复 Assert（3D X-ray 确认虚焊）

## 用户现象

售后仅有两台设备异常，表现为不识卡、Modem 起不来或 radio 不可用。日志中 MD1 可以完成上电并短暂进入 READY，但约 1 秒后进入 EXCEPTION，随后持续复位重启。

问题最初可能以 STK、不识卡或 Telephony 不可用的形式暴露，但第一坏点发生在 Modem RF 初始化阶段，不属于 STK、SIM ATR 或 AP Telephony 业务问题。

## 结论

> [!success] 根因
> 3D X-ray 检查确认目标 RFIC 焊点存在虚焊。虚焊导致 Modem 无法正确读取 RFIC 版本：软件期望值为 `0x02`，RFIC1 和 RFIC2 回读均为 `0x00`，触发 `mml1_rf_error_check.c line 156` Assert，最终形成 Modem 反复重启。

故障链路如下：

```text
RFIC 焊点虚焊
  -> RFIC 供电、时钟或 BSI 控制/回读链路异常
  -> RFIC1/RFIC2 version 均回读 0x00
  -> MML1 RF_Chip_Version_Check Assert
  -> MD1 进入 EXCEPTION 并复位
  -> AP 表现为不识卡、radio unavailable、IMEI/Modem 版本不可用
```

## 关键证据

### 1. Modem 已经完成基础启动

```text
[ccci1/fsm] md_state change from 3 to 4
```

MD1 能够进入 READY，说明不是 Modem 镜像完全未加载、上电失败或 AP 侧服务未拉起。

### 2. READY 后立即进入异常

```text
[ccci1/fsm] md_state change from 4 to 5
[ccci1/fsm] filename = mcu/l1/mml1/mml1_rf/src/mmrf/gen95/mml1_rf_error_check.c
[ccci1/fsm] line = 156
[ccci1/fsm] assert para0 = 0x00000002, para1 = 0x00000000, para2 = 0x00000000
```

同一 Assert 在每次 Modem 重启后重复出现，说明 RF 初始化检查稳定复现，而非偶发 AP Telephony 超时。

### 3. Assert 参数含义

依据 MTK FAQ33228 和 `CS0021-GAK1J-AND-V1.0EN_Platform_System_RF_MMRF_RF_Error_Check_Application_Note` 第 5.1.8 节：

| 参数 | 含义 | 本次取值 |
|---|---|---|
| `para0` | 软件期望的 RF Chip version | `0x02` |
| `para1` | 从 RFIC1 读取的 RF Chip version | `0x00` |
| `para2` | 从 RFIC2 读取的 RF Chip version | `0x00` |

`para1` 或 `para2` 与 `para0` 不一致时会触发 Assert。本次两个回读值均为 `0x00`，优先指向 RFIC 公共供电、26 MHz 时钟、BSI/3-wire 通信链路或焊接连接异常。

> [!note] RFIC1/RFIC2 不是 SIM1/SIM2
> RFIC1 和 RFIC2 是 Modem 软件中的 RF 收发器实例编号，具体对应一颗还是多颗实体 RF Transceiver 取决于项目硬件设计。

### 4. 硬件证据

- 异常范围只有两台售后机，不是批量软件问题。
- 普通 2D X-ray 未能可靠排除不润湿、界面裂纹等隐性虚焊。
- 后续 3D X-ray 可见目标 RFIC 焊点虚焊，完成硬件根因确认。

## 排查要点

| 检查项 | 判断方法 |
|---|---|
| 单机还是批量 | 零星售后机优先检查焊接、器件和板级链路；批量问题再优先核对 RF custom、BOM 和 SW load |
| Modem 状态 | 先确认是否进入 READY；READY 后立即 Assert 与镜像完全无法加载是两类问题 |
| Assert 参数 | `expected != RFIC readback` 时按 RF Chip version check 处理，不要转 SIM/Registration 排查 |
| RF 供电 | 对比正常机检查 `VTCXO24`、`VIO18`、`VRF18`、`VRF12` 和 `SRCLKEN_O0/O1` |
| RF 时钟 | 检查 RFIC 26 MHz 时钟的幅度、起振时刻和稳定性 |
| RF 控制总线 | 检查 BSI/3-wire 的 `CLK`、`CS`、`DATA` 是否有开路、短路、无返回或接触不良 |
| X-ray | 2D X-ray 正常不能排除 Head-in-Pillow、焊点界面裂纹或 Pad cratering；必要时做斜角/3D CT |
| 最终确认 | 对目标 RFIC 重焊、Reball 或更换后，复测 Assert 是否消失并确认 RFIC version 回读恢复 |

## 容易误判的日志

日志中可能同时出现：

```text
open /dev/block/by-name/modem_a fail
```

该报错不是本案根因。系统随后能够从实际 Modem 分区继续启动并进入 READY；真正的第一坏点是 RFIC version readback 不匹配。

## 处理与复测建议

1. 对 3D X-ray 标识的 RFIC 异常焊点执行规范返修，优先采用 Reball 或更换 RFIC，避免只做无法控制温度曲线的局部加热。
2. 返修前后保留 X-ray 图片，并记录 RFIC 料号、主板 SN、维修动作和复测结果。
3. 返修后确认 Modem 不再出现 `mml1_rf_error_check.c line 156`，MD 状态可以持续保持 READY。
4. 确认 IMEI、Modem 版本、SIM 识别、注册和数据业务恢复，避免只以“能开机”作为关闭标准。
5. 若返修后仍复现，再按 MTK line 121 SOP 检查 RF 供电、26 MHz 和 BSI/3-wire 波形。

## 复用规则

- 售后零星设备出现 line 156，且 RFIC 回读为 `0x00`：优先转 RF 硬件和焊接分析。
- 相同版本出现批量问题：优先核对实际 RFIC 型号/ECO version、RF custom、BOM 和 Modem SW load。
- 2D X-ray 未见异常不能直接排除虚焊；日志高度指向 RFIC 且电气检查异常时，应升级到斜角 X-ray、3D CT 或返修交叉验证。
- AP 层不识卡、radio unavailable、IMEI/Modem 版本为空是 Modem 未正常工作的连带现象，不应拆成多个业务问题分别排查。

## 相关案例

- [[Imported_SIM_05_GH66B2Astech售后反馈不识卡]]：旧导入记录，保留最初的 RFIC version check 证据。
- [[2024-01-25_Stability_UNISOC_RFIC读取失败Modem不起]]：UNISOC 平台 RFIC type 读取失败的同类售后案例。

## 参考资料

- MTK FAQ33228：`mml1_rf_error_check.c line = 156`
- `CS0021-GAK1J-AND-V1.0EN_Platform_System_RF_MMRF_RF_Error_Check_Application_Note`
  - 5.1.8：`MML1_ErrorCheck_RF_Chip_Version_Check`
  - line 121 SOP：RF power、RF chip、3-wire layout、SW load 排查方法
