---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# 校准参数检查SOP

## 适用场景

用于检查样机是否存在 RF 校准参数缺失、异常或未下载。典型现象包括无服务、射频能量低、发射/接收异常、刷机后 IMEI/校准异常。

## UNISOC 方法一：CFT Result

路径：`DEBUG&LOG -> CFT Result`。

![](../../attachments/outline/5bd697af-fecf-4453-8986-ca64627dd007.png)

## UNISOC 方法二：Logel DSP Test Point

1. 点击 `DSP LTE`。
2. 在 `LTE DSP Test Point List` 空白页面右键，选择 `test point chan 1`。
3. 在 `Addr` 中分别输入 `D33A`、`D33B` 并点击 `Add`。
4. 点击 `Start` 查看对应参数。
5. 如果值为负数，优先怀疑样机未校准、校准数据异常或刷机未正确保留校准数据。

`校准后的 agcgain 值不应为负值`。

![](../../attachments/outline/60984a28-2725-416f-a932-c308baa2a566.png)

异常示例：

![](../../attachments/outline/79e354ea-675c-4a00-92f9-598d30fe9f6b.png)

## MTK 方法一：modem log 关键字

在 System Trace 中搜索：

```text
calibration
RF Calibration was not downloaded
There is no any RF calibration data in DUT
please perform RF calibration or download calibration data
```

异常示例：

![](../../attachments/outline/fea56b8a-4533-4ba7-adf6-b696707d3d1d.png)

![](../../attachments/outline/b0aac2e3-e0dc-4861-93ce-a0cc927a7047.png)

![](../../attachments/outline/c43849b5-e8ac-4b5d-a87a-f8b59bb9cbaa.png)

## MTK 方法二：Engineer Mode

1. 进入 Engineer Mode。
2. 点击 `MDML EM Components`。
3. 选择 `SIM1`。
4. 勾选 `RF Calibration Status Check`。
5. 点击 `Check information`。

![](../../attachments/outline/b42ad1c9-bd37-445c-8953-567138a1432c.png)

异常示例：

![](../../attachments/outline/10c604ff-982f-47ab-8728-7c0c1ba33777.png)

## 判断口径

- 校准缺失是硬件/产线/刷机/NV 保留问题的强信号，不要先归因网络侧。
- 刷机后出现校准异常，先确认是否覆盖了个体化 NV / calibration 分区。
- 需要同时记录样机 SN、IMEI、版本、刷机方式、PAC/镜像名和是否保留 NV。

## 来源记录

- [查看校准参数方法](http://192.168.3.94:8888/doc/5pl55yl5qch5yeg5yc5pww5pa55rov-woi7oetCP4) (`woi7oetCP4`)
