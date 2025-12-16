# User2 发送验证码使用说明

## 功能说明

使用 user2 的 cookie 来发送验证码，完整流程包括：
1. 获取授权 token
2. 发送验证码请求

## 文件说明

### 核心文件

- `user2_send_sms_complete.py` - **主要脚本**，完整的发送验证码流程（推荐使用）
- `get_auth_token.py` - 单独获取授权 token
- `sendSms_curl.py` - 单独发送验证码（需要先获取 token）
- `sendSms_params_final.py` - AES 加密/解密工具库

### Cookie 文件

- `user2/cooike_user2.json` - user2 的 cookie 数据
- `user2/token_user2.txt` - 保存的授权 token（自动生成）

## 使用方法

### 方法一：一键运行（推荐）

```bash
python user2_send_sms_complete.py
```

这个脚本会自动完成以下步骤：
1. 读取 user2 的 cookie
2. 调用 userAuth API 获取授权 token
3. 使用 token 发送验证码请求
4. 保存 token 到文件以便后续使用

### 方法二：分步执行

#### 步骤1：获取 token

```bash
python get_auth_token.py
```

Token 会保存到 `user2/token_user2.txt`

#### 步骤2：发送验证码

```bash
python sendSms_curl.py
```

## 参数说明

### sendSms 接口参数

在 `user2_send_sms_complete.py` 的 `send_sms()` 函数中可以修改以下参数：

- `busi_id`: 业务ID，默认 "2"
- `norm_ids`: 规格ID，默认 "2259177"
- `user_effect_type`: 用户生效类型，默认 "Type_Default"

### 自定义参数示例

```python
# 修改 main() 函数中的调用
response = send_sms(
    token, 
    cookies_dict,
    busi_id="2",
    norm_ids="YOUR_NORM_ID",  # 修改为你的规格ID
    user_effect_type="Type_Default"
)
```

## 响应说明

### 成功响应

```json
{
  "returnCode": "0",
  "returnMessage": null,
  "data": {
    "status": "0",
    "message": "success",
    "smsContent": null
  },
  "ok": true
}
```

### 常见错误

| 错误代码 | 错误消息 | 原因 | 解决方法 |
|---------|---------|------|---------|
| `401` | token为空 或 无效的token | Authorization token 无效或过期 | 重新运行获取 token |
| `01_9999` | 验证码获取失败，请稍后再试 | 请求太频繁 | 等待几分钟后重试 |
| `SSL Error` | SSL握手失败 | Python OpenSSL 3.0 兼容性问题 | 使用 curl 版本的脚本 |

## 技术细节

### 为什么使用 curl？

由于 Python 使用 OpenSSL 3.0，对 10086 服务器的某些 TLS 配置不兼容，会导致 SSL 握手失败。使用 curl 可以绕过这个问题。

### API 端点

1. **获取 token**: `https://wx.10086.cn/website/nrapigate/nrauth/auth/encryt/userAuth`
2. **发送验证码**: `https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms`

### 加密方式

- **算法**: AES-CBC
- **密钥**: `1234123412ABCDEF`
- **IV**: `ABCDEF1234123412`
- **填充**: PKCS7
- **输出格式**: 十六进制大写字符串

请求和响应都使用相同的加密方式。

## 故障排除

### 1. SSL 错误

**错误**: `SSLError: SSL握手失败`

**解决**: 确保使用带 `_curl` 后缀的脚本，这些脚本使用 curl 来避免 SSL 问题。

### 2. Token 过期

**错误**: `401 无效的token`

**解决**: 重新运行 `get_auth_token.py` 或 `user2_send_sms_complete.py` 获取新的 token。

### 3. Cookie 过期

**错误**: 无法获取 token 或返回未授权错误

**解决**: 从浏览器中导出最新的 cookie 并更新 `user2/cooike_user2.json` 文件。

### 4. 请求频繁

**错误**: `01_9999 验证码获取失败，请稍后再试`

**解决**: 等待 1-2 分钟后再次尝试。

## 依赖项

```bash
pip install pycryptodome requests
```

## 注意事项

1. **Cookie 有效期**: shareToken 通常在几小时后过期，需要定期更新
2. **Token 有效期**: Authorization token 的有效期较长（约 29 天），可以保存后重复使用
3. **请求频率**: 避免短时间内频繁请求，建议间隔至少 60 秒
4. **安全性**: 不要将 cookie 和 token 泄露给他人

## 示例输出

```
================================================================================
User2 发送验证码完整流程
================================================================================

Cookie 信息:
  shareToken: m-gp5A.ybB2rH-SvcwSmu627Lr0hC4WSMjs_e2FJA2VnjLtQqq...
  riskToken: 6940e7d4h8TfdNBFh64W2HN3epAMLUumjHx7drh1
  uuid: 8a0e9d48-3dea-4ce9-a370-452a70951dd7
  clientId: 2d716501-5442-4d9b-9553-1cdb704be5c2

================================================================================
步骤 1: 获取授权 Token
================================================================================
[SUCCESS] 成功获取 token
Token (前50字符): 089A05D5E79C6F2860D0D425612D6AF5C8E2F913AF52B4296E...
用户信息: 手机号=EB5F2B265B1F783E95F7421C93E3A2C9, 省份=871, 城市=871
Token 已保存到: user2/token_user2.txt

================================================================================
步骤 2: 发送验证码
================================================================================

请求参数:
{
  "busiId": "2",
  "normIds": "2259177",
  "userEffectType": "Type_Default"
}

加密后的请求体 (前50字符):
4CAEE24050ECAB62FA24F7D0655544886C27887E0989B2C4F4...

正在发送请求...

================================================================================
响应结果
================================================================================
{
  "returnCode": "0",
  "returnMessage": null,
  "data": {
    "status": "0",
    "message": "success",
    "smsContent": null
  },
  "ok": true
}

================================================================================
[SUCCESS] 验证码发送成功！
状态: 0
消息: success
================================================================================
```

## 更新日志

### 2025-12-16
- ✅ 解决 OpenSSL 3.0 SSL 握手问题（使用 curl）
- ✅ 实现自动获取授权 token
- ✅ 创建完整的一键发送流程
- ✅ 添加详细的错误处理和用户反馈

## 相关文档

- `docs/sendSms验证结果.md` - sendSms 接口详细分析
- `docs/createOrder接口分析.md` - createOrder 接口分析

