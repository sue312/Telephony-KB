---
doc_type: index
domain: Meta
status: active
quality: curated
search_tier: main_entry
---

# Data Cases

APN、默认承载/PDU Session、DNS、TCP、代理、吞吐量、快速回 4G 相关 case 放这里。注册 case 只说明“入网是否成功”，入网后的数据不可用、速率差、回 4G 策略都归到 Data。

## 已整理案例

| Case | 场景 | 用途 |
|---|---|---|
| [[2024-11-13_Data_UNISOC_MMS大小限制CarrierConfig]] | MMS 大小限制调整 | 通过 CarrierConfig 按运营商覆盖 MMS max message size |
| [[2022-10-31_Data_UNISOC_APN_XCAP类型被隐藏]] | APN xcap type 不显示 | 检查 APN XML、数据库和 CarrierConfig 隐藏列表 |
| [[2026-09-03_Data_UNISOC_白卡EF_AD测试模式导致XCAP复用默认承载]] | 42004 白卡执行 UT 时未建立独立 XCAP 承载 | 检查 `EF_AD/6FAD` 测试卡判定、Operator NV 运行值和实际 APN/NSAPI |
| [[2026-04-24_Data_UNISOC_RTOS_DataPDN按需激活后主动释放]] | 注册后几分钟 UE 主动释放 data PDN | 区分按需激活策略、上层去激活和协议层 PDN disconnect |
| [[2026-05-08_Data_UNISOC_CGDCONT修改APN不触发PDN重建]] | AT+CGDCONT 修改 APN 后未自动断链重建 | 区分 PDP context 定义和 PDN disconnect/connect |
| [[2026-01-20_Data_UNISOC_India注册4G但DNS超时无法上网]] | India 注册 4G 但无网络 | 用 NetworkMonitor/netlog 定位 DNS 超时和 TCP 重传 |
| [[2025-02-06_Data_UNISOC_APN_WAP类型显示为空]] | APN `type=wap` 显示为空 | 区分 APN 名称和 Android 标准 APN type 枚举 |
| [[2023-09-13_Data_UNISOC_MMS发送失败_APN使用错误]] | MMS 发送失败提示 user not found | 用 PDP/APN 日志判断彩信是否使用了错误 APN |
| [[2023-12-04_Data_UNISOC_Phoenix视频加载失败DNS无响应]] | 视频播放中断，重启恢复 | 用 DNS timeout、UnknownHostException 和 CP 组包切分 AP/modem/网络 |
| [[2023-10-27_Data_UNISOC_Safaricom_WiFi切蜂窝被重定向]] | Wi-Fi 切蜂窝后无网络，飞行模式恢复 | 区分 data call 成功、NetworkMonitor redirect 和运营商门户 |
| [[2023-09-28_Data_UNISOC_MTN弱网DNS超时与TCP重传]] | 4G 已注册但移动数据很慢 | 结合 DNS/TCP 与弱场信号判断网络质量问题 |
| [[Case_Data_APN_IPV6代理不支持]] | APN 改 IPv6 后连接成功但无法上网 | 区分 APN 协议、CLAT/NAT64、DNS/TCP、proxy 兼容性 |
| [[Case_Data_快速回4G与吞吐量KPI]] | 2/3G 回 LTE 策略和吞吐量 KPI | 快速回网策略、吞吐量测试条件、Wireshark 分段 |

建议命名：

```text
YYYY-MM-DD_Data_现象_根因.md
```
