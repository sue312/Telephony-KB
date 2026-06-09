---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# Kali-WiFi-Sniffer抓包SOP

## 适用场景

用于通过 VMware + Kali Linux + Wireshark 抓取 Wi-Fi 空口包，尤其是 Wi-Fi 6E / 6 GHz 频段问题。

## 环境准备

1. 安装 VMware Workstation Pro。
2. 打开已准备好的 Kali Linux 虚拟机。

![](../../attachments/outline/122a47fb-35d9-44e5-9380-e1e170f5d7b3.png)

![](../../attachments/outline/f168a136-3b3e-4185-a514-54cc97c14ee6.png)

3. 选择 Kali 虚拟机的 `.vmx` 文件。

![](../../attachments/outline/eeb6e404-268e-442e-aab0-1f646bbbb9db.png)

4. 启动虚拟机；默认资料中用户名和密码均为 `kali`。

![](../../attachments/outline/0b832e92-9362-446e-8790-f16fc09fa1c7.png)

![](../../attachments/outline/c781fee4-aa31-4819-820d-29cf04c590e4.png)

## 连接 Wi-Fi 网卡

1. 插入 Wi-Fi 6/6E 网卡。
2. 进入虚拟机设置，在 `USB Controller` 中选择合适的 USB 兼容性，例如 `USB 3.1`。

![](../../attachments/outline/08a00813-947d-4026-8ba7-48ee885c667e.png)

3. 在 VMware 菜单选择 `VM -> Removable Devices -> MediaTek Wireless_Device -> Connect`，将网卡挂载到 Kali。

![](../../attachments/outline/f549718e-a08d-43c1-a84e-d0c7ac6fef08.png)

![](../../attachments/outline/02c36729-5ff2-461b-8fe5-3620d64d17ee.png)

4. 在 Kali 终端执行 `iwconfig`，确认已识别出 `wlan0`。

![](../../attachments/outline/93b1f54e-e590-42d3-9e57-08c4f6e52c38.png)

![](../../attachments/outline/fa6ae8bf-dcd7-459b-bba7-4f48f4c3d053.png)

## 开启 6 GHz 频段

国内区域码下 6 GHz 可能显示为 `disabled`。如需抓 Wi-Fi 6E，可临时将 Kali 区域码设置为支持 6 GHz 的区域，例如 `US`。

```bash
sudo iw reg get
sudo iw reg set US
iw list
```

检查 `iw list` 中 6 GHz 状态是否从 `disabled` 变为可监听状态，例如 `no IR`。

![](../../attachments/outline/ae1e4db4-7be1-4572-b877-70837990256c.png)

![](../../attachments/outline/703259b3-9e9b-42e9-85da-a456057c22a1.png)

![](../../attachments/outline/e3740ec0-1459-40e4-b71a-5c8176fb7b2e.png)

![](../../attachments/outline/5394eb1b-a035-4858-acb7-b82848af66d4.png)

## 开启监听并抓包

1. 清除可能影响监听模式的进程。
2. 启动监听模式。
3. 设置监听频率。
4. 打开 Wireshark，选择 `wlan0mon` 开始抓包。

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
sudo iw dev wlan0mon set freq 5975
```

![](../../attachments/outline/2252873e-2b21-4003-8538-d8eb3c0c5574.png)

![](../../attachments/outline/e612c739-d6eb-4378-89b1-f881c4e5903e.png)

## 停止并保存

1. 复现问题后点击 Wireshark 停止按钮。
2. 通过 `File -> Save` 保存抓包文件。
3. Kali 中保存的 log 文件可以直接拖拽到主机桌面或目标目录。

![](../../attachments/outline/4c7bdb49-3f8d-4862-8c89-70cec1d1b8ac.png)

![](../../attachments/outline/1487d953-5e0c-4366-935a-4205777eaae0.png)

![](../../attachments/outline/c9846b00-8ba9-454a-b26b-dfa80317f22c.png)

## 信道和频率补充

扫描 AP 工作信道：

```bash
sudo airodump-ng wlan0mon --band bga
```

![](../../attachments/outline/83c8d196-60df-48dc-b211-66bd5560d496.png)

修改监听信道或频率：

```bash
sudo iw dev wlan0mon set channel 6
sudo iw dev wlan0mon set freq 5975
```

6 GHz 抓包优先使用 `set freq` 指定频率；原导入资料记录过 `set channel` 在 6 GHz 场景下未抓到包的情况。

## 提交检查

| 检查项 | 要求 |
| --- | --- |
| 网卡识别 | `iwconfig` 能看到 `wlan0` |
| 监听接口 | `airmon-ng start wlan0` 后存在 `wlan0mon` |
| 频段状态 | 6 GHz 场景确认 `iw list` 中目标频段不是 `disabled` |
| 监听频率 | 与 AP 实际工作频率一致 |
| 文件格式 | Wireshark 保存为可复查的抓包文件 |

## 来源记录

- [Kali-linux 抓取WiFi sniffer log，安装、抓取指导(支持抓WiFi 6e空口)](http://192.168.3.94:8888/doc/kali-linux-wifi-sniffer-logwifi-6e-6VveQH6Zq6) (`6VveQH6Zq6`)
