# sendSms 参数对比分析

## 分析时间
2025-12-16

## 测试产品

### 产品1：升档流量大促活动-399融合套餐（5G-A版）
- **URL**: https://wx.10086.cn/website/businessPlatform/shopDetail?productId=2170496&productCode=10715220
- **productId**: 2170496
- **productCode**: 10715220

#### sendSms 请求参数
```json
{
  "busiId": "2",
  "normIds": "2259167,2259177"
}
```

**加密后的请求体**:
```
4CAEE24050ECAB62FA24F7D065554488D9BF553FC0DA5A6B1851D4D71249F6CFD6B99C65703EF89A702C819A387E24AE
```

#### 响应结果
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

---

### 产品2：升档流量大促活动-29套餐（云南）
- **URL**: https://wx.10086.cn/website/businessPlatform/shopDetail?productId=2170362&productCode=1087078
- **productId**: 2170362
- **productCode**: 1087078

#### sendSms 请求参数
```json
{
  "busiId": "2",
  "normIds": "2258951,2258995"
}
```

**加密后的请求体**:
```
4CAEE24050ECAB62FA24F7D065554488B2EBC7152D77E178673970D0FD843E19DE05853C08868BF141FE75CD903F4738
```

#### 响应结果
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

---

## 参数分析总结

### 共同特征

1. **busiId**
   - 两个产品都使用 `"2"`
   - 这似乎是一个固定的业务类型标识

2. **normIds 格式**
   - 都是逗号分隔的字符串格式
   - 格式：`"规格ID1,规格ID2"`
   - 两个产品都包含**两个规格ID**

3. **缺失字段**
   - 两个请求都**没有** `userEffectType` 字段
   - 与之前 user2 测试的参数不同（user2 的请求包含 `userEffectType: "0"`）

4. **请求结构**
   - 都使用 AES 加密
   - 请求体为加密后的十六进制字符串
   - 响应体也是加密的

### 不同之处

1. **normIds 的具体值**
   - 产品1: `"2259167,2259177"`
   - 产品2: `"2258951,2258995"`
   - **结论**: 不同产品有不同的规格ID组合

2. **产品信息**
   - 产品1: 399元套餐，5G-A版
   - 产品2: 29元套餐，云南地区

---

## normIds 的规律

### 观察
1. 每个产品都有**2个规格ID**
2. 规格ID是7位数字
3. ID之间用**英文逗号**分隔（无空格）
4. 产品2的两个ID：`2258951` 和 `2258995`，相差44
5. 产品1的两个ID：`2259167` 和 `2259177`，相差10

### 推测
- normIds 可能对应产品的不同规格选项（如套餐档位、附加服务等）
- 需要从产品详情页面的规格选择中获取正确的 normIds

---

## 与 user2 测试数据的对比

### user2 之前的测试参数
```json
{
  "busiId": "2",
  "normIds": "2258934,2259113",
  "userEffectType": "0"
}
```

### 关键差异

| 参数 | user2 测试 | 产品1 | 产品2 |
|-----|-----------|------|------|
| busiId | "2" | "2" | "2" |
| normIds | "2258934,2259113" | "2259167,2259177" | "2258951,2258995" |
| userEffectType | "0" | ❌ 无 | ❌ 无 |

**重要发现**:
- user1 的实际请求中**没有** `userEffectType` 字段
- 但 user2 的测试中包含了 `userEffectType: "0"`
- 这可能是因为：
  1. 不同用户类型的参数不同
  2. userEffectType 是可选参数
  3. 前端在某些情况下会自动添加此参数

---

## 实际应用建议

### 发送验证码的参数构建

```python
def build_sendSms_params(busi_id, norm_ids, user_effect_type=None):
    """
    构建 sendSms 参数
    
    Args:
        busi_id: 业务ID，通常为 "2"
        norm_ids: 规格ID列表，如 ["2259167", "2259177"]
        user_effect_type: 用户生效类型，可选，默认不传
    
    Returns:
        参数字典
    """
    params = {
        "busiId": str(busi_id),
        "normIds": ",".join(str(id) for id in norm_ids)
    }
    
    # 只在明确需要时才添加 userEffectType
    if user_effect_type is not None:
        params["userEffectType"] = str(user_effect_type)
    
    return params
```

### 使用示例

```python
# 产品1（399元套餐）
params_1 = build_sendSms_params(
    busi_id="2",
    norm_ids=["2259167", "2259177"]
)

# 产品2（29元套餐）
params_2 = build_sendSms_params(
    busi_id="2",
    norm_ids=["2258951", "2258995"]
)

# 如果需要添加 userEffectType
params_with_effect = build_sendSms_params(
    busi_id="2",
    norm_ids=["2258951", "2258995"],
    user_effect_type="0"
)
```

---

## Authorization Token

### 观察
两个请求使用了**相同的** authorization token:
```
089A05D5E79C6F2860D0D425612D6AF53D539B7527D6153F893DFDA52D7ED0B0061409B3D28DFAA23504E772BB56AFC5EE7FDE97E4893EEBD056F288F30D5BB2C7B2EE47BB6EC659799EB9816EE38C5B813FC46DC90C24F4CDCEDAC8B9D639E2A2F3FFB509157A83FF378C84DA404F0F
```

### 结论
- authorization token 在会话期间保持不变
- 同一个 token 可以用于多次 sendSms 请求
- token 需要通过 `/nrauth/auth/encryt/userAuth` 接口获取
- token 的有效期未知，建议定期刷新

---

## 重要发现总结

1. ✅ **busiId 固定为 "2"** - 所有测试产品都相同
2. ✅ **normIds 格式统一** - 逗号分隔的规格ID字符串
3. ⚠️ **userEffectType 可选** - user1 实际请求中没有此字段
4. ✅ **每个产品有特定的 normIds** - 需要从产品页面获取
5. ✅ **authorization token 可复用** - 会话期间有效

---

## 下一步工作

### 需要进一步研究的问题

1. **normIds 的来源**
   - 如何从产品详情页面提取 normIds？
   - 是否有 API 可以查询产品的规格列表？
   - 推荐查看 `/nrmix/product/norm` 或 `/nrproduct/atom/norm/normList` 接口

2. **userEffectType 的作用**
   - 什么情况下需要传递此参数？
   - "0" 代表什么含义？
   - 是否有其他可能的值？

3. **busiId 的含义**
   - "2" 代表什么业务类型？
   - 是否存在其他 busiId 值？
   - 不同业务类型的区别是什么？

4. **验证码频率限制**
   - 同一手机号的发送间隔限制
   - 同一IP的请求频率限制
   - 如何处理 "01_9999" 频繁请求错误

---

## 测试环境

- **浏览器**: Chrome 143.0.0.0
- **用户**: user1 (手机号: 19532990319)
- **Cookie**: user1 的 shareToken
- **工具**: Chrome DevTools Network Monitor
- **解密工具**: sendSms_params_final.py

---

## 相关文件

- `analyze_sendSms_requests.py` - 参数解密分析脚本
- `sendSms_params_final.py` - AES 加密/解密工具
- `user2_send_sms_complete.py` - user2 发送验证码完整流程
- `get_auth_token.py` - 获取 authorization token
- `sendSms_curl.py` - 使用 curl 发送验证码

---

## 结论

通过对比两个不同产品的 sendSms 请求参数，我们确认了：

1. **参数结构是统一的**：`busiId` + `normIds` (+ 可选的 `userEffectType`)
2. **关键差异在于 normIds**：每个产品有唯一的规格ID组合
3. **实现方案可行**：可以根据产品信息动态构建正确的 sendSms 参数

**建议的实现流程**：
1. 从产品详情页面获取 normIds（通过网络请求或页面解析）
2. 使用固定的 busiId = "2"
3. userEffectType 可以省略或根据需要添加
4. 使用 AES 加密参数后发送请求

