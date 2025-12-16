#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解密 sendSms 接口的加密请求体
"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import json

# 从JS代码中提取的密钥和IV
# r() function: "1234,1234,12".split(",").join("") + "FEDCBA".reverse() = "123412341" + "ABCDEF"
KEY = "1234123412ABCDEF"
# o() function: "FEDCBA".reverse() + "1234,1234,12".split(",").join("") = "ABCDEF" + "123412341"  
IV = "ABCDEF1234123412"

# 实际捕获的加密请求体（160个十六进制字符 = 80字节）
encrypted_request_hex = "4CAEE24050ECAB62FA24F7D0655544886C27887E0989B2C4F4590FCDB305C95C917797D1E24DE068B1EA080222E20906BEDA079F0098299F4C130C27164A6A0441C778434ACB7C5C10BADC2CB673633E"

# 加密的响应体
encrypted_response_hex = "28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FCA30824A171BEF67046BB64F30D194C14D3F606879007E983FCF9A1827654797B049FC155A7891F7E951475A48DB3C084D5FCA01281CDB650C908B89E3D258E1B"

def decrypt_aes_cbc(encrypted_hex, key, iv):
    """
    解密AES-CBC加密的数据
    
    Args:
        encrypted_hex: 十六进制格式的加密数据
        key: 密钥字符串
        iv: IV字符串
        
    Returns:
        解密后的明文字符串
    """
    # 将十六进制字符串转换为字节
    encrypted_bytes = binascii.unhexlify(encrypted_hex)
    
    # 将密钥和IV转换为字节
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')
    
    # 创建AES解密器
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    
    # 解密
    decrypted_padded = cipher.decrypt(encrypted_bytes)
    
    # 去除PKCS7填充
    decrypted = unpad(decrypted_padded, AES.block_size)
    
    # 转换为字符串
    return decrypted.decode('utf-8')

if __name__ == "__main__":
    print("=" * 80)
    print("解密 sendSms 接口请求")
    print("=" * 80)
    print(f"\nAES密钥: {KEY}")
    print(f"AES IV: {IV}")
    print(f"\n加密的请求体（十六进制）: {encrypted_request_hex}")
    print(f"长度: {len(encrypted_request_hex)} 字符 = {len(encrypted_request_hex)//2} 字节")
    
    try:
        # 解密请求体
        decrypted_request = decrypt_aes_cbc(encrypted_request_hex, KEY, IV)
        print(f"\n解密后的请求体:")
        print(decrypted_request)
        
        # 尝试解析为JSON
        try:
            request_json = json.loads(decrypted_request)
            print(f"\n解析后的JSON参数:")
            print(json.dumps(request_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("\n注意: 解密后的数据不是有效的JSON格式")
            
    except Exception as e:
        print(f"\n解密请求体失败: {e}")
    
    print("\n" + "=" * 80)
    print("解密 sendSms 接口响应")
    print("=" * 80)
    print(f"\n加密的响应体（十六进制）: {encrypted_response_hex}")
    print(f"长度: {len(encrypted_response_hex)} 字符 = {len(encrypted_response_hex)//2} 字节")
    
    try:
        # 解密响应体
        decrypted_response = decrypt_aes_cbc(encrypted_response_hex, KEY, IV)
        print(f"\n解密后的响应体:")
        print(decrypted_response)
        
        # 尝试解析为JSON
        try:
            response_json = json.loads(decrypted_response)
            print(f"\n解析后的JSON:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("\n注意: 解密后的数据不是有效的JSON格式")
            
    except Exception as e:
        print(f"\n解密响应体失败: {e}")

