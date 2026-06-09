param(
  [string]$Root = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

$configDir = Join-Path $Root '60_Configuration'
$markerStart = '<!-- CONFIG_TEMPLATE_BLOCK_START -->'
$markerEnd = '<!-- CONFIG_TEMPLATE_BLOCK_END -->'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Join-Lines {
  param([string[]]$Lines)
  return ($Lines -join "`n").Trim()
}

function Get-ConfigHint {
  param([string]$Name)

  switch -Wildcard ($Name) {
    'APN*' {
      return @{
        Source = 'apns-conf.xml / APN database / APN overlay'
        Runtime = 'content://telephony/carriers、APN UI、RILJ setupDataCall'
        Modem = 'PDN Connectivity、ESM cause、DataCall profile'
      }
    }
    'CarrierConfig*' {
      return @{
        Source = 'CarrierConfig XML / overlay / CarrierService'
        Runtime = 'dumpsys carrier_config、CarrierConfigLoader log'
        Modem = '读取方业务 log，必要时结合 IMS/Data/Call trace'
      }
    }
    '*CarrierService*' {
      return @{
        Source = 'CarrierConfigLoader / DefaultCarrierConfigService / carrier app'
        Runtime = 'dumpsys carrier_config、bind service log、phoneId/subId'
        Modem = '读取方业务 log，确认配置是否被业务模块采用'
      }
    }
    'ECC*' {
      return @{
        Source = 'EF_ECC / ECC database / CarrierConfig / vendor EccList'
        Runtime = 'EmergencyNumberTracker、Telecom/Dialer log'
        Modem = 'emergency call routing、CS/IMS emergency trace'
      }
    }
    '*NV*' {
      return @{
        Source = 'fixnv / operator NV / MCFG / NVTool 导入文件'
        Runtime = 'NVTool readback、版本号、modem 运行时读取值'
        Modem = 'modem NV trace、能力开关、profile 选择'
      }
    }
    '运营商名称*' {
      return @{
        Source = 'EFSPN / EFPNN / OPL / spn-conf / CarrierConfig'
        Runtime = 'ServiceState、TelephonyRegistry、UI operator name log'
        Modem = 'PLMN/RPLMN/registered PLMN 与 AP 显示名映射'
      }
    }
    'IMS*' {
      return @{
        Source = 'CarrierConfig / SBP/DSBP/CXP / IMS profile / UA'
        Runtime = 'dumpsys ims、ImsService log、AT+EIMSCFG'
        Modem = 'SIP、IKE、IMS bearer、IMS modem trace'
      }
    }
    'SMS*' {
      return @{
        Source = 'SMSC / FDN / short code / voicemail / CarrierConfig'
        Runtime = 'RILJ SEND_SMS、SmsDispatcher、TelephonyProvider'
        Modem = 'RP/CP/SMS over SGs 或 SMS over IMS trace'
      }
    }
    '补充业务*' {
      return @{
        Source = 'CarrierConfig / UT/XCAP / CISS / supplementary service profile'
        Runtime = 'PhoneInterfaceManager、GsmCdmaPhone、XCAP HTTP log'
        Modem = 'AT/CISS/USSD/UT domain selection trace'
      }
    }
    'SIMLock*' {
      return @{
        Source = 'modem SIMLock 配置 / 白名单 / 解锁策略 / AP UI'
        Runtime = 'SIMLock service log、锁网状态、卡槽状态'
        Modem = 'modem lock result、PLMN allow/deny、NV readback'
      }
    }
    '小区广播*' {
      return @{
        Source = 'CellBroadcast 配置 / channel range / emergency alert rules'
        Runtime = 'CellBroadcastService、CBS settings、logcat alert flow'
        Modem = 'CB message 上报、ETWS/CMAS trace'
      }
    }
    'User-Agent*' {
      return @{
        Source = 'IMS/MMS/HTTP User-Agent 配置和运营商要求'
        Runtime = 'SIP REGISTER、MMS HTTP、streaming request log'
        Modem = 'SIP/HTTP 报文中的最终 UA 字段'
      }
    }
    '网络制式图标*' {
      return @{
        Source = 'MobileMappings / CarrierConfig / RAT display policy'
        Runtime = 'TelephonyDisplayInfo、ServiceState、SystemUI log'
        Modem = 'RAT/NR state/EN-DC 状态与 AP 显示映射'
      }
    }
    '卫星通信*' {
      return @{
        Source = 'Satellite feature flag / CarrierConfig / resource overlay'
        Runtime = 'dumpsys satellite、Telephony satellite log'
        Modem = 'satellite modem capability / registration state'
      }
    }
    default {
      return @{
        Source = '源码配置 / 产物配置 / 运营商需求'
        Runtime = 'dumpsys、logcat、业务模块运行时 dump'
        Modem = 'modem trace、协议字段或运行时状态'
      }
    }
  }
}

function Add-CommonTemplateSections {
  param(
    [string]$Name,
    [string]$Path,
    [string]$Block
  )

  if ($Block.Contains('### 平台差异') -or -not $Block.Contains('### 常见失败模式')) {
    return $Block
  }

  $hint = Get-ConfigHint -Name $Name
  $configReadmeLink = 'README.md'
  $caseIndexLink = '../40_Case-Library/Case横向索引.md'
  $platformCodeLink = '../50_Platform-Code/README.md'
  $toolsLink = '../70_Tools-Debug/Commands/常用命令.md'

  if (-not [string]::IsNullOrWhiteSpace($Path) -and $Path -like '60_Configuration/Core-Config/*') {
    $configReadmeLink = '../README.md'
    $caseIndexLink = '../../40_Case-Library/Case横向索引.md'
    $platformCodeLink = '../../50_Platform-Code/README.md'
    $toolsLink = '../../70_Tools-Debug/Commands/常用命令.md'
  } elseif (-not [string]::IsNullOrWhiteSpace($Path) -and $Path -like '60_Configuration/Business-Config/*') {
    $configReadmeLink = '../README.md'
    $caseIndexLink = '../../40_Case-Library/Case横向索引.md'
    $platformCodeLink = '../../50_Platform-Code/README.md'
    $toolsLink = '../../70_Tools-Debug/Commands/常用命令.md'
  } elseif (-not [string]::IsNullOrWhiteSpace($Path) -and $Path -like '60_Configuration/References/*') {
    $configReadmeLink = '../../README.md'
    $caseIndexLink = '../../../40_Case-Library/Case横向索引.md'
    $platformCodeLink = '../../../50_Platform-Code/README.md'
    $toolsLink = '../../../70_Tools-Debug/Commands/常用命令.md'
  }

  $extra = Join-Lines -Lines @(
    '### 平台差异',
    '',
    '| 平台 | 重点看点 | 验证口径 |',
    '|---|---|---|',
    '| Android common | AOSP 公共 XML、Provider、framework 读取点 | 先证明 common 默认值和运行时 dump 是否一致 |',
    '| UNISOC | carrier overlay、CarrierService、Operator NV、modem profile | 同时看 AP log、产物配置、NV/readback 和 modem trace |',
    '| MTK | vendor/mediatek 私有配置、SBP/DSBP/CXP、NVRAM | 结合 debuglogger、ELT/MD log、AP dump 验证最终值 |',
    '| Qualcomm | CarrierConfig overlay、MCFG/QCRIL、modem profile | 结合 dumpsys、QXDM/QCAT、MCFG 产物确认 |',
    '',
    '### 验证命令与 log',
    '',
    '| 目标 | 证据入口 | 预期结论 |',
    '|---|---|---|',
    "| 源配置存在 | $($hint.Source) | 能定位到需求字段、默认值和项目覆盖值 |",
    "| 运行时 dump 生效 | $($hint.Runtime) | 设备当前值与预期配置一致 |",
    '| AP/vendor 已采用 | Telephony/RILJ/vendor service log | 能看到读取、选择、下发或业务判断动作 |',
    "| modem/协议侧采用 | $($hint.Modem) | 协议字段、modem 状态或 reject cause 能与配置结果闭环 |",
    '',
    '### 关联入口',
    '',
    '| 入口 | 用途 |',
    '|---|---|',
    "| [配置目录 README]($configReadmeLink) | 回到配置分类和放置规则 |",
    "| [Case横向索引]($caseIndexLink) | 查历史同类问题和第一坏点 |",
    "| [平台代码入口]($platformCodeLink) | 查厂商代码读取位置 |",
    "| [常用命令]($toolsLink) | 查 dumpsys、logcat 和 adb 命令 |"
  )

  return $Block -replace '(?m)^### 常见失败模式', "$extra`n`n### 常见失败模式"
}

function Update-ConfigDoc {
  param(
    [string]$Name,
    [string]$Path,
    [string]$Block
  )

  if ([string]::IsNullOrWhiteSpace($Path)) {
    $docPath = Join-Path $configDir $Name
  } else {
    $docPath = Join-Path $Root $Path
  }
  if (-not (Test-Path -LiteralPath $docPath)) {
    throw "Config doc not found: $docPath"
  }

  $text = [System.IO.File]::ReadAllText($docPath, [System.Text.Encoding]::UTF8)
  $Block = Add-CommonTemplateSections -Name $Name -Path $Path -Block $Block
  $wrappedBlock = "`n$markerStart`n$Block`n$markerEnd`n"

  if ($text.Contains($markerStart)) {
    $pattern = "(?s)\r?\n?$([regex]::Escape($markerStart)).*?$([regex]::Escape($markerEnd))\r?\n?"
    $newText = [regex]::Replace($text, $pattern, $wrappedBlock, 1)
  } else {
    $headingMatch = [regex]::Match($text, '(?m)^##\s+(速查结论|阅读入口|使用入口)\s*$')
    if ($headingMatch.Success) {
      $searchStart = $headingMatch.Index + $headingMatch.Length
      $nextHeading = [regex]::Match($text.Substring($searchStart), '(?m)^##\s+')
      if ($nextHeading.Success) {
        $insertAt = $searchStart + $nextHeading.Index
        $newText = $text.Insert($insertAt, $wrappedBlock)
      } else {
        $newText = $text.TrimEnd() + $wrappedBlock
      }
    } else {
      $h1 = [regex]::Match($text, '(?m)^#\s+.+$')
      if (-not $h1.Success) {
        throw "No insertion point found: $docPath"
      }
      $insertAt = $h1.Index + $h1.Length
      $newText = $text.Insert($insertAt, $wrappedBlock)
    }
  }

  [System.IO.File]::WriteAllText($docPath, $newText, $utf8NoBom)
  Write-Host "Normalized: $Name"
}

$docs = @(
  @{
    Name = 'APN配置方法_重构.md'
    Path = '60_Configuration/Core-Config/APN配置方法_重构.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| AOSP / 产品 APN 库 | `apns-conf.xml`、项目 overlay、运营商 APN 表 | `content://telephony/carriers`、APN UI、bugreport APN dump |',
      '| CarrierConfig / APN 可见性 | APN type 隐藏、编辑限制、MMS/IMS/XCAP 相关开关 | `dumpsys carrier_config`、APN 列表是否显示目标 type |',
      '| AP DataProfile | `DataProfileManager` 选择 IA APN 和业务 APN | RILJ `SET_INITIAL_ATTACH_APN`、`setupDataCall` |',
      '| modem / 网络侧 | PDN Connectivity Request、ESM reject、default bearer | modem ESM/SM trace、APN/protocol/auth 字段 |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'APN XML / database',
      '-> TelephonyProvider 入库',
      '-> DataProfileManager 按 APN type / carrier / roaming 选择',
      '-> setInitialAttachApn 或 setupDataCall 下发',
      '-> modem 发起 PDN / PDP',
      '-> 网络接受或返回 ESM cause',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| APN 看得见但连不上 | IA APN / data APN 是否同一个、protocol/auth 是否正确 | AP 已下发且 ESM reject 时，第一坏点通常在 APN/订阅/网络侧 |',
      '| APN 配了但 UI 不显示 | APN type、CarrierConfig hide list、MVNO 匹配 | 入库失败或被 AP 策略过滤，不是 modem 问题 |',
      '| IMS/MMS/XCAP 失败 | 是否使用了正确专用 APN | 默认 Internet APN 成功不代表专用 APN 成功 |'
    ))
  },
  @{
    Name = 'CarrierConfig配置方法_重构.md'
    Path = '60_Configuration/Core-Config/CarrierConfig配置方法_重构.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| AOSP 默认配置 | `packages/apps/CarrierConfig` 默认 XML | `dumpsys carrier_config` 默认值 |',
      '| 厂商 / 项目 overlay | `vendor/*/overlays/packages/apps/CarrierConfig` | 产物中 XML、overlay 是否打入 |',
      '| CarrierService | `CarrierConfigLoader` 绑定默认包或 carrier app | `CarrierConfigLoader` log、bind/fetch 结果 |',
      '| 临时 override | `overrideConfig()`、测试命令 | `dumpsys carrier_config` 是否出现 override 值 |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'SIM / carrier id / MCCMNC / GID / SPN',
      '-> CarrierConfigLoader.updateConfigForPhoneId',
      '-> bindToConfigPackage / CarrierService.onLoadConfig',
      '-> PersistableBundle 合并',
      '-> Telephony / Data / IMS / UI 模块读取',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| XML 已改但 dump 不变 | overlay 是否进产物、carrier id 是否命中、是否被 override 覆盖 | 源配置未进入运行时 bundle |',
      '| dump 正确但业务不变 | 消费方是否读取该 key，是否还有厂商私有开关 | 第一坏点在读取链路或私有配置优先级 |',
      '| 换卡后仍旧值 | SIM 状态触发、缓存、subId/phoneId 映射 | 配置刷新或卡槽映射问题 |'
    ))
  },
  @{
    Name = 'ECC配置方法_重构.md'
    Path = '60_Configuration/Core-Config/ECC配置方法_重构.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| SIM / 网络 | EF_ECC、网络下发 emergency number | radio log、EmergencyNumberTracker dump |',
      '| 本地号码库 | AOSP / 厂商 ECC database、`eccdata` | emergency number list、拨号前号码分类 |',
      '| CarrierConfig / 客制化 | category、URN、routing、fallback、card condition | `dumpsys carrier_config`、Dialer/Telecom log |',
      '| modem / 域选 | CS / IMS emergency、CSFB/EPSFB、无卡拨号路径 | NAS/RRC/CC/SIP trace |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'SIM / network / local ECC source',
      '-> EmergencyNumberTracker 合并号码池',
      '-> Dialer / Telecom 判断紧急号码',
      '-> domain selection 选择 CS / IMS / fallback',
      '-> RIL / modem 发起紧急呼叫',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 号码被误识别成 ECC | 本地号码库、MCC/MNC、category/fallback | 第一坏点在号码池或匹配条件 |',
      '| 无卡紧急呼叫失败 | card flag、slot selection、eSIM/physical SIM 过滤 | AP 选卡失败和 modem 拒绝要分开 |',
      '| ECC 后不回 LTE | 是否走 CSFB、是否因 `ecc_cs_prefer` 直接选网进 3G | 不是所有 3G 停留都属于 CSFB fast return |'
    ))
  },
  @{
    Name = 'NV参数配置.md'
    Path = '60_Configuration/Core-Config/NV参数配置.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| modem NV / Operator NV | NVTool、Operator NV、RDNV、产品默认 NV | NV readback、版本号、LID/verno |',
      '| fixnv / NVRAM / NVDATA | 个体化参数、IMEI、RF calibration | 主备分区回读、factory log、工模参数 |',
      '| 编译产物 | modem image、PAC、patch list、流水线参数 | 设备实际 image 时间戳、out/PAC 对比 |',
      '| AP 侧表象 | IMEI unknown、META 失败、radio unavailable、不识卡 | bugreport、radio log、modem assert |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '源 NV / 默认参数 / 工厂写入',
      '-> 编译或下载产物',
      '-> 刷机 / 写号 / 校准',
      '-> modem boot 读取 NV / NVRAM',
      '-> AP 看到注册、SIM、IMEI、射频或稳定性表象',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| IMEI unknown | 加密宏控、LID size/verno、SML、fixnv 主备 | 先判 NV 读取/解密，不先判 SIM |',
      '| META 无法连接 | modem 是否已 EE/assert、SML 数据是否为空 | META 是表象，第一坏点常在 modem/NV 链路 |',
      '| 升级后 modem assert | modem image、RF parameter、patch list、NV 迁移 | 产物不一致优先于业务配置 |'
    ))
  },
  @{
    Name = '运营商名称配置方法.md'
    Path = '60_Configuration/Business-Config/运营商名称配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| SIM EF | EF_SPN、EF_PNN、EF_OPL、EF_OPL5G | UICC log、SIM records dump |',
      '| 网络侧 | NITZ / ONS / registered PLMN | radio log、ServiceState、NITZ log |',
      '| 本地名称库 | `numeric_operator.xml`、overlay、CarrierConfig | bugreport、资源匹配、显示名 dump |',
      '| 漫游策略 | non-roaming、roaming display、MVNO 匹配 | `ServiceStateTracker.updateSpnDisplay`、UI 显示 |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'SIM EF / network name / local PLMN database',
      '-> SIMRecords / ServiceState / CarrierConfig',
      '-> CarrierDisplayNameResolver 或平台私有名称解析',
      '-> ServiceStateTracker.updateSpnDisplay',
      '-> 状态栏 / 锁屏 / 手动搜网列表显示',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 手动搜网名称为空 | MCCMNC 5/6 位、numeric_operator key、PLMN list 字段 | 本地名称库未命中或 key 位数错误 |',
      '| MVNO 显示主网名 | SPN/PNN/OPL、APN MVNO 字段、fallback 顺序 | MVNO 匹配失败优先于 UI 问题 |',
      '| 飞行模式后名称变化 | NITZ 缓存、SIM records 是否重读、ServiceState 更新 | 缓存清理或刷新时序问题 |'
    ))
  },
  @{
    Name = 'Modem NV参数映射.md'
    Path = '60_Configuration/References/NV/Modem NV参数映射.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| UNISOC Operator NV 文档 | 字段定义和分组说明 | NVTool / readback 对照 |',
      '| Qualcomm MCFG / NV 映射 | 字段级大表入口 | MCFG 产物和运行时 modem 行为 |',
      '| 拆分字段表 | `References/NV` 下的大表 | 主文档只做索引和读法，不承载全量字段 |',
      '',
      '### 使用链路',
      '',
      '```text',
      '需求字段 / 历史问题关键词',
      '-> 本文找到 NV 分组',
      '-> References/NV 查字段含义',
      '-> 回到 NV参数配置 确认写入和运行时验证',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 查到字段但不知道怎么验证 | 回到 `NV参数配置.md` 的读写和回读方法 | 映射表只解释字段，不证明生效 |',
      '| 字段名相似 | 平台、分组、版本、operator profile | 不跨平台套用字段 |'
    ))
  },
  @{
    Name = 'CarrierConfig参数映射.md'
    Path = '60_Configuration/References/CarrierConfig/CarrierConfig参数映射.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| AOSP CarrierConfig key | 按 APN / IMS / Call / MMS / Network 等分组索引 | `dumpsys carrier_config` |',
      '| 字段级参考表 | `References/CarrierConfig` | 主文档只做入口，不重复大表 |',
      '| 业务文档 | APN、IMS、ECC、SMS、网络图标等配置方法 | 关联业务现象和验证动作 |',
      '',
      '### 使用链路',
      '',
      '```text',
      '业务现象',
      '-> 本文定位 CarrierConfig key 分组',
      '-> References/CarrierConfig 查字段',
      '-> 对应配置方法文档验证生效链路',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| key 存在但无效 | 读取模块是否消费该 key、平台是否覆盖 | dump 正确不等于业务已采用 |',
      '| key 找不到 | Android 版本、厂商私有 key、命名变化 | 先确认基线和平台差异 |'
    ))
  },
  @{
    Name = 'IMS配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| CarrierConfig / IMS profile | VoLTE/VoWiFi/VoNR/SMS over IMS 开关 | `dumpsys carrier_config`、IMS service log |',
      '| MTK SBP / DSBP / CXP | 运营商支持状态、IMC 条件 | `AT+EIMSCFG`、IMC / SBP log |',
      '| modem / IMS APN | P-CSCF、IMS PDN、IKE/ePDG、SIP | modem IMS/SIP/IWLAN trace |',
      '| AP IMS service | 注册状态、MMTel capability、feature update | `dumpsys ims`、radio/IMS log |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '运营商 / SIM / CarrierConfig / IMS profile',
      '-> AP IMS service 和 modem IMC 判定能力',
      '-> 建 IMS PDN 或 IWLAN/ePDG',
      '-> SIP REGISTER',
      '-> MMTel / SMS / VoWiFi / ViLTE capability',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| LTE 正常但不发 IMS PDN | SBP/DSBP/CXP、allow_ims、MCCMNC whitelist | IMS 配置门控早于 SIP |',
      '| SIP 403 | IMEI/签约/P-CSCF/realm/profile | 网络拒绝和本地配置要用 SIP response 区分 |',
      '| VoWiFi 不注册 | IKE/ePDG、Wi-Fi 网络、IMS profile | 没有 IKE 证据时不直接判 SIP |'
    ))
  },
  @{
    Name = 'SMS配置方法.md'
    Path = '60_Configuration/Business-Config/SMS配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| SIM EF / SMSC | SMSP、SMSC、FDN | UICC log、RILJ `SEND_SMS` 前检查 |',
      '| CarrierConfig / short code XML | premium SMS、短码、voicemail、SMS over IMS | `dumpsys carrier_config`、SMSDispatcher log |',
      '| IMS / SDM profile | SMS over IP / SGs / CS 域选 | SDM/IMS log、SIP MESSAGE / SGs trace |',
      '| modem / network | RP/CP 层、网络返回 cause | modem SMS trace |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'App / Dialer / SMS provider',
      '-> SMSDispatcher / FDN / short code 判断',
      '-> 域选 IMS / SGs / CS',
      '-> RILJ SEND_SMS 或 SIP MESSAGE',
      '-> modem / network response',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| RILJ 无 SEND_SMS | short code、permission、FDN、AP 拦截 | AP 分发前失败 |',
      '| 配了 SMS over IMS 仍走 SGs | SDM prefer rule、IMS 注册、profile 开关 | 域选配置优先级问题 |',
      '| FDN 下短信失败 | 收件人和 SMSC 是否都在 FDN | FDN 双重校验问题 |'
    ))
  },
  @{
    Name = 'SIMLock配置方法.md'
    Path = '60_Configuration/Business-Config/SIMLock配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| modem SIMLock 配置 | 白名单、锁类型、剩余次数、锁卡策略 | modem log、锁卡状态、AT/NV 读取 |',
      '| AP UI / Telephony | 锁卡弹框、SubInfo、MCC/MNC 显示 | radio log、Settings/Telephony log |',
      '| 编译产物 | modem image、operator NV、市场版本 | PAC/out 对比、产物时间戳 |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '锁网白名单 / modem profile',
      '-> 编译或下载进入 modem 产物',
      '-> 插卡后 modem 判锁',
      '-> AP 同步锁卡状态和 UI',
      '-> 注册允许或拒绝',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 非白名单卡仍可驻网 | modem 产物是否含锁网配置 | 第一坏点通常在产物链路，不是 AP UI |',
      '| AP 显示 MCC/MNC 为空 | 锁卡状态下是否允许读卡 | 不等于 SIM 读卡失败 |',
      '| 升级后锁网失效 | modem image / NV 是否被替换 | 先查版本和产物一致性 |'
    ))
  },
  @{
    Name = '补充业务配置方法.md'
    Path = '60_Configuration/Business-Config/补充业务配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| IMS / XCAP profile | XCAP AUID、BSF/GBA、UT/XCAP APN | HTTP log、XCAP URL、401/200/400 |',
      '| USSD / SS 域选 | IMS USSI、CS USSD、运营商能力 | AT+ECUSD / CISS / SIP / USSI log |',
      '| CarrierConfig / NV | 运营商开关、fallback 策略 | dump、AT 命令、modem log |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '用户发起 CF/CB/USSD/UT',
      '-> AP 判断目标域和配置',
      '-> XCAP HTTP / IMS USSI / CS SS',
      '-> 网络返回状态',
      '-> AP 更新 UI 或触发回落',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| XCAP HTTP 400 | AUID 是否重复拼接、URL 是否符合运营商要求 | 配置拼接错误早于网络业务失败 |',
      '| USSD 失败 | 运营商是否支持 IMS USSI | 目标域选错时不能先判网络拒绝 |',
      '| CSFB 后才成功 | XCAP/IMS 失败原因和回落触发点 | 要区分主路径失败和 fallback 成功 |'
    ))
  },
  @{
    Name = '小区广播配置方法.md'
    Path = '60_Configuration/Business-Config/小区广播配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| CellBroadcast 配置 | channel range、MCC/MNC、开关默认值 | CB app / cellbroadcast log |',
      '| Mainline / full 版本 | 版本限制、资源位置差异 | APK/模块版本、配置是否进入目标包 |',
      '| modem / network | LTE/NR CB/CMAS/ETWS 上报 | modem CB trace、RIL indication |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '配置 channel / MCCMNC / 开关',
      '-> CellBroadcast 模块加载',
      '-> modem 上报 CB / CMAS / ETWS',
      '-> AP 过滤和展示',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 配置信道后仍不过测 | full/Mainline 版本和 MCC/MNC 条件 | 配置进入错误包或条件未命中 |',
      '| 关闭菜单仍收到紧急广播 | 普通 CB 和 emergency alert 边界 | 紧急告警可能不受普通菜单开关控制 |'
    ))
  },
  @{
    Name = 'User-Agent配置方法.md'
    Path = '60_Configuration/Business-Config/User-Agent配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| IMS / SIP UA | IMS profile、CarrierConfig、vendor IMS 配置 | SIP REGISTER/INVITE header |',
      '| MMS UA | MMS CarrierConfig、MmsService 配置 | HTTP UA、MMS send log |',
      '| Video Streaming UA | 浏览器/媒体/运营商 profile | HTTP header、业务抓包 |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      '运营商 UA 需求',
      '-> 对应业务配置源',
      '-> AP/IMS/MMS 模块读取',
      '-> HTTP 或 SIP header 出现在网络侧',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| dump 正确但 header 不变 | 业务模块是否读取该字段 | 配置未被消费 |',
      '| 只有某业务 UA 错 | 区分 IMS / MMS / streaming 三套来源 | 不跨业务套用同一配置 |'
    ))
  },
  @{
    Name = '网络制式图标配置方法.md'
    Path = '60_Configuration/Business-Config/网络制式图标配置方法.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| CarrierConfig | 5G/4G icon、show 4G for LTE、NR display rule | `dumpsys carrier_config`、DisplayInfo log |',
      '| Framework mapping | MobileMappings、ServiceState、TelephonyDisplayInfo | status bar / QS / Settings 显示 |',
      '| modem 状态 | LTE/NR 注册态、ENDC/NR availability | RILJ data reg、NR state、physical channel config |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'RAT / NR state / carrier config',
      '-> ServiceState / TelephonyDisplayInfo',
      '-> MobileMappings',
      '-> SystemUI 图标显示',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 注册 5G 但图标不显示 | NR state、config key、DisplayInfo | 先区分真实 NR 和 UI 显示策略 |',
      '| LTE 显示 4G/4G+ 不符 | CarrierConfig、CA/physical channel | 图标策略不等于 RAT 注册失败 |'
    ))
  },
  @{
    Name = '卫星通信配置.md'
    Path = '60_Configuration/Business-Config/卫星通信配置.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 配置来源',
      '',
      '| 来源 | 本文落点 | 运行时验证 |',
      '|---|---|---|',
      '| Feature flag / resource | Satellite telephony 开关、国家/运营商限制 | feature dump、Settings 可见性 |',
      '| CarrierConfig / config updater | 卫星接入控制、国家码、S2 cell 文件 | `dumpsys carrier_config`、satellite service log |',
      '| modem / radio capability | modem 是否支持 satellite radio 能力 | radio HAL / modem capability log |',
      '',
      '### 匹配与生效链路',
      '',
      '```text',
      'feature flag / resource / carrier config',
      '-> SatelliteAccessController / telephony service',
      '-> modem capability / region restriction',
      '-> UI 和接入行为',
      '```',
      '',
      '### 常见失败模式',
      '',
      '| 现象 | 优先检查 | 第一坏点判断 |',
      '|---|---|---|',
      '| 菜单不可见 | feature flag、device capability、country/carrier 限制 | UI 不显示不一定是 modem 不支持 |',
      '| 配置已下发但不可用 | access control、区域文件、modem capability | 先区分门控和无线能力 |'
    ))
  },
  @{
    Name = '配置与客户定制.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 使用边界',
      '',
      '| 模板项 | 本文角色 |',
      '|---|---|',
      '| 配置来源 | 只做总入口，具体来源放到 APN / ECC / CarrierConfig / NV 等专题 |',
      '| 匹配与生效链路 | 只给判断顺序，不展开字段细节 |',
      '| 平台差异 | 链接到具体配置方法和 Platform-Code |',
      '| 验证命令与 log | 链接到具体专题，不在总入口重复维护 |',
      '',
      '### 入口判断',
      '',
      '```text',
      '先判断问题属于 APN / ECC / NV / CarrierConfig / IMS / SMS / SIMLock / 运营商名',
      '-> 进入对应配置方法',
      '-> 按源配置、运行时 dump、AP/vendor 下发、modem/协议采用四步验证',
      '```'
    ))
  },
  @{
    Name = '运营商应答资料索引.md'
    Block = (Join-Lines -Lines @(
      '## 模板化定位',
      '',
      '### 使用边界',
      '',
      '| 模板项 | 本文角色 |',
      '|---|---|',
      '| 配置来源 | 保存运营商需求 / 应答资料入口 |',
      '| 匹配与生效链路 | 不直接写生效链路，转到对应配置方法文档 |',
      '| 平台差异 | 只记录资料来源，平台实现放 APN / IMS / ECC / CarrierConfig 等专题 |',
      '| 验证命令与 log | 不在本索引维护，避免资料索引变成排障文档 |',
      '',
      '### 使用链路',
      '',
      '```text',
      '运营商资料',
      '-> 提取字段或需求',
      '-> 归入具体配置方法',
      '-> 用运行时 dump 和 log 验证是否生效',
      '```'
    ))
  }
)

foreach ($doc in $docs) {
  Update-ConfigDoc -Name $doc.Name -Path $doc.Path -Block $doc.Block
}

Write-Host "Configuration docs normalized: $($docs.Count)"
