#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 normIds 获取脚本
复用通用工具获取接口结果
"""
import json
from api_utils import call_api_with_curl
from user_send_sms_complete import get_auth_token
from sendSms_params_final import aes_encrypt

def load_cookies_from_file(cookie_file):
    """加载 cookie 文件"""
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookie_data = json.load(f)
    
    # 转换为字典格式
    if isinstance(cookie_data, list):
        return {item['name']: item['value'] for item in cookie_data}
    return cookie_data

def get_normids(product_code, cookies_dict, authorization):
    """
    获取产品的 normIds
    
    Args:
        product_code: 产品代码
        cookies_dict: Cookie字典
        authorization: 授权token
        
    Returns:
        normIds字符串（逗号分隔）
    """
    url = "https://wx.10086.cn/website/nrapigate/nrmix/product/prodWithNormList"
    
    # 构建请求参数
    params = {"productCode": str(product_code)}
    encrypted_body = aes_encrypt(json.dumps(params, separators=(',', ':')))
    
    print(f"\n[INFO] 获取产品 {product_code} 的 normIds...")
    
    # 请求头
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
    
    # 调用 API
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] API 调用失败: {response['error']}")
        return None
    
    # 保存完整响应用于分析
    with open('normids_response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 完整响应已保存到 normids_response.json")
    
    # 提取 normIds
    if response.get('returnCode') != '0':
        print(f"[ERROR] API 返回错误: {response.get('returnMessage')}")
        return None
    
    data = response.get('data', {})
    
    # 查找包含 norm 的字段
    normids = []
    for key in data.keys():
        if 'norm' in key.lower() and isinstance(data[key], list):
            print(f"[INFO] 发现字段: {key}, 包含 {len(data[key])} 个元素")
            
            if data[key]:
                first_item = data[key][0]
                print(f"[INFO] 元素的键: {list(first_item.keys())}")
                
                # 尝试提取 normId
                if 'normId' in first_item:
                    normids = [str(item['normId']) for item in data[key]]
                    break
                elif 'id' in first_item:
                    normids = [str(item['id']) for item in data[key]]
                    break
    
    if normids:
        return ','.join(normids)
    
    print("[ERROR] 未能从响应中提取 normIds")
    print(f"[DEBUG] data 的键: {list(data.keys())}")
    return None


if __name__ == "__main__":
    print("=" * 80)
    print("获取产品 normIds")
    print("=" * 80)
    
    # 读取 user2 的 cookies
    cookies = load_cookies_from_file('user2/cooike_user2.json')
    if not cookies:
        print("[ERROR] 无法加载 cookies")
        exit(1)
    
    print("[SUCCESS] 成功加载 user2 的 cookies")
    
    # 获取 token
    token, user_info = get_auth_token(cookies)
    
    if not token:
        print("\n[ERROR] 无法获取 token")
        exit(1)
    
    # 测试两个产品
    test_products = [
        {"code": "1087078", "name": "29元套餐（云南）", "expected": "2258951,2258995"},
        {"code": "10715220", "name": "399元融合套餐（5G-A版）", "expected": "2259167,2259177"},
    ]
    
    print("\n" + "=" * 80)
    print("测试获取 normIds")
    print("=" * 80)
    
    for product in test_products:
        print(f"\n{'='*80}")
        print(f"产品: {product['name']}")
        print(f"产品代码: {product['code']}")
        print(f"预期 normIds: {product['expected']}")
        print("="*80)
        
        normids = get_normids(product['code'], cookies, token)
        
        if normids:
            print(f"\n[SUCCESS] 获取到的 normIds: {normids}")
            print(f"[VERIFY] 预期: {product['expected']}")
            
            if normids == product['expected']:
                print("[MATCH] ✓ 完全匹配!")
            else:
                print("[WARNING] ✗ 与预期不匹配")
        else:
            print("\n[FAILED] 未能获取 normIds")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)

