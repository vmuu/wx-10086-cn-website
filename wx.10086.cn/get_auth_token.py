#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取授权token的脚本
"""
import json
import subprocess
from sendSms_params_final import aes_encrypt, aes_decrypt

def get_auth_token_curl(cookies_dict, back_url="/website/businessPlatform/shopDetail"):
    """
    使用 curl 调用 userAuth 接口获取 token
    
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
        "-H", "cache-control: no-cache",
        "-H", "channelid: BUSINESS_H5",
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
            print(f"[ERROR] Curl failed: {result.stderr}")
            return None
        
        # 解析响应
        response_json = json.loads(result.stdout)
        encrypted_response = response_json.get("body", "")
        
        if encrypted_response:
            # 解密响应
            decrypted_response = aes_decrypt(encrypted_response)
            data = json.loads(decrypted_response)
            
            print(f"\n[DEBUG] userAuth 响应:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 提取 token
            if data.get('returnCode') == '0' and data.get('data'):
                token = data['data'].get('token')
                if token:
                    print(f"\n[SUCCESS] 成功获取 token:")
                    print(f"Token: {token}")
                    return token
                else:
                    print(f"\n[ERROR] 响应中没有 token")
                    return None
            else:
                print(f"\n[ERROR] 获取 token 失败:")
                print(f"返回码: {data.get('returnCode')}")
                print(f"返回消息: {data.get('returnMessage')}")
                return None
        else:
            print(f"\n[ERROR] 响应中没有加密的body")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            return None
    
    except subprocess.TimeoutExpired:
        print(f"\n[ERROR] Request timeout")
        return None
    except json.JSONDecodeError as e:
        print(f"\n[ERROR] JSON decode error: {str(e)}")
        print(f"Raw output: {result.stdout[:500]}")
        return None
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        return None


if __name__ == "__main__":
    # 读取 user2 的 cookie
    with open('user2/cooike_user2.json', 'r', encoding='utf-8') as f:
        cookies_list = json.load(f)
    
    # 转换为字典格式
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    
    print("=" * 80)
    print("获取 User2 的授权 Token")
    print("=" * 80)
    print(f"shareToken: {cookies_dict.get('shareToken', 'N/A')[:50]}...")
    print(f"uuid: {cookies_dict.get('uuid', 'N/A')}")
    
    # 获取 token
    token = get_auth_token_curl(cookies_dict)
    
    if token:
        # 保存 token 到文件
        token_file = 'user2/token_user2.txt'
        with open(token_file, 'w', encoding='utf-8') as f:
            f.write(token)
        print(f"\n[SUCCESS] Token 已保存到: {token_file}")
    else:
        print(f"\n[FAILED] 无法获取 token")

