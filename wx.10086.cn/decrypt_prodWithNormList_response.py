#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解密浏览器捕获的 prodWithNormList 成功响应
"""
import json
from sendSms_params_final import aes_decrypt

print("=" * 80)
print("解密 prodWithNormList 的成功响应")
print("=" * 80)

# 从之前的分析脚本中，我们知道 reqid=390 的请求是 prodWithNormList
# 但响应很长，被截断了。让我从之前的输出中提取开头部分

# 产品2 (1087078) 的 prodWithNormList 响应（开头部分）
encrypted_response_start = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FC9E7044AC1993CB8CAE5E9218DF524080A28D093B8D4DCCB24CCB7A1803497FA85877F2E13CC71CCCD2F9A46D9B9B8F384"

print(f"\n加密内容（前{len(encrypted_response_start)}字符）:")
print(encrypted_response_start)

print("\n解密中...")

try:
    # AES加密通常是16字节的倍数，这个长度是128字节
    decrypted = aes_decrypt(encrypted_response_start)
    print("\n解密成功!")
    print(f"解密内容:\n{decrypted}")
    
    # 尝试解析 JSON
    try:
        data = json.loads(decrypted)
        print("\nJSON 解析成功!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 分析数据结构
        if 'data' in data:
            print("\n[分析] data 字段的键:")
            for key in data['data'].keys():
                value = data['data'][key]
                if isinstance(value, list):
                    print(f"  - {key}: 列表，长度={len(value)}")
                    if value and isinstance(value[0], dict):
                        print(f"    元素示例: {list(value[0].keys())}")
                elif isinstance(value, dict):
                    print(f"  - {key}: 对象，键={list(value.keys())}")
                else:
                    print(f"  - {key}: {type(value).__name__} = {value}")
    except json.JSONDecodeError as e:
        print(f"\nJSON解析失败: {e}")
        print("可能响应被截断了")
        
except Exception as e:
    print(f"\n解密失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("分析完成")
print("=" * 80)

