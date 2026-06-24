---
doc_type: case
quality: imported_reference
domain: Call
rat: 3G
feature: 'ECC'
platform: MTK
layer: 'Config/Modem/AP'
symptom: 'LA Réunion重定向'
cause: 'RE 国家本地 ECC 配置把 15/17/18 识别为 emergency 并配置 fallback=112，导致普通应急短号被紧急路由重定向到 112'
source_log: 'Old Outline knowledge base; split from 通话问题案例补充.md'
first_bad_point: 'eccdata / EccList 中 RE 的 15、17、18 本地配置与运营商期望不一致'
confidence: high
status: summarized
tags:
  - imported
  - split_from_bucket
  - ecc
  - eccdata
  - local-config
search_tier: case_summary
---

# LA Réunion重定向

<!-- IMPORTED_CASE_BOUNDARY_START -->
> 使用口径：本页已整理出可复用 Case 卡片。排查时优先看“用户现象 / 结论 / 关键证据 / 定位口径”；“原始案例内容”只用于回溯来源，不作为单独结论引用。
<!-- IMPORTED_CASE_BOUNDARY_END -->


## 阅读入口

本 case 从旧 Outline 案例集合拆出，已提炼为本地 ECC 配置 / fallback 导致号码被重定向的问题。原始配置步骤保留在后文，便于追溯。

## 用户现象
LA Réunion重定向

## 结论

首坏点是本地 ECC 配置与 Orange La Réunion 需求不一致。`RE` 国家下把 `15`、`17`、`18` 配成 ambulance / police / fire，并存在 `ecc_fallback: "112"`，导致这些号码被平台按紧急号码处理并重定向到 `112`。

MTK 方案是从 `vendor/mediatek/proprietary/packages/services/Telephony/ecc/input/eccdata.txt` 删除 `RE` 下的 `15/17/18` 条目并重新生成 ecc database。UNISOC 方案类似，修改当前分支实际生效的 `uniecc/input/eccdata.txt` 后同步生成物。

## 关键证据

- 原始分类：一、紧急通话
- 来源：通话问题案例补充.md
- 拆分序号：3
- 需求现象：RE 区域拨打 `15`、`17`、`18` 被重定向到 `112`。
- 本地配置：`iso_code: "RE"` 下存在 `15/17/18` emergency number 条目。
- 配置中存在 `ecc_fallback: "112"`。

## 定位口径

| 检查项 | 判断 |
|---|---|
| 是否本地配置命中 | 看 `eccdata` / `EccList` 是否把目标号码识别为 ECC |
| 是否网络下发 | 若 Attach/TAU Accept 也下发同号码，需要分清网络来源和本地来源优先级 |
| fallback | `ecc_fallback` 可能让号码识别和实际拨出号码不一致 |
| 修改路径 | MTK / UNISOC 分支路径不同，以当前编译实际打包路径为准 |
| 回归矩阵 | 插卡、无卡、PIN 锁、飞行模式、目标运营商 SIM 都要测号码识别和实际下发 |

## 复用边界

- 适用于“本地紧急号码配置导致号码被误识别或重定向”的问题。
- 如果号码没有被识别为 ECC，但网络侧将普通呼叫转接到 `112`，应转网络策略排查。

## 原始案例内容

### 案例3：**LA Réunion重定向**

**前言**

关于紧急通话，3GPP有以下说明(3GPP 22101-j20)：

10.1.1 Identification of emergency numbers The ME shall identify an emergency number dialled by the end user as a valid emergency number and initiate emergency call establishment if it occurs under one or more of the following conditions. If it occurs outside of the following conditions, the ME should not initiate emergency call establishment but normal call establishment. Emergency number identification takes place before and takes precedence over any other (e.g. supplementary service related) number analysis.

a)112 and 911 shall always be available. These numbers shall be stored on the ME.

b)Any emergency call number stored on a SIM/USIM when the SIM/USIM is present.

c)000, 08, 110, 999, 118 and 119 when a SIM/USIM is not present. These numbers shall be stored on the ME.

d)Additional emergency call numbers that may have been downloaded by the serving network when the SIM/USIM is present.

**【客户反馈】【QC-61】【P1】Emergency call not well managed for Orange La Réunion**

ID：redmine#161748

Class ：BUG

平台：MTK

地区：RE

问题描述：拨打15，17，18号码会重定向到112

MTK 方案如下，

在vendor/mediatek/proprietary/packages/services/Telephony/ecc/input/eccdata.txt中删除高亮部分

countries {
iso_code: "RE"
`eccs {`
`phone_number: "17"`
`types: POLICE`
`}`
`eccs {`
`phone_number: "15"`
`types: AMBULANCE`
`}`
`eccs {`
`phone_number: "18"`
`types: FIRE`
`}`
ecc_fallback: "112"
}

完整过程如下，

1.修改eccdata.txt内容

2.更新ecc database

   1）根目录执行 source build/envsetup.sh ，lunch full_xxx-eng（xxx是project名字），

   **注意：展锐平台还需要执行一次m aprotoc**

   2）cd 到ecc目录，cd vendor/mediatek/proprietary/packages/services/Telephony/ecc

   3）执行./gen_eccdata.sh

   4）回到alps/目录，执行clean_project_Sagereal.sh清楚之前编译环境

   5）修改/sagereal/mk/VQ558_GH5581_SFR_MEO_SRR_OT(项目名)/下ProjectConfig.mk verno值为软件版本号(记得修改MMDD)

   6）回到alps/目录，整编

展锐方案与MTK类似，修改路径如下，

__[alps/vendor/sprd/platform/packages/apps/UniTelephony/uniecc/input/eccdata.txt](http://192.168.3.81:8085/c/SPRD_V/SPRDROID15_SYS_MAIN_W24.37.2_P1/+/96858/2/alps/vendor/sprd/platform/packages/apps/UniTelephony/uniecc/input/eccdata.txt)__

## 原始资料边界

- 本 case 来自旧 Outline 迁入资料，已提炼为 RE 本地 ECC 配置案例。
- 复用到其它国家时不要照搬删除动作，先确认当地法规、运营商需求表和现场拨打期望。
