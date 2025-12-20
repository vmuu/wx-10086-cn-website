#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sendSms 接口完整参数说明和代码生成

经过实际解密验证，确认参数和加密方式
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import json
import requests

# AES加密配置（从JS代码中提取）
AES_KEY = "1234123412ABCDEF"  # r()函数: "123412341" + "ABCDEF"
AES_IV = "ABCDEF1234123412"   # o()函数: "ABCDEF" + "123412341"

def aes_encrypt(plaintext):
    """
    AES-CBC加密，与前端保持一致
    
    Args:
        plaintext: 明文字符串
        
    Returns:
        加密后的十六进制大写字符串
    """
    # 将明文转换为字节
    plaintext_bytes = plaintext.encode('utf-8')
    
    # 将密钥和IV转换为字节
    key_bytes = AES_KEY.encode('utf-8')
    iv_bytes = AES_IV.encode('utf-8')
    
    # 创建AES加密器
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    
    # 添加PKCS7填充并加密
    padded_data = pad(plaintext_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    
    # 转换为十六进制大写字符串（与JS的toUpperCase()对应）
    return binascii.hexlify(encrypted).decode('utf-8').upper()

def aes_decrypt(encrypted_hex):
    """
    AES-CBC解密
    
    Args:
        encrypted_hex: 十六进制格式的加密数据
        
    Returns:
        解密后的明文字符串
    """
    # 将十六进制字符串转换为字节
    encrypted_bytes = binascii.unhexlify(encrypted_hex)
    
    # 将密钥和IV转换为字节
    key_bytes = AES_KEY.encode('utf-8')
    iv_bytes = AES_IV.encode('utf-8')
    
    # 创建AES解密器
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    
    # 解密并去除PKCS7填充
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    decrypted = unpad(decrypted_padded, AES.block_size)
    
    return decrypted.decode('utf-8')

def generate_sendSms_params(busi_id="2", norm_ids=None, user_effect_type="Type_Default", 
                           user_mobile=None, session_id=None, touch_code=None, 
                           jctg=None, contract_operation=None):
    """
    生成 sendSms 接口的加密请求体
    
    参数说明（根据实际代码分析）：
    
    必需参数：
    - busi_id: 业务ID，默认"2"，特殊页面可能是"123"
    - norm_ids: 规格ID，字符串格式，例如"2259177"
    
    可选参数：
    - user_effect_type: 用户生效类型，默认"Type_Default"
    - user_mobile: 用户手机号（已加密），用于创建用户场景
    - session_id: 会话ID，特殊渠道需要
    - touch_code: 触点代码，特殊渠道需要  
    - jctg: 特殊标识
    - contract_operation: 合同操作参数
    
    Returns:
        加密后的请求体（十六进制大写字符串）
    """
    # 构建请求参数（只包含非空参数）
    params = {}
    
    # 必需参数
    if busi_id:
        params["busiId"] = busi_id
    if norm_ids:
        params["normIds"] = norm_ids
        
    # 可选参数
    if user_effect_type:
        params["userEffectType"] = user_effect_type
    if user_mobile:
        params["userMobile"] = user_mobile
    if session_id:
        params["sessionId"] = session_id
    if touch_code:
        params["touchCode"] = touch_code
    if jctg:
        params["jctg"] = jctg
    if contract_operation:
        params["contractOperation"] = contract_operation
    
    # 转换为JSON字符串
    json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    
    # AES加密
    encrypted = aes_encrypt(json_str)
    
    return encrypted, params

def call_sendSms_api(encrypted_body, authorization, cookies, verify_ssl=False):
    """
    调用 sendSms 接口
    
    Args:
        encrypted_body: 加密的请求体
        authorization: 授权token
        cookies: Cookie字典或字符串
        verify_ssl: 是否验证SSL证书
        
    Returns:
        解密后的响应JSON
    """
    url = "https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms"
    
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
    
    try:
        # 禁用 SSL 警告
        import urllib3
        import ssl
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 创建一个带有自定义SSL配置的session
        session = requests.Session()
        
        # 尝试使用更兼容的SSL配置
        from requests.adapters import HTTPAdapter
        from urllib3.poolmanager import PoolManager
        
        class TLSAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                # 创建支持更多TLS版本和加密套件的SSL上下文
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                # 降低安全级别以支持更多加密套件
                ctx.set_ciphers('DEFAULT:@SECLEVEL=1')
                # 支持 TLS 1.0, 1.1, 1.2, 1.3
                ctx.minimum_version = ssl.TLSVersion.TLSv1
                ctx.maximum_version = ssl.TLSVersion.MAXIMUM_SUPPORTED
                kwargs['ssl_context'] = ctx
                return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)
        
        session.mount('https://', TLSAdapter())
        
        response = session.post(url, data=encrypted_body, headers=headers, cookies=cookies, 
                                verify=False, timeout=10)
        
        # 获取响应信息
        response_data = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "raw_body": response.text[:200] if response.text else ""
        }
        
        # 获取加密的响应体
        response_json = response.json()
        encrypted_response = response_json.get("body", "")
        
        if encrypted_response:
            # 解密响应
            decrypted_response = aes_decrypt(encrypted_response)
            result = json.loads(decrypted_response)
        else:
            result = response_json
        
        result["_meta"] = response_data
        return result
    
    except Exception as e:
        return {"error": str(e), "error_type": type(e).__name__}

# ============================================================================
# 示例用法
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("sendSms 接口参数生成示例（已验证）")
    print("=" * 80)
    
    # 示例1：普通场景（从实际解密的请求中获取）
    print("\n【示例1】普通商品详情页发送验证码")
    encrypted_body, params = generate_sendSms_params(
        busi_id="2",
        norm_ids="2259177",
        user_effect_type="Type_Default"
    )
    
    print(f"\n原始参数:")
    print(json.dumps(params, indent=2, ensure_ascii=False))
    
    print(f"\n加密后的请求体:")
    print(encrypted_body)
    print(f"长度: {len(encrypted_body)} 字符 = {len(encrypted_body)//2} 字节")
    
    # 验证解密
    decrypted = aes_decrypt(encrypted_body)
    print(f"\n解密验证:")
    print(decrypted)
    
    # 示例2：广东营销案例场景
    print("\n" + "=" * 80)
    print("【示例2】广东营销案例场景")
    encrypted_body2, params2 = generate_sendSms_params(
        busi_id="123",
        norm_ids="1234567",
        user_effect_type="Type_Custom"
    )
    
    print(f"\n原始参数:")
    print(json.dumps(params2, indent=2, ensure_ascii=False))
    
    print(f"\n加密后的请求体:")
    print(encrypted_body2)
    
    # 示例3：特殊渠道（30011）场景
    print("\n" + "=" * 80)
    print("【示例3】特殊渠道场景（需要sessionId和touchCode）")
    encrypted_body3, params3 = generate_sendSms_params(
        busi_id="2",
        norm_ids="2259177",
        user_effect_type="Type_Default",
        session_id="abc123xyz",
        touch_code="CH30011"
    )
    
    print(f"\n原始参数:")
    print(json.dumps(params3, indent=2, ensure_ascii=False))
    
    print(f"\n加密后的请求体:")
    print(encrypted_body3)
    
    # API信息总结
    print("\n" + "=" * 80)
    print("API调用信息总结")
    print("=" * 80)
    print(f"""
URL: https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms
Method: POST
Content-Type: application/json; charset=UTF-8

必需请求头:
- authorization: 从cookie中的shareToken或登录接口获取
- channelid: BUSINESS_H5
- cookie: 包含用户认证信息

加密方式:
- 算法: AES-CBC
- 密钥: {AES_KEY}
- IV: {AES_IV}
- 填充: PKCS7
- 输出格式: 十六进制大写字符串

核心参数（未加密前）:
- busiId: 业务ID，通常为"2"
- normIds: 规格ID，商品的规格编号
- userEffectType: 用户生效类型，默认"Type_Default"

响应格式（解密后）:
{{
  "returnCode": "0",        // 0表示成功
  "returnMessage": null,    // 错误消息
  "data": {{
    "status": "0",          // 0表示验证码发送成功
    "message": "success",
    "smsContent": null
  }},
  "ok": true
}}
""")

