#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试解密实际捕获的 prodWithNormList 请求
"""
import json
from sendSms_params_final import aes_decrypt, aes_encrypt

print("=" * 80)
print("测试 prodWithNormList 接口的加密解密")
print("=" * 80)

# 从浏览器捕获的实际请求（产品2: 1087078）
encrypted_request_captured = "A3C62A567EA655C567956961E1A25DF6BC3873EDA0B5A471D852C5402B1F1EE8"

print("\n[1] 解密捕获的请求:")
print(f"加密内容: {encrypted_request_captured}")

decrypted = aes_decrypt(encrypted_request_captured)
print(f"解密结果: {decrypted}")

request_params = json.loads(decrypted)
print(f"解析后: {json.dumps(request_params, indent=2, ensure_ascii=False)}")

# 测试我们的加密
print("\n[2] 测试我们的加密:")
product_code = "1087078"
params = {"productCode": product_code}
json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
print(f"原始JSON: {json_str}")

encrypted = aes_encrypt(json_str)
print(f"加密结果: {encrypted}")

# 验证：解密我们自己加密的内容
decrypted_check = aes_decrypt(encrypted)
print(f"解密验证: {decrypted_check}")

print("\n[3] 对比:")
print(f"浏览器捕获: {encrypted_request_captured}")
print(f"我们生成的: {encrypted}")
print(f"是否相同: {encrypted == encrypted_request_captured}")

if encrypted != encrypted_request_captured:
    print("\n[分析] 加密结果不同，可能的原因:")
    print("1. JSON 格式化方式不同（空格、换行等）")
    print("2. 加密时使用的IV或padding不同")
    print("3. AES 加密每次生成的密文可能不同（如果使用随机IV）")
    
    # 尝试不同的格式
    print("\n[4] 尝试不同的JSON格式:")
    
    formats = [
        json.dumps(params, separators=(',', ':')),  # 无空格
        json.dumps(params, separators=(',', ':'), ensure_ascii=False),  # UTF-8
        json.dumps(params, separators=(', ', ': ')),  # 有空格
        json.dumps(params),  # 默认格式
    ]
    
    for i, fmt in enumerate(formats, 1):
        enc = aes_encrypt(fmt)
        print(f"  格式{i}: {fmt} -> {enc[:40]}...")
        if enc == encrypted_request_captured:
            print(f"  ✓ 匹配!")
else:
    print("\n✓ 加密结果完全相同!")

# 无论如何，我们的加密应该都能被服务器正确解密
print("\n[结论]")
print("即使加密结果不同，只要解密后的 JSON 内容相同，服务器就应该能正确处理")
print(f"我们的内容: {decrypted_check}")
print(f"浏览器的内容: {decrypted}")
print(f"内容是否相同: {decrypted_check == decrypted}")

