#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 API 调用工具
封装 curl 调用与超时控制，供各业务脚本复用。
"""
import json
import subprocess
from typing import Dict, Any
from sendSms_params_final import aes_decrypt


def call_api_with_curl(url: str, encrypted_body: str, headers: Dict[str, str], cookies_dict: Dict[str, str], timeout_seconds: int = 30) -> Any:
    """
    使用 curl 调用 API（解决 OpenSSL 3.0 SSL 握手问题）
    
    Args:
        url: API URL
        encrypted_body: 加密的请求体
        headers: 请求头字典
        cookies_dict: Cookie 字典
        timeout_seconds: 请求超时时长（秒），默认 30，可视网络状况调整
    
    Returns:
        解密后的响应 JSON 或错误信息字典
    """
    def _short(text: str, limit: int = 400) -> str:
        return text if len(text) <= limit else text[:limit] + "...(truncated)"

    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies_dict.items()])
    curl_cmd = ["curl", "-X", "POST", url]

    for key, value in headers.items():
        curl_cmd.extend(["-H", f"{key}: {value}"])

    curl_cmd.extend(["-H", f"cookie: {cookie_str}"])
    curl_cmd.extend(["-d", encrypted_body])
    curl_cmd.extend(["-k", "--compressed"])

    try:
        print("\n" + "=" * 80)
        print("[REQUEST] URL:", url)
        print("[REQUEST] Headers:")
        for k, v in headers.items():
            print(f"  {k}: {v}")
        print("[REQUEST] Cookie:", _short(cookie_str, 300))
        print("[REQUEST] Body (hex) len:", len(encrypted_body))

        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            encoding='utf-8'
        )

        if result.returncode != 0:
            return {
            "error": f"Curl failed: {result.stderr}",
            "error_type": "CurlError",
            "returncode": result.returncode
        }

        print("[RESPONSE] status:", result.returncode)
        print("[RESPONSE] raw:", _short(result.stdout, 500))

        response_json = json.loads(result.stdout)
        encrypted_response = response_json.get("body", "")

        if encrypted_response:
            decrypted_response = aes_decrypt(encrypted_response)
            print("[RESPONSE] decrypted:", _short(decrypted_response, 500))
            return json.loads(decrypted_response)
        return response_json

    except subprocess.TimeoutExpired:
        return {
            "error": f"Request timeout after {timeout_seconds}s",
            "error_type": "TimeoutError"
        }
    except json.JSONDecodeError as e:
        return {
            "error": f"JSON decode error: {str(e)}",
            "error_type": "JSONDecodeError",
            "raw_output": result.stdout[:500] if 'result' in locals() else ''
        }
    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
        }
