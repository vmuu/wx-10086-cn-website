#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 sendSms 接口的请求参数
"""
import json
from sendSms_params_final import aes_decrypt

print("=" * 80)
print("分析 sendSms 请求参数")
print("=" * 80)

# 产品1: productId=2170496&productCode=10715220
print("\n【产品1】升档流量大促活动-399融合套餐（5G-A版）")
print("URL: https://wx.10086.cn/website/businessPlatform/shopDetail?productId=2170496&productCode=10715220")

encrypted_request_1 = "4CAEE24050ECAB62FA24F7D065554488D9BF553FC0DA5A6B1851D4D71249F6CFD6B99C65703EF89A702C819A387E24AE"
encrypted_response_1 = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FCA30824A171BEF67046BB64F30D194C14D3F606879007E983FCF9A1827654797B049FC155A7891F7E951475A48DB3C084D5FCA01281CDB650C908B89E3D258E1B"

print("\n加密的请求体:")
print(encrypted_request_1)

print("\n解密后的请求参数:")
decrypted_request_1 = aes_decrypt(encrypted_request_1)
print(decrypted_request_1)
params_1 = json.loads(decrypted_request_1)
print(json.dumps(params_1, indent=2, ensure_ascii=False))

print("\n加密的响应体:")
print(encrypted_response_1)

print("\n解密后的响应:")
decrypted_response_1 = aes_decrypt(encrypted_response_1)
print(decrypted_response_1)
response_1 = json.loads(decrypted_response_1)
print(json.dumps(response_1, indent=2, ensure_ascii=False))

print("\n" + "=" * 80)
print("参数分析总结")
print("=" * 80)
print(f"""
产品信息:
  - productId: 2170496
  - productCode: 10715220
  - 产品名称: 升档流量大促活动-399融合套餐（5G-A版）

sendSms 参数:
  - busiId: {params_1.get('busiId')}
  - normIds: {params_1.get('normIds')}
  - userEffectType: {params_1.get('userEffectType')}

响应结果:
  - returnCode: {response_1.get('returnCode')}
  - returnMessage: {response_1.get('returnMessage')}
  - status: {response_1.get('data', {}).get('status')}
  - message: {response_1.get('data', {}).get('message')}
""")

print("\n" + "=" * 80)
print("=" * 80)

# 产品2: productId=2170362&productCode=1087078
print("\n【产品2】升档流量大促活动-29套餐（云南）")
print("URL: https://wx.10086.cn/website/businessPlatform/shopDetail?productId=2170362&productCode=1087078")

encrypted_request_2 = "4CAEE24050ECAB62FA24F7D065554488B2EBC7152D77E178673970D0FD843E19DE05853C08868BF141FE75CD903F4738"
encrypted_response_2 = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FCA30824A171BEF67046BB64F30D194C14D3F606879007E983FCF9A1827654797B049FC155A7891F7E951475A48DB3C084D5FCA01281CDB650C908B89E3D258E1B"

print("\n加密的请求体:")
print(encrypted_request_2)

print("\n解密后的请求参数:")
decrypted_request_2 = aes_decrypt(encrypted_request_2)
print(decrypted_request_2)
params_2 = json.loads(decrypted_request_2)
print(json.dumps(params_2, indent=2, ensure_ascii=False))

print("\n加密的响应体:")
print(encrypted_response_2)

print("\n解密后的响应:")
decrypted_response_2 = aes_decrypt(encrypted_response_2)
print(decrypted_response_2)
response_2 = json.loads(decrypted_response_2)
print(json.dumps(response_2, indent=2, ensure_ascii=False))

print("\n" + "=" * 80)
print("参数分析总结")
print("=" * 80)
print(f"""
产品信息:
  - productId: 2170362
  - productCode: 1087078
  - 产品名称: 升档流量大促活动-29套餐（云南）

sendSms 参数:
  - busiId: {params_2.get('busiId')}
  - normIds: {params_2.get('normIds')}
  - userEffectType: {params_2.get('userEffectType')}

响应结果:
  - returnCode: {response_2.get('returnCode')}
  - returnMessage: {response_2.get('returnMessage')}
  - status: {response_2.get('data', {}).get('status')}
  - message: {response_2.get('data', {}).get('message')}
""")

print("\n" + "=" * 80)
print("两个产品的对比")
print("=" * 80)
print(f"""
【产品1】 升档流量大促活动-399融合套餐（5G-A版）
  - busiId: {params_1.get('busiId')}
  - normIds: {params_1.get('normIds')}
  - 规格数量: {len(params_1.get('normIds', '').split(','))}

【产品2】 升档流量大促活动-29套餐（云南）
  - busiId: {params_2.get('busiId')}
  - normIds: {params_2.get('normIds')}
  - 规格数量: {len(params_2.get('normIds', '').split(','))}

共同点:
  - 都是 busiId = "2"
  - 都没有 userEffectType 字段
  - normIds 格式相同（逗号分隔的规格ID列表）

不同点:
  - normIds 的具体值不同（不同产品有不同的规格ID）
""")

