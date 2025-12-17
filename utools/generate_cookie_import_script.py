#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成可在浏览器控制台执行的 Cookie 导入代码
"""
import json
import sys

def generate_cookie_script(cookie_file, user_name="user"):
    """
    生成浏览器控制台可执行的 Cookie 导入脚本
    
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
        
        # 生成 JavaScript 代码
        js_code = f"""// ==========================================
// {user_name} Cookie 导入脚本
// 自动生成，可直接在浏览器控制台执行
// ==========================================

(async function() {{
    console.log('开始导入 {user_name} 的 Cookies...');
    
    const cookies = {json.dumps(cookies, indent=4, ensure_ascii=False)};
    
    let successCount = 0;
    let failCount = 0;
    
    // 方式1: 使用 document.cookie（简单但有限制）
    console.log('\\n方式1: 使用 document.cookie 设置');
    for (const cookie of cookies) {{
        try {{
            let cookieStr = `${{cookie.name}}=${{cookie.value}}`;
            
            // 添加可选属性
            if (cookie.domain) {{
                cookieStr += `; domain=${{cookie.domain}}`;
            }} else {{
                cookieStr += '; domain=.wx.10086.cn';
            }}
            
            if (cookie.path) {{
                cookieStr += `; path=${{cookie.path}}`;
            }} else {{
                cookieStr += '; path=/';
            }}
            
            if (cookie.secure) {{
                cookieStr += '; secure';
            }}
            
            if (cookie.sameSite) {{
                cookieStr += `; samesite=${{cookie.sameSite}}`;
            }}
            
            if (cookie.expirationDate) {{
                const expires = new Date(cookie.expirationDate * 1000).toUTCString();
                cookieStr += `; expires=${{expires}}`;
            }}
            
            document.cookie = cookieStr;
            console.log(`✓ ${{cookie.name}}`);
            successCount++;
        }} catch (e) {{
            console.error(`✗ ${{cookie.name}}: ${{e.message}}`);
            failCount++;
        }}
    }}
    
    console.log(`\\n导入完成! 成功: ${{successCount}}, 失败: ${{failCount}}`);
    console.log('\\n当前 Cookies:');
    console.log(document.cookie);
    
    // 如果在 Chrome DevTools，也可以尝试使用 Chrome API
    if (typeof chrome !== 'undefined' && chrome.cookies) {{
        console.log('\\n检测到 Chrome API，可以使用更强大的方式导入');
        console.log('注意: 这需要在扩展程序环境中执行');
    }}
    
    console.log('\\n提示: 导入后请刷新页面使 Cookie 生效');
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
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("浏览器 Cookie 导入脚本生成器")
    print("=" * 80)
    
    # 用户列表
    users = {
        "1": {"name": "user1", "file": "user1/cooike_user1.json"},
        "2": {"name": "user2", "file": "user2/cooike_user2.json"},
    }
    
    print("\n可用用户:")
    for key, user in users.items():
        print(f"  {key}. {user['name']} ({user['file']})")
    
    choice = input("\n选择用户 (1-2): ").strip()
    
    if choice not in users:
        print("[ERROR] 无效选择")
        return
    
    selected_user = users[choice]
    
    print(f"\n正在生成 {selected_user['name']} 的导入脚本...")
    
    # 生成脚本
    js_code = generate_cookie_script(selected_user['file'], selected_user['name'])
    
    if not js_code:
        print("[ERROR] 脚本生成失败")
        return
    
    # 保存到文件
    output_file = f"utools/import_{selected_user['name']}_cookies.js"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"[SUCCESS] 脚本已保存到: {output_file}")
    
    # 输出使用说明
    print("\n" + "=" * 80)
    print("使用方法:")
    print("=" * 80)
    print(f"""
1. 打开浏览器并访问 https://wx.10086.cn
2. 按 F12 打开开发者工具
3. 切换到 Console (控制台) 标签
4. 复制以下文件的全部内容: {output_file}
5. 粘贴到控制台并按回车执行
6. 等待显示 "导入完成!"
7. 刷新页面 (F5)

提示:
- 如果某些 Cookie 导入失败，可能是因为 httpOnly 或 secure 限制
- 导入后建议立即刷新页面
- 可以在 Application → Cookies 中查看导入的 Cookie
""")
    
    # 询问是否直接显示代码
    show_code = input("\n是否在控制台显示代码? (y/n): ").strip().lower()
    
    if show_code == 'y':
        print("\n" + "=" * 80)
        print("复制以下代码到浏览器控制台:")
        print("=" * 80)
        print(js_code)
        print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户中断")
    except Exception as e:
        print(f"\n[ERROR] 发生错误: {e}")
        import traceback
        traceback.print_exc()

