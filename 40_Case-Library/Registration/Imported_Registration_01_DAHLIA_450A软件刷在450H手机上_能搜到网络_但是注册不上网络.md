---
doc_type: case
quality: imported_reference
domain: Registration
rat: LTE/NR
feature: 'RF parameter / Attach'
platform: Mixed
layer: 'RF/NV/Modem'
symptom: 'DAHLIA 450A软件刷在450H手机上，能搜到网络，但是注册不上网络'
cause: '450A 软件刷到 450H 硬件后 RF 参数不匹配，终端能发起 Attach/RRC 但射频参数异常导致注册失败'
source_log: 'Old Outline knowledge base; split from 注网问题案例补充.md'
first_bad_point: 'ATTACH_REQUEST / RRCCONNECTIONREQUEST 已发出，首坏点回到 RF 参数/硬件版本错配'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - rf-parameter
  - product-mismatch
search_tier: case_summary
---

# DAHLIA 450A软件刷在450H手机上，能搜到网络，但是注册不上网络

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，当前保留原始内容和初步 frontmatter。复用前需要核对平台、版本、运营商和完整 log。

## 用户现象
DAHLIA 450A软件刷在450H手机上，能搜到网络，但是注册不上网络

## 结论

这是产物/硬件错配导致的 RF 参数问题，不是网络侧 reject。450A 使用独立软件，刷到 450H 硬件后 RF 参数乱，表现为能看到 Attach/RRC 入口，但注册不上网络。

复用时先确认软件版本、硬件版本、RF 参数包和校准状态，不要只按 NAS reject 方向排查。

## 关键证据

- 原始分类：一、RF 参数未配置
- 来源：注网问题案例补充.md
- 拆分序号：1
- log 已出现 `ATTACH_REQUEST` 和 `RRCCONNECTIONREQUEST`，说明流程至少走到 NAS/RRC 发起阶段。
- 原始结论明确为“450A 软件刷到 450H 上射频参数是乱的”。

## 定位口径

| 检查项 | 判断 |
|---|---|
| 软件 / 硬件匹配 | 确认项目名、硬件版本、modem/RF 参数是否同一套 |
| RF 参数 | 查 RF 参数是否已合入，是否使用了错误项目的 RF package |
| 注册 log | 如果 Attach/RRC 已发起但无稳定驻网，不能只看 NAS，需要回头查 RF |
| 复测动作 | 刷回正确硬件版本软件或补齐 RF 参数后再验证注册 |

## 原始资料边界

- 原始内容保留用于回溯旧知识库、日志片段和历史结论。
- 如原始描述与前文 Case 卡片冲突，默认以前文“结论 / 关键证据 / 定位口径”为阅读入口。
- 复用到新问题时必须重新核对平台、版本、运营商、log 和第一坏点。

## 原始案例内容

### 案例：DAHLIA 450A软件刷在450H手机上，能搜到网络，但是注册不上网络

分析：

```javascript
7535-1	14:05:26.475 	SIM1	LTE   	--	                                             	<- MIB                                       	0:00:18.615
7571-1	14:05:26.504 	SIM1	LTE   	--	                                             	<- SYSTEMINFORMATIONBLOCKTYPE1               	0:00:18.644
7741-1	14:05:26.561 	SIM1	LTE   	--	                                             	<- SYSTEMINFORMATION                         	0:00:18.701
8364-1	14:05:26.580 	SIM1	LTE   	--	                                             	<- SYSTEMINFORMATION                         	0:00:18.720
8901-1	14:05:26.584 	SIM1	      	--	-> PDN_CONNECTIVITY_REQUEST                  	                                             	0:00:18.724
8915-1	14:05:26.584 	 --	      	    --  -> ATTACH_REQUEST                            	                                             	0:00:18.724
9102-1	14:05:26.586 	SIM1	LTE   	--	                                             	-> RRCCONNECTIONREQUEST                      	0:00:18.726
9717-1	14:05:26.761 	SIM1	LTE   	--	                                             	<- SYSTEMINFORMATION                         	0:00:18.901
11446-1	14:05:27.121 	SIM1	LTE   	--	                                             	<- SYSTEMINFORMATION                         	0:00:19.261
11713-1	14:05:27.208 	SIM1	LTE   	--	                                             	<- PAGING                                    	0:00:19.348
```

根本原因：RF 参数未配置，450a是单独自己的软件，刷到450h上射频参数是乱的

场景：驱动还未合入RF参数、刷错手机
