---
quality: draft
doc_type: flow
domain: BT
feature: First Bad Point
layer: AP/Framework/BTStack/HCI/Controller/RemoteDevice
status: draft
search_tier: supplemental
---

# BT第一坏点速查

## 一句话

蓝牙排障第一轮目标不是解释协议细节，而是快速判断失败在 UI/Framework、蓝牙进程、native stack、HCI/controller、空口/对端，还是具体 Profile。

## 最小抓取命令

```bash
adb logcat -b main -b system -b crash -v threadtime | grep -iE "BluetoothManagerService|AdapterService|BluetoothAdapter|BluetoothBondStateMachine|BluetoothDevice|GattService|ScanManager|BluetoothLeScanner|A2dpService|HeadsetService|Avrcp|bt_stack|bt_btif|bt_btm|bt_gattc|smp|bluetooth_jni"
adb shell dumpsys bluetooth_manager
adb shell dumpsys activity service com.android.bluetooth/.btservice.AdapterService
adb shell dumpsys activity broadcasts > broadcasts.txt
```

底层连接、配对、扫描或数据传输问题需要打开 Bluetooth HCI snoop log，复现后从 bugreport 或设备路径导出并用 Wireshark 分析。

远距离和射频能力问题还要补 BT OTA 报告、CP2/WCN log；如果需要证明空口重传、干扰或实际发射功率，优先补 Ellisys、Frontline 等空口仪 log。

## 按现象分诊

| 现象 | 第一坏点优先级 | 先看证据 |
|---|---|---|
| 蓝牙打不开 | enable 请求 -> AdapterService 绑定 -> JNI/native init -> controller | `BluetoothManagerService`、`AdapterService`、`bt_stack_manager`、crash |
| 蓝牙关不掉 | disable 请求 -> profile stop -> BLE 保留策略 -> native shutdown | `MESSAGE_DISABLE`、`isBleScanAlwaysAvailable`、`event_shut_down_stack` |
| 列表搜不到经典设备 | discovery 是否发起 -> HCI 是否发现 -> UI 是否过滤 | `startDiscovery`、`ACTION_FOUND`、HCI inquiry |
| BLE 设备搜不到 | scanner 注册 -> scan filter -> advertising report -> App 回调 | `registerScanner`、`onScanResult`、HCI LE advertising report |
| 搜到但配不上 | createBond -> pairing request -> 用户确认 -> SMP/SSP/HCI reason | `createBond`、`PAIRING_REQUEST`、`setPairingConfirmation`、HCI |
| 已配对但连不上 | ACL -> SDP/UUID -> Profile connect | `connectAllEnabledProfiles`、`ACTION_UUID`、Profile log、HCI |
| BLE 连接后无服务 | GATT connected -> discoverServices -> ATT response | `connectGatt`、`discoverServices`、ATT error |
| BLE 远距离断链或业务质量差 | OTA 能力 -> PHY -> 连接参数 -> ATT/GATT 包大小 -> App 重试 | TRP/TIS、`LE PHY Update Complete`、connection update、MTU、ATT value、disconnect reason |
| 音乐无声 | A2DP state -> active device -> Audio HAL -> HCI data | `A2dpService`、`AudioService`、`BluetoothAudioHal` |
| 耳机按键无效 | AVRCP 连接 -> 控制命令 -> MediaSession | `Avrcp`、media key、playback state |
| 通话不走蓝牙 | HFP 连接 -> SCO -> call audio route | `HeadsetService`、`SCO`、`AudioService`、Telecom |

## 关键字速查

| 场景 | 关键字 |
|---|---|
| 开关 | `enable(`、`disable(`、`MESSAGE_ENABLE`、`MESSAGE_DISABLE`、`STATE_CHANGED` |
| 服务绑定 | `binding Bluetooth service`、`onServiceConnected`、`sendBluetoothServiceUpCallback` |
| native stack | `libbluetooth_jni.so`、`bt_stack_manager`、`event_init_stack`、`event_shut_down_stack` |
| 经典扫描 | `startDiscovery`、`cancelDiscovery`、`deviceFoundCallback`、`ACTION_FOUND` |
| BLE 扫描 | `BluetoothLeScanner`、`GattService`、`ScanManager`、`onScanResult`、`onScanFailed` |
| BLE 远距离 | `LE PHY Update`、`LE_CODED`、`Connection Update`、`supervision timeout`、`Connection Timeout`、`0x08`、`MTU`、`ATT`、`CID 0x0004`、`TRP`、`TIS` |
| 配对 | `createBond`、`BluetoothBondStateMachine`、`PAIRING_REQUEST`、`BOND_BONDED` |
| 安全协商 | `smp`、`sspRequestCallback`、`btm_sec_bond_by_transport` |
| Profile | `connectAllEnabledProfiles`、`A2dpService`、`HeadsetService`、`Avrcp`、`HidHostService` |
| 音频 | `BluetoothAudioHal`、`A2DP_SOFTWARE_ENCODING_DATAPATH`、`SCO`、`AudioPolicy` |

## 结论模板

```text
现象：
入口：
失败阶段：
第一坏点：
AP证据：
HCI/底层证据：
对端/对比机证据：
结论置信度：
后续补证：
```

## 常见结论边界

- AP log 只有扫描请求，没有 HCI 证据时，不能直接判定对端不广播。
- HCI 有设备发现，但 UI 列表没有显示时，优先查 Framework/UI 过滤或权限策略。
- `BOND_BONDED` 只能说明配对完成，不能证明 Profile 连接成功。
- A2DP connected 不能证明 HFP/SCO 正常，音频问题必须按 Profile 分开写。
- RSSI 只能辅助判断距离和环境，不能单独作为兼容性或硬件根因。
- TRP/TIS 是整机 OTA 能力指标，TRP 越大越好，TIS 越负越好；二者不能替代 HCI 里的 PHY、连接参数和断开原因。
- AP 侧 vendor 功率表或广播 `selected_tx_power` 只能作为线索，不能直接证明连接态数据包运行时 TX power 已经最大。
- GATT/ATT `CID 0x0004` 说明数据走属性协议；不要把它误判成 L2CAP CoC。
