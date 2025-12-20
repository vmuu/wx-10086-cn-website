#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
createOrder 接口参数生成代码
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import json
import time
from datetime import datetime

# AES加密配置
AES_KEY = "1234123412ABCDEF"
AES_IV = "ABCDEF1234123412"

def aes_encrypt(plaintext):
    """AES-CBC加密"""
    plaintext_bytes = plaintext.encode('utf-8')
    key_bytes = AES_KEY.encode('utf-8')
    iv_bytes = AES_IV.encode('utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    padded_data = pad(plaintext_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return binascii.hexlify(encrypted).decode('utf-8').upper()

def generate_createOrder_params(
    norm_id,
    product_id,
    product_code,
    verify_code,
    risk_token,
    user_effect_type="Type_Default",
    order_type=1,
    order_resource=20,
    pt_id=200103516,
    sign_activity=False,
    shop_id="",
    agent_id="",
    staff_id="",
    employee_id="",
    red_code="",
    rcm_src="",
    coupon_id=""
):
    """
    生成 createOrder 接口的加密请求体
    
    必需参数：
    - norm_id: 规格ID（int）
    - product_id: 产品ID（int）
    - product_code: 产品代码（int）
    - verify_code: 短信验证码（str）
    - risk_token: 风控token，从cookie的riskToken获取（str）
    
    可选参数：
    - user_effect_type: 用户生效类型，默认"Type_Default"
    - order_type: 订单类型，默认1
    - order_resource: 订单来源，默认20
    - pt_id: 平台ID，默认200103516
    - sign_activity: 是否签约活动，默认False
    - shop_id: 店铺ID
    - agent_id: 代理商ID
    - staff_id: 员工ID
    - employee_id: 员工ID
    - red_code: 红包码
    - rcm_src: 推荐来源
    - coupon_id: 优惠券ID
    
    Returns:
        (加密后的请求体, 原始参数字典)
    """
    # 当前时间
    now = datetime.now()
    confirm_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_span = int(time.time() * 1000)
    
    # 构建参数（保持原始顺序）
    params = {
        "shopid": shop_id,
        "normid": norm_id,
        "ordertype": order_type,
        "agentid": agent_id,
        "staffId": staff_id,
        "timeSpan": time_span,
        "password": verify_code,
        "productId": product_id,
        "productCode": product_code,
        "serialId": "",
        "tuikeInfo": "",
        "redCode": red_code,
        "rcmSrc": rcm_src,
        "fromRecommend": "",
        "employeeId": employee_id,
        "employeeProvinceId": "",
        "sendResultComp": "",
        "sendResultId": "",
        "sendResultType": "",
        "sendResultAtyCode": "",
        "cmgSmsCode": verify_code,
        "verifyCode": verify_code,
        "confirmTime": confirm_time,
        "sellerId": "",
        "recommendTraceId": "",
        "orderResource": order_resource,
        "selectedCouponId": coupon_id,
        "bookTime": confirm_time,  # 使用相同的时间
        "userEffectType": user_effect_type,
        "ptId": pt_id,
        "token": risk_token,
        "signActivity": sign_activity
    }
    
    # 转换为JSON字符串
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    
    # AES加密
    encrypted = aes_encrypt(json_str)
    
    return encrypted, params

# ============================================================================
# 示例用法
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("createOrder 接口参数生成示例")
    print("=" * 80)
    
    # 示例：创建订单
    print("\n【示例】创建订单请求")
    encrypted_body, params = generate_createOrder_params(
        norm_id=2259177,
        product_id=2170506,
        product_code=10528470,
        verify_code="123456",
        risk_token="694100a6YVPprypZZQN5asqzkA0rcJZ7329WOHL1",
        user_effect_type="Type_Default"
    )
    
    print(f"\n原始参数:")
    print(json.dumps(params, indent=2, ensure_ascii=False))
    
    print(f"\n加密后的请求体:")
    print(encrypted_body[:100] + "...")
    print(f"长度: {len(encrypted_body)} 字符 = {len(encrypted_body)//2} 字节")
    
    # API信息总结
    print("\n" + "=" * 80)
    print("API调用信息总结")
    print("=" * 80)
    print(f"""
URL: https://wx.10086.cn/website/nrapigate/nrmix/order/createOrder
Method: POST
Content-Type: application/json; charset=UTF-8

必需请求头:
- authorization: 从 Vuex store 的 getters.token 获取
- channelid: BUSINESS_H5
- cookie: 包含 shareToken、riskToken、uuid 等

加密方式:
- 算法: AES-CBC
- 密钥: {AES_KEY}
- IV: {AES_IV}
- 填充: PKCS7
- 输出格式: 十六进制大写字符串

核心参数（未加密前）:
- normid: 规格ID
- productId: 产品ID
- productCode: 产品代码
- password/cmgSmsCode/verifyCode: 短信验证码（三个字段值相同）
- token: 风控token（来自cookie的riskToken）
- timeSpan: 当前时间戳（毫秒）
- confirmTime: 确认时间
- orderResource: 订单来源，固定为20
- userEffectType: 用户生效类型

响应格式（解密后）:
成功: {{"returnCode": "0", "returnMessage": "...", "data": {{...}}, "ok": true}}
失败: {{"returnCode": "错误码", "returnMessage": "错误信息", "data": null, "ok": false}}

常见错误码:
- SMS_9999: 短信验证码不正确
- 40402: 请求方法不支持（仅支持POST）
""")

