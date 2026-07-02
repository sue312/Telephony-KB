---
quality: draft
doc_type: flow
domain: BT
feature: BLE Long Range
layer: App/GATT/HCI/Controller/RF/OTA
status: draft
search_tier: supplemental
---

# BLE远距离链路与OTA指标

## 一句话

BLE 远距离问题不要只看“能不能连上”。要按 `OTA 射频能力 -> PHY 和连接参数 -> ATT/GATT 数据路径 -> 上层协议和编码` 拆开，分别定义可连接极限、消息可用极限和通话可用极限。

## 适用场景

- BLE 或 GATT 自定义业务距离不达标、远距离断链、弱信号下消息/语音断续。
- 需要对比两台手机或两个硬件版本的 BT OTA 报告。
- HCI log 中看到 `LE_CODED`、connection parameter update、MTU exchange、ATT write/notification 或 `0x08 Connection Timeout`。
- App 通过 GATT 传文字、语音、图片、定位等业务数据，而不是走 A2DP/HFP/SCO。

## 指标速查

| 指标 | 含义 | 方向 | 定位价值 |
|---|---|---|---|
| TRP | Total Radiated Power，总辐射功率，表示整机天线真正辐射到空中的总发射功率 | dBm 越大越好 | 判断“发得有多强”。同等条件下 TRP 更高，对端更容易收到 |
| TIS | Total Isotropic Sensitivity，总全向灵敏度，表示整机各方向综合接收灵敏度 | dBm 越负越好 | 判断“收得有多灵”。例如 `-90 dBm` 优于 `-86 dBm` |
| RSSI | 接收信号强度 | 辅助参考 | 只能辅助判断距离、遮挡和方向，不能单独作为硬件根因 |
| LE Coded PHY | BLE 长距离 PHY，通过编码提升鲁棒性，牺牲吞吐和时延 | 需要 HCI 证据确认 | 远距离场景优先确认 Tx/Rx PHY 是否实际切到 Coded |
| connection interval | BLE 连接事件间隔 | 结合业务取舍 | 间隔越大，空口占用和功耗可能降低，但交互时延增加 |
| slave latency | 从设备可跳过的连接事件数 | 远距离实时业务通常慎用 | latency 高会增加空窗，实时语音一般更倾向 `0` |
| supervision timeout | 连接监控超时 | 弱链路可适当加大 | timeout 太短时，远距离丢包容易过早断链 |
| MTU / ATT value | GATT 单次 ATT value 承载大小 | 越大不一定越好 | 弱链路下小包更稳，大包需要分片和重传策略 |

TRP/TIS 是整机 OTA 结果，不等于芯片 PA 表项。自由空间下，链路预算增加 `N dB` 的理论距离提升约为 `10^(N/20)` 倍；实际距离还会受天线方向、人体遮挡、地面反射、干扰和重传策略影响。

## 第一轮证据

| 证据 | 看什么 |
|---|---|
| BT OTA 报告 | TRP AVG、TIS AVG、各信道 TRP/TIS，确认硬件射频能力和 PASS 条件 |
| HCI snoop / bugreport | PHY、connection update、MTU、ATT/GATT 数据路径、disconnect reason |
| CP2/WCN log | 厂商 controller 侧功率、PHY、异常原因补充；普通文本搜索不命中时用二进制文本方式搜索 |
| App 业务 log | 包大小、分片、ACK/重试、发送 pacing、消息成功率、语音卡顿点 |
| 现场记录 | 距离、视距/遮挡、手机高度、朝向、电量、环境干扰、测试持续时间 |

如果需要空口级证据，优先用 Ellisys、Frontline 等蓝牙协议分析仪。没有空口仪时，HCI 只能证明 Host 和 Controller 之间的数据，不能完整证明空口重传和干扰。

## HCI判断点

| 目标 | 证据点 |
|---|---|
| 是否真的走 Coded PHY | `LE PHY Update Complete` 中 Tx/Rx PHY 是否为 `LE_CODED` |
| 是 GATT/ATT 还是 L2CAP CoC | ACL 数据里的 L2CAP CID；`0x0004` 表示 ATT/GATT，不是 LE Credit Based CoC |
| 单包实际大小 | ATT value 长度、L2CAP length、HCI ACL length；不要只看 App 原始 payload |
| MTU 是否生效 | ATT MTU exchange 后的 MTU 值，以及后续 ATT value 是否按预期限制 |
| 连接参数是否适合弱链路 | `LE Connection Update Complete` 中 interval、latency、supervision timeout |
| 断开原因 | `0x08 Connection Timeout` 通常表示 supervision timeout 内没有收到有效链路包，优先看距离、遮挡、PHY、功率和重试 |

## 弱链路优化方向

| 层级 | 优化方向 | 说明 |
|---|---|---|
| OTA/硬件 | 提升 TRP、改善 TIS、确认天线方向和整机遮挡 | 硬件差距会直接反映到远距离极限 |
| PHY/连接 | 确认 Coded PHY，调整 connection interval、latency、supervision timeout | 目标是减少弱信号下过早 timeout，同时接受更高时延 |
| GATT 承载 | 限制 ATT value，降低大包分片风险，控制 write without response pacing | 弱链路下“小包 + 慢 pacing”通常比大包猛发更稳 |
| 上层协议 | 加 sequence、ACK、重试、去重、续传 | GATT 成功写入不等于业务消息完整到达 |
| 编码 | 语音降低码率、缩短或调整帧大小，图片/定位/文字做紧凑编码 | 编码只降低业务 payload，不会改变硬件链路预算 |
| 播放/录音 | 降噪、AGC、jitter buffer | 改善主观语音质量，但不解决空口断链本身 |

## 测试记录模板

```text
设备/版本：
OTA 结果：TRP AVG=，TIS AVG=，信道：
场地：空旷/遮挡/室内，手机高度，朝向，电量：
距离点：300m / 350m / 400m / ...
业务类型：短文字 / 语音消息 / 实时通话 / 图片 / 定位
PHY：Tx=，Rx=
连接参数：interval=，latency=，timeout=
MTU/ATT：MTU=，ATT value=，L2CAP length=，HCI ACL length=
结果：成功率，平均时延，卡顿，重试次数，断开时间
断开原因：HCI reason / AP log / CP2 log
结论：可连接极限，消息可用极限，通话可用极限
```

## 结论边界

- BT OTA PASS 说明整机射频指标满足测试要求，但不自动证明当前 App 业务的 PHY、连接参数和上层协议都最优。
- AP 侧功率表、vendor 配置或 `selected_tx_power` 只能作为线索；连接态数据包实际发射功率需要 controller/CP2 证据或空口仪补证。
- `0x08 Connection Timeout` 更偏底层链路超时，不应直接归因于 APK 主动断开。
- GATT/ATT `CID 0x0004` 说明走属性协议，不是 L2CAP CoC；不要把二者的分片、重传和流控策略混用。
- 远距离通话质量由链路预算、PHY、连接参数、包大小、重传策略、编码码率、jitter buffer、录放音处理共同决定。

## 关联文档

- [[BLE广播扫描连接GATT流程]]
- [[BT基础概念与分层]]
- [[BT第一坏点速查]]
