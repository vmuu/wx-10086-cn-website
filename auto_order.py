#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的自动化订单创建流程
支持：获取token → 发送验证码 → 创建订单
"""
import json
import sys
import time
from user_send_sms_complete import call_api_with_curl, get_auth_token
from createOrder_params import generate_createOrder_params
from sendSms_params_final import aes_encrypt

def load_cookies_from_file(cookie_file):
    """加载 cookie 文件"""
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        # 转换为字典格式
        if isinstance(cookie_data, list):
            return {item['name']: item['value'] for item in cookie_data}
        return cookie_data
    except Exception as e:
        print(f"[ERROR] 加载 cookies 失败: {e}")
        return None


def get_auth_token_with_debug(cookies_dict, back_url="/website/businessPlatform/shopDetail"):
    """
    获取授权token（带完整请求响应打印）
    
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
    
    print(f"\n[请求] URL: {url}")
    print(f"[请求] 原始参数: {json_str}")
    print(f"[请求] 加密后的请求体: {encrypted_body}")
    
    # 构建请求头
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
    
    print(f"\n[请求] 请求头:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    # 调用API
    print("\n正在发送请求...")
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    print(f"\n[响应] 完整响应:")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    # 处理响应
    if 'error' in response:
        print(f"\n[ERROR] 获取 token 失败: {response.get('error')}")
        return None, None
    
    if response.get('returnCode') == '0' and response.get('data'):
        token = response['data'].get('token')
        user_info = response['data'].get('userInfo')
        if token:
            print(f"\n[SUCCESS] 成功获取 token")
            print(f"Token (前50字符): {token[:50]}...")
            if user_info:
                print(f"用户信息: 手机号={user_info.get('telephone')}, 省份={user_info.get('provinceCode')}, 城市={user_info.get('cityCode')}")
            return token, user_info
        else:
            print(f"\n[ERROR] 响应中没有 token")
            return None, None
    else:
        print(f"\n[ERROR] 获取 token 失败")
        print(f"返回码: {response.get('returnCode')}")
        print(f"返回消息: {response.get('returnMessage')}")
        return None, None


def send_sms(authorization, cookies_dict, busi_id="2", norm_ids="2258951,2258995"):
    """
    发送验证码
    
    Args:
        authorization: 授权token
        cookies_dict: Cookie字典
        busi_id: 业务ID，默认"2"
        norm_ids: 规格ID，逗号分隔
        
    Returns:
        是否成功
    """
    print("\n" + "=" * 80)
    print("步骤 2: 发送验证码")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms"
    
    # 构建请求参数
    # 注意：根据之前的分析，userEffectType 是可选的，但为了兼容性可以添加
    params = {
        "busiId": busi_id,
        "normIds": norm_ids
        # "userEffectType": "Type_Default"  # 可选，根据实际需要添加
    }
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"[INFO] 发送参数: {json_str}")
    print(f"[INFO] 加密后的请求体 (前50字符): {encrypted_body[:50]}...")
    
    # 请求头（使用与 user2_send_sms_complete.py 相同的完整请求头）
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
    
    # 调用 API
    print("\n正在发送请求...")
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] API 调用失败: {response['error']}")
        print(f"[ERROR] 错误类型: {response.get('error_type', 'Unknown')}")
        return False
    
    # 打印完整响应用于调试
    print(f"\n[DEBUG] 完整响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
    
    if response.get('returnCode') == '0':
        print("[SUCCESS] 验证码发送成功!")
        print(f"状态: {response.get('data', {}).get('status')}")
        return True
    else:
        print(f"[FAILED] 验证码发送失败")
        print(f"错误代码: {response.get('returnCode')}")
        return_msg = response.get('returnMessage', 'Unknown error')
        
        # 尝试解码中文
        try:
            if '\\u' in return_msg:
                return_msg = return_msg.encode().decode('unicode_escape')
        except:
            pass
        
        print(f"错误消息: {return_msg}")
        
        # 如果是服务异常，给出建议
        if response.get('returnCode') == '01_9999':
            print("\n[提示] 服务异常可能的原因:")
            print("  1. 短时间内请求太频繁，请等待 1-2 分钟后重试")
            print("  2. Cookie 或 Token 可能已过期，请更新")
            print("  3. 服务器临时故障，请稍后重试")
        
        return False


def create_order(authorization, cookies_dict, verify_code, product_id, product_code, norm_ids):
    """
    创建订单
    
    Args:
        authorization: 授权token
        cookies_dict: Cookie字典
        verify_code: 验证码
        product_id: 产品ID
        product_code: 产品代码
        norm_ids: 规格ID（逗号分隔的字符串，如 "2259167,2259177"）
        
    Returns:
        订单信息或None
    """
    print("\n" + "=" * 80)
    print("步骤 3: 创建订单")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrmix/order/createOrder"
    
    # 获取 riskToken
    risk_token = cookies_dict.get('riskToken', '')
    
    if not risk_token:
        print("[ERROR] 未找到 riskToken，无法创建订单")
        return None
    
    # 从 normIds 中提取第一个作为 norm_id（用于 generate_createOrder_params）
    norm_ids_list = [nid.strip() for nid in norm_ids.split(',')]
    first_norm_id = int(norm_ids_list[0])
    
    print(f"\n[请求] URL: {url}")
    print(f"[请求] 产品ID: {product_id}")
    print(f"[请求] 产品代码: {product_code}")
    print(f"[请求] 规格IDs: {norm_ids}")
    print(f"[请求] 验证码: {verify_code}")
    print(f"[请求] 风控Token: {risk_token[:30]}...")
    
    # 生成请求参数（使用第一个 norm_id）
    encrypted_body, params = generate_createOrder_params(
        norm_id=first_norm_id,
        product_id=int(product_id),
        product_code=int(product_code),
        verify_code=verify_code,
        risk_token=risk_token,
        user_effect_type="Type_Default",
        order_type=1,
        order_resource=20,
        pt_id=200103516,
        sign_activity=False
    )
    
    # 添加 normIds 字段（逗号分隔的字符串）
    params['normIds'] = norm_ids
    params['busiId'] = "2"  # 根据用户要求添加 busiId
    
    # 重新生成 JSON 和加密（包含 normIds 和 busiId）
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"\n[请求] 完整请求参数:")
    print(json.dumps(params, indent=2, ensure_ascii=False))
    print(f"\n[请求] 加密后的请求体: {encrypted_body}")
    
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
    
    print(f"\n[请求] 请求头:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
    
    # 调用 API
    print("\n正在发送请求...")
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    print(f"\n[响应] 完整响应:")
    print(json.dumps(response, indent=2, ensure_ascii=False))
    
    if 'error' in response:
        print(f"\n[ERROR] API 调用失败: {response['error']}")
        return None
    
    print("\n" + "=" * 80)
    print("订单创建结果")
    print("=" * 80)
    
    if response.get('returnCode') == '0':
        print("[SUCCESS] 订单创建成功!")
        data = response.get('data', {})
        order_no = data.get('orderNo', 'N/A')
        print(f"订单号: {order_no}")
        
        # 打印更多订单信息
        if data:
            print("\n订单详情:")
            for key, value in data.items():
                if key not in ['orderNo']:
                    print(f"  {key}: {value}")
        
        return data
    else:
        print(f"[FAILED] 订单创建失败")
        print(f"错误代码: {response.get('returnCode')}")
        return_msg = response.get('returnMessage', 'Unknown error')
        
        # 尝试解码中文
        try:
            if '\\u' in return_msg:
                return_msg = return_msg.encode().decode('unicode_escape')
        except:
            pass
        
        print(f"错误消息: {return_msg}")
        return None


def main():
    """主流程"""
    print("=" * 80)
    print("10086 自动化订单创建工具")
    print("=" * 80)
    
    # 配置
    config = {
        "user": "user1",
        "cookie_file": "user1/cooike_user1.json",
        "token_file": "user1/token_user1.txt"
    }
    
    # 产品配置（示例）
    products = {
        "1": {
            "name": "29元套餐（云南）",
            "product_id": 2170362,
            "product_code": 1087078,
            "normIds": "2258951,2258995"
        },
        "2": {
            "name": "399元融合套餐（5G-A版）",
            "product_id": 2170496,
            "product_code": 10715220,
            "normIds": "2259167,2259177"
        },
        "3": {"name": "自定义", "product_id": 0, "product_code": 0, "normIds": "custom"},
    }
    
    print("\n可用产品:")
    for key, product in products.items():
        if key == "3":
            print(f"  {key}. {product['name']}")
        else:
            print(f"  {key}. {product['name']} (productId: {product['product_id']}, productCode: {product['product_code']}, normIds: {product['normIds']})")
    
    choice = input("\n选择产品 (1-3): ").strip()
    
    if choice not in products:
        print("[ERROR] 无效选择")
        return
    
    selected_product = products[choice]
    
    # 如果选择自定义
    if choice == "3":
        product_id = input("请输入 productId: ").strip()
        product_code = input("请输入 productCode: ").strip()
        norm_ids = input("请输入 normIds (逗号分隔): ").strip()
        
        if not product_id or not product_code or not norm_ids:
            print("[ERROR] 所有参数都不能为空")
            return
        
        try:
            selected_product["product_id"] = int(product_id)
            selected_product["product_code"] = int(product_code)
            selected_product["normIds"] = norm_ids
        except ValueError:
            print("[ERROR] productId 和 productCode 必须是数字")
            return
    
    print(f"\n已选择: {selected_product['name']}")
    print(f"产品ID: {selected_product.get('product_id', 'N/A')}")
    print(f"产品代码: {selected_product.get('product_code', 'N/A')}")
    print(f"normIds: {selected_product['normIds']}")
    
    # 步骤1: 加载 cookies
    print("\n" + "=" * 80)
    print("步骤 1: 加载配置")
    print("=" * 80)
    
    cookies = load_cookies_from_file(config['cookie_file'])
    if not cookies:
        print("[ERROR] 无法加载 cookies")
        return
    
    print(f"[SUCCESS] 成功加载 {config['user']} 的 cookies")
    
    # 步骤2: 获取 token（带完整请求响应打印）
    token, user_info = get_auth_token_with_debug(cookies)
    if not token:
        print("[ERROR] 无法获取 token")
        return
    
    # 保存 token
    with open(config['token_file'], 'w', encoding='utf-8') as f:
        f.write(token)
    
    # 添加延迟，避免请求太频繁
    print("\n[INFO] 等待 2 秒后发送验证码，避免请求过于频繁...")
    time.sleep(2)
    
    # 步骤3: 发送验证码
    success = send_sms(token, cookies, busi_id="2", norm_ids=selected_product['normIds'])
    
    if not success:
        print("\n[ERROR] 验证码发送失败，无法继续")
        return
    
    # 步骤4: 等待用户输入验证码
    print("\n" + "=" * 80)
    verification_code = input("请输入收到的验证码: ").strip()
    
    if not verification_code or not verification_code.isdigit():
        print("[ERROR] 验证码格式不正确")
        return
    
    # 步骤5: 创建订单
    # 传递所有 normIds（逗号分隔的字符串）
    norm_ids = selected_product['normIds']
    print(f"\n[INFO] 将使用所有 normIds: {norm_ids}")
    
    order_data = create_order(
        authorization=token,
        cookies_dict=cookies,
        verify_code=verification_code,
        product_id=selected_product['product_id'],
        product_code=selected_product['product_code'],
        norm_ids=norm_ids
    )
    
    if order_data:
        print("\n" + "=" * 80)
        print("流程完成!")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("流程失败")
        print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户中断")
    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()

