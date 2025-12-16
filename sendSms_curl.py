#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 curl 发送 sendSms 请求（解决 OpenSSL 3.0 SSL 握手问题）
"""
import json
import subprocess
import sys
from sendSms_params_final import aes_encrypt, aes_decrypt

def call_sendSms_api_curl(encrypted_body, authorization, cookies_dict):
    """
    使用 curl 调用 sendSms 接口
    
    Args:
        encrypted_body: 加密的请求体
        authorization: 授权token
        cookies_dict: Cookie字典
        
    Returns:
        解密后的响应JSON
    """
    url = "https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms"
    
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
        "-H", 'sec-ch-ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", 'sec-ch-ua-platform: "Windows"',
        "-H", "sec-fetch-dest: empty",
        "-H", "sec-fetch-mode: cors",
        "-H", "sec-fetch-site: same-origin",
        "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "-H", "x-app-version: 1.0.1",
        "-H", "x-center-env: 1",
        "-H", "x-requested-with: XMLHttpRequest",
        "-H", f"cookie: {cookie_str}",
        "-d", encrypted_body,
        "-k",  # 忽略SSL证书验证
        "--compressed"
    ]
    
    try:
        # 执行 curl 命令
        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            return {
                "error": f"Curl failed: {result.stderr}",
                "error_type": "CurlError",
                "returncode": result.returncode
            }
        
        # 解析响应
        response_json = json.loads(result.stdout)
        encrypted_response = response_json.get("body", "")
        
        if encrypted_response:
            # 解密响应
            decrypted_response = aes_decrypt(encrypted_response)
            return json.loads(decrypted_response)
        else:
            return response_json
    
    except subprocess.TimeoutExpired:
        return {"error": "Request timeout", "error_type": "TimeoutError"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {str(e)}", "error_type": "JSONDecodeError", "raw_output": result.stdout[:500]}
    except Exception as e:
        return {"error": str(e), "error_type": type(e).__name__}


if __name__ == "__main__":
    # 读取 user2 的 cookie
    with open('user2/cooike_user2.json', 'r', encoding='utf-8') as f:
        cookies_list = json.load(f)
    
    # 转换为字典格式
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    
    print("=" * 80)
    print("使用 Curl 调用 sendSms 接口 (User2)")
    print("=" * 80)
    print(f"shareToken: {cookies_dict.get('shareToken', 'N/A')[:50]}...")
    print(f"riskToken: {cookies_dict.get('riskToken', 'N/A')}")
    print(f"uuid: {cookies_dict.get('uuid', 'N/A')}")
    
    # 读取已保存的 token
    try:
        with open('user2/token_user2.txt', 'r', encoding='utf-8') as f:
            authorization = f.read().strip()
        print(f"Authorization: {authorization[:50]}...")
    except FileNotFoundError:
        print("[ERROR] 请先运行 get_auth_token.py 获取 token")
        sys.exit(1)
    
    # 构建请求参数
    params = {
        "busiId": "2",
        "normIds": "2259177",
        "userEffectType": "Type_Default"
    }
    
    print(f"\n请求参数:")
    print(json.dumps(params, indent=2, ensure_ascii=False))
    
    # 加密
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"\n加密后的请求体:")
    print(encrypted_body)
    
    print("\n" + "=" * 80)
    print("发送请求...")
    print("=" * 80)
    
    # 调用接口
    response = call_sendSms_api_curl(encrypted_body, authorization, cookies_dict)
    
    print(f"\n响应结果:")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    if 'error' not in response:
        if response.get('returnCode') == '0':
            print("\n[SUCCESS] 验证码发送成功！")
            print(f"状态: {response.get('data', {}).get('status')}")
            print(f"消息: {response.get('data', {}).get('message')}")
        else:
            print(f"\n[FAILED] 验证码发送失败")
            print(f"错误代码: {response.get('returnCode')}")
            print(f"错误消息: {response.get('returnMessage', 'Unknown error')}")
    else:
        print(f"\n[ERROR] 请求出错")
        print(f"错误类型: {response.get('error_type', 'Unknown')}")
        print(f"错误详情: {response['error'][:200] if 'error' in response else 'Unknown'}")

