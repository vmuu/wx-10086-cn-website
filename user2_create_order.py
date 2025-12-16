#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User2 创建订单脚本
使用验证码调用 createOrder 接口
"""
import json
import subprocess
import sys
import os
from createOrder_params import generate_createOrder_params
from sendSms_params_final import aes_decrypt


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
    
    # 忽略SSL证书验证
    curl_cmd.extend(["-k", "--compressed"])
    
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


def create_order(authorization, cookies_dict, verify_code, norm_id=2259177, 
                product_id=2170506, product_code=10528470):
    """
    创建订单
    
    Args:
        authorization: 授权token
        cookies_dict: Cookie字典
        verify_code: 短信验证码
        norm_id: 规格ID
        product_id: 产品ID
        product_code: 产品代码
        
    Returns:
        响应JSON
    """
    print("\n" + "=" * 80)
    print("创建订单")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrmix/order/createOrder"
    
    # 获取 riskToken
    risk_token = cookies_dict.get('riskToken', '')
    
    print(f"\n订单信息:")
    print(f"  产品ID: {product_id}")
    print(f"  产品代码: {product_code}")
    print(f"  规格ID: {norm_id}")
    print(f"  验证码: {verify_code}")
    print(f"  风控Token: {risk_token}")
    
    # 生成加密的请求体
    encrypted_body, params = generate_createOrder_params(
        norm_id=norm_id,
        product_id=product_id,
        product_code=product_code,
        verify_code=verify_code,
        risk_token=risk_token,
        user_effect_type="Type_Default",
        order_type=1,
        order_resource=20,
        pt_id=200103516,
        sign_activity=False
    )
    
    print(f"\n请求参数（部分）:")
    important_params = {
        "normid": params["normid"],
        "productId": params["productId"],
        "productCode": params["productCode"],
        "password": params["password"],
        "verifyCode": params["verifyCode"],
        "cmgSmsCode": params["cmgSmsCode"],
        "token": params["token"],
        "confirmTime": params["confirmTime"],
        "timeSpan": params["timeSpan"],
        "userEffectType": params["userEffectType"]
    }
    print(json.dumps(important_params, indent=2, ensure_ascii=False))
    
    print(f"\n加密后的请求体 (前80字符):")
    print(encrypted_body[:80] + "...")
    print(f"总长度: {len(encrypted_body)} 字符")
    
    # 构建请求头
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
        "referer": "https://wx.10086.cn/website/businessPlatform/shopDetail",
        "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "x-app-version": "1.0.1",
        "x-center-env": "1",
        "x-requested-with": "XMLHttpRequest"
    }
    
    # 调用API
    print("\n正在发送创建订单请求...")
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    return response


def main():
    """主函数"""
    print("=" * 80)
    print("User2 创建订单 - 使用验证码 627398")
    print("=" * 80)
    
    # 验证码
    VERIFY_CODE = "627398"
    
    # 读取 user2 的 cookie
    cookie_file = 'user2/cooike_user2.json'
    if not os.path.exists(cookie_file):
        print(f"[ERROR] Cookie 文件不存在: {cookie_file}")
        sys.exit(1)
    
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookies_list = json.load(f)
    
    # 转换为字典格式
    cookies_dict = {}
    for cookie in cookies_list:
        cookies_dict[cookie['name']] = cookie['value']
    
    print(f"\nCookie 信息:")
    print(f"  shareToken: {cookies_dict.get('shareToken', 'N/A')[:50]}...")
    print(f"  riskToken: {cookies_dict.get('riskToken', 'N/A')}")
    print(f"  uuid: {cookies_dict.get('uuid', 'N/A')}")
    
    # 读取保存的 token
    token_file = 'user2/token_user2.txt'
    if not os.path.exists(token_file):
        print(f"\n[ERROR] Token 文件不存在: {token_file}")
        print(f"[提示] 请先运行 user2_send_sms_complete.py 获取 token")
        sys.exit(1)
    
    with open(token_file, 'r', encoding='utf-8') as f:
        authorization = f.read().strip()
    
    print(f"  Authorization (前50字符): {authorization[:50]}...")
    
    # 创建订单
    response = create_order(
        authorization=authorization,
        cookies_dict=cookies_dict,
        verify_code=VERIFY_CODE,
        norm_id=2259177,
        product_id=2170506,
        product_code=10528470
    )
    
    # 处理响应
    print("\n" + "=" * 80)
    print("响应结果")
    print("=" * 80)
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 80)
    if 'error' not in response:
        if response.get('returnCode') == '0':
            print("[SUCCESS] 订单创建成功！")
            if response.get('data'):
                data = response['data']
                print(f"\n订单信息:")
                for key, value in data.items():
                    print(f"  {key}: {value}")
        else:
            print("[FAILED] 订单创建失败")
            print(f"错误代码: {response.get('returnCode')}")
            print(f"错误消息: {response.get('returnMessage', 'Unknown error')}")
            
            # 常见错误提示
            error_code = response.get('returnCode')
            if error_code == 'SMS_9999':
                print("\n[提示] 验证码错误！请确认验证码是否正确或已过期。")
            elif error_code == '401':
                print("\n[提示] Token 无效或已过期，请重新获取 token。")
    else:
        print("[ERROR] 请求出错")
        print(f"错误类型: {response.get('error_type', 'Unknown')}")
        error_msg = response.get('error', 'Unknown')
        if len(str(error_msg)) > 200:
            error_msg = str(error_msg)[:200]
        print(f"错误详情: {error_msg}")
    print("=" * 80)


if __name__ == "__main__":
    main()

