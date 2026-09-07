---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# IKE消息解密SOP

## 适用场景

用于 VoWiFi / ePDG / IKE 问题中，把 AP 侧 `tcpdump.cap` 的 IKE 报文和 modem log 中的密钥材料对齐后，在 Wireshark 中解密 IKEv2 消息。

## UNISOC 解密流程

1. 用 Wireshark 打开 AP log 目录下的 `tcpdump.cap`。
2. 过滤：

```text
isakmp
```

3. 找到 `IKE_SA_INIT MID=00`，记录该次 IKE 协商的 `Initiator SPI` 和 `Responder SPI`。

![](../../attachments/outline/4e7a4c63-7b11-49cc-9de0-d52ccac2c106.png)

4. 使用 modem log 工具回放 modem log。
5. 在 modem log trace 中搜索 AP 侧拿到的 `Initiator SPI` 和 `Responder SPI`，定位对应 IKE 流程。
6. 在相近时间点搜索以下密钥材料：

```text
PayLoadDump:SK_ai
PayLoadDump:SK_ar
PayLoadDump:SK_ei
PayLoadDump:SK_er
```

同时记录加密算法和完整性算法。

![](../../attachments/outline/adac4f23-de85-4f8e-a3a0-02528c63e24a.png)

7. 在 Wireshark 中进入 `Edit -> Preferences -> Protocols -> ISAKMP -> IKEv2`。
8. 按 IKEv2 Decryption Table 格式填写 SPI、SK_ai、SK_ar、SK_ei、SK_er、加密算法和完整性算法。

![](../../attachments/outline/994463b2-a7e1-4548-8cad-8b41ce367ebd.png)

## 解密后显示 `Malformed Packet` 的判定

> [!warning]
> `Malformed Packet` 只说明当前解析结果非法，不能单独证明网络发送了畸形 IKE 报文。SPI、方向密钥、算法或密钥长度错误，都可能把正常密文解成随机 Payload。

按以下顺序检查：

1. 确认抓包和 Modem log 属于同一次 IKE SA，`Initiator SPI`、`Responder SPI`、Message ID 一致。
2. 确认方向：UE 发送使用 `SK_ei/SK_ai`，ePDG 响应使用 `SK_er/SK_ar`。
3. 检查密钥声明长度与实际内容，特别留意零尾、全零和固定边界截断。
4. 若 `SK_ar` 可以通过响应完整性校验，但 `SK_er` 解密后出现非法 next payload、reserved、payload length 或 padding，优先检查终端密钥派生/保存和 Wireshark 密钥表。
5. 只有使用已确认正确的完整密钥仍无法通过完整性和结构校验时，才继续怀疑报文传输损坏或网络侧生成异常。

### PRF+ 轮次检查

密钥存在零尾、全零或固定边界截断时，不能只检查单个密钥的声明长度，还要核算整段 key material：

```text
total_key_len = 所有待派生密钥的实际长度之和
rounds = ceil(total_key_len / prf_output_len)
```

例如某次 IKE SA 需要 `252 bytes`，PRF 单轮输出 `20 bytes`，则至少需要 `13` 轮。若只得到 `200 bytes`，等价于只产出 `10` 个 PRF block，后续密钥可能出现零尾或全零。具体算法数值与 PRF 输出长度应以目标平台运行日志和 schema 为准。

相关案例：

- [[../../40_Case-Library/IMS/2026-09-03_VoWiFi_UNISOC_41903_PRF密钥展开截断导致IKE_AUTH解密失败|UNISOC 41903 VoWiFi：PRF+ 密钥展开在 200 字节处截断]]

## MTK 解密流程

1. 使用 modem log 工具回放 modem log。
2. 运行 `External -> Extract IP packets`，生成 `*.pcapng` 文件。
3. 运行 `Parse IKE tunnel SA for WireShark` 完成解密。

![](../../attachments/outline/17a680fa-460b-4ee3-9693-68f51467b32f.png)

4. 解密内容默认只在本机可看；如果需要给其他人复查，可在 Wireshark 中查看密钥并导出。

![](../../attachments/outline/798c43b8-319d-417f-8fca-d8588aa6410f.png)

## 提交检查

| 检查项 | 要求 |
| --- | --- |
| AP 抓包 | 有 `tcpdump.cap` / `pcapng` |
| modem log | 能找到同一时间点的 IKE 流程 |
| SPI | `Initiator SPI` / `Responder SPI` 与 modem log 匹配 |
| 密钥材料 | SK_ai / SK_ar / SK_ei / SK_er 齐全 |
| 算法 | 加密算法、完整性算法、PRF / DH 信息可对齐 |

## 关联入口

- [Wireshark-SIP与抓包分析SOP](../Log-Analysis/Wireshark-SIP与抓包分析SOP.md)
- [MTK-WFC-ePDG配置与排查索引](../../60_Configuration/MTK-WFC-ePDG配置与排查索引.md)

## 来源记录

- [IKE消息解密](http://192.168.3.94:8888/doc/ike-deG9XhOSMY) (`deG9XhOSMY`)
