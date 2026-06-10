---
doc_type: tool
quality: curated
search_tier: supplemental
domain: LogAnalysis
layer: AP/Modem/RIL
rat: LTE
platform: UNISOC/MTK
status: active
tags: [LTE, Registration, LogAnalysis, UNISOC, MTK]
---

# LTE注册-平台Log速查


## 使用边界

这篇只放平台 log、trace、字段口径。完整 LTE 注册流程放在 [[LTE注册流程]]，平台代码入口放在 [[平台代码与产物速查#LTE注册-平台代码架构速查|LTE注册-平台代码架构速查]]。

## 展锐平台速查

### 分层

| 层级 | 作用 | 定位关注点 |
|---|---|---|
| NAS/ASM | 发起PLMN选择、PLMN搜索、RRC连接请求 | 目标PLMN/RAT、EPLMN、禁用TA、CSG白名单、搜索请求 |
| LRRC/LAS | 组织LTE AS流程并向NAS回报结果 | 小区选择、系统消息、驻留、OOC、RRC建链结果 |
| PHY/DSP | 频点搜索、同步、BCCH读取、测量 | EARFCN、PCI、MIB/SIB、RSRP/RSRQ、OOC测量 |

### 网络模式关键字

展锐 log 里常见网络模式会以 bitmask 或字符串出现。看到下面关键字时先判断目标 RAT 是否包含 LTE：

| 关键字 | 含义 |
|---|---|
| `GSM_ONLY` | 只搜2G |
| `WCDMA_ONLY` | 只搜3G |
| `LTE_ONLY` | 只搜LTE |
| `GSM_WCDMA_AUTO` | 2G/3G自动 |
| `GSM_WCDMA_LTE_AUTO` | 2G/3G/LTE自动 |
| `LTE_NR_AUTO` | LTE/NR自动 |

定位口径：

- 如果配置不包含LTE，后面没有LTE小区选择和Attach不是modem异常。
- 手动搜网和飞行模式恢复时，要确认实际下发的 RAT mask 是否和用户预期一致。
- 双卡平台要确认当前 phoneId/slotId，避免把另一张卡的网络模式当成本卡问题。

### 小区选择消息链

展锐LTE找网驻留建议按下面顺序对齐：

```text
PLMN/RAT选择
-> 频点搜索
-> MIB
-> SIB1
-> SIB2
-> Cell is Suitable
-> Camped
```

关键判断：

- 搜到频点不等于可驻留，要看到SIB和小区适合性判断。
- `Cell is Barred`、`not suitable`、`OOC`、`S criteria fail` 是驻留前失败。
- 已驻留但后续RRC失败，断点转到RACH/RRC建链。

### PLMN搜索

常见观察点：

| 阶段 | 关键证据 | 判断 |
|---|---|---|
| 发起搜索 | PLMN search request、target PLMN/RAT | 目标网络是否正确 |
| 搜索频点 | EARFCN list、band、历史频点/全频段 | 是否只搜错band或历史频点 |
| 发现小区 | PCI、MIB/SIB、PLMN list | 小区是否广播目标PLMN |
| 选择结果 | PLMN search confirm、camp result | 是否成功驻留或返回失败cause |

### OOC与无LTE覆盖

OOC问题优先看：

- 是否完全搜不到LTE频点。
- 是否能同步但读不到MIB/SIB。
- 是否S准则不满足。
- 是否小区被barred或PLMN不允许。
- 是否只因当前band/频点配置不完整导致漏搜。

### RRC建链消息链

```text
RRCConnectionRequest
-> RRCConnectionSetup
-> RRCConnectionSetupComplete
-> LTE AS connection establishment confirm
```

注意：工具显示顺序可能受trace聚合影响，不要只按单条显示先后判断RACH配置和RRC Request关系，要结合上下文。

### RSRP/RSRQ换算

展锐 trace 中某些 RSRP/RSRQ 上报值需要做符号扩展后再判断。常见换算口径：

```text
实际值 = ((上报十六进制值 >> 4) | 0xF000) 转十进制 - 65536
```

例如上报值 `0xFB40`，换算后约为 `-76 dBm`。遇到弱网、OOC、驻留失败时，先确认当前工具是否已经完成换算。

### Trace模块名校准

展锐代码里的 LogManager 模块列表可以用来校准抓log时到底开了哪些trace。LTE注册问题至少关注下面几类：

| 模块/接口 | 用途 |
|---|---|
| `ATC`、`SIM` | 开机、radio on、SIM状态、运营商配置入口 |
| `MM`、`EMM`、`PLM` | PLMN选择、EMM注册、Attach/TAU、禁用PLMN/TA策略 |
| `RABM`、`NAS_SWTH` | NAS/承载管理、跨RAT或注册态切换辅助判断 |
| `GAS` | 2G/3G兜底或回退时的AS侧证据 |
| `LRRC`、`LRRCA` | LTE小区选择、系统消息、RRC建链、连接释放 |
| `LL2_*`、`LTE_L2` | RACH、MAC/RLC/PDCP侧辅助证据 |

常用SAP/接口名：

| SAP/接口 | 典型用途 |
|---|---|
| `GMM_REG_SAP`、`MMCTRL_EMM_SAP` | 注册请求和EMM控制入口 |
| `GMM_NAS_SWTH_SAP`、`PLM_NAS_SWTH_SAP` | 注册态或RAT切换相关线索 |
| `EMM_PH_SAP`、`EMM_ESM_SAP` | EMM与物理层、ESM之间的关键交互 |
| `PLM_AS_SAP`、`MM_PLM_SAP` | PLMN搜索、选网、驻留结果上报 |
| `LRRC_ASM_SAP`、`LRRCA_LRRC_SAP`、`LRRC_LRRCA_SAP` | LTE AS和RRC内部流程 |
| `LRRC_LL2_SAP`、`LL2_LRRC_SAP`、`LTE_L2_SAP` | RRC到L2的连接建立、释放和承载面证据 |

抓log建议：如果只开AP radio log，最多能确认Framework/RIL状态；要定位第一个坏点，至少要保证 `EMM/PLM/LRRC/LRRCA/LL2` 相关trace可解。

## MTK平台速查

### debuglogger结构

| 路径 | 内容 | 用途 |
|---|---|---|
| `mdlog1\*.muxz` | modem主日志 | 用 ELT/MACE2 解 EMM、ESM、ERRC、AT、PS trace |
| `mdlog1\MDDB_PHONE_*.EDB` | modem数据库 | 必须与 muxz 匹配，否则字段容易解不全 |
| `mobilelog\APLog_*\radio_log*` | AP radio log | 看 RILJ、RILC、ServiceStateTracker、NetworkRegistrationInfo、APN下发 |
| `netlog\*.cap` | 网络抓包 | 注册后数据业务、DNS、TCP问题再看 |
| `mdlog1_config` | mdlog配置 | 判断当前抓取是否包含需要的 PS/OTA/SYS trace |

### 解码入口

MTK优先先做三件事：

```text
MDLogMan --info muxz
-> 确认 PlatformInformation / TimeInfo / SW version
-> 用 MACE2 按 SYS、PS/NAS、OTA 过滤
-> 再和 AP radio_log 的 RILJ / ServiceState 时间线对齐
```

常用过滤口径：

| 过滤 | 重点看什么 |
|---|---|
| `SYS` | AT命令、URC、平台初始化、`+EREG/+EGREG/+EIAREG/+PSBEARER` |
| `PS/NAS` | `EMM REG`、`ESM`、Attach Request/Accept/Complete、注册状态 |
| `OTA` | RRC/NAS空口消息；不同数据库可能需要用 MTK 内部短名过滤 |

### MTK开机成功链

详细证据已沉淀到 Case Library：[[2026-05-14_Registration_MTK_LTE开机注册成功]]。

| 阶段 | 关键证据 | 口径 |
|---|---|---|
| PLMN确定 | `getCurPlmn()= KAL_TRUE, cur_plmn = 46001f` | 目标PLMN为中国联通46001 |
| ESM准备 | `REG needs ESM msg to trigger attach` | EMM等待默认PDN/ESM容器后触发attach |
| Attach启动 | `Initial check for attach is passed`、`Procedure is started` | Attach前置检查通过并启动流程 |
| Attach类型 | `EMM_ATTACH_TYPE_COMBINED_ATTACH` | combined EPS/IMSI attach |
| NAS上行 | Attach Request、send success | Attach Request已发出 |
| NAS下行 | Attach Accept、accept OK | 网络接受Attach |
| 默认承载 | `active EPS bearer ID: 5`、`PTI: 1, EBI: 5` | 默认EPS bearer建立 |
| Attach完成 | Attach Complete、send success | UE完成Attach Complete |
| 状态收敛 | `NAS_REG_STATUS_REGISTERED_HOME` | modem侧注册完成 |
| AP同步 | `DATA_REGISTRATION_STATE REG_HOME, rat: LTE`、`IN_SERVICE` | Android侧同步为LTE服务态 |

### 关键字段对齐

| 字段 | Modem/AT侧 | AP侧 | 判断 |
|---|---|---|---|
| PLMN | `46001f`、`+EREG/+EGREG` | `OPERATOR {CHN-UNICOM, UNICOM, 46001}`、`registeredPlmn:46001` | PLMN一致 |
| TAC | `+EREG: 1,"E68A"...` | `tac: 59018` | `0xE68A = 59018` |
| Cell ID | `+EREG: ... "04E0C636"` | `ci: 81839670` | `0x04E0C636 = 81839670` |
| PCI | modem trace/小区上下文 | `pci: 251` | AP可用于和RRC/测量侧对齐 |
| EARFCN/Band | AP `earfcn:1650`、`bands:[3]` | `earfcn:1650` | Band 3 |
| 带宽 | `+ELTEBWINFO: 200` | `bandwidth:20000` | 同一带宽口径的不同单位/缩放 |
| 默认APN | `+EIAREG: ME ATTACH "3gnet.MNC001.MCC460.GPRS",IPV4V6,0` | `SET_INITIAL_ATTACH_APN ... 3gnet ... IPV4V6 ... preferred=true` | APN/PDN type一致 |

### 常见误判

- MTK双卡日志要先确认 phoneId，不要把另一卡的 radio off / unknown 作为本卡失败证据。
- 只看到 AP `REG_HOME` 还不够，最好向 modem 侧补证 Attach Accept、默认 bearer、Attach Complete。
- 只看到 modem attach 成功也不够，仍要确认 AP侧 `NetworkRegistrationInfo`、`ServiceState`、data registration 是否同步。
- `+EREG/+EGREG` 的 TAC/CI 通常是十六进制，和 AP 十进制字段对齐前不要误判为小区不一致。
- `SET_DATA_PROFILE` 里可能包含多个 APN；LTE注册主流程只跟初始 attach/default data APN，其他业务承载另行分析。
- `SET_INITIAL_ATTACH_APN` 只是AP请求入口；MTK最终要看 `AT+EIAAPN` / `MIPC_APN_SET_IA_REQ` / `+EIAREG: ME ATTACH`。
