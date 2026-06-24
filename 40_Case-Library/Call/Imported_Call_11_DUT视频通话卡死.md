---
doc_type: case
quality: imported_reference
domain: IMS
rat: LTE
feature: 'VideoCall'
platform: UNISOC
layer: 'IMS/RTP/AP/Modem'
symptom: 'DUT视频通话卡死'
cause: 'modem 侧 IMS 注册、SIP 建呼、音视频 RTP/RTCP 收发均正常；卡死第一坏点更可能在 AP 视频渲染/UI/媒体栈，需补 AP 证据'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: 'modem/TCPIP 可见 audio/video 数据交互正常，缺少 AP media/render/UI 卡死证据'
confidence: medium
status: summarized_with_log_gap
tags:
  - imported
  - split_from_bucket
  - ims
  - vilte
  - rtp
  - ap-media
search_tier: case_summary
---

# DUT视频通话卡死

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，已收敛为 IMS 视频通话卡死的 AP/媒体栈补证 case。

## 用户现象
DUT视频通话卡死

## 结论

modem 侧证据显示 IMS 注册、SIP INVITE、183/180/200/ACK 以及音视频 UDP 数据交互均正常；kernel `sprd-imsbr` 也能看到 audio/video tuple。因此当前资料不能把“卡死”归到网络或 modem 建呼失败。第一缺口在 AP 视频渲染、UI、camera/media codec 或 Surface 侧，需要补 AP 证据。

## 关键证据

- 原始分类：五、视频通话
- 来源：通话问题案例补充.md
- 拆分序号：11
- IMS 注册：REGISTER / 401 / REGISTER / 200 正常。
- 建呼：INVITE 携带 audio/video SDP，100 / 183 / PRACK / 200 / 180 / 200 / ACK 正常。
- 数据：TCPIP 可见 audio `59000 -> 10000` 和 video `60001 -> 10003` UDP 交互。
- kernel：`sprd-imsbr` 添加 `rtp-audio`、`rtcp-video` tuple。

## 定位口径

| 判断点 | 结论 |
|---|---|
| SIP 和 RTP 正常 | 不优先归网络/IMS 建呼失败 |
| 视频画面卡死 | 查 AP media codec、camera、Surface、UI thread |
| 只有本机卡死 | 补设备性能、内存、GPU/codec log 和对比机 |
| 双向 RTP 有收发 | 重点确认 AP 是否解码/渲染，而不是只看 modem |

## 下次复现补证清单

| 必抓证据 | 具体内容 | 能证明什么 |
|---|---|
| AP logcat | `media.codec`、`CameraService`、`SurfaceFlinger`、Dialer、IMS service、卡死时间点 | AP 视频解码/渲染/UI 是否异常 |
| Perfetto / systrace | UI thread、RenderThread、binder、camera、codec、GPU 时间线 | 判断是否 UI 卡顿、渲染阻塞或 codec 阻塞 |
| tombstone / ANR | native crash、Java ANR、watchdog | 判断卡死是否已经变成崩溃/无响应 |
| modem SIP/RTP/TCPIP | SIP 建呼、RTP/RTCP audio/video 持续收发、端口 tuple | 证明网络和 modem 媒体流是否仍正常 |
| 画面/音频现象记录 | 本地画面、远端画面、双向音频、卡死时刻截图/录像 | 区分本地预览、远端视频、编码或解码问题 |
| 对比机同场景 | codec、resolution、SDP、RTP、UI 行为 | 判断是 DUT AP 渲染差异还是网络媒体条件变化 |

判定口径：

- RTP 持续收发且 SIP 未释放时，优先查 AP media/render，不再按网络建呼失败处理。
- 只有远端画面卡死、本地预览正常时，重点查下行 RTP 解码/渲染。
- 双向视频都停但音频正常时，重点查 video codec、Surface 或 QCI2/视频 RTP。

## 原始案例内容

### 案例2：DUT视频通话卡死

分析思路：
重点检查modem侧log，检查通话建立流程

展锐分析：
DUT MODEM LOG,

log可以看到通话流程正常，并且也有语音和视频数据在传输
146771-1   07:03:50.103   SIM2   IMS   --   -> \[1\]REGISTER
146772-4   07:03:50.103   07:03:50.103   Time: 622512 From: <sip:622010123456789@ims.mnc001.mcc622.3gppnetwork.org>;tag=yINe5Teszh
146772-17   07:03:50.103   07:03:50.103   Time: 622512 P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=6220100011a2d001
147006-1   07:03:50.129   SIM2   IMS   --   <- \[1\]401
147409-1   07:03:50.203   SIM2   IMS   --   -> \[1\]REGISTER
147638-1   07:03:50.229   SIM2   IMS   --   <- \[1\]200
147710-1   07:03:50.235   SIM2   IMS   --   -> \[1\]SUBSCRIBE
148343-1   07:03:50.308   SIM2   IMS   --   <- \[1\]200
148627-1   07:03:50.342   SIM2   IMS   --   <- \[1\]NOTIFY
148656-1   07:03:50.345   SIM2   IMS   --   -> \[1\]200

48   183354-1   07:03:58.986   --   ATC: ATC_RecNewLineSig,link_id:5,sim:1,len:8,line:ATD=666   ATC
183780-1   07:03:59.003   SIM2   IMS   --   -> \[1\]INVITE
183781-4   07:03:59.003   07:03:59.003   Time: 623516 From: <sip:622010123456789@ims.mnc001.mcc622.3gppnetwork.org>;tag=odWfh
183781-5   07:03:59.003   07:03:59.003   Time: 623516 To: <tel:666;phone-context=ims.mnc001.mcc622.3gppnetwork.org>
183781-16   07:03:59.003   07:03:59.003   Time: 623516 P-Access-Network-Info: 3GPP-E-UTRAN-FDD;utran-cell-id-3gpp=6220100011a2d001
183783-6   07:03:59.003   07:03:59.003   Time: 623516 m=audio 59000 RTP/AVP 98 100 110 112 101 103
183783-25   07:03:59.003   07:03:59.003   Time: 623516 m=video 60000 RTP/AVP 104 105
183783-35   07:03:59.003   07:03:59.003   Time: 623516 a=rtpmap:104 H264/90000
183783-36   07:03:59.003   07:03:59.003   Time: 623516 a=fmtp:104 profile-level-id=42C01E;packetization-mode=1;sprop-parameter-sets=Z0LAHukDwKJALCIRqA`,aM48gA`
183783-37   07:03:59.003   07:03:59.003   Time: 623516 a=rtpmap:105 H264/90000
183783-38   07:03:59.003   07:03:59.003   Time: 623516 a=fmtp:105 profile-level-id=42C01E;packetization-mode=0;sprop-parameter-sets=Z0LAHukDwKJALCIRqA`,aM48gA`
184122-1   07:03:59.045   SIM2   IMS   --   <- \[1\]100
184364-1   07:03:59.080   SIM2   IMS   --   <- \[1\]183
184559-1   07:03:59.091   SIM2   IMS   --   -> \[1\]PRACK
184968-1   07:03:59.127   SIM2   IMS   --   <- \[1\]200
184993-1   07:03:59.130   SIM2   IMS   --   <- \[1\]180
185331-1   07:03:59.160   SIM2   IMS   --   <- \[1\]200
185378-1   07:03:59.164   SIM2   IMS   --   -> \[1\]ACK
195   193439-1   07:04:00.684   --   Time: 623516 \[ TCPIP \] MtSend, pkt(0):8c7d04dc, netif(8d30b2c0), IP6, cksum(43b8), 59000 -> 10000, UDP(67)   //语音数据交互
196   193490-1   07:04:00.699   --   Time: 623516 \[ TCPIP \] MtRecv, pkt(0):8c7d0654, netif(8d30b2c0), IP6, cksum(e8ac), 10000 -> 59000, UDP(67)   67字节数据包
197   193921-1   07:04:00.795   --   Time: 623516 \[ TCPIP \] MtSend, pkt(0):8c7d07cc, netif(8d30b2c0), IP6, cksum(4e6c), 60001 -> 10003, UDP(88)   //视频数据交互
199   194123-1   07:04:00.819   --   Time: 623516 \[ TCPIP \] MtRecv, pkt(0):8c7d0abc, netif(8d30b2c0), IP6, cksum(c7c6), 10003 -> 60001, UDP(88)   88字节数据包
(20251029T02:11:23)

//从kernel log中可以确认语音和视频数据发送端口

sprd-imsbr: cptuple-add(**rtp-audio**) ... 59000 -> ... 10000

sprd-imsbr: cptuple-add(**rtcp-video**) ... 60001 -> ... 10003

## 原始资料边界

- 当前资料足以证明 modem/IMS 建呼和媒体流不是首要失败点，但不足以闭合 AP 卡死根因。
- 后续 IMS 视频通话专项应与 [视频通话界面与Log](../../20_Service-Flows/IMS/视频通话界面与Log.md) 互链。
