---
quality: curated
search_tier: main_entry
doc_type: tool
domain: Debug
layer: AP/Modem
status: active
---

# Log分析方法

AP log 和 modem log 的通用分析方法统一放在这里。LTE 注册专项字段仍放在 [[LTE注册-平台Log速查]]。

## AP-log分析方法

### AP log能回答什么

- Framework有没有发起请求。
- RIL有没有收到响应或UNSOL。
- ServiceState/IMS/SIM状态是否正确更新。
- CarrierConfig是否加载。
- 上层API和UI看到的状态是什么。

### AP log不能直接回答什么

- 网络侧真实拒绝原因的完整上下文。
- modem内部状态机为什么走到某个分支。
- 无线底层失败原因。
- IMS核心网内部错误。

### 建议分析顺序

1. 定时间窗：从用户操作前30秒到恢复后30秒。
2. 搜SIM状态：`UiccController`、`SIMRecords`、`IccCardProxy`。
3. 搜注册状态：`ServiceStateTracker`、`NetworkRegistrationManager`、`RILJ`。
4. 搜IMS状态：`ImsResolver`、`ImsManager`、`ImsPhoneCallTracker`。
5. 搜配置：`CarrierConfigLoader`、`carrier_config`。
6. 搜异常：`Exception`、`RADIO_NOT_AVAILABLE`、`not registered`、`reject`。

### 常用关键字

```text
RILJ
ServiceStateTracker
NetworkRegistrationManager
VoiceRegState
DataRegState
UiccController
SIMRecords
CarrierConfig
ImsResolver
ImsManager
ImsPhoneCallTracker
RADIO_NOT_AVAILABLE
OUT_OF_SERVICE
IN_SERVICE
```

### Data连通性关键字

数据连接成功但上不了网时，AP log 先看 `NetworkMonitor` 和 `ConnectivityService`，再用 netlog/pcap 和 modem log 对齐。

| 关键字 | 用途 |
|---|---|
| `SETUP_DATA_CALL` / `DataCallResponse` | 确认 APN、cid、ifname、IP、DNS 是否下发 |
| `ConnectivityService` | 默认网络切换、蜂窝网络 connected/disconnected、validation 结果 |
| `NetworkMonitor` | DNS/HTTP/HTTPS 连通性检测 |
| `PROBE_DNS` | DNS query 是否 timeout |
| `PROBE_HTTP` / `PROBE_HTTPS` | 连通性 URL 是否返回 204、是否 timeout |
| `UnknownHostException` | 域名解析失败后的应用层表现 |
| `validation failed with redirect` | 运营商门户或网关重定向 |
| `SocketTimeoutException` | HTTP/HTTPS 建连或读超时 |

输出结论建议明确分层：

```text
建链事实：data call 已成功，IP/DNS/ifname 已下发。
AP侧事实：NetworkMonitor 在 xx:xx:xx 出现 PROBE_DNS timeout / redirect / HTTPS timeout。
数据面事实：netlog 中 DNS query 是否有 response，TCP 是否重传。
边界：注册成功不代表数据可用，飞行模式恢复也不能单独证明 APN 或 modem 根因。
```

### 输出要求

AP log分析结论建议这样写：

```text
AP侧事实：xx:xx:xx RILJ收到xxx，ServiceStateTracker随后将data registration更新为xxx。
AP侧推断：framework状态更新链路正常/异常。
盲点：缺少modem log，无法确认网络侧reject的底层原因。
```

## Modem-log分析方法

### Modem log优先回答什么

- 是否完成搜网、小区选择、RRC建立。
- NAS注册/TAU/Registration是否被拒绝。
- IMS SIP是否发出、收到什么响应。
- CS call是否收到SETUP/RELEASE和cause。
- 是否发生assert、SSR、内部状态机异常。

### 建议分析顺序

1. 先定业务：注册、IMS、call、SIM、data、assert。
2. 找触发事件：开机、插卡、飞行模式、拨号、Wi-Fi切换、弱网。
3. 拉关键流程：RRC -> NAS -> IMS/SIP 或 CS call。
4. 标 cause code、timer、retry。
5. 与AP时间线对齐：看AP是否正确收到modem结果。

### 典型判断

| 现象        | 需要找的modem证据                               |
| --------- | ----------------------------------------- |
| 无服务       | PLMN search、cell selection、NAS reject     |
| LTE注册失败   | Attach/TAU reject cause                   |
| SA注册失败    | 5GMM Registration reject cause            |
| IMS未注册    | IMS bearer、P-CSCF、SIP REGISTER            |
| VoLTE拨号失败 | SIP INVITE、SIP error、media setup          |
| CS拨号失败    | SETUP、RELEASE COMPLETE、Q.850 cause        |
| Modem重启   | assert reason、call stack、trigger scenario |

### 注意

如果只有modem log，不要直接下 Android framework 根因。最多写：

```text
Modem侧已上报/已完成xxx；是否被AP正确处理需要AP log确认。
```

### MTK日志工具速查

MTK 平台优先确认日志格式和工具链是否匹配：

| 工具/视图 | 用途 | 备注 |
|---|---|---|
| DebugLoggerUI | 端侧抓取 AP / modem / network issue log | 网络类问题建议打开 TelephonyLog 动态配置并重启复现 |
| ELT | 打开 `.MUXZ`，做 MTK modem trace 离线分析 | 需要匹配版本工具和数据库 |
| PS Integrated | 顺序查看 trace、primitive、基础日志 | 适合拉完整时间线 |
| PS Modules | 按模块过滤 trace | 适合定位 NWSEL、EMM/ESM、NRRC、SIM_DRV 等模块 |
| PS Trace Peer | 查看 L3/L4 OTA 消息 | 适合看 NAS/RRC/SIP 等空口/协议消息 |
| Find Result | 保存和复用搜索结果 | 适合沉淀关键字集合 |

网络/IMS/注册问题抓 MTK log 时建议：

1. 打开 USB debugging。
2. 进入 Engineer Mode 的 Log and Debugging / DebugLoggerUI。
3. 打开 Tag Log。
4. 网络类问题打开 Dynamic Settings -> TelephonyLog。
5. 重启后复现，确保包含完整开机注册链路。
6. 停止日志并导出 debuglogger 目录。

### 平台关键字分层

| 方向 | MTK常见关键字 | UNISOC常见关键字 |
|---|---|---|
| 选网 | `NWSEL`、HPLMN/EHPLMN/FPLMN | `GMM`、`EMM`、`PLMN`、平台 NW 模块 |
| NR RRC | `NRRC_SI`、`NRRC_PDU_Event`、T300 | NRRC/RRC setup/release |
| RACH | `NL2_MAC_RACH_Attempt_*`、`NL1_RACH_Information` | MAC/RACH attempt/result |
| SIM | `SIM_DRV`、`No ATR`、`SIM_PLUG_OUT_IND` | `USIMDRV`、`USIMCHIP` |
| IMS | `VDM`、SIP、IMS CC cause | IMS/SIP/PDN/P-CSCF |
| Assert | `ModemEE`、AEE、assert dump | modem assert、systemdump、memdump、ETB |
