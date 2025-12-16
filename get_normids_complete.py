#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的 normIds 获取工具
包含自动获取 token 和提取 normIds 的完整流程
"""
import json
import subprocess
import sys
import os
from sendSms_params_final import aes_encrypt, aes_decrypt


def call_api_with_curl(url, encrypted_body, headers, cookies_dict):
    """
    使用 curl 调用 API（解决 OpenSSL 3.0 SSL 握手问题）
    
    Args:
        url: API URL
        encrypted_body: 加密的请求体
        headers: 请求头字典
        cookies_dict: Cookie字典
        
    Returns:
        解密后的响应JSON
    """
    # 构建 cookie 字符串
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    
    # 构建 curl 命令
    curl_cmd = ["curl", "-X", "POST", url]
    
    # 添加请求头
    for key, value in headers.items():
        curl_cmd.extend(["-H", f"{key}: {value}"])
    
    # 添加 cookie
    curl_cmd.extend(["-H", f"cookie: {cookie_str}"])
    
    # 添加请求体
    curl_cmd.extend(["-d", encrypted_body])
    
    # SSL 相关选项
    curl_cmd.extend(["-k", "--compressed"])
    
    # 调试：打印 curl 命令（可选）
    # print(f"[DEBUG] curl 命令: {' '.join(curl_cmd[:5])}... (共{len(curl_cmd)}个参数)")
    
    try:
        # 执行 curl 命令
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore',
            timeout=30
        )
        
        # 调试：打印原始输出（前500字符）
        if result.stdout:
            pass  # print(f"[DEBUG] curl stdout前500字符: {result.stdout[:500]}")
        if result.stderr:
            pass  # print(f"[DEBUG] curl stderr: {result.stderr[:200]}")
        
        if result.returncode != 0:
            return {
                'error': f"curl 命令执行失败: {result.stderr}",
                'error_type': 'curl_failed'
            }
        
        # 检查输出是否为空
        if not result.stdout or not result.stdout.strip():
            return {
                'error': f"curl 返回空响应。stderr: {result.stderr}",
                'error_type': 'empty_response'
            }
        
        # 解析响应
        try:
            response = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {
                'error': f"JSON 解析失败: {str(e)}",
                'error_type': 'json_decode_error',
                'raw_output': result.stdout[:500]
            }
        
        if 'body' in response:
            # 解密响应体
            encrypted_response = response['body']
            decrypted_response = aes_decrypt(encrypted_response)
            
            # 解析解密后的JSON
            response_data = json.loads(decrypted_response)
            
            return response_data
        else:
            # 可能是未加密的错误响应
            return response
            
    except subprocess.TimeoutExpired:
        return {
            'error': "请求超时",
            'error_type': 'timeout'
        }
    except Exception as e:
        return {
            'error': f"未知错误: {str(e)}",
            'error_type': 'unknown'
        }


def get_auth_token(cookies_dict, back_url="/website/businessPlatform/shopDetail"):
    """
    获取授权 token
    
    Args:
        cookies_dict: Cookie字典
        back_url: 返回URL
        
    Returns:
        token字符串或None
    """
    url = "https://wx.10086.cn/website/nrapigate/nrauth/auth/encryt/userAuth"
    
    # 构建请求参数
    params = {
        "backUrl": back_url
    }
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print("[INFO] 正在获取授权 token...")
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "channelid": "BUSINESS_H5",
        "chop-real-host": "wx.10086.cn",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://wx.10086.cn",
        "referer": "https://wx.10086.cn/website/businessPlatform/shopDetail",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] 获取 token 失败: {response['error']}")
        return None
    
    if response.get('returnCode') == '0' and 'data' in response:
        token = response['data'].get('token')
        if token:
            print(f"[SUCCESS] Token 获取成功: {token[:50]}...")
            return token
        else:
            print("[ERROR] 响应中未找到 token")
            return None
    else:
        print(f"[ERROR] Token 获取失败: {response.get('returnMessage', 'Unknown error')}")
        return None


def get_normids_from_api(product_code, cookies_dict, authorization):
    """
    调用 prodWithNormList 接口获取产品的 normIds
    
    Args:
        product_code: 产品代码
        cookies_dict: Cookie字典
        authorization: 授权token
        
    Returns:
        normIds字符串（逗号分隔）或None
    """
    url = "https://wx.10086.cn/website/nrapigate/nrmix/product/prodWithNormList"
    
    # 构建请求参数
    params = {
        "productCode": str(product_code)
    }
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"\n[INFO] 正在获取产品 {product_code} 的规格信息...")
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": authorization,
        "cache-control": "no-cache",
        "channelid": "BUSINESS_H5",
        "chop-real-host": "wx.10086.cn",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://wx.10086.cn",
        "referer": f"https://wx.10086.cn/website/businessPlatform/shopDetail?productCode={product_code}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] API 调用失败: {response['error']}")
        return None
    
    # 提取 normIds
    normids = extract_normids_from_response(response)
    
    return normids


def extract_normids_from_response(response_data):
    """
    从响应数据中提取 normIds
    
    Args:
        response_data: API响应数据
        
    Returns:
        normIds字符串（逗号分隔）或None
    """
    normids = []
    
    try:
        if response_data.get('returnCode') != '0':
            print(f"[ERROR] API返回错误: {response_data.get('returnMessage', 'Unknown error')}")
            return None
        
        if 'data' not in response_data:
            print("[ERROR] 响应中没有 data 字段")
            return None
        
        data = response_data['data']
        
        # 尝试不同的可能路径
        norm_sources = [
            ('norms', 'normId'),
            ('normList', 'normId'),
            ('prodNormList', 'normId'),
            ('norms', 'id'),
            ('normList', 'id'),
        ]
        
        for list_key, id_key in norm_sources:
            if list_key in data and isinstance(data[list_key], list):
                for norm in data[list_key]:
                    if id_key in norm:
                        normids.append(str(norm[id_key]))
                
                if normids:
                    print(f"[SUCCESS] 从 data.{list_key}[].{id_key} 提取到 {len(normids)} 个规格ID")
                    break
        
        # 如果还是没找到，尝试打印数据结构帮助调试
        if not normids:
            print("[DEBUG] 未找到标准的 normIds 路径，尝试分析响应结构...")
            print(f"[DEBUG] data 的键: {list(data.keys())}")
            
            # 尝试查找任何包含 "norm" 的字段
            for key in data.keys():
                if 'norm' in key.lower() and isinstance(data[key], list):
                    print(f"[DEBUG] 发现可能的字段: {key}")
                    if data[key]:
                        print(f"[DEBUG] 第一个元素的键: {list(data[key][0].keys()) if data[key] else 'empty'}")
        
    except Exception as e:
        print(f"[ERROR] 提取 normIds 失败: {e}")
        import traceback
        traceback.print_exc()
    
    if normids:
        return ','.join(normids)
    return None


def load_cookies(cookie_file):
    """
    加载 cookie 文件
    
    Args:
        cookie_file: cookie 文件路径
        
    Returns:
        cookie 字典
    """
    if not os.path.exists(cookie_file):
        print(f"[ERROR] Cookie文件不存在: {cookie_file}")
        return None
    
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookie_data = json.load(f)
    
    # 转换为字典格式
    if isinstance(cookie_data, list):
        cookies = {item['name']: item['value'] for item in cookie_data}
    else:
        cookies = cookie_data
    
    return cookies


if __name__ == "__main__":
    print("=" * 80)
    print("完整的 normIds 获取工具")
    print("=" * 80)
    
    # 用户选择
    user = input("\n使用哪个用户的 cookie？(user1/user2，默认 user1): ").strip() or "user1"
    
    # 加载 cookies
    cookie_file = f"{user}/cooike_{user}.json"
    cookies = load_cookies(cookie_file)
    
    if not cookies:
        sys.exit(1)
    
    print(f"[SUCCESS] 成功加载 {user} 的 cookies")
    
    # 获取 token
    authorization = get_auth_token(cookies)
    
    if not authorization:
        print("\n[ERROR] 无法获取授权 token，退出")
        sys.exit(1)
    
    # 保存 token
    token_file = f"{user}/token_{user}.txt"
    with open(token_file, 'w', encoding='utf-8') as f:
        f.write(authorization)
    print(f"[INFO] Token 已保存到 {token_file}")
    
    # 测试产品列表
    test_products = [
        {"code": "1087078", "name": "升档流量大促活动-29套餐（云南）", "expected": "2258951,2258995"},
        {"code": "10715220", "name": "升档流量大促活动-399融合套餐（5G-A版）", "expected": "2259167,2259177"},
    ]
    
    print("\n" + "=" * 80)
    print("开始测试获取 normIds")
    print("=" * 80)
    
    for product in test_products:
        print(f"\n{'=' * 80}")
        print(f"产品: {product['name']}")
        print(f"产品代码: {product['code']}")
        print(f"预期 normIds: {product['expected']}")
        print("=" * 80)
        
        normids = get_normids_from_api(product['code'], cookies, authorization)
        
        if normids:
            print(f"\n[RESULT] 获取到的 normIds: {normids}")
            print(f"[VERIFY] 预期: {product['expected']}")
            
            if normids == product['expected']:
                print("[SUCCESS] ✓ 匹配成功！")
            else:
                print("[WARNING] ✗ 与预期不匹配")
        else:
            print("\n[FAILED] 未能获取 normIds")
        
        print()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

