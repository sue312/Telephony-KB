---
doc_type: index
domain: BT
status: active
quality: draft
search_tier: main_entry
---

# BT

## 阅读顺序

- 先看基础分层，分清 Android Framework、蓝牙进程、native stack、HCI、Controller 和对端设备分别负责什么。
- 再按现象进入开关、扫描发现、配对绑定、Profile 连接、BLE/GATT 或音频专项流程。
- 真实项目 log、根因和修复结论放到 `40_Case-Library`，本文只保留可复用流程、第一坏点和证据入口。

本目录用于沉淀 Android 蓝牙问题的基础概念和业务流程。首版参考 `F:\Codex\Knowledge\lte\蓝牙基础.pdf`，重点覆盖蓝牙开关、经典扫描、BLE 扫描、配对绑定、Profile 连接和 HCI 证据。

## 入口

| 文档 | 用途 |
|---|---|
| [[BT基础概念与分层]] | BR/EDR、BLE、Profile、GATT、SMP、HCI、Controller 等基础概念和分层 |
| [[BT开关流程]] | Settings/SystemUI 到 BluetoothManagerService、AdapterService、native stack、状态广播的开关链路 |
| [[BT扫描与发现流程]] | 经典蓝牙 discovery 和 BLE scan 的入口、回调、广播和常见失败点 |
| [[BT配对与绑定流程]] | createBond、BondStateMachine、SSP/SMP、PAIRING_REQUEST、BOND 状态变化 |
| [[BT连接与Profile流程]] | 配对后 ACL/Profile 连接，A2DP、AVRCP、HFP、HID、PAN 等 Profile 分诊 |
| [[BLE广播扫描连接GATT流程]] | BLE 广播、扫描、connectGatt、discoverServices、read/write/notify 主流程 |
| [[BLE远距离链路与OTA指标]] | BLE 远距离通信、BT OTA TRP/TIS、Coded PHY、连接参数、GATT 包大小和断链分析 |
| [[BT音频流程-A2DP-AVRCP-HFP]] | 蓝牙音乐、媒体控制、通话音频和 Audio HAL 观察点 |
| [[BT第一坏点速查]] | 按现象决定第一轮抓什么证据、先看哪一层 |

## 问题分流

| 用户现象 | 优先入口 | 第一轮判断 |
|---|---|---|
| 蓝牙打不开或关闭卡住 | [[BT开关流程]] | Framework 状态机、AdapterService 是否拉起、native stack 是否 init/shutdown 完成 |
| 搜不到设备 | [[BT扫描与发现流程]] | 经典 discovery 还是 BLE scan、权限/过滤条件、controller 是否有发现事件 |
| 能搜到但配不上 | [[BT配对与绑定流程]] | createBond 是否发起、配对请求是否弹出、SSP/SMP 是否失败、HCI reason |
| 配对成功但连不上 | [[BT连接与Profile流程]] | ACL 是否建立、SDP/UUID 是否完成、目标 Profile 是否启用和连接 |
| BLE 设备偶现搜不到或连接慢 | [[BLE广播扫描连接GATT流程]] | scan filter、advertising report、connectGatt、GATT service discovery |
| BLE 远距离断链、消息丢失或通话断续 | [[BLE远距离链路与OTA指标]] | OTA TRP/TIS、Coded PHY、connection interval、supervision timeout、ATT/GATT 包大小、HCI disconnect reason |
| 蓝牙耳机无声、按键无效或通话异常 | [[BT音频流程-A2DP-AVRCP-HFP]] | A2DP/AVRCP/HFP 分开看，确认 profile 状态、audio route 和 HAL |

## 最小证据包

| 证据 | 用途 |
|---|---|
| `adb logcat -b main -b system -b crash -v threadtime` | Framework、蓝牙进程、广播、状态机和 Java service |
| `adb shell dumpsys bluetooth_manager` | system_server 内的 BluetoothManagerService 状态、绑定和 enable/disable 记录 |
| `adb shell dumpsys activity service com.android.bluetooth/.btservice.AdapterService` | AdapterService 组件运行和绑定状态 |
| `adb shell dumpsys activity broadcasts` | ACTION_FOUND、PAIRING_REQUEST、BOND_STATE_CHANGED 等广播是否发出 |
| bugreport + Bluetooth HCI snoop log | HCI command/event、pairing reason、ACL/GATT/audio 数据路径证据 |
| BT OTA 报告 / CP2 或 WCN log / 空口仪 log | TRP/TIS、controller 侧功率和 PHY、远距离断链、空口重传与干扰证据 |

## 写法约定

- 流程文档写“正常路径 + 常见异常分叉 + 第一坏点”，不要把单次项目日志全文贴入。
- 经典蓝牙和 BLE 分开描述；同一个设备可能是 Dual mode，结论中要写清 transport。
- 配对成功不等于连接成功，连接成功也不等于目标 Profile 可用。
- HCI 只能证明 Host 和 Controller 之间的命令/事件，应用 UI、权限、策略和 profile 状态仍要回到 AP log 交叉验证。
