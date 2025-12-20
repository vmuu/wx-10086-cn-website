#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取产品的 normIds
通过 productCode 调用 prodWithNormList 接口
"""
import json
import subprocess
import sys
from sendSms_params_final import aes_encrypt, aes_decrypt


def get_normids_with_curl(product_code, cookies_dict, authorization):
    """
    使用 curl 调用 prodWithNormList 接口获取产品的 normIds
    
    Args:
        product_code: 产品代码
        cookies_dict: Cookie字典
        authorization: 授权token
        
    Returns:
        normIds列表或None
    """
    url = "https://wx.10086.cn/website/nrapigate/nrmix/product/prodWithNormList"
    
    # 构建请求参数
    params = {
        "productCode": str(product_code)
    }
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"[INFO] 请求参数: {json_str}")
    print(f"[INFO] 加密后: {encrypted_body}\n")
    
    # 构建 cookie 字符串
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    
    # 构建 curl 命令
    curl_cmd = [
        "curl",
        "-X", "POST",
        url,
        "-H", "accept: application/json, text/plain, */*",
        "-H", "accept-encoding: gzip, deflate, br, zstd",
        "-H", "accept-language: zh-CN,zh;q=0.9",
        "-H", f"authorization: {authorization}",
        "-H", "cache-control: no-cache",
        "-H", "channelid: BUSINESS_H5",
        "-H", "chop-real-host: wx.10086.cn",
        "-H", "content-type: application/json; charset=UTF-8",
        "-H", "origin: https://wx.10086.cn",
        "-H", "referer: https://wx.10086.cn/website/businessPlatform/shopDetail",
        "-H", f"cookie: {cookie_str}",
        "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-d", encrypted_body,
        "-k",
        "--compressed"
    ]
    
    try:
        # 执行 curl 命令
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return {
                'error': f"curl 命令执行失败: {result.stderr}",
                'error_type': 'curl_failed'
            }
        
        # 解析响应
        response = json.loads(result.stdout)
        
        if 'body' in response:
            # 解密响应体
            encrypted_response = response['body']
            decrypted_response = aes_decrypt(encrypted_response)
            
            # 解析解密后的JSON
            response_data = json.loads(decrypted_response)
            
            return response_data
        else:
            return {
                'error': f"响应格式不正确: {result.stdout}",
                'error_type': 'invalid_response'
            }
            
    except subprocess.TimeoutExpired:
        return {
            'error': "请求超时",
            'error_type': 'timeout'
        }
    except json.JSONDecodeError as e:
        return {
            'error': f"JSON解析失败: {str(e)}",
            'error_type': 'json_error',
            'raw_output': result.stdout if 'result' in locals() else 'N/A'
        }
    except Exception as e:
        return {
            'error': f"未知错误: {str(e)}",
            'error_type': 'unknown'
        }


def extract_normids(response_data):
    """
    从响应数据中提取 normIds
    
    Args:
        response_data: API响应数据
        
    Returns:
        normIds列表
    """
    normids = []
    
    try:
        # 根据实际的响应结构提取 normIds
        # 可能的路径：data.norms[].normId 或 data.normList[].normId
        
        if 'data' in response_data:
            data = response_data['data']
            
            # 尝试不同的可能路径
            if 'norms' in data and isinstance(data['norms'], list):
                normids = [str(norm['normId']) for norm in data['norms'] if 'normId' in norm]
            elif 'normList' in data and isinstance(data['normList'], list):
                normids = [str(norm['normId']) for norm in data['normList'] if 'normId' in norm]
            elif 'prodNormList' in data and isinstance(data['prodNormList'], list):
                normids = [str(norm['normId']) for norm in data['prodNormList'] if 'normId' in norm]
            
            # 如果以上都没找到，打印数据结构帮助调试
            if not normids:
                print("[DEBUG] 响应数据结构:")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
                
    except Exception as e:
        print(f"[ERROR] 提取 normIds 失败: {e}")
    
    return normids


if __name__ == "__main__":
    # 测试：获取产品2的 normIds
    import os
    
    # 读取 user1 的 cookies
    cookie_file = "user1/cooike_user1.json"
    if not os.path.exists(cookie_file):
        print(f"[ERROR] Cookie文件不存在: {cookie_file}")
        sys.exit(1)
    
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookie_list = json.load(f)
    
    # 转换为字典格式
    if isinstance(cookie_list, list):
        cookies = {item['name']: item['value'] for item in cookie_list}
    else:
        cookies = cookie_list
    
    # 读取 token
    token_file = "user1/token_user1.txt"
    if not os.path.exists(token_file):
        print("[INFO] token文件不存在，尝试获取新token...")
        # 这里可以调用 get_auth_token.py
        print("[ERROR] 请先运行 get_auth_token.py 获取 user1 的 token")
        sys.exit(1)
    
    with open(token_file, 'r', encoding='utf-8') as f:
        authorization = f.read().strip()
    
    print("=" * 80)
    print("测试获取产品的 normIds")
    print("=" * 80)
    
    # 测试产品2 (云南29元套餐)
    product_code = "1087078"
    print(f"\n产品代码: {product_code}")
    print(f"产品名称: 升档流量大促活动-29套餐（云南）\n")
    
    response = get_normids_with_curl(product_code, cookies, authorization)
    
    if 'error' in response:
        print(f"[ERROR] 请求失败")
        print(f"错误类型: {response.get('error_type')}")
        print(f"错误信息: {response['error']}")
    else:
        print("[SUCCESS] 成功获取产品信息\n")
        
        # 提取 normIds
        normids = extract_normids(response)
        
        if normids:
            print(f"找到 {len(normids)} 个规格ID:")
            for i, normid in enumerate(normids, 1):
                print(f"  {i}. normId = {normid}")
            
            print(f"\nsendSms 参数中的 normIds: \"{','.join(normids)}\"")
            
            # 验证是否与之前抓包的一致
            expected_normids = "2258951,2258995"
            actual_normids = ",".join(normids)
            
            print(f"\n验证:")
            print(f"  预期值: {expected_normids}")
            print(f"  实际值: {actual_normids}")
            print(f"  匹配: {'✓ 一致' if actual_normids == expected_normids else '✗ 不一致'}")
        else:
            print("[WARNING] 未能提取到 normIds")
            print("响应数据结构可能与预期不同，需要调整提取逻辑")

