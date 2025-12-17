# Cookie 导入快速指南 ⚡

## 🌟 推荐：精简版（自动清空 + 只导入4个关键Cookie）

### 📂 直接使用现成脚本
1. 打开 `utools/import_user2_essential.js`
2. 全选复制（Ctrl+A, Ctrl+C）
3. 浏览器控制台执行（详见下方）

✅ **自动清空旧Cookie，避免冲突！**

---

## 📖 详细步骤

### 1️⃣ 生成脚本（可选）

**精简版**（推荐）- 只导入4个必要Cookie：
```bash
cd d:\work\10086
python utools/import_essential_cookies.py
```

**完整版** - 导入所有Cookie：
```bash
cd d:\work\10086
python utools/generate_cookie_import_script.py
```

选择用户后，会生成脚本文件

---

### 2️⃣ 复制脚本

打开生成的 `.js` 文件，全选复制（Ctrl+A, Ctrl+C）

---

### 3️⃣ 浏览器执行

1. 访问 https://wx.10086.cn
2. 按 **F12** 打开控制台
3. 切换到 **Console** 标签
4. **粘贴代码**并按回车
5. 看到 "导入完成!" 后按 **F5 刷新**

✅ 完成！

---

## 🚀 超级快速版（一行命令）

如果你想更快，直接在浏览器控制台执行：

```javascript
// User2 快速导入（替换为你的实际 Cookie 数据）
(function(){const c=[{name:"shareToken",value:"YOUR_VALUE"},{name:"riskToken",value:"YOUR_VALUE"},{name:"uuid",value:"YOUR_VALUE"},{name:"clientId",value:"YOUR_VALUE"}];c.forEach(x=>document.cookie=`${x.name}=${x.value}; domain=.wx.10086.cn; path=/; max-age=2592000`);console.log("✓ Done! Press F5");})();
```

**修改方法:**
1. 打开 `user2/cooike_user2.json`
2. 找到 `shareToken`, `riskToken`, `uuid`, `clientId` 的值
3. 替换上面代码中的 `YOUR_VALUE`
4. 粘贴到控制台执行

---

## 📱 手机端导入

手机浏览器通常不支持开发者工具，建议：
1. 直接在手机上登录（最简单）
2. 或使用桌面模式 + 远程调试

---

## ⚡ 常用快捷键

| 操作 | 快捷键 |
|-----|-------|
| 打开控制台 | **F12** 或 **Ctrl+Shift+I** |
| 清空控制台 | **Ctrl+L** |
| 刷新页面 | **F5** 或 **Ctrl+R** |
| 强制刷新 | **Ctrl+F5** 或 **Ctrl+Shift+R** |

---

## 🆘 遇到问题？

### Cookie 导入失败
→ 检查是否在正确的域名 (wx.10086.cn)

### 导入后还是未登录
→ 刷新页面 (F5)

### 某些 Cookie 显示警告
→ 正常，httpOnly 的 Cookie 会在刷新后自动设置

---

**详细文档**: 查看 `README_COOKIE_IMPORT.md`

