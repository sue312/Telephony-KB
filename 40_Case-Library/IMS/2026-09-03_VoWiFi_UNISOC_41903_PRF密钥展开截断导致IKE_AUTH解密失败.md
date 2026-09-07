---
quality: curated
search_tier: case_summary
doc_type: case
target_doc_type: case
domain: IMS
rat: LTE/IWLAN
feature: VoWiFi / IKEv2 / ePDG / EAP-AKA
platform: UNISOC
layer: Modem/IKE/Crypto/IMS
symptom: "A01 插入 41903 SIM，注册 LTE 并打开 Wi-Fi 后，VoWiFi 始终无法注册"
cause: "4G_MODEM_22B_W24.36.3 计算 PRF+ 轮次时未按实际总密钥长度取足轮次，只生成 200/252 字节，导致 SK_er 尾部及 SK_pi/SK_pr 被零填充，首个 IKE_AUTH 响应解密失败"
operator: 41903 / Ooredoo Kuwait
project: A01
chipset: qogirl6
vendor_customization: Operator NV / IKE proposal
android_version: TBD
modem_version: FAIL 4G_MODEM_22B_W24.36.3; REF 4G_MODEM_22B_W25.45.3; PATCH 临时验证版本号待归档
source_log: "F:/Log/A01/A01_VOWIFI/2026-09-03-10-47-15_41903 VOWIFI; F:/Log/A01/A01_VOWIFI/2026-09-03-17-33-50_REF_41903 VOWIFI"
first_bad_point: "IKE_SA_INIT 后生成的 SK_er 仅前 20/32 字节有效，后 12 字节为 0；SK_pi/SK_pr 全 0，密钥展开恰在累计 200 字节处停止"
confidence: high
status: closed
tags:
  - ims
  - vowifi
  - ikev2
  - epdg
  - eap-aka
  - prf
  - key-derivation
  - unisoc
  - 41903
  - ooredoo-kuwait
---

# UNISOC 41903 VoWiFi 注册失败：IKE PRF+ 密钥展开在 200 字节处截断

## 基本信息

| 项目 | 内容 |
|---|---|
| 日期 | 2026-09-03 |
| 项目 | A01 |
| 平台 | UNISOC |
| 芯片/基线 | 问题机 `qogirl6`；REF 为 `SC9863A`，非同型号 |
| 厂商客制化 | 41903 Operator NV / IKE proposal |
| Android版本 | TBD |
| Modem版本 | FAIL：`4G_MODEM_22B_W24.36.3`；REF：`4G_MODEM_22B_W25.45.3`；PATCH：展锐临时版本，构建号待归档 |
| 原始log | `F:\Log\A01\A01_VOWIFI\2026-09-03-10-47-15_41903 VOWIFI`；`F:\Log\A01\A01_VOWIFI\2026-09-03-17-33-50_REF_41903 VOWIFI` |
| 第一坏点 | IKE SA 密钥展开到累计第 200 字节后停止，`SK_er` 尾部及 `SK_pi/SK_pr` 被零填充 |
| SIM/运营商 | `41903` / Ooredoo Kuwait，原 Wataniya Telecom |
| RAT | LTE + IWLAN |
| 场景 | 注册 LTE、连接 Wi-Fi 后发起 VoWiFi 注册 |
| 复现概率 | 问题机原版本稳定失败；REF 同环境成功；展锐临时 Patch 下原 FAIL 项验证 PASS |

## 状态说明

`closed`：问题机与 REF 对比、IKE 密钥材料和独立重算结果形成高置信根因证据；UNISOC 确认原因为 PRF 函数计算轮次不足，并提供按实际总密钥长度动态计算轮次的临时 Patch。2026-09-07 用户确认原 FAIL 项使用该 Patch 验证 PASS，完成“故障现象 -> 根因 -> Patch -> 功能恢复”的闭环。Patch 构建号、变更号及 PASS 日志路径仍待归档，不影响本案例的功能验证结论，但引用详细协议证据时应保留该边界。

## 用户现象

A01 插入 `41903` SIM，完成 LTE 注册并打开 Wi-Fi 后，VoWiFi 注册失败。期望终端通过 ePDG 建立 IKE/IPsec 隧道，并完成 IMS over IWLAN 注册。

复现步骤：

1. 插入 41903 SIM。
2. 注册 LTE 网络并打开 Wi-Fi。
3. 等待 VoWiFi 注册，实际始终失败。

## 结论

> [!bug] 根因
> 问题机 `4G_MODEM_22B_W24.36.3` 的 PRF+ 轮次计算没有覆盖实际所需的全部密钥材料。当前 IKE 协商组合需要生成 252 字节，但实际只生成前 200 字节。`SK_er` 仅前 20 字节正确、后 12 字节为 `0`，后续 `SK_pi`、`SK_pr` 全部为 `0`。终端因此无法正确解密首个 `IKE_AUTH[R]`，把解密后的随机数据误解析成非法 IDr/Payload，最终报 `DecodeMsg fail`。

同一 SIM、CMW/AP 和 ePDG 环境下，REF 能解出 EAP-AKA Challenge，随后收到 `EAP_SUCCESS` 并进入 `IKE ATTACHED`，说明 DNS、Wi-Fi、ePDG 可达性和网络侧基本流程可用。

> [!success] 修复验证
> 2026-09-07，用户确认展锐上周提供的临时 Patch 已使原 FAIL 项验证 PASS。这一 A/B 结果进一步证明 PRF 轮次计算缺陷是本次 VoWiFi 注册失败的直接根因。当前记录的是用户确认的功能结果，尚未附带 Patch 版本号及 PASS 日志明细。

```text
IKE_SA_INIT 成功
  -> Modem 执行 IKEv2 PRF+ 密钥展开
  -> W24.36.3 未按实际总密钥长度计算足够的 PRF 轮次
  -> 只生成前 200/252 字节
  -> SK_er 后 12 字节、SK_pi、SK_pr 被零填充
  -> 首个 IKE_AUTH[R] 完整性校验可通过，但 SK_er 解密结果错误
  -> IDr/Payload 被解析成 next payload=130、payload length=21572 等非法值
  -> Ike_DecodeIkeAuth / DecodeMsg fail
  -> EAP-AKA 不启动，IKE attach 失败
  -> VoWiFi 不注册
```

## 输入材料

- 问题机 Modem log：`F:\Log\A01\A01_VOWIFI\2026-09-03-10-47-15_41903 VOWIFI\modem\md_20260902-053648.log`
- 问题机抓包：`F:\Log\A01\A01_VOWIFI\2026-09-03-10-47-15_41903 VOWIFI\ap\tcpdump\001_1231_201753_0902_053734_tcpdump.cap`
- REF Modem log：`F:\Log\A01\A01_VOWIFI\2026-09-03-17-33-50_REF_41903 VOWIFI\modem\md_20260903-051903.log`
- REF AP log：`F:\Log\A01\A01_VOWIFI\2026-09-03-17-33-50_REF_41903 VOWIFI\ap\000-0903_051835--0903_122044_poweron\0-android_main.log`
- REF 抓包：`F:\Log\A01\A01_VOWIFI\2026-09-03-17-33-50_REF_41903 VOWIFI\ap\tcpdump\001_0903_121939_0903_122044_tcpdump.cap`
- UNISOC 回复：建议 CPM 升级 Modem 到 `4G_MODEM_22B_W24.45.6` 或更新版本后复测。
- 临时 Patch 验证：2026-09-07 用户确认原 FAIL 项验证 PASS；Patch 构建号、变更号和 PASS 日志路径待归档。

## 时间线

| 时间 | 来源 | 事件 | 含义 | 重要性 |
|---|---|---|---|---|
| 05:36:48.320 | FAIL Modem | 运行版本 `4G_MODEM_22B_W24.36.3` | 锁定问题版本 | 高 |
| 05:37:04.491 | FAIL Modem | 读取 `ike_encr=12`、`ike_encr_key_len=256`、`ike_intg=14`、`ike_prf=2`、`ike_dh=2` | Operator NV 已加载 | 中 |
| 05:37:04.729 | FAIL Modem | FQDN 解析到 `192.168.1.201` | DNS/ePDG 地址正常 | 中 |
| 05:37:04.775 | FAIL Modem | 发送 `IKE_SA_INIT[I]` | IKE 开始 | 中 |
| 05:37:04.791 | FAIL Modem | 收到 `IKE_SA_INIT[R]` | 第一阶段协商成功 | 高 |
| 05:37:05 前 | FAIL Modem | `SK_er` 后 12 字节、`SK_pi/SK_pr` 为零 | 实际第一坏点 | 最高 |
| 05:37:05.097 | FAIL Modem | 发送 `IKE_AUTH[I]`，随后收到 ePDG 响应 | 网络可达且 ePDG 有响应 | 高 |
| 05:37:05.120 | FAIL Modem | `Ike_MsgAddId para invalid`、`Ike_DecodeIkeAuth PayldHand fail`、`DecodeMsg fail` | 错误密钥导致解密后 Payload 非法 | 高 |
| REF 同流程 | REF Modem/AP | `EAP_SUCCESS`、`IKE_EVENT_IN_ATTACH_OK`、`ATTACHED`、`isWifiRegistered:true` | 同环境可完成 VoWiFi 注册 | 高 |
| 2026-09-07 | PATCH 验证 | 展锐临时 Patch 下原 FAIL 项验证 PASS | 修复与根因形成 A/B 闭环 | 最高 |

## 正常流程对比

- [[../../20_Service-Flows/IMS/IMS业务流程#VoWiFi注册流程|VoWiFi注册流程]]
- [[Imported_IMS_03_6032+_Spark反馈WFC注册有问题|Spark VoWiFi IKE 算法配置错误案例]]
- [[../../70_Tools-Debug/Debug-Tips/IKE消息解密SOP|IKE消息解密SOP]]

```text
DNS/ePDG discovery
-> IKE_SA_INIT[I/R]
-> 生成完整 SK_d/SK_ai/SK_ar/SK_ei/SK_er/SK_pi/SK_pr
-> IKE_AUTH[I]
-> 解密 IKE_AUTH[R]，获得 IDr + EAP Request/AKA-Challenge
-> EAP Response/AKA-Challenge
-> EAP_SUCCESS
-> IKE_EVENT_IN_ATTACH_OK
-> IKE state ATTACHED
-> IMS over IWLAN 注册
-> isWifiRegistered:true
```

本次失败发生在 SIP REGISTER 之前，不能先归因 P-CSCF、SIP 鉴权或 IMS 账号。

## 第一个异常点

```text
第一个坏点：
IKE_SA_INIT 后生成的 SK_er 只有前 20/32 字节有效，后 12 字节为 0；SK_pi/SK_pr 全 0。

上一条正常证据：
IKE_SA_INIT[I/R] 已完成，协商算法和 SPI/Nonce/SKEYSEED 均可用于重新计算密钥。

下一条异常证据：
首个 IKE_AUTH[R] 到达后，Modem 解码出非法 next payload、reserved 和 payload length，随后 DecodeMsg fail。

影响层级：
Modem IKEv2 PRF+ 轮次计算 -> IKE SA key material -> SK_er -> IKE_AUTH 解密 -> EAP-AKA -> IKE attach -> IMS over IWLAN。
```

## 关键证据

### 1. 问题机与 REF 的核心 IKE 参数相同

```text
ike_encr=12
ike_encr_key_len=256
ike_intg=14
ike_prf=2
ike_dh=2
ipsec_encr=12
ipsec_encr_key_len=256
ipsec_integ=14
ike_with_proposal2=1
ike_cfg_attr_ims=20
inner_ip_type_ims=1
epdg_apn_ims=IMS
```

问题机 `epdg_addr_type=2`，REF 为 `1`，但两机最终都生成相同 FQDN，并访问相同 ePDG：

```text
epdg.epc.mnc003.mcc419.pub.3gppnetwork.org
192.168.1.201
```

因此 `epdg_addr_type` 不是本次首个解码失败的直接原因。

### 2. 问题机密钥材料在累计 200 字节处停止

```text
md_20260902-053648.log:117204  Ike_SaGetSk SK_d   len=20  非零
md_20260902-053648.log:117205  Ike_SaGetSk SK_ai  len=64  非零
md_20260902-053648.log:117206  Ike_SaGetSk SK_ar  len=64  非零
md_20260902-053648.log:117207  Ike_SaGetSk SK_ei  len=32  非零
md_20260902-053648.log:117208  Ike_SaGetSk SK_er  len=32  前20字节非零，后12字节全0
md_20260902-053648.log:117209  Ike_SaGetSk SK_pi  len=20  全0
md_20260902-053648.log:117210  Ike_SaGetSk SK_pr  len=20  全0
```

| 密钥 | 长度/Byte | 累计结束位置/Byte | 问题机结果 |
|---|---:|---:|---|
| `SK_d` | 20 | 20 | 正确 |
| `SK_ai` | 64 | 84 | 正确 |
| `SK_ar` | 64 | 148 | 正确 |
| `SK_ei` | 32 | 180 | 正确 |
| `SK_er` | 32 | 212 | 仅到第 200 字节，后 12 字节为零 |
| `SK_pi` | 20 | 232 | 全零 |
| `SK_pr` | 20 | 252 | 全零 |

`180 + 20 = 200`，与实际截断点严格吻合。展锐补充确认根因是 PRF 函数计算轮次不足。

本次 PRF 单轮输出长度为 20 字节，因此：

```text
实际所需总长度 = 20 + 64 + 64 + 32 + 32 + 20 + 20 = 252 bytes
正确轮次       = ceil(252 / 20) = 13
问题机有效输出 = 200 bytes = 10 * 20
```

由日志可以推导问题机只产出了相当于 10 轮的结果；但旧实现中是否直接写死 10 轮、通过错误公式算出 10 轮，仍需源码或展锐变更记录确认。

### 3. 独立重算验证是终端密钥异常

使用问题日志中的 `SKEYSEED + Ni + Nr + SPIi + SPIr`，按 IKEv2 PRF+ 规则独立重算：

- 重算结果前 200 字节与问题机日志完全一致。
- 正确 `SK_er` 的后 12 字节应为非零，问题机却写为零。
- 使用完整重算的 `SK_er` 可以正确解出 ePDG IDr 和 EAP Request/AKA-Challenge。
- `SK_ar` 可以通过响应报文的完整性校验，说明报文传输未损坏。
- 使用问题机零尾的 `SK_er` 解密，则得到错误 padding 和非法 Payload，复现 `DecodeMsg fail`。

这把第一坏点定位在终端密钥展开/保存阶段，而不是网络生成 IKE_AUTH 阶段。

### 4. REF 完成相同网络流程

```text
md_20260903-051903.log:29811  SK_er 32字节完整非零
md_20260903-051903.log:29812  SK_pi 20字节完整非零
md_20260903-051903.log:29813  SK_pr 20字节完整非零
md_20260903-051903.log:31700  <- [0]EAP_SUCCESS
md_20260903-051903.log:31894  E_IKE_EVENT_IN_ATTACH_OK
md_20260903-051903.log:31904  E_IKE_SESS_STATE_ATTACHED
0-android_main.log:27746         isWifiRegistered:true
```

REF 是 `SC9863A / W25.45.3`，不是 A01 同型号，只能证明 SIM、CMW/AP、ePDG 和当前算法组合可完成注册；不能单独证明 `qogirl6` 的旧 Modem 实现正确。

## 抓包 `Malformed Packet` 的正确解释

```text
IKE_AUTH MID=01 Responder Response [Malformed Packet]
Payload: Identification - Responder (36)
Next payload: 130
Critical Bit: 1
Reserved: 0x5e
Payload length: 21572
```

这些字段是使用错误 `SK_er` 解密后产生的随机结果，不是 ePDG 在明文中真正发送的 Payload 结构。已知正确密钥可以把同一密文解出合法 IDr 和 EAP-AKA Challenge。

> [!warning] 判定边界
> Wireshark 显示 `Malformed Packet` 只证明“当前解析结果非法”，不能单独证明网络原始报文异常。必须先核对 SPI、方向、算法、密钥长度、零尾和完整性校验结果。

## 异常分析

### 已确认事实

- DNS 成功，问题机和 REF 都访问 `192.168.1.201`。
- 两机完成 `IKE_SA_INIT`，核心算法运行值相同。
- ePDG 返回首个 `IKE_AUTH[R]`，问题机在本地解密/解析时报错。
- 问题机密钥材料从累计第 200 字节开始异常。
- 完整重算的 `SK_er` 可以正确解密同一网络报文。
- REF 在同一测试环境下进入 `EAP_SUCCESS` 和 `IKE ATTACHED`。

### 供应商确认

- 根因：PRF 函数计算轮次不够，可能导致 IKE 与 IPsec 密钥计算错误。
- 修复：计算密钥时，先根据各密钥的实际长度得到所需总密钥长度，再据此计算实际 PRF 轮次，确保生成完整 key material。

本案例实际观测到的是 IKE SA 密钥不完整，并在首个 `IKE_AUTH[R]` 解密阶段失败；由于流程尚未走到 CHILD_SA/IPsec 建立，不能用本次日志证明已发生 IPsec 密钥错误。IPsec 是展锐说明的同类风险范围。

### 高置信推断

- `qogirl6 / W24.36.3` 的 IKEv2 PRF+ 轮次计算实现不能覆盖当前 252 字节输出需求。
- `200 = 10 * 20`，问题机相当于只产出 10 个 PRF block；具体旧代码公式或上限仍需源码确认。
- 问题机后续出现的 ICMP `192.168.1.201 unreachable` 位于首次解码失败和重传之后，更像 ePDG/CMW 清理异常会话后的次生现象。

### 归档待补

- 展锐临时 Patch 的构建号、commit/change ID 和正式合入分支。
- PASS Modem/AP 日志路径，以及完整 `SK_er/SK_pi/SK_pr`、`EAP_SUCCESS`、`IKE_EVENT_IN_ATTACH_OK`、`isWifiRegistered:true` 证据。
- `4G_MODEM_22B_W24.45.6` 或后续正式版本是否已合入相同修复。
- 旧实现是固定轮次、轮次公式错误，还是长度传递错误，需要源码或变更记录确认。

## 容易误判的方向

| 方向 | 为什么不是当前第一根因 |
|---|---|
| DNS/ePDG 地址 | FQDN 已解析到 `192.168.1.201`，IKE_SA_INIT 和首个 IKE_AUTH 都有收发 |
| `epdg_addr_type` 差异 | 两机最终使用相同 FQDN 和 ePDG IP |
| IKE 算法 NV 未加载 | 问题机运行日志已打印目标算法，且 IKE_SA_INIT 协商成功 |
| 网络 IKE_AUTH 报文损坏 | `SK_ar` 完整性校验通过，完整重算 `SK_er` 可解出合法 EAP-AKA Challenge |
| 抓包显示 `Malformed Packet` | 是错误密钥解密后的解析结果，不等于线上原始报文错误 |
| 后续 ICMP unreachable | 发生在首次解密失败之后，是次生现象 |
| SIP/P-CSCF | 失败发生在 EAP-AKA/IKE attach 阶段，尚未进入 IMS SIP REGISTER |

## 处理方案

### 正式方案

代码修复原则：

```text
total_key_len = len(SK_d) + len(SK_ai) + len(SK_ar)
              + len(SK_ei) + len(SK_er) + len(SK_pi) + len(SK_pr)

rounds = ceil(total_key_len / prf_output_len)
```

PRF+ 必须执行足够轮次，并按顺序切分出所有 IKE 密钥；若同一函数用于 CHILD_SA/IPsec key material，也必须按实际加密、完整性算法的密钥长度重新计算总长度与轮次，不能复用固定轮次。

展锐临时 Patch 已按上述方向修正，原 FAIL 项验证 PASS。正式版本仍应确认相同修改已经合入，避免仅依赖临时补丁包。

按 UNISOC 建议，将 A01 Modem 升级到：

```text
4G_MODEM_22B_W24.45.6 或更新版本
```

升级本身不是修复完成证据。必须确认设备运行版本，并使用同 SIM、同 CMW/AP、同 ePDG、同 Operator NV 重新抓取 AP/Modem log。

### 最小诊断方案

若需要在拿到正式版本前隔离假设，可只调整 `ike_intg` 到目标平台和测试网允许、且总密钥材料不超过 200 字节的组合，其他 IKE/ePDG/IPsec 参数全部保持不变。若修改后可以继续解码，可进一步支持“200 字节截断”判断。

该修改仅限实验室诊断或运营商明确允许的临时规避，不能替代 Modem 正式修复，也不能在未确认算法兼容性时作为商用配置下发。

## 升级复测检查表

| 层级 | 检查项 | 通过标准 |
|---|---|---|
| 版本 | Modem 运行版本 | `4G_MODEM_22B_W24.45.6` 或更新版本 |
| 配置 | Operator NV | 保持本次配置不变，避免多变量修改 |
| 密钥 | `SK_er/SK_pi/SK_pr` | 长度正确，无异常零尾或全零 |
| IKE 解码 | 首个 `IKE_AUTH[R]` | 无 `Ike_MsgAddId para invalid`、`DecodeMsg fail` |
| EAP | AKA 流程 | 出现 EAP Request/AKA-Challenge、EAP Response、`EAP_SUCCESS` |
| IKE 状态 | attach | 出现 `IKE_EVENT_IN_ATTACH_OK`、`IKE_SESS_STATE_ATTACHED` |
| AP 状态 | VoWiFi 注册 | `isWifiRegistered:true` |
| 稳定性 | 重复验证 | 飞行模式/Wi-Fi 开关/重启后重复注册均通过 |

> [!success] 当前结果
> 原 FAIL 项在展锐临时 Patch 下已验证 PASS（用户于 2026-09-07 确认）。上表中密钥、EAP、IKE 状态和 AP 注册关键字仍作为 PASS 日志归档检查项；在未收到新日志前，不把这些逐项写成已从 Patch 日志确认。

如果升级后仍失败，应保留新的密钥长度打印和首个失败报文，不要同时修改 `epdg_addr_type`、DH、加密、完整性算法或 IPsec 参数。

## 供应商沟通口径

```text
同一 SIM 和 CMW/ePDG 环境下，REF 可完成 EAP-AKA 和 IKE attach。
问题机 W24.36.3 的 IKE 密钥材料在累计 200 字节处停止：
SK_er 后 12 字节以及 SK_pi/SK_pr 被零填充。
使用完整重算的 SK_er 可以解密同一 IKE_AUTH 响应，SK_ar 完整性校验也通过。
因此应描述为“终端 IKE_AUTH 解密/密钥计算异常”，不宜描述为“网络 IKE_AUTH 消息异常”。
展锐已补充确认为 PRF 函数轮次计算不足，修复原则是先计算实际总密钥长度，再计算所需轮次。
请确认 W24.45.6 已合入该修复，并提供对应变更信息。
```

## 复盘

下次遇到 VoWiFi 在首个 `IKE_AUTH[R]` 报 `DecodeMsg fail` 时，优先执行：

1. 确认 `IKE_SA_INIT` 是否完成，以及失败是在网络收包前还是本地解密后。
2. 对齐问题机和成功机的 SPI、Nonce、proposal、FQDN、ePDG IP。
3. 检查 `SK_ai/SK_ar/SK_ei/SK_er/SK_pi/SK_pr` 的声明长度、实际非零长度和累计结束位置。
4. 若完整性通过但解密结构非法，优先检查方向密钥、总密钥长度、PRF 轮次、密钥切分和 Wireshark Decryption Table，不先定性网络报文异常。
5. 功能 FAIL 项恢复可用于关闭案例；正式版本归档仍建议保留运行版本、密钥完整性、EAP 成功、IKE attach 和 AP `isWifiRegistered:true` 五层证据。
