---
quality: curated
doc_type: case
domain: Data
rat: LTE
feature: XCAP dedicated APN / UT bearer
platform: UNISOC
layer: SIM EF / Operator NV / Modem SS / Data bearer
symptom: "42004 白卡注册 LTE 后执行补充业务，AP 已有 xcap DataProfile，但没有发起独立 xcap 数据承载，SS 复用默认 zain PDN"
cause: "白卡 EF_AD(6FAD) 首字节为 0x80，被 UNISOC 识别为测试卡，目标 42004 Operator NV 未按普通运营商卡路径加载/应用"
operator: "Zain KSA / 42004"
project: "A01 / qogirl6"
chipset: "UNISOC 4G platform"
source_log: "F:/Log/A01/A01_XCAP/2026-09-03-16-45-38_42004_XCAP"
first_bad_point: "SIM 初始化读到 EF_AD=80000002，首字节 0x80 触发 UNISOC 测试卡判定"
confidence: high
status: open
search_tier: case_summary
tags:
  - unisoc
  - xcap
  - apn
  - operator-nv
  - sim
  - ef-ad
  - test-sim
---

# 白卡 `EF_AD` 测试模式导致 XCAP 复用默认承载

## 用户现象

白卡写入 42004/42003/42010 PLMN，设备注册 LTE 后执行 Call Forwarding 等补充业务。预期建立独立 `xcap` APN 承载，实际没有看到 `SETUP_DATA_CALL` 请求 `xcap`，XCAP/UT 流量复用了默认 `zain` PDN。

## 结论

第一坏点在白卡 `EF_AD`（文件 ID `6FAD`），不是 APN XML 缺失，也不是 XCAP 服务器不可达。

本次日志读到：

```text
EF_AD = 80 00 00 02
```

按展锐问题分析，`EF_AD` 首字节为 `0x80` 或 `0x81` 时，平台会把白卡识别为测试卡；测试卡不会按普通运营商卡路径加载/应用 Operator NV。因此，即使 IMSI 能得到 `42004`，AP 也加载出了 `xcap` DataProfile，仍不能证明 modem 已采用 42004 Operator NV 中的独立 XCAP APN 策略。

当前根因判断置信度高，但案例暂保持 `open`：还需要把白卡首字节改为普通模式并复测，确认出现独立 `xcap` 承载后再关闭。

## 关键证据

### 1. SIM 初始化直接读到 `EF_AD=80000002`

AP radio log：

```text
08-14 06:09:44.770  AT+CRSM=176,28589,0,0,4,0,"3F007FFF"
08-14 06:09:44.863  +CRSM: 144,0,80000002

08-14 06:10:07.800  IMSI: 420040...
08-14 06:10:07.801  EF_AD: 80000002
08-14 06:10:07.801  update mccmnc=42004
```

其中：

| 字段 | 值 | 含义 |
|---|---|---|
| 文件 ID | `28589 = 0x6FAD` | `EF_AD` |
| 第 1 字节 | `0x80` | Type Approval / test operation；本平台按测试卡处理 |
| 第 4 字节 | `0x02` | MNC 长度为 2 |

`update mccmnc=42004` 只证明 MCC/MNC 已算出，不能反证 42004 Operator NV 已加载并生效。

### 2. AP 已经有 `xcap` profile，排除 APN 数据缺失

```text
08-14 06:10:18.054
DPM-1: Added [DataProfile=[ApnSetting] zain-xcap, ..., 42004, xcap, ...,
type=xcap, ... TrafficDescriptor={mDnn=xcap, null}]
```

这只能证明 AP/Telephony 已生成 `xcap` DataProfile，不代表 CP 的 42004 Operator NV 已加载，也不代表业务一定会请求该 profile。

### 3. 实际建链请求全部使用默认 `zain` APN

```text
08-14 06:12:02.285
RILJ: SETUP_DATA_CALL ... Zain Saoudi Arabia ... mDnn=zain

08-14 06:12:41.256
RILJ: SETUP_DATA_CALL ... Zain Saoudi Arabia ... mDnn=zain

08-14 06:12:41.436
SETUP_DATA_CALL ... cid=1 ... addresses=[172.22.1.100/32, ...]
trafficDescriptors=[TrafficDescriptor={mDnn=zain, null}]
```

问题窗口内没有 `SETUP_DATA_CALL ... mDnn=xcap`，所以没有建立 AP 可见的独立 XCAP 数据承载。

### 4. CP 明确把 SS 绑定到默认 PDN 的 `nsapi 5`

modem log 经字符串抽取后可见：

```text
CSM_RADIO_REASON_IP_CHANGE_SS
172.22.1.100,...
OSAL_netSetNetId: multi-sys 1, type 3, nsapi 5, access_type 0

SS, IP4, TCP, L(172.22.1.100, 0) ~ P(172.22.1.201, 80)
HTTP/1.1 200
```

`172.22.1.100` 与 AP 侧 `mDnn=zain / cid=1` 的地址一致，说明 XCAP/SS 使用的是默认 `zain` PDN，而不是新建独立 XCAP NSAPI。

### 5. 补充业务成功不等于承载符合预期

```text
08-14 06:12:46.841  requesting call forwarding query
08-14 06:12:46.853  RIL_IMS_REQUEST_QUERY_CALL_FORWARD_STATUS
08-14 06:12:49.093  getCallForwardStatusUriResponse
```

CP 侧同时收到 XCAP HTTP 200。它证明服务器可达、业务可完成，但不能证明使用了独立 XCAP APN；本问题检查的是承载选择，而不是补充业务结果。

## NV 证据边界

构建侧 `qogirl6_pubcp_customer_operator_nvitem.bin` 已能解出：

```text
Item 3095: ims APN=ims, xcap APN=xcap, default APN=zain
Item 2959: ss_domain=0
Item 2933: vowifi_ut=1
```

但本次启动日志只看到相关 item 被读取，没有输出 42004 profile 下这些 item 的最终运行值。以下证据均不足以单独证明运行态 Operator NV 已生效：

- 构建 BIN 中存在 42004 配置；
- AP 加载出 `xcap` DataProfile；
- 日志出现 `[DELTA NV] ... already loaded`；
- 日志计算出 `mccmnc=42004`。

运行态结论至少应包含“选中了哪个 Operator profile、目标 item 最终值、实际业务承载”三类证据。

## 修复与最小验证

按展锐建议，白卡 `EF_AD/6FAD` 首字节不要设置为 `0x80` 或 `0x81`。本场景的最小单变量修改为：

```text
修改前：80 00 00 02
修改后：00 00 00 02
```

保留末字节 `02`，即保持 2 位 MNC；修改后必须重新上电，让 SIM 初始化和 Operator NV 选择重新执行。

复测闭环标准：

1. SIM log 读到 `EF_AD=00000002`，MCC/MNC 仍为 `42004`。
2. modem log 能证明加载/采用 42004 对应 Operator profile，并回读目标 XCAP APN/SS 策略值。
3. 执行补充业务时，AP 出现 `SETUP_DATA_CALL ... mDnn=xcap`。
4. CP 出现独立于默认 `zain` PDN 的 XCAP NSAPI/IP；不能只看 `type 3, nsapi 5` 名称，要结合 APN、地址和默认承载对比。
5. XCAP HTTP 成功，补充业务查询/设置通过。

首轮只改 `EF_AD`，不要同时修改 `mn_vowifi_ut` 等其他 NV。若修卡后仍复用默认承载，再单独检查 42004 running NV、XCAP bearer policy 和相关 UT 配置。

## 可复用经验

- 白卡写入目标 IMSI/PLMN，不等于白卡处于普通运营商卡模式；先检查 `EF_AD/6FAD`。
- “AP 有 APN profile”和“CP 加载 Operator NV”是两条配置链，不能互相替代。
- XCAP HTTP 200 只证明业务路径可达；是否建立独立承载，要看 `SETUP_DATA_CALL`、DNN/APN、CID/NSAPI 和 IP 地址。
- 测试 Operator NV 时，优先做单变量验证：先修正 SIM operation mode，再查具体 NV 字段。

## 关联入口

- [[README|Data Cases]]
- [[../../10_Basics/SIM-USIM-EF文件速查#白卡-EF_AD-与-Operator-NV|SIM / USIM EF 文件速查]]
- [[../../60_Configuration/Core-Config/NV参数配置#UNISOC-白卡测试-Operator-NV-前置检查|NV参数配置]]
- [[../../60_Configuration/Core-Config/APN配置方法_重构|APN配置方法]]
