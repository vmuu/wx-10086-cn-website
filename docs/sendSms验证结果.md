# sendSms 接口验证结果

## 验证状态：✅ 完全验证成功

### 1. 接口基本信息

```
URL: https://wx.10086.cn/website/nrapigate/nrmix/sms/sendSms
Method: POST
Content-Type: application/json; charset=UTF-8
```

### 2. 加密配置（已验证）

- **算法**: AES-CBC
- **密钥**: `1234123412ABCDEF`
- **IV**: `ABCDEF1234123412`
- **填充**: PKCS7
- **输出格式**: 十六进制大写字符串

**密钥来源**（从 index.c8422640.js 提取）：
```javascript
// 第 624-636 行
var r = function() {
    var e = ""
      , n = "1234,1234,12"
      , a = "FEDCBA".split("").reverse().join("");
    return e = "".concat(n.split(",").join("")).concat(a),
    e  // 结果: "123412341" + "ABCDEF" = "1234123412ABCDEF"
}
var o = function() {
    var e = ""
      , n = "1234,1234,12"
      , a = "FEDCBA".split("").reverse().join("");
    return e = "".concat(a).concat(n.split(",").join("")),
    e  // 结果: "ABCDEF" + "123412341" = "ABCDEF1234123412"
}
var i = t.enc.Utf8.parse(r())  // KEY
var u = t.enc.Utf8.parse(o())  // IV
```

### 3. 请求参数（已解密验证）

**原始参数**:
```json
{
  "busiId": "2",
  "normIds": "2259177",
  "userEffectType": "Type_Default"
}
```

**加密后**:
```
4CAEE24050ECAB62FA24F7D0655544886C27887E0989B2C4F4590FCDB305C95C917797D1E24DE068B1EA080222E20906BEDA079F0098299F4C130C27164A6A0441C778434ACB7C5C10BADC2CB673633E
```

### 4. 必需的请求头

```http
Content-Type: application/json; charset=UTF-8
Authorization: <从 Vuex store 的 getters.token 获取>
channelid: BUSINESS_H5
x-requested-with: XMLHttpRequest
x-app-version: 1.0.1
x-center-env: 1
Cookie: shareToken=<用户登录token>; uuid=<设备标识>; ...
```

**关键发现**: 
- `Authorization` header 是必需的，否则返回 `{"returnCode":"401", "returnMessage":"token为空"}`
- `Authorization` 值来自 Vuex store: `window.$nuxt.$store.getters.token`
- 这个 token 似乎是从 cookie 中的 `shareToken` 派生而来

### 5. 响应格式（已解密验证）

**加密的响应体**:
```
28B47789BB1B38D19FA5250EBE33B2D2AB0C05C51A6F390DF157920858EF5E8B4BB55C7E1FD83CFC1F556859DC4939FCA30824A171BEF67046BB64F30D194C14D3F606879007E983FCF9A1827654797B049FC155A7891F7E951475A48DB3C084D5FCA01281CDB650C908B89E3D258E1B
```

**解密后**:
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

### 6. 参数说明

#### 核心参数（从代码分析）

| 参数 | 类型 | 必需 | 说明 | 示例值 |
|------|------|------|------|--------|
| `busiId` | string | 是 | 业务ID | "2" (默认), "123" (广东营销案例) |
| `normIds` | string | 是 | 规格ID | "2259177" |
| `userEffectType` | string | 否 | 用户生效类型 | "Type_Default" |

#### 可选参数（特殊场景）

| 参数 | 类型 | 说明 | 使用场景 |
|------|------|------|----------|
| `userMobile` | string | 加密的手机号 | 创建用户场景 (showTelInput) |
| `sessionId` | string | 会话ID | 渠道 30011 |
| `touchCode` | string | 触点代码 | 渠道 30011 |
| `jctg` | string | 特殊标识 | sessionStorage 中存在时 |
| `contractOperation` | string | 合同操作 | 特定业务场景 |

### 7. 不同页面类型的参数差异

```javascript
// 普通商品详情页 (shopDetail)
{
  busiId: "2",
  normIds: "规格ID",
  userEffectType: "Type_Default"
}

// 广东营销案例 (gdMarketingCase)
{
  busiId: "123",
  normIds: "规格ID",
  userEffectType: "Type_Default"
}

// 河北宽带 (hebeiBroadband) - 使用不同的 API
// URL: /nrapigate/nrmix/sms/sendCommonSms
{
  telephone: "加密的手机号",
  bizType: "业务类型",
  productId: "产品ID"
}

// 融合商品详情 (integrationShopDetail) - 使用不同的 API
// URL: /nrapigate/nrmix/product/package/sendSms
{
  packageId: "套餐ID",
  normInfoList: "规格信息列表"
}
```

### 8. 验证过程

1. ✅ **JS代码分析**: 找到了加密函数和密钥生成逻辑
2. ✅ **网络请求捕获**: 获取了实际的加密请求和响应
3. ✅ **解密验证**: 成功解密请求和响应，确认参数
4. ✅ **加密验证**: 生成的加密数据与实际请求完全一致
5. ✅ **实际调用测试**: 在浏览器中成功调用接口并获得响应
6. ✅ **Token 机制**: 找到了 Authorization token 的来源（Vuex store）

### 9. 完整调用流程

```
1. 用户点击"获取验证码"
   ↓
2. 前端收集参数（busiId, normIds, userEffectType）
   ↓
3. 转换为 JSON 字符串
   ↓
4. 使用 AES-CBC 加密（KEY: 1234123412ABCDEF, IV: ABCDEF1234123412）
   ↓
5. 转换为十六进制大写字符串
   ↓
6. 从 Vuex store 获取 Authorization token
   ↓
7. POST 到 /nrapigate/nrmix/sms/sendSms
   ↓
8. 服务器返回加密的响应体
   ↓
9. 前端使用相同密钥解密响应
   ↓
10. 显示结果或开始倒计时
```

### 10. 安全考虑

- ⚠️ AES 密钥硬编码在前端代码中（安全性较低）
- ✓ 使用 HTTPS 传输
- ✓ 需要有效的 Authorization token
- ✓ Cookie 包含用户认证信息
- ⚠️ 密钥可以通过前端代码逆向获取

### 11. 代码文件

- `sendSms_params_final.py`: 完整的参数生成和加密/解密实现
- `decrypt_request.py`: 解密工具
- `test_user2_sendSms.py`: 测试脚本

---
**验证日期**: 2025-12-16
**验证方法**: 实际网络请求 + 代码分析 + 加密解密测试
**验证结果**: ✅ 100% 准确

