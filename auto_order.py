#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的自动化订单创建流程
支持：获取token → 发送验证码 → 创建订单
"""
import json
import sys
import time
from user2_send_sms_complete import call_api_with_curl, get_auth_token
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
    params = {
        "busiId": busi_id,
        "normIds": norm_ids
    }
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"[INFO] 发送参数: {json_str}")
    
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 调用 API
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] API 调用失败: {response['error']}")
        return False
    
    if response.get('returnCode') == '0':
        print("[SUCCESS] 验证码发送成功!")
        print(f"状态: {response.get('data', {}).get('status')}")
        return True
    else:
        print(f"[FAILED] 验证码发送失败")
        print(f"错误代码: {response.get('returnCode')}")
        print(f"错误消息: {response.get('returnMessage')}")
        return False


def create_order(authorization, cookies_dict, verification_code, busi_id="2", norm_ids="2258951,2258995"):
    """
    创建订单
    
    Args:
        authorization: 授权token
        cookies_dict: Cookie字典
        verification_code: 验证码
        busi_id: 业务ID，默认"2"
        norm_ids: 规格ID，逗号分隔
        
    Returns:
        订单信息或None
    """
    print("\n" + "=" * 80)
    print("步骤 3: 创建订单")
    print("=" * 80)
    
    url = "https://wx.10086.cn/website/nrapigate/nrmix/order/createOrder"
    
    # 生成请求参数
    params = generate_createOrder_params(
        verification_code=verification_code,
        busi_id=busi_id,
        norm_ids=norm_ids
    )
    
    # 加密请求体
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    encrypted_body = aes_encrypt(json_str)
    
    print(f"[INFO] 验证码: {verification_code}")
    print(f"[INFO] normIds: {norm_ids}")
    
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
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    # 调用 API
    response = call_api_with_curl(url, encrypted_body, headers, cookies_dict)
    
    if 'error' in response:
        print(f"[ERROR] API 调用失败: {response['error']}")
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
        "user": "user2",
        "cookie_file": "user2/cooike_user2.json",
        "token_file": "user2/token_user2.txt"
    }
    
    # 产品配置（示例）
    products = {
        "1": {"name": "29元套餐（云南）", "code": "1087078", "normIds": "2258951,2258995"},
        "2": {"name": "399元融合套餐（5G-A版）", "code": "10715220", "normIds": "2259167,2259177"},
        "3": {"name": "自定义", "code": "custom", "normIds": "custom"},
    }
    
    print("\n可用产品:")
    for key, product in products.items():
        print(f"  {key}. {product['name']} (normIds: {product['normIds']})")
    
    choice = input("\n选择产品 (1-3): ").strip()
    
    if choice not in products:
        print("[ERROR] 无效选择")
        return
    
    selected_product = products[choice]
    
    # 如果选择自定义
    if choice == "3":
        norm_ids = input("请输入 normIds (逗号分隔): ").strip()
        if not norm_ids:
            print("[ERROR] normIds 不能为空")
            return
        selected_product["normIds"] = norm_ids
    
    print(f"\n已选择: {selected_product['name']}")
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
    
    # 步骤2: 获取 token
    token, user_info = get_auth_token(cookies)
    if not token:
        print("[ERROR] 无法获取 token")
        return
    
    # 保存 token
    with open(config['token_file'], 'w', encoding='utf-8') as f:
        f.write(token)
    
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
    order_data = create_order(token, cookies, verification_code, busi_id="2", norm_ids=selected_product['normIds'])
    
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

