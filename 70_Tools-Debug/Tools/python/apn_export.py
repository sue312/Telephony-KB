#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APN表格转apns-conf.xml工具
遵循规则：
1. 空参数忽略
2. 一行对应一条<apn>配置
3. 字段映射/特殊值转换
4. 格式严格匹配示例（缩进、换行）
"""

import pandas as pd
import os
from typing import Dict, Optional

# ===================== 核心配置 =====================
# 规则3：字段映射表
FIELD_MAPPING = {
    'Carrier': 'carrier',
    'MCC': 'mcc',
    'MNC': 'mnc',
    'APN': 'apn',
    'Type': 'type',
    'Proxy': 'proxy',
    'Port': 'port',
    'Mmsc': 'mmsc',
    'Mmsproxy': 'mmsproxy',
    'Mmsport': 'mmsport',
    'User': 'user',
    'Password': 'password',
    'Protocol': 'protocol',
    'Roaming Protocol': 'roaming_protocol',
    'Mvno Type': 'mvno_type',
    'Mvno Match Data': 'mvno_match_data',
    'Bearer Bitmask': 'bearer_bitmask',
    'MTU': 'mtu',
    'Authentication Type': 'authtype'
}

# 规则6：Authentication Type -> authtype映射
AUTHTYPE_MAPPING = {
    'NULL': None,       # 不配置该属性
    'None': '0',
    'PAP': '1',
    'CHAP': '2',
    'PAP or CHAP': '3'
}

# 规则4：V & E -> user_visible/user_editable映射
VE_MAPPING = {
    'Visible & Editable': {'user_visible': 'true', 'user_editable': 'true'},
    'Visible & Uneditable': {'user_visible': 'true', 'user_editable': 'false'},
    'Invisible & Editable': {'user_visible': 'false', 'user_editable': 'true'},
    'Invisible & Uneditable': {'user_visible': 'false', 'user_editable': 'false'}
}

# XML基础配置
XML_VERSION = "8"
INDENT = "    "          # 缩进符（制表符）
LINE_BREAK = "\n"      # 换行符


# ===================== 核心函数 =====================
def is_empty(value) -> bool:
    """判断值是否为空（处理NaN、空字符串、None等）"""
    if pd.isna(value):
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    if value is None:
        return True
    return False


def format_mcc_mnc(value: str, length: int) -> str:
    """
    格式化MCC/MNC，确保保留前导0（规则7）
    :param value: 原始值
    :param length: 目标长度（MCC=3，MNC=2）
    :return: 补零后的字符串
    """
    if is_empty(value):
        return ""
    # 转字符串并去除非数字字符（防止表格中的格式问题）
    str_val = str(value).strip().replace(" ", "")
    # 补前导0到指定长度
    return str_val.zfill(length)


def process_row(row: pd.Series) -> str:
    """
    处理单行数据，生成<apn>标签字符串
    :param row: 表格单行数据
    :return: 格式化的apn标签字符串
    """
    # 存储要生成的属性键值对
    apn_attrs = []
    
    # 1. 处理基础字段（FIELD_MAPPING中的字段）
    for excel_col, xml_attr in FIELD_MAPPING.items():
        # 跳过不存在的列
        if excel_col not in row.index:
            continue
        
        value = row[excel_col]
        
        # 空值忽略（规则1）
        if is_empty(value):
            continue
        
        # 特殊处理MCC/MNC（保留前导0）
        if xml_attr == 'mcc':
            formatted_val = format_mcc_mnc(value, 3)
        elif xml_attr == 'mnc':
            formatted_val = format_mcc_mnc(value, 2)
        # 特殊处理authtype（规则6）
        elif xml_attr == 'authtype':
            str_val = str(value).strip()
            formatted_val = AUTHTYPE_MAPPING.get(str_val, None)
            # authtype为NULL则跳过
            if formatted_val is None:
                continue
        # 其他字段直接使用原始值
        else:
            formatted_val = str(value).strip()
        
        # 添加属性（格式：\t属性名="值"）
        formatted_val = (formatted_val
                         .replace('&', '&amp;')
                         .replace('"', '&quot;')
                         .replace('<', '&lt;')
                         .replace('>', '&gt;'))
        apn_attrs.append(f"{INDENT}{INDENT}{xml_attr}=\"{formatted_val}\"")
    
    # 2. 处理V & E字段（生成user_visible/user_editable）
    if 'V & E' in row.index and not is_empty(row['V & E']):
        ve_value = row['V & E'].strip()
        if ve_value in VE_MAPPING:
            for attr, val in VE_MAPPING[ve_value].items():
                apn_attrs.append(f"{INDENT}{INDENT}{attr}=\"{val}\"")
    
    # 3. 构建<apn>标签
    if not apn_attrs:  # 无有效属性时跳过该行
        return ""
    
    # 拼接属性（每行一个属性）
    attrs_str = LINE_BREAK.join(apn_attrs)
    # 完整的apn标签
    apn_tag = (
        f"{INDENT}<apn{LINE_BREAK}"
        f"{attrs_str}{LINE_BREAK}"
        f"{INDENT}/>"
    )
    
    return apn_tag


def convert_excel_to_apns_xml(excel_path: str, output_path: str = "apns-conf.xml") -> None:
    """
    将Excel表格转换为apns-conf.xml
    :param excel_path: 输入Excel文件路径
    :param output_path: 输出XML文件路径
    """
    # 1. 读取Excel文件（支持xlsx/xls，自动读取第一个sheet）
    print(f"正在读取Excel文件: {excel_path}")
    try:
        df = pd.read_excel(excel_path, dtype=str)  # 强制按字符串读取，防止前导0丢失
        print(f"成功读取 {len(df)} 行数据")
    except Exception as e:
        print(f"读取Excel失败: {e}")
        return
    
    # 2. 处理每一行数据
    print("开始处理数据...")
    apn_tags = []
    processed_rows = 0
    skipped_rows = 0
    
    for idx, row in df.iterrows():
        apn_tag = process_row(row)
        if apn_tag:
            apn_tags.append(apn_tag)
            processed_rows += 1
        else:
            skipped_rows += 1
        
        # 进度提示（每1000行输出一次）
        if (idx + 1) % 1000 == 0:
            print(f"已处理 {idx + 1}/{len(df)} 行")
    
    # 3. 构建完整XML内容
    xml_content = (
        f"<apns version=\"{XML_VERSION}\">{LINE_BREAK}"
        f"{LINE_BREAK.join(apn_tags)}{LINE_BREAK}"
        f"</apns>"
    )
    
    # 4. 写入文件
    print(f"开始写入XML文件: {output_path}")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print(f"写入完成！")
        print(f"统计信息：")
        print(f"  - 总行数：{len(df)}")
        print(f"  - 生成有效APN配置：{processed_rows}")
        print(f"  - 跳过空行/无效行：{skipped_rows}")
        print(f"  - 输出文件大小：{os.path.getsize(output_path) / 1024:.2f} KB")
    except Exception as e:
        print(f"写入文件失败: {e}")


# ===================== 执行入口 =====================
if __name__ == "__main__":
    # 配置输入输出路径（请根据实际情况修改）
    INPUT_EXCEL_PATH = "APN_list-2026-08-26 14_53_16.xls"  # 你的APN表格路径
    OUTPUT_XML_PATH = "apns-conf.xml"    # 输出XML路径
    
    # 检查输入文件是否存在
    if not os.path.exists(INPUT_EXCEL_PATH):
        print(f"错误：输入文件 {INPUT_EXCEL_PATH} 不存在！")
    else:
        # 执行转换
        convert_excel_to_apns_xml(INPUT_EXCEL_PATH, OUTPUT_XML_PATH)
