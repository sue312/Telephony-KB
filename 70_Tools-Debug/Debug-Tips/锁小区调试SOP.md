---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# 锁小区调试SOP

## 适用场景

用于固定测试小区，排除小区切换、重选、弱覆盖变化对复现结果的影响。锁小区是临时调试手段，测试完成后必须解除。

## MTK Engineer Mode

1. 拨号进入 Engineer Mode：`*#*#3646633#*#*`。
2. 进入 `Channel Lock`。
3. 选择对应 SIM 卡。
4. 按目标网络配置：
   - `Lock`: `enable`
   - `RAT`: 选择目标制式，例如 `4G`
   - `ARFCN`: 目标 `UARFCN` / `ARFCN`
   - `CELL ID`: 目标 `CID` / `PCI`

![](../../attachments/outline/a82c6996-5f54-4b68-a520-a006aa04832f.png)

ARFCN 和 Cell ID 可通过 Cellular-Z 等工具读取；原导入资料中 EARFCN 对应 ARFCN，PCI 对应 Cell ID。

![](../../attachments/outline/6909898a-79da-432a-a025-9c952dbecaca.png)

5. 点击 `Apply Channel Lock settings`。
6. 按弹框提示选择 `Reset by Airplane Mode`。
7. 验证是否锁定到目标小区。

## UNISOC AT 命令

示例：`1725` 为 ARFCN，`204` 为 PCI。

锁小区：

```text
AT+SFUN=5
AT+SPFORCEFRQ=12,2,1725,204
AT+SFUN=4
```

解锁：

```text
AT+SFUN=5
AT+SPFORCEFRQ=12,0
AT+SFUN=4
```

## 注意事项

- 测试完成后必须解除锁小区。
- 锁小区前先确认目标位置、目标 PCI / ARFCN、信号强度和小区稳定性。
- 不要把锁小区后的注册成功直接等价为正常移动场景成功；它只证明固定小区条件下链路可用。

## 来源记录

- [锁小区](http://192.168.3.94:8888/doc/6zsb5bcp5yy6-tQf6HovYEI) (`tQf6HovYEI`)
