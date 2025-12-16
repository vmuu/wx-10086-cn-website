#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取 normIds - 使用 user2 的方法
"""
import json
import subprocess
from sendSms_params_final import aes_encrypt, aes_decrypt

# 读取 user2 的 cookies
with open('user2/cooike_user2.json', 'r', encoding='utf-8') as f:
    cookie_data = json.load(f)

# 转换为字典格式
if isinstance(cookie_data, list):
    cookies = {item['name']: item['value'] for item in cookie_data}
else:
    cookies = cookie_data

print("=" * 80)
print("测试获取 product normIds")
print("=" * 80)

# 步骤1: 获取 token
print("\n[步骤1] 获取授权 token...")

url_auth = "https://wx.10086.cn/website/nrapigate/nrauth/auth/encryt/userAuth"
auth_params = {"backUrl": "/website/businessPlatform/shopDetail"}
encrypted_auth = aes_encrypt(json.dumps(auth_params, separators=(',', ':')))

cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

curl_auth = [
    "curl", "-s", "-X", "POST", url_auth,
    "-H", "accept: application/json, text/plain, */*",
    "-H", "accept-encoding: gzip, deflate, br, zstd",
    "-H", "accept-language: zh-CN,zh;q=0.9",
    "-H", "cache-control: no-cache",
    "-H", "channelid: BUSINESS_H5",
    "-H", "chop-real-host: wx.10086.cn",
    "-H", "content-type: application/json; charset=UTF-8",
    "-H", "origin: https://wx.10086.cn",
    "-H", "referer: https://wx.10086.cn/website/businessPlatform/shopDetail",
    "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "-H", f"cookie: {cookie_str}",
    "-d", encrypted_auth,
    "-k", "--compressed"
]

result_auth = subprocess.run(curl_auth, capture_output=True, text=True, encoding='utf-8', errors='ignore')
print(f"stdout[:200]: {result_auth.stdout[:200]}")
print(f"stderr[:200]: {result_auth.stderr[:200]}")

if result_auth.stdout:
    try:
        auth_response = json.loads(result_auth.stdout)
        if 'body' in auth_response:
            decrypted_auth = aes_decrypt(auth_response['body'])
            auth_data = json.loads(decrypted_auth)
            if auth_data.get('returnCode') == '0':
                token = auth_data['data']['token']
                print(f"[SUCCESS] Token: {token[:50]}...")
                
                # 保存 token
                with open('user2/token_user2.txt', 'w') as f:
                    f.write(token)
                
                # 步骤2: 获取 normIds
                print("\n[步骤2] 获取产品 normIds...")
                
                test_product_code = "1087078"  # 29元套餐
                url_norm = "https://wx.10086.cn/website/nrapigate/nrmix/product/prodWithNormList"
                norm_params = {"productCode": test_product_code}
                encrypted_norm = aes_encrypt(json.dumps(norm_params, separators=(',', ':')))
                
                curl_norm = [
                    "curl", "-X", "POST", url_norm,
                    "-H", "accept: application/json, text/plain, */*",
                    "-H", f"authorization: {token}",
                    "-H", "content-type: application/json; charset=UTF-8",
                    "-H", "channelid: BUSINESS_H5",
                    "-H", f"cookie: {cookie_str}",
                    "-d", encrypted_norm,
                    "-k", "--compressed"
                ]
                
                result_norm = subprocess.run(curl_norm, capture_output=True, text=True, encoding='utf-8', errors='ignore')
                
                if result_norm.stdout:
                    norm_response = json.loads(result_norm.stdout)
                    if 'body' in norm_response:
                        decrypted_norm = aes_decrypt(norm_response['body'])
                        
                        # 保存原始响应以便分析
                        with open('normids_response.json', 'w', encoding='utf-8') as f:
                            f.write(decrypted_norm)
                        
                        print(f"\n[INFO] 响应已保存到 normids_response.json")
                        print(f"响应前1000字符:\n{decrypted_norm[:1000]}")
                        
                        # 尝试解析
                        norm_data = json.loads(decrypted_norm)
                        print(f"\n[INFO] returnCode: {norm_data.get('returnCode')}")
                        print(f"[INFO] returnMessage: {norm_data.get('returnMessage')}")
                        
                        if 'data' in norm_data:
                            data_keys = list(norm_data['data'].keys())
                            print(f"[INFO] data 的键: {data_keys}")
                            
                            # 查找包含 norm 的字段
                            for key in data_keys:
                                if 'norm' in key.lower():
                                    value = norm_data['data'][key]
                                    if isinstance(value, list) and value:
                                        print(f"\n[INFO] 发现字段: {key}")
                                        print(f"[INFO] 列表长度: {len(value)}")
                                        print(f"[INFO] 第一个元素的键: {list(value[0].keys()) if value else 'empty'}")
                                        
                                        # 尝试提取 normId
                                        if 'normId' in value[0]:
                                            normids = [str(item['normId']) for item in value]
                                            normids_str = ','.join(normids)
                                            print(f"\n[SUCCESS] normIds: {normids_str}")
                                            print(f"[EXPECTED] 预期: 2258951,2258995")
                                            print(f"[MATCH] {'✓ 匹配' if normids_str == '2258951,2258995' else '✗ 不匹配'}")
                    else:
                        print(f"[ERROR] 无 body 字段: {result_norm.stdout[:500]}")
                else:
                    print(f"[ERROR] 无响应输出")
                    print(f"stderr: {result_norm.stderr[:500]}")
            else:
                print(f"[ERROR] Token获取失败: {auth_data}")
        else:
            print(f"[ERROR] 无 body 字段: {auth_response}")
    except Exception as e:
        print(f"[ERROR] 处理失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("[ERROR] 无响应")

