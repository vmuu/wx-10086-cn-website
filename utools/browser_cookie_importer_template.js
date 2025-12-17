// ==========================================
// Cookie 手动导入模板
// 使用方法：
// 1. 将下面的 COOKIES_DATA 替换为你的 cookie 数据
// 2. 复制整个脚本到浏览器控制台执行
// ==========================================

(async function() {
    console.log('%c开始导入 Cookies...', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    
    // ====================================
    // 在这里粘贴你的 Cookie 数据
    // 格式1: [{"name": "cookie1", "value": "value1"}, ...]
    // 格式2: {"cookie1": "value1", "cookie2": "value2", ...}
    // ====================================
    const COOKIES_DATA = [
        // 示例数据，请替换为实际数据
        {"name": "shareToken", "value": "your_token_here"},
        {"name": "riskToken", "value": "your_token_here"},
        {"name": "uuid", "value": "your_uuid_here"},
        {"name": "clientId", "value": "your_client_id_here"}
    ];
    
    // ====================================
    // 配置项
    // ====================================
    const CONFIG = {
        domain: '.wx.10086.cn',  // Cookie 域名
        path: '/',               // Cookie 路径
        secure: true,            // 是否需要 HTTPS
        sameSite: 'Lax',        // SameSite 属性
        maxAge: 86400 * 30      // 过期时间（秒），默认30天
    };
    
    // ====================================
    // 自动检测数据格式并转换
    // ====================================
    let cookies = COOKIES_DATA;
    
    // 如果是对象格式，转换为数组格式
    if (!Array.isArray(cookies) && typeof cookies === 'object') {
        cookies = Object.entries(cookies).map(([name, value]) => ({name, value}));
    }
    
    // ====================================
    // 开始导入
    // ====================================
    console.log(`准备导入 ${cookies.length} 个 Cookies...`);
    
    let successCount = 0;
    let failCount = 0;
    const results = [];
    
    for (const cookie of cookies) {
        try {
            // 构建 cookie 字符串
            let cookieStr = `${cookie.name}=${cookie.value}`;
            
            // 添加域名
            cookieStr += `; domain=${cookie.domain || CONFIG.domain}`;
            
            // 添加路径
            cookieStr += `; path=${cookie.path || CONFIG.path}`;
            
            // 添加过期时间
            if (cookie.expirationDate) {
                const expires = new Date(cookie.expirationDate * 1000).toUTCString();
                cookieStr += `; expires=${expires}`;
            } else {
                cookieStr += `; max-age=${CONFIG.maxAge}`;
            }
            
            // 添加 secure
            if (cookie.secure || CONFIG.secure) {
                cookieStr += '; secure';
            }
            
            // 添加 sameSite
            const sameSite = cookie.sameSite || CONFIG.sameSite;
            if (sameSite) {
                cookieStr += `; samesite=${sameSite}`;
            }
            
            // 设置 cookie
            document.cookie = cookieStr;
            
            // 验证是否设置成功
            const currentCookies = document.cookie;
            const isSet = currentCookies.includes(`${cookie.name}=`);
            
            if (isSet) {
                console.log(`%c✓ ${cookie.name}`, 'color: #4CAF50');
                successCount++;
                results.push({name: cookie.name, status: 'success'});
            } else {
                console.warn(`%c⚠ ${cookie.name} (可能因 httpOnly 限制无法设置)`, 'color: #FF9800');
                failCount++;
                results.push({name: cookie.name, status: 'warning', reason: 'httpOnly or other restriction'});
            }
            
        } catch (e) {
            console.error(`%c✗ ${cookie.name}: ${e.message}`, 'color: #F44336');
            failCount++;
            results.push({name: cookie.name, status: 'error', error: e.message});
        }
    }
    
    // ====================================
    // 显示结果
    // ====================================
    console.log('\n' + '='.repeat(60));
    console.log('%c导入完成!', 'color: #4CAF50; font-size: 14px; font-weight: bold;');
    console.log('='.repeat(60));
    console.log(`✓ 成功: ${successCount}`);
    console.log(`✗ 失败: ${failCount}`);
    console.log(`总计: ${cookies.length}`);
    
    // 显示详细结果
    console.log('\n详细结果:');
    console.table(results);
    
    // 显示当前所有 cookies
    console.log('\n当前网站的所有 Cookies:');
    const currentCookies = document.cookie.split('; ').map(c => {
        const [name, value] = c.split('=');
        return {name, value: value.substring(0, 50) + (value.length > 50 ? '...' : '')};
    });
    console.table(currentCookies);
    
    // 给出建议
    console.log('\n%c💡 下一步操作:', 'color: #2196F3; font-size: 14px; font-weight: bold;');
    console.log('1. 刷新页面 (按 F5)');
    console.log('2. 查看 Application → Cookies 验证导入结果');
    console.log('3. 如果登录失败，可能需要重新获取 Cookie');
    
    if (failCount > 0) {
        console.log('\n%c⚠️ 注意:', 'color: #FF9800; font-size: 14px; font-weight: bold;');
        console.log('有些 Cookie 可能因为 httpOnly 或 secure 标志无法通过控制台设置');
        console.log('这些 Cookie 通常由服务器设置，可能需要通过正常登录获取');
    }
    
    return {
        success: successCount,
        failed: failCount,
        total: cookies.length,
        results: results
    };
})();

