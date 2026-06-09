---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# SpeechAnalyzer音频日志分析SOP

## 速查结论

SpeechAnalyzer 用于从 MTK 通话 log 里的 VM 音频文件分析 UL / DL 音频链路。它适合判断第一坏点是在 mic 原始采样、算法处理、modem 发送、网络下行、解码还是下行算法处理。

## 使用入口

| 项目 | 内容 |
| --- | --- |
| 适用平台 | MTK |
| 适用问题 | 通话无声、杂音、断续、音质异常、上下行方向判断 |
| 前置输入 | modem log 同级目录下存在 `VM` 文件夹 |
| 输出结果 | 工具解析出的 UL / DL 音频文件和链路节点 |
| 风险 | 工具只能定位音频链路坏点，不能替代 AP log、modem log、tone 实验或算法参数确认 |

## 工具下载

- 在线工具入口：<https://online.mediatek.com/apps/tool?id=83013128040877&action=download>
- 本地附件：[SpeechAnalyzer_exe_v6.2229.00.zip](../../attachments/outline/files/79325c03-6d5c-4170-9e4a-0370fc5228a5_SpeechAnalyzer_exe_v6.2229.00.zip)

## 安装

解压后第一次需要运行 `run_as_administrator.bat`。否则打开文件时可能报 `无效指针`。

![](../../attachments/outline/b5877070-08ad-4523-922f-a88cb5dfa2a1.png)

Win11 下可能需要修改 `run_as_administrator.bat`。

![](../../attachments/outline/bfbf3702-d2fa-413c-80db-ce54e2270271.png)

## 操作步骤

1. 检查 modem log 同级目录是否存在 `VM` 文件夹。通话 log 正常生成后，会包含该目录。

![](../../attachments/outline/c61abdf0-c926-4ea3-a9fd-9f723406f654.png)

2. 用 SpeechAnalyzer 打开对应 log / VM 资料。

![](../../attachments/outline/786d754d-9e29-4b51-b4a2-0cdea267c76d.png)

3. 查看工具输出目录，确认解析出的音频文件。

![](../../attachments/outline/126487ce-f9ba-4588-adcc-d58bf8630532.png)

4. 按 UL / DL 节点判断第一坏点。

![](../../attachments/outline/5c3c8599-02e5-4cf2-95d1-d487a6903a77.png)

## 第一坏点判断表

| 方向 | 节点 | 含义 | 异常时优先确认 |
| --- | --- | --- | --- |
| UL | `UL0` | mic 录制上来的原始数据 | mobile log、寄存器、tone 音实验 |
| UL | `UL1` | mic 数据经过算法处理后的结果 | MTK 算法或 Hifi3 三方通话算法参数，找 tuning / 算法团队 |
| UL | `UL` | 最终发送给网络的数据 | 先确认是否按下 mute；未 mute 时找 modem team |
| DL | `DL` | 网络下来的原始数据 | modem team |
| DL | `DL0` | 网络数据解码后的结果 | MTK 协助确认解码链路 |
| DL | `DL1` | 解码后经过算法处理的结果 | MTK 算法或 Hifi3 三方通话算法参数，找 tuning / 算法团队 |

## 证据要求

- 记录问题时间点、通话方向、主叫 / 被叫、是否 mute、是否免提或耳机。
- 保留 AP log、modem log、VM 文件夹和 SpeechAnalyzer 输出。
- 如果结论指向算法，需要保留对应节点的异常音频文件和对比样本。
- 如果结论指向 modem 或网络侧，需要回到通话流程和 modem log 继续定位。

## 来源记录

- [SpeechAnalyzer](http://192.168.3.94:8888/doc/speechanalyzer-YKpiyRiGBR) (`YKpiyRiGBR`)
