---
doc_type: tool
domain: Tools-Debug
status: active
quality: curated
search_tier: supplemental
---

# FCC-B40禁用验证SOP

## 适用场景

用于 FCC / 北美认证场景下验证 LTE B40 是否已按项目策略禁用。该文只写验证方法，不定义项目是否必须禁用 B40；是否禁用以认证、RF 和客户需求为准。

## 背景口径

- 北美 FCC 场景中，LTE B40 可能只能支持并测试部分频段范围，例如 `2305-2315 MHz` 和 `2350-2360 MHz`。
- 如果项目支持 B40，就可能需要做对应 RFSPEC / band edge 验证。
- 如果认证策略要求不支持 B40，需要能从 UE capability 和 log 中证明 B40 已不在能力声明里。

## 测试准备

| 项 | 要求 |
| --- | --- |
| 白卡 | 准备两张白卡，例如 `50501` 和 `310260` |
| 鉴权 | `INC KI` 按仪表要求写入，算法选择 `Milenage`，OPC 按配置文件要求写入 |
| 仪表 | 使用支持 IMS 的 CMW500 或项目指定综测仪 |
| 配置 | 加载项目提供的 `FccDisableB40.dfl` 或等效配置 |

白卡鉴权示例：

![](../../attachments/outline/1e2ff72a-2b85-4c10-89c8-8f76409f762d.png)

## 加载仪表配置

1. 点击 `SAVE RCL`。
2. 在弹窗中进入 `IMS` 文件夹，选择 `FccDisableB40.dfl`。
3. 点击 `Recall`。

![](../../attachments/outline/921caaa9-3a38-4b6e-9600-bccd7ac808a2.png)

## 打开综测仪信号

1. 如果 `LTE signaling` 为 `OFF`，点击 `ON/OFF` 打开。
2. 等待左上角图标变绿，仪器接口信号灯亮起。

![](../../attachments/outline/efd22d33-2e72-4fd4-be24-66b29ac656a6.png)

## 连接手机

1. 将手机放到耦合板上并连接仪表。
2. 观察手机是否注册到综测仪 LTE 网络。
3. 如果不能自动注册，先开关飞行模式。
4. 仍不能注册时，关闭自动选网并手动选网。

路径示例：`Settings -> SIM -> Automatically select network`。

![](../../attachments/outline/d5086457-bdc4-43fe-bb48-6eeced248fe4.png)

## 验证结果

建议验证两次：

- 插 `50501` 白卡验证漫游场景。
- 插 `310260` 白卡验证非漫游场景。

### 仪表查看

连接综测仪网络后，将 `UE Info` 改为 `UE Capabilities`。

![](../../attachments/outline/c1ddf619-d5c9-43ed-bed5-d79fba4ce3b4.png)

查看 `RF Parameters` 中是否仍包含 B40。

![](../../attachments/outline/27c6f96c-86d3-45dd-b1bd-4f451058fd63.png)

### Log 查看

需要抓取注网过程 log，建议先打开 log 再连接仪表或切换网络。

MTK log 示例：

![](../../attachments/outline/fb676324-9ec9-4ec3-8d81-5b165eb890b2.png)

![](../../attachments/outline/f836ea26-79ea-4475-b068-4696abbf1f8c.png)

UNISOC log 示例：

![](../../attachments/outline/9eb562d1-2ede-4910-9da1-5d91170c789d.png)

## 输出结论模板

```text
项目 / 版本：
测试场景：FCC B40 禁用验证
白卡：50501 / 310260
仪表配置：
是否注册综测仪网络：
UE Capability 中是否包含 B40：
Log 中能力上报证据：
结论：B40 已禁用 / 仍声明支持 B40 / 证据不足
```

## 来源记录

- [FCC 禁用B40 结果验证](http://192.168.3.94:8888/doc/fcc-b40-NKKleLJQVh) (`NKKleLJQVh`)
