#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成精简的 Cookie 导入脚本
只导入必要的关键 Cookie，并在导入前清空旧 Cookie
"""
import json
import sys

# 定义必要的 Cookie 键名（只包含非 httpOnly 的）
ESSENTIAL_COOKIES = [
    'uuid',            # 用户唯一标识
    'clientId',        # 客户端ID
    'grayscale',       # 灰度标识
    # httpOnly 的 Cookie 无法通过 JS 设置，需要用扩展或手动添加：
    # 'shareToken',    # httpOnly: true - 用扩展导入
    # 'riskToken',     # httpOnly: true - 用扩展导入
]

def generate_essential_cookie_script(cookie_file, user_name="user"):
    """
    生成只包含必要 Cookie 的导入脚本
    
    Args:
        cookie_file: cookie JSON 文件路径
        user_name: 用户名称
        
    Returns:
        JavaScript 代码字符串
    """
    try:
        # 读取 cookie 文件
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        # 确保是列表格式
        if isinstance(cookies, dict):
            cookies = [{"name": k, "value": v} for k, v in cookies.items()]
        
        # 筛选出必要的 cookies
        essential_cookies = [
            c for c in cookies 
            if c.get('name') in ESSENTIAL_COOKIES
        ]
        
        if not essential_cookies:
            print(f"[WARNING] 未找到任何必要的 Cookie!")
            print(f"[INFO] 必要的 Cookie 列表: {', '.join(ESSENTIAL_COOKIES)}")
            return None
        
        # 生成 JavaScript 代码
        js_code = f"""// ==========================================
// {user_name} 精简 Cookie 导入脚本
// 自动清空旧 Cookie + 只导入必要 Cookie
// ==========================================

(async function() {{
    console.log('%c🚀 开始导入 {user_name} 的必要 Cookies...', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    
    // ==========================================
    // 步骤 1: 清空旧的 Cookies
    // ==========================================
    console.log('\\n%c📝 步骤 1: 清空旧 Cookies', 'color: #2196F3; font-weight: bold;');
    
    const oldCookies = document.cookie.split('; ');
    let clearCount = 0;
    
    // 清空当前域名的所有 cookies
    oldCookies.forEach(cookie => {{
        const name = cookie.split('=')[0];
        if (name) {{
            // 尝试多种方式删除 cookie
            const domains = ['', '.wx.10086.cn', 'wx.10086.cn', '.10086.cn'];
            const paths = ['/', '/website', '/website/'];
            
            domains.forEach(domain => {{
                paths.forEach(path => {{
                    let deleteStr = `${{name}}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${{path}}`;
                    if (domain) {{
                        deleteStr += `; domain=${{domain}}`;
                    }}
                    document.cookie = deleteStr;
                }});
            }});
            
            clearCount++;
        }}
    }});
    
    console.log(`✓ 已清空 ${{clearCount}} 个旧 Cookie`);
    
    // 等待一下确保清空生效
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // ==========================================
    // 步骤 2: 导入必要的 Cookies
    // ==========================================
    console.log('\\n%c📝 步骤 2: 导入必要 Cookies', 'color: #2196F3; font-weight: bold;');
    
    const essentialCookies = {json.dumps(essential_cookies, indent=4, ensure_ascii=False)};
    
    console.log(`准备导入 ${{essentialCookies.length}} 个必要 Cookie:`);
    console.log(essentialCookies.map(c => c.name).join(', '));
    
    let successCount = 0;
    let failCount = 0;
    const results = [];
    
    for (const cookie of essentialCookies) {{
        try {{
            let cookieStr = `${{cookie.name}}=${{cookie.value}}`;
            
            // 设置域名
            const domain = cookie.domain || '.wx.10086.cn';
            cookieStr += `; domain=${{domain}}`;
            
            // 设置路径
            cookieStr += `; path=${{cookie.path || '/'}}`;
            
            // 设置过期时间
            if (cookie.expirationDate) {{
                const expires = new Date(cookie.expirationDate * 1000).toUTCString();
                cookieStr += `; expires=${{expires}}`;
            }} else {{
                // 默认30天
                cookieStr += `; max-age=2592000`;
            }}
            
            // 设置其他属性
            if (cookie.secure) {{
                cookieStr += '; secure';
            }}
            
            if (cookie.sameSite) {{
                cookieStr += `; samesite=${{cookie.sameSite}}`;
            }}
            
            // 设置 cookie
            document.cookie = cookieStr;
            
            // 验证
            const isSet = document.cookie.includes(`${{cookie.name}}=`);
            
            if (isSet) {{
                console.log(`%c✓ ${{cookie.name}}`, 'color: #4CAF50');
                successCount++;
                results.push({{name: cookie.name, status: '✓ 成功', value: cookie.value.substring(0, 30) + '...'}});
            }} else {{
                console.warn(`%c⚠ ${{cookie.name}} (可能因限制无法设置)`, 'color: #FF9800');
                failCount++;
                results.push({{name: cookie.name, status: '⚠ 警告', value: '未能设置'}});
            }}
            
        }} catch (e) {{
            console.error(`%c✗ ${{cookie.name}}: ${{e.message}}`, 'color: #F44336');
            failCount++;
            results.push({{name: cookie.name, status: '✗ 失败', value: e.message}});
        }}
    }}
    
    // ==========================================
    // 步骤 3: 显示结果
    // ==========================================
    console.log('\\n' + '='.repeat(60));
    console.log('%c✅ 导入完成!', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    console.log('='.repeat(60));
    console.log(`✓ 成功: ${{successCount}}`);
    console.log(`✗ 失败: ${{failCount}}`);
    console.log(`📊 总计: ${{essentialCookies.length}}`);
    
    console.log('\\n详细结果:');
    console.table(results);
    
    // 显示当前的 cookies
    console.log('\\n当前网站的所有 Cookies:');
    const currentCookies = document.cookie.split('; ').filter(c => c).map(c => {{
        const [name, value] = c.split('=');
        return {{
            name, 
            value: value ? (value.substring(0, 40) + (value.length > 40 ? '...' : '')) : ''
        }};
    }});
    console.table(currentCookies);
    
    // ==========================================
    // 步骤 4: 下一步提示
    // ==========================================
    console.log('\\n%c💡 下一步操作:', 'color: #2196F3; font-size: 14px; font-weight: bold;');
    console.log('1️⃣  刷新页面 (按 F5 或 Ctrl+R)');
    console.log('2️⃣  检查是否已登录');
    console.log('3️⃣  如果仍未登录，可能需要重新获取最新的 Cookie');
    
    if (failCount > 0) {{
        console.log('\\n%c⚠️ 注意:', 'color: #FF9800; font-size: 14px; font-weight: bold;');
        console.log('部分 Cookie 可能因 httpOnly 或其他限制无法设置');
        console.log('刷新页面后，这些 Cookie 会由服务器自动设置');
    }}
    
    console.log('\\n%c🎉 全部完成! 请刷新页面查看效果', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    
    return {{
        cleared: clearCount,
        success: successCount,
        failed: failCount,
        total: essentialCookies.length,
        results: results
    }};
}})();
"""
        
        return js_code
        
    except FileNotFoundError:
        print(f"[ERROR] Cookie 文件不存在: {cookie_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 解析失败: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("精简 Cookie 导入脚本生成器")
    print("=" * 80)
    
    # 用户列表
    users = {
        "1": {"name": "user1", "file": "user1/cooike_user1.json"},
        "2": {"name": "user2", "file": "user2/cooike_user2.json"},
    }
    
    print("\n可用用户:")
    for key, user in users.items():
        print(f"  {key}. {user['name']} ({user['file']})")
    
    print(f"\n必要的 Cookie 列表:")
    for cookie_name in ESSENTIAL_COOKIES:
        print(f"  - {cookie_name}")
    
    choice = input("\n选择用户 (1-2): ").strip()
    
    if choice not in users:
        print("[ERROR] 无效选择")
        return
    
    selected_user = users[choice]
    
    print(f"\n正在生成 {selected_user['name']} 的精简导入脚本...")
    
    # 生成脚本
    js_code = generate_essential_cookie_script(selected_user['file'], selected_user['name'])
    
    if not js_code:
        print("[ERROR] 脚本生成失败")
        return
    
    # 保存到文件
    output_file = f"utools/import_{selected_user['name']}_essential.js"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"[SUCCESS] 脚本已保存到: {output_file}")
    
    # 输出使用说明
    print("\n" + "=" * 80)
    print("特性:")
    print("=" * 80)
    print("""
[+] 自动清空旧 Cookie（避免冲突）
[+] 只导入必要的关键 Cookie（更安全）
[+] 彩色输出，一目了然
[+] 详细的执行反馈
[+] 自动验证导入结果
""")
    
    print("=" * 80)
    print("使用方法:")
    print("=" * 80)
    print(f"""
1. 打开浏览器并访问 https://wx.10086.cn
2. 按 F12 打开开发者工具
3. 切换到 Console (控制台) 标签
4. 复制文件内容: {output_file}
5. 粘贴到控制台并按回车执行
6. 等待显示 "全部完成!"
7. 刷新页面 (F5)

提示:
- 该脚本会先清空所有旧 Cookie
- 只导入 {len(ESSENTIAL_COOKIES)} 个必要的 Cookie
- 更安全、更干净、更快速
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户中断")
    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()

