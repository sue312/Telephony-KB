# QXDM 常见业务筛选配置包实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 基于本机 QXDM 5.2.660 生成并验证 11 组 LTE/NR 常见业务 `.dmc + .cfg + .items.txt` 配置。

**架构：** 以本机 QXDM 数据库为唯一 item key 来源，按业务建立独立 Filtered View，再由 QXDM 保存 DMC、导出启用项清单并生成设备端 CFG。PowerShell 验证脚本负责结构、命名、非空、DMC XML 和业务清单一致性检查，QXDM 负责格式加载验证。

**技术栈：** QXDM 5.2.660、QXDM COM/GUI automation、PowerShell 7、XML、Telephony-KB Markdown。

---

## 文件结构

- 创建：`70_Tools-Debug/QXDM/README.md`，说明 DMC/CFG 差异、导入方法、组合策略和兼容性边界。
- 创建：`70_Tools-Debug/QXDM/profiles/<profile>/<profile>.dmc`，保存 QXDM logging masks 和命名 Filtered View。
- 创建：`70_Tools-Debug/QXDM/profiles/<profile>/<profile>.cfg`，保存 Stream 1 设备端 SD Logging mask。
- 创建：`70_Tools-Debug/QXDM/profiles/<profile>/<profile>.items.txt`，保存业务目标、实际启用项和未匹配候选。
- 创建：`70_Tools-Debug/QXDM/validation/Test-QxdmProfiles.ps1`，自动检查 11 组交付物。
- 创建：`70_Tools-Debug/QXDM/validation/QXDM-5.2.660-validation.md`，记录本机加载验证和设备端待验证边界。

### 任务 1：盘点本机格式与自动化能力

- [ ] **步骤 1：记录 QXDM 版本与原生样例**

运行：

```powershell
(Get-Item 'C:\Program Files\Qualcomm\QXDM5\QXDM.exe').VersionInfo.ProductVersion
Get-ChildItem 'C:\ProgramData\Qualcomm\QXDM\Config\Qualcomm DMC Library' -Recurse -File
```

预期：版本为 `5.2.660.0`，能看到 `Default.dmc`、`Default.cfg` 和 Qualcomm Secondary DMC。

- [ ] **步骤 2：检查 DMC/CFG 文件结构和 QXDM 自动化接口**

运行：

```powershell
python 'D:\CodexHome\skills\modem-log-parser\scripts\qxdm_runner.py' probe-automation
Select-String -Path 'C:\Program Files\Qualcomm\QXDM5\AutomationSamples\*.pl' -Pattern 'LoadConfig|SaveConfig|ConvertDMCtoCFG'
```

预期：QXDM COM 可启动，且本机样例公开 `LoadConfig`、`SaveConfig`、`ConvertDMCtoCFG`。

### 任务 2：建立业务候选项与生成链路

- [ ] **步骤 1：从本机数据库和默认 DMC 提取可用 item family**

对 LTE/NR RRC、NAS、IMS、WDS/DSD、UIM/MCFG、SMS、mobility、emergency、SSR/fatal 逐组搜索；输出只接受本机 QXDM 可识别的 item key。

- [ ] **步骤 2：建立 11 个命名 Filtered View**

每个视图名与 profile 名一致，启用 `Accept Unknowns`，选择 Stream 1；控制面项独立成组，高频 L1/RF 项保持关闭。

- [ ] **步骤 3：为每个视图保存 DMC、CFG 和 items 文本**

使用 QXDM `Save Configuration`/`Save As DMC` 生成 DMC，使用 `Tools -> CFG File Generator -> Save Diag Mask for Stream 1` 生成 CFG，使用 `Save As TXT` 生成实际启用项清单。

预期：每个 profile 目录恰好有一个同名 `.dmc`、`.cfg` 和 `.items.txt`。

### 任务 3：编写自动验证脚本

- [ ] **步骤 1：创建 `Test-QxdmProfiles.ps1`**

脚本固定检查设计中的 11 个 profile；验证目录和三种扩展名存在、文件非空、文件 basename 一致、DMC 根节点为 `QXDMProfessional`、items 文件包含业务说明和启用项章节。

- [ ] **步骤 2：运行结构验证**

运行：

```powershell
pwsh -NoProfile -File 'F:\Codex\Knowledge\Telephony-KB\70_Tools-Debug\QXDM\validation\Test-QxdmProfiles.ps1'
```

预期：输出 `Profiles passed: 11/11`，退出码为 0。

### 任务 4：执行 QXDM 原生加载验证

- [ ] **步骤 1：逐个加载 DMC**

通过 QXDM Automation `LoadConfig` 依次加载 11 个 DMC，随后用 `SaveConfig` 保存到临时路径；每个输出必须非空且 QXDM debug log 不出现 load/parse error。

- [ ] **步骤 2：逐个验证 CFG**

通过本机 QXDM CFG Generator/转换接口读取或往返转换 11 个 CFG；记录成功数、失败数和错误文本。

- [ ] **步骤 3：写入验证报告**

报告固定记录工具版本、验证日期、11 个 profile 结果、QXDM debug log 证据、未匹配候选，以及“未连接目标设备，runtime mask acceptance 待验证”。

### 任务 5：编写使用说明并完成仓库检查

- [ ] **步骤 1：编写 README**

README 包含：DMC/CFG 用途差异、11 个业务包选择表、QXDM 导入 DMC 步骤、CFG 设备端 SD Logging 用法、多个 DMC 组合方式、日志量注意事项和版本兼容性。

- [ ] **步骤 2：执行最终检查**

运行：

```powershell
pwsh -NoProfile -File 'F:\Codex\Knowledge\Telephony-KB\70_Tools-Debug\QXDM\validation\Test-QxdmProfiles.ps1'
git -C 'F:\Codex\Knowledge\Telephony-KB' diff --check
git -C 'F:\Codex\Knowledge\Telephony-KB' status --short
```

预期：11/11 通过，`git diff --check` 无输出，状态只包含本任务新增文件。
