---
title: Qualcomm平台代码
aliases:
  - Qualcomm Modem代码入口
quality: curated
doc_type: index
domain: Platform
platform: Qualcomm
layer: Modem/RF/MCFG/Build
status: active
search_tier: main_entry
tags:
  - Qualcomm
  - Modem
---

# Qualcomm平台代码

## 速查入口

| 文档 | 回答的问题 |
|---|---|
| [[Qualcomm-Modem-RF配置与编译链路]] | RF Card、FEM/RFFE、RF NV、RF Target 分别做什么，如何生成、编译、链接、打包和排障 |
| [[60_Configuration/Qualcomm-MCFG运营商配置与生效链路]] | SIM 如何选择 MCFG、运营商 NV 如何聚合为 `mcfg_sw.mbn`、运行时如何激活和验证 |

## 当前工程

本组文档基于以下实机源码核对：

```text
/home/wx/Project/QCOM/qcom4490/S1E4ProPlus
├── modem/modem_proc
│   └── 当前 MPSS 开发与编译树
└── amss/MPSS.DE.3.1.1/modem_proc
    └── AMSS meta 打包时引用的 MPSS 树
```

目标变体：

```text
clarence.geniot.prod
PRODUCT_LINE=MPSS.DE.3.1.1
```

> [!warning] 两棵 MPSS 树不是同一个目录
> `modem/modem_proc` 编译成功后，不能直接推导 `amss/MPSS.DE.3.1.1/modem_proc` 已同步，也不能直接推导 `NON-HLOS.bin` 已生成。必须继续核对同步、meta 打包和最终镜像。

## 定位原则

1. 先看源配置，再看 SCons/生成器。
2. 再看生成源码、对象、库和 MBN。
3. 最后看 AMSS 实际消费的目录和最终刷机包。
4. 对 cleanpack 目录先执行 `git ls-files`，不要因为目录名是 `build` 就直接删除。

## 关联基础

- [[10_Basics/RF基础概念]]
- [[60_Configuration/配置与客户定制]]
- [[70_Tools-Debug/README|工具与调试]]
