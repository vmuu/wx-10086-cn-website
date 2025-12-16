#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 norm 接口获取 normIds
"""
import json
from sendSms_params_final import aes_decrypt

print("=" * 80)
print("分析 /nrmix/product/norm 接口")
print("=" * 80)

# 产品2 (2170362) 的 norm 接口请求
encrypted_request = "2DDD190EA04BB94F6CDF2CFE14D2FB9193D9C4A72D061B94BD7DA97B22BCEB50"
encrypted_response_start = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FC9E7044AC1993CB8CAE5E9218DF524080A28D093B8D4DCCB24CCB7A1803497FA85877F2E13CC71CCCD2F9A46D9B9B8F384"

print("\n加密的请求体:")
print(encrypted_request)

print("\n解密后的请求参数:")
try:
    decrypted_request = aes_decrypt(encrypted_request)
    print(decrypted_request)
    request_params = json.loads(decrypted_request)
    print(json.dumps(request_params, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"解密请求失败: {e}")

print("\n" + "=" * 80)
print("关键发现:")
print("=" * 80)
print("""
/nrmix/product/norm 接口:
  - 这个接口用于获取**单个**规格的详细信息
  - 请求参数: {"normId": 规格ID}
  - 响应包含该规格的详细信息
""")

print("\n" + "=" * 80)
print("分析 /nrproduct/atom/norm/normList 接口")
print("=" * 80)

# normList 接口请求
encrypted_request_list = "28F122CBF4F8B2F80F63716ADE5E2B8EE815DC83062B29727CE8BEA1B84BDA2F"
encrypted_response_list_start = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4DB9AFD0A2775426F2412E90DB1DF66B8D73A689347F0156A55726C10E94EEC0871021164C164D0062DC7844E837F12C9F269C3230B73811E2DE064AE8416FCF"

print("\n加密的请求体:")
print(encrypted_request_list)

print("\n解密后的请求参数:")
try:
    decrypted_request_list = aes_decrypt(encrypted_request_list)
    print(decrypted_request_list)
    request_params_list = json.loads(decrypted_request_list)
    print(json.dumps(request_params_list, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"解密请求失败: {e}")

print("\n加密的响应体开头:")
print(encrypted_response_list_start + "...")

print("""
说明: 响应体太长，无法完整显示，但我们可以尝试解密开头部分
""")

