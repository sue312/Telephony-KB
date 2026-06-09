---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# Wireshark-SIP与抓包分析SOP

## 适用场景

用于打开 `cap` / `pcap` 文件查看 SIP、DNS、TCP、UDP 和基础 IP 抓包。通信问题中常见用途是看 MTK net log 中的 SIP、DNS/TCP 失败，或对齐 AP/modem log 的数据面证据。

官网地址：<https://www.wireshark.org/download.html>

## cap 文件来源

Wireshark 解析的是抓包文件，不直接解析 modem 原始 log。

| 平台 | cap 来源 | 备注 |
| --- | --- | --- |
| MTK | DebugLogger / net log 目录中的 `cap` 文件 | IMS/SIP、DNS/TCP 问题常用 |
| UNISOC | 可先用 Logel 解析 modem log，再在解析输出目录中找 cap 文件 | Logel 也能直接查看 SIP，Wireshark 用作补充 |

MTK net log 示例：

![](../../attachments/outline/0243a184-b5f7-4775-97a7-39891ab8e8ef.png)

![](../../attachments/outline/dbbbd465-63e9-42b3-ab75-f44c59323241.png)

UNISOC Logel 解析后 cap 文件示例：

![](../../attachments/outline/74090307-95f2-49af-93b2-250ebd6cd451.png)

![](../../attachments/outline/7462b075-facb-4c4d-8289-02b98ff4e4bd.png)

## 打开和阅读 cap

1. 用 Wireshark 打开目标 `cap` / `pcap` 文件。
2. 上方列表按时间展示 packet。
3. 下方详情展示来源地址、目的地址、协议头、消息体和序列号。
4. 先确认时间点，再用过滤器缩小范围。

![](../../attachments/outline/200d6c9d-38d2-481a-8d90-f97bb01be4d0.png)

## SIP 消息查看

方式一：在过滤栏输入：

```text
sip
```

![](../../attachments/outline/4f9f6e44-9b30-4932-82d8-d528791d2bde.png)

方式二：菜单进入 `Telephony -> SIP Flows`。

![](../../attachments/outline/ed450759-8abf-4efb-ac58-e7a93a0022a2.png)

![](../../attachments/outline/bed107a7-41dd-4384-ae17-0a0bde1cec2f.png)

在 SIP Flows 中选择单条或 `Ctrl+A` 全选，再查看 `Flow Sequence`。点击序列图中的行可跳转到对应 packet。

![](../../attachments/outline/74b86d6b-3902-4307-a202-7e729293a2f8.png)

## 现场抓包

用于 PC 侧基础抓包，空口 Wi-Fi 抓包另看 [Kali-WiFi-Sniffer抓包SOP](../Log-Capture/Kali-WiFi-Sniffer抓包SOP.md)。

1. 进入 `Capture -> Options`。
2. 选择实际有流量的接口，例如 WLAN 或以太网。
3. 开始抓包，复现问题。
4. 复现后停止并保存。

![](../../attachments/outline/4493736b-c1bc-43ec-84b4-7429452789e8.png)

![](../../attachments/outline/3fe4556b-c422-4d1a-b34e-986964262ea4.png)

## 流量图和协议过滤

菜单路径：`Statistics -> Flow Graph`。

![](../../attachments/outline/c7d10db6-632c-4de8-adef-f51b9e2fe0e8.png)

常用过滤器：

| 目标 | 过滤器 |
| --- | --- |
| SIP | `sip` |
| TCP | `tcp` |
| UDP | `udp` |
| DNS | `dns` |
| HTTP | `http` |
| 指定 IP | `ip.addr == <ip>` |

## TCP / UDP 包结构速查

TCP 包通常可按以太帧、IP、TCP、应用层数据逐层展开。

![](../../attachments/outline/aa351693-b3b5-4cd6-a4e7-c88ffe0b4628.png)

![](../../attachments/outline/a475a0d6-984f-4e4f-a85f-c827fd7fd282.png)

![](../../attachments/outline/dff2c423-ceb6-4501-9a97-ad7db8db04fc.png)

UDP 包结构类似，也可以逐层展开检查源/目的地址、端口和 payload。

![](../../attachments/outline/0dfa18aa-7615-4f94-9879-b52b56e18ed6.png)

其他协议也按相同方式从 Frame / Ethernet / IP / 传输层 / 应用层逐层查看。

![](../../attachments/outline/297048ac-e8b8-4de9-a2a9-abde6e9bd06f.png)

## 提交检查

| 检查项 | 要求 |
| --- | --- |
| 时间点 | 标出问题发生时间，与 AP / modem log 对齐 |
| 文件来源 | 说明 cap 来自 MTK net log、UNISOC Logel 解析目录还是 PC 抓包 |
| 过滤条件 | 说明使用的过滤器，例如 `sip`、`dns`、`tcp` |
| 关键 packet | 标出请求、响应、重传、timeout 或 SIP error 所在 packet |

## 来源记录

- [Wireshark工具使用](http://192.168.3.94:8888/doc/wireshark-3kJdZ2oqNB) (`3kJdZ2oqNB`)
