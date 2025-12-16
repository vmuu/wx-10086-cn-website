#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
寻找 normIds 的来源
分析 /nrmix/product/prodWithNormList 接口
"""
import json
from sendSms_params_final import aes_decrypt

print("=" * 80)
print("分析 /nrmix/product/prodWithNormList 接口")
print("=" * 80)
print("这个接口名称表示：产品及其规格列表")
print("应该就是获取 normIds 的源头！")

# 产品2 (2170362) 的 prodWithNormList 接口请求
encrypted_request = "A3C62A567EA655C567956961E1A25DF6BC3873EDA0B5A471D852C5402B1F1EE8"

print("\n加密的请求体:")
print(encrypted_request)

print("\n解密后的请求参数:")
try:
    decrypted_request = aes_decrypt(encrypted_request)
    print(decrypted_request)
    request_params = json.loads(decrypted_request)
    print("\n格式化后的请求参数:")
    print(json.dumps(request_params, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 80)
    print("关键发现!")
    print("=" * 80)
    print(f"""
请求参数分析:
  - productCode: {request_params.get('productCode')}
  - productId: {request_params.get('productId')}
  - 其他字段: {list(request_params.keys())}
  
结论:
  这个接口通过 productCode 和 productId 来获取产品的规格列表
  返回的响应中应该包含该产品的所有 normIds
""")
    
except Exception as e:
    print(f"解密请求失败: {e}")

# 响应太长，只解密前面一部分看看结构
print("\n" + "=" * 80)
print("响应体分析")
print("=" * 80)
print("响应体非常长，说明包含了大量的产品和规格信息")
print("我们需要在响应中找到 normIds 的位置")

