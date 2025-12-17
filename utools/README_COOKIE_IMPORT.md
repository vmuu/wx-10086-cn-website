# 浏览器 Cookie 导入指南

> 通过浏览器控制台手动导入用户的 Cookie

## 📋 目录

- [快速开始](#快速开始)
- [方式一：使用自动生成脚本](#方式一使用自动生成脚本推荐)
- [方式二：使用通用模板](#方式二使用通用模板)
- [方式三：手动设置](#方式三手动设置)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 最简单的方式（三步搞定）

1. **生成导入脚本**
   ```bash
   python utools/generate_cookie_import_script.py
   # 选择用户（1=user1, 2=user2）
   ```

2. **复制生成的脚本**
   - 打开生成的文件: `utools/import_user2_cookies.js`
   - 全选并复制（Ctrl+A, Ctrl+C）

3. **在浏览器执行**
   - 访问 https://wx.10086.cn
   - 按 F12 打开开发者工具
   - 切换到 Console 标签
   - 粘贴代码并回车
   - 刷新页面（F5）

---

## 📖 详细教程

### 方式一：使用自动生成脚本（推荐）

#### 步骤 1: 生成脚本

```bash
cd d:\work\10086
python utools/generate_cookie_import_script.py
```

**选择用户:**
```
可用用户:
  1. user1 (user1/cooike_user1.json)
  2. user2 (user2/cooike_user2.json)

选择用户 (1-2): 2
```

#### 步骤 2: 打开浏览器

1. 打开 Chrome/Edge 浏览器
2. 访问 `https://wx.10086.cn`
3. 按 `F12` 打开开发者工具
4. 点击 `Console` (控制台) 标签

#### 步骤 3: 执行导入脚本

1. 打开生成的文件: `utools/import_user2_cookies.js`
2. 全选内容 (`Ctrl+A`)
3. 复制 (`Ctrl+C`)
4. 切换回浏览器控制台
5. 粘贴代码 (`Ctrl+V`)
6. 按 `Enter` 执行

#### 步骤 4: 查看结果

控制台会显示：
```javascript
开始导入 user2 的 Cookies...

方式1: 使用 document.cookie 设置
✓ shareToken
✓ riskToken
✓ uuid
✓ clientId
...

导入完成! 成功: 10, 失败: 0

当前 Cookies:
shareToken=xxx; riskToken=xxx; ...
```

#### 步骤 5: 刷新页面

按 `F5` 刷新页面，Cookie 即可生效。

---

### 方式二：使用通用模板

如果你想手动控制或修改 Cookie 数据：

#### 步骤 1: 准备 Cookie 数据

从 JSON 文件中复制 Cookie 数据：
```json
[
    {"name": "shareToken", "value": "your_token_value"},
    {"name": "riskToken", "value": "your_risk_token"},
    {"name": "uuid", "value": "your_uuid"},
    {"name": "clientId", "value": "your_client_id"}
]
```

#### 步骤 2: 修改模板

1. 打开 `utools/browser_cookie_importer_template.js`
2. 找到 `COOKIES_DATA` 部分
3. 替换为你的 Cookie 数据

```javascript
const COOKIES_DATA = [
    // 粘贴你的 Cookie 数据
    {"name": "shareToken", "value": "m-gp5A.ybB2rH-..."},
    {"name": "riskToken", "value": "6940e650Rdws..."},
    // ... 更多 cookies
];
```

#### 步骤 3: 执行脚本

复制整个文件内容到浏览器控制台执行。

---

### 方式三：手动设置

如果你只需要设置几个关键 Cookie：

#### 在控制台直接执行

```javascript
// 设置单个 Cookie
document.cookie = "shareToken=your_value; domain=.wx.10086.cn; path=/; max-age=2592000; secure; samesite=Lax";

// 设置多个 Cookies
const cookies = {
    'shareToken': 'your_token_value',
    'riskToken': 'your_risk_value',
    'uuid': 'your_uuid_value',
    'clientId': 'your_client_id_value'
};

Object.entries(cookies).forEach(([name, value]) => {
    document.cookie = `${name}=${value}; domain=.wx.10086.cn; path=/; max-age=2592000; secure; samesite=Lax`;
    console.log(`✓ Set ${name}`);
});

console.log('Done! Refresh the page (F5)');
```

---

## 🔍 验证 Cookie 是否导入成功

### 方法 1: 查看控制台输出

成功导入后会显示：
```
✓ shareToken
✓ riskToken
✓ uuid
...
导入完成! 成功: X, 失败: 0
```

### 方法 2: 检查 Application 标签

1. 开发者工具中点击 `Application` 标签
2. 左侧展开 `Cookies`
3. 点击 `https://wx.10086.cn`
4. 右侧应显示所有导入的 Cookie

### 方法 3: 在控制台查询

```javascript
// 查看所有 cookies
console.log(document.cookie);

// 查看特定 cookie
console.log(document.cookie.split('; ').find(c => c.startsWith('shareToken=')));
```

---

## ❓ 常见问题

### Q1: 某些 Cookie 无法导入

**现象:**
```
⚠ sessionId (可能因 httpOnly 限制无法设置)
```

**原因:**
- Cookie 带有 `httpOnly` 标志
- 只能由服务器设置，JavaScript 无法访问

**解决:**
- `httpOnly` 的 Cookie 会在正常登录后由服务器自动设置
- 导入其他 Cookie 后刷新页面即可

---

### Q2: 导入后还是未登录状态

**可能原因:**
1. Cookie 已过期
2. 缺少关键 Cookie
3. 需要刷新页面

**解决步骤:**
1. 先刷新页面 (F5)
2. 检查 Cookie 是否存在（Application 标签）
3. 确认 Cookie 的域名和路径正确
4. 如仍未登录，重新获取最新的 Cookie

---

### Q3: 如何更新 Cookie 文件

#### 从浏览器导出当前 Cookie

1. **方法 A: 使用开发者工具**
   - F12 → Application → Cookies
   - 右键某个域名 → Clear (清除旧的)
   - 重新登录
   - 手动复制需要的 Cookie

2. **方法 B: 使用控制台导出**
   ```javascript
   // 导出所有 cookies 为 JSON
   const cookies = document.cookie.split('; ').map(c => {
       const [name, value] = c.split('=');
       return {name, value};
   });
   console.log(JSON.stringify(cookies, null, 2));
   ```

3. **方法 C: 使用浏览器扩展**
   - 安装 "EditThisCookie" 或类似扩展
   - 导出 Cookie 为 JSON 格式
   - 保存到对应的 cookie 文件

---

### Q4: domain 和 path 应该设置什么

**推荐配置:**
```javascript
domain: '.wx.10086.cn'  // 带点表示包括所有子域名
path: '/'               // 整个网站都可用
```

**说明:**
- `.wx.10086.cn` - 对 wx.10086.cn 及其所有子域名有效
- `wx.10086.cn` - 仅对主域名有效（不推荐）
- `/` - 网站所有页面都可用
- `/website/` - 仅该路径下可用

---

### Q5: Cookie 多久会过期

**查看过期时间:**

在 Application → Cookies 中查看 `Expires / Max-Age` 列

**设置过期时间:**

```javascript
// 30天后过期
document.cookie = "name=value; max-age=2592000";

// 指定具体时间
const expires = new Date('2025-12-31').toUTCString();
document.cookie = `name=value; expires=${expires}`;

// 会话 Cookie（关闭浏览器即失效）
document.cookie = "name=value";
```

---

## 🛠️ 工具文件说明

| 文件 | 说明 | 使用场景 |
|-----|------|---------|
| `generate_cookie_import_script.py` | Python 脚本生成器 | 自动生成导入脚本 |
| `browser_cookie_importer_template.js` | 通用 JS 模板 | 手动修改后使用 |
| `import_user1_cookies.js` | user1 导入脚本 | 直接在控制台执行 |
| `import_user2_cookies.js` | user2 导入脚本 | 直接在控制台执行 |
| `convert_cookies_for_devtools.js` | Node.js 转换工具 | 格式转换 |

---

## 💡 最佳实践

### 1. Cookie 管理建议

- ✅ 定期更新 Cookie 文件
- ✅ 不要分享 Cookie 文件（包含登录凭证）
- ✅ 使用不同文件夹管理不同用户
- ✅ 及时删除过期的 Cookie

### 2. 导入前检查

```javascript
// 导入前先清除旧 cookies
document.cookie.split(';').forEach(c => {
    document.cookie = c.trim().split('=')[0] + '=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;domain=.wx.10086.cn';
});
console.log('Old cookies cleared');
```

### 3. 批量导入多个用户

```bash
# 生成 user1
python utools/generate_cookie_import_script.py

# 生成 user2  
python utools/generate_cookie_import_script.py
```

然后在浏览器中：
- 使用隐身窗口测试 user1
- 使用普通窗口测试 user2

---

## 🔐 安全提示

⚠️ **重要提醒:**

1. **不要分享 Cookie**
   - Cookie 包含登录凭证
   - 他人获取后可以冒充你的身份

2. **不要上传到公开位置**
   - 不要提交到 Git 仓库
   - 不要上传到公开的网盘

3. **定期更新**
   - Cookie 会过期
   - 定期重新登录更新

4. **使用后清理**
   - 测试完成后清除浏览器 Cookie
   - 或使用隐身模式

---

## 📚 参考资料

### Cookie 属性说明

| 属性 | 说明 | 示例 |
|-----|------|------|
| `name` | Cookie 名称 | `shareToken` |
| `value` | Cookie 值 | `m-gp5A.ybB2rH-...` |
| `domain` | 有效域名 | `.wx.10086.cn` |
| `path` | 有效路径 | `/` |
| `expires` | 过期时间 | `Wed, 31 Dec 2025 23:59:59 GMT` |
| `max-age` | 有效时长（秒） | `2592000` (30天) |
| `secure` | 仅 HTTPS | `true` |
| `httpOnly` | 仅服务器访问 | `true` |
| `sameSite` | 跨站策略 | `Lax`, `Strict`, `None` |

### 控制台常用命令

```javascript
// 查看所有 cookies
document.cookie

// 设置 cookie
document.cookie = "name=value; path=/"

// 删除 cookie
document.cookie = "name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/"

// 格式化显示 cookies
console.table(document.cookie.split('; ').map(c => {
    const [name, ...rest] = c.split('=');
    return {name, value: rest.join('=')};
}))
```

---

**最后更新**: 2025-12-17

