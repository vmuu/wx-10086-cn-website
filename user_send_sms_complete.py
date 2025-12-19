#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User 完整的验证码发送流程
包含：1. 获取授权token  2. 发送验证码
"""
import json
import sys
import os
from sendSms_params_final import aes_encrypt
from api_utils import call_api_with_curl


def get_auth_token(cookies_dict, back_url="/website/businessPlatform/shopDetail"):
    """
    获取授权token
    
    Args:
        cookies_dict: Cookie字典
        back_url: 返回URL
        
    Returns:
        (token, userInfo) 或 (None, None)
    """
    print("\n" + "=" * 80)
    print("步骤 1: 获取授权 Token")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrauth/auth/encryt/userAuth"
    
    # 构建请求参数
    params = {"backUrl": back_url}
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    # 构建请求头
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "channelid": "BUSINESS_H5",
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
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    # 处理响应
    if 'error' in response:
        print(f"[ERROR] 获取 token 失败: {response.get('error')}")
        return None, None
    
    if response.get('returnCode') == '0' and response.get('data'):
        token = response['data'].get('token')
        user_info = response['data'].get('userInfo')
        if token:
            print(f"[SUCCESS] 成功获取 token")
            print(f"Token (前50字符): {token[:50]}...")
            if user_info:
                print(f"用户信息: 手机号={user_info.get('telephone')}, 省份={user_info.get('provinceCode')}, 城市={user_info.get('cityCode')}")
            return token, user_info
        else:
            print(f"[ERROR] 响应中没有 token")
            return None, None
    else:
        print(f"[ERROR] 获取 token 失败")
        print(f"返回码: {response.get('returnCode')}")
        print(f"返回消息: {response.get('returnMessage')}")
        return None, None


def send_sms(authorization, cookies_dict, busi_id="2", norm_ids="2259111", user_effect_type="Type_Default"):
    """
    发送验证码
    
    Args:
        authorization: 授权token
        cookies_dict: Cookie字典
        busi_id: 业务ID
        norm_ids: 规格ID
        user_effect_type: 用户生效类型
        
    Returns:
        响应JSON
    """
    print("\n" + "=" * 80)
    print("步骤 2: 发送验证码")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms"
    
    # 构建请求参数
    params = {
        "busiId": busi_id,
        "normIds": norm_ids,
        "userEffectType": user_effect_type
    }
    
    print(f"\n请求参数:")
    print(json.dumps(params, indent=2, ensure_ascii=False))
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"\n加密后的请求体 (前50字符):")
    print(encrypted_body[:50] + "...")
    
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
    print("\n正在发送请求...")
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    return response


def main():
    """主函数"""
    print("=" * 80)
    print("User 发送验证码完整流程")
    print("=" * 80)
    
    # 读取 user 的 cookie
    cookie_file = 'user1/cooike_user1.json'
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
    print(f"  clientId: {cookies_dict.get('clientId', 'N/A')}")
    
    # 步骤1: 获取授权token
    token, user_info = get_auth_token(cookies_dict)
    
    if not token:
        print("\n[FAILED] 无法获取授权 token，流程终止")
        sys.exit(1)
    
    # 保存 token 到文件
    token_file = 'user1/token_user1.txt'
    with open(token_file, 'w', encoding='utf-8') as f:
        f.write(token)
    print(f"Token 已保存到: {token_file}")
    
    # 步骤2: 发送验证码
    response = send_sms(token, cookies_dict)
    
    # 处理响应
    print("\n" + "=" * 80)
    print("响应结果")
    print("=" * 80)
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 80)
    if 'error' not in response:
        if response.get('returnCode') == '0':
            print("[SUCCESS] 验证码发送成功！")
            print(f"状态: {response.get('data', {}).get('status')}")
            print(f"消息: {response.get('data', {}).get('message')}")
        else:
            print("[FAILED] 验证码发送失败")
            print(f"错误代码: {response.get('returnCode')}")
            print(f"错误消息: {response.get('returnMessage', 'Unknown error')}")
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

