---
doc_type: case
quality: imported_reference
domain: Stability
rat: LTE
feature: 'Modem Assert / PWM bus contention'
platform: MTK
layer: 'BSP/PWM/Modem'
symptom: 'G100 通话过程中，出现Modem Assert'
cause: '灯环 PWM 时钟源使用 32K，访问 PWM 寄存器耗时长并占用总线，通话过程中诱发 modem assert；改为 26MHz 时钟源规避'
source_log: 'Old Outline knowledge base; split from SIM问题案例补充.md'
first_bad_point: 'ccci modem assert 指向 lte_scheduler.c，同时二分定位到灯环 PWM 32K clock source'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - modem-assert
  - pwm
  - bsp
search_tier: case_summary
---

# G100 通话过程中，出现Modem Assert

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从 SIM 导入区迁到 Stability。它的首坏点不是 SIM，而是 BSP 灯环 PWM 修改导致 modem assert。

## 用户现象
G100 通话过程中，出现Modem Assert

## 结论

首坏点在 BSP 灯环 PWM 配置。问题通过软件二分定位到灯环修改；最终确认 PWM clock source 使用 32K 后，访问 PWM 寄存器耗时变长并占用总线，通话过程中诱发 modem assert。处理方案是把 PWM 时钟源改为 26MHz。

该 case 应归 Stability / BSP / Modem Assert，不应放在 SIM 问题库里。

## 关键证据

- 原始分类：一、Modem 崩溃
- 来源：SIM问题案例补充.md
- 拆分序号：14
- Assert 文件：`dsp2/md32/usip/inner/modem/lte/lte_scheduler/src/lte_scheduler.c`
- Assert 行号：`line = 2135`
- 二分结果：问题由灯环修改引入。
- 根因：PWM clock source 使用 32K，访问 PWM 寄存器耗时长，占用总线时间较长。
- 修复：PWM clock source 改为 26MHz。

## 定位口径

| 判断点 | 结论 |
|---|---|
| modem assert 发生在通话过程中 | 先看 assert 文件/行号和触发业务，不直接归网络 |
| 软件二分指向 BSP 灯环 | 按 BSP 外设/总线占用方向查 |
| 拆灯环/换闪光灯/常亮验证 | 用于排除硬件器件和 PWM 频率影响 |
| 改 26MHz 后规避 | 说明时钟源/访问耗时是关键变量 |

## 复用边界

- 适用于“业务过程中 modem assert，但最终由 AP/BSP 外设访问诱发”的交叉问题。
- 新项目复用时必须补齐 assert dump、二分区间和 PWM clock 变更验证，不能只凭同样行号直接套结论。

## 原始案例内容

### 案例：G100 通话过程中，出现Modem Assert

```javascript
<5>[  157.035281][  T523] [ccci1/fsm]filename = dsp2/md32/usip/inner/modem/lte/lte_scheduler/src/lte_scheduler.c
<5>[  157.035284][  T523] [ccci1/fsm]line = 2135
<5>[  157.035288][  T523] [ccci1/fsm]assert para0 = 0x00000012, para1 = 0x00000000, para2 = 0x00000000
```

分析：FAQ上没找到类似报错，提MTK分析是硬件问题。后续排查软件，发现之前软件没这个问题。

二分法找到是灯环修改导致的问题，排查到底层灯环修改导致的，然后又做了一系列问题定位找root cause，排除了很多猜测。

1.先拆除灯环芯片验证，不行再更换闪光灯芯片（更换成OCP81375）  @薛逢军(Xue FengJun)
2.不走PWM,设置常亮验证   @马紫鹏(Ma ZiPeng)
3.保持灯环闪烁频率一致，先验证来电时频率，再验证接通后的频率。   @马紫鹏(Ma ZiPeng)

根本原因：pwm clock source用的32K，读写速度会比较慢，访问PWM寄存器所需时间更长。这会导致总线占用时间延长，导致占用总线时间较长，进而导致modem crash

解决方案：将时钟源更改为26MHZ，修改26Mhz没什么风险

## 原始资料边界

- 本 case 来自旧 SIM 问题集合，但已迁移到 Stability。
- 如果后续整理 BSP/外设诱发 modem assert 专题，可将本 case 作为模板。
