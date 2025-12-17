// ==========================================
// user2 精简 Cookie 导入脚本
// 自动清空旧 Cookie + 只导入必要 Cookie
// ==========================================

(async function() {
    console.log('%c🚀 开始导入 user2 的必要 Cookies...', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    
    // ==========================================
    // 步骤 1: 清空旧的 Cookies
    // ==========================================
    console.log('\n%c📝 步骤 1: 清空旧 Cookies', 'color: #2196F3; font-weight: bold;');
    
    const oldCookies = document.cookie.split('; ');
    let clearCount = 0;
    
    // 清空当前域名的所有 cookies
    oldCookies.forEach(cookie => {
        const name = cookie.split('=')[0];
        if (name) {
            // 尝试多种方式删除 cookie
            const domains = ['', '.wx.10086.cn', 'wx.10086.cn', '.10086.cn'];
            const paths = ['/', '/website', '/website/'];
            
            domains.forEach(domain => {
                paths.forEach(path => {
                    let deleteStr = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path}`;
                    if (domain) {
                        deleteStr += `; domain=${domain}`;
                    }
                    document.cookie = deleteStr;
                });
            });
            
            clearCount++;
        }
    });
    
    console.log(`✓ 已清空 ${clearCount} 个旧 Cookie`);
    
    // 等待一下确保清空生效
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // ==========================================
    // 步骤 2: 导入必要的 Cookies
    // ==========================================
    console.log('\n%c📝 步骤 2: 导入必要 Cookies', 'color: #2196F3; font-weight: bold;');
    
    const essentialCookies = [
    {
        "domain": "wx.10086.cn",
        "expirationDate": 1768453584.811288,
        "hostOnly": true,
        "httpOnly": false,
        "name": "clientId",
        "path": "/",
        "sameSite": null,
        "secure": false,
        "session": false,
        "storeId": null,
        "value": "2d716501-5442-4d9b-9553-1cdb704be5c2"
    },
    {
        "domain": "wx.10086.cn",
        "expirationDate": 1765878355.705206,
        "hostOnly": true,
        "httpOnly": false,
        "name": "grayscale",
        "path": "/",
        "sameSite": null,
        "secure": false,
        "session": false,
        "storeId": null,
        "value": "luoyang"
    },
    {
        "domain": "wx.10086.cn",
        "expirationDate": 1766120786.811395,
        "hostOnly": true,
        "httpOnly": true,
        "name": "uuid",
        "path": "/",
        "sameSite": null,
        "secure": false,
        "session": false,
        "storeId": null,
        "value": "8a0e9d48-3dea-4ce9-a370-452a70951dd7"
    }
];
    
    console.log(`准备导入 ${essentialCookies.length} 个必要 Cookie:`);
    console.log(essentialCookies.map(c => c.name).join(', '));
    
    let successCount = 0;
    let failCount = 0;
    const results = [];
    
    for (const cookie of essentialCookies) {
        try {
            let cookieStr = `${cookie.name}=${cookie.value}`;
            
            // 设置域名
            const domain = cookie.domain || '.wx.10086.cn';
            cookieStr += `; domain=${domain}`;
            
            // 设置路径
            cookieStr += `; path=${cookie.path || '/'}`;
            
            // 设置过期时间
            if (cookie.expirationDate) {
                const expires = new Date(cookie.expirationDate * 1000).toUTCString();
                cookieStr += `; expires=${expires}`;
            } else {
                // 默认30天
                cookieStr += `; max-age=2592000`;
            }
            
            // 设置其他属性
            if (cookie.secure) {
                cookieStr += '; secure';
            }
            
            if (cookie.sameSite) {
                cookieStr += `; samesite=${cookie.sameSite}`;
            }
            
            // 设置 cookie
            document.cookie = cookieStr;
            
            // 验证
            const isSet = document.cookie.includes(`${cookie.name}=`);
            
            if (isSet) {
                console.log(`%c✓ ${cookie.name}`, 'color: #4CAF50');
                successCount++;
                results.push({name: cookie.name, status: '✓ 成功', value: cookie.value.substring(0, 30) + '...'});
            } else {
                console.warn(`%c⚠ ${cookie.name} (可能因限制无法设置)`, 'color: #FF9800');
                failCount++;
                results.push({name: cookie.name, status: '⚠ 警告', value: '未能设置'});
            }
            
        } catch (e) {
            console.error(`%c✗ ${cookie.name}: ${e.message}`, 'color: #F44336');
            failCount++;
            results.push({name: cookie.name, status: '✗ 失败', value: e.message});
        }
    }
    
    // ==========================================
    // 步骤 3: 显示结果
    // ==========================================
    console.log('\n' + '='.repeat(60));
    console.log('%c✅ 导入完成!', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    console.log('='.repeat(60));
    console.log(`✓ 成功: ${successCount}`);
    console.log(`✗ 失败: ${failCount}`);
    console.log(`📊 总计: ${essentialCookies.length}`);
    
    console.log('\n详细结果:');
    console.table(results);
    
    // 显示当前的 cookies
    console.log('\n当前网站的所有 Cookies:');
    const currentCookies = document.cookie.split('; ').filter(c => c).map(c => {
        const [name, value] = c.split('=');
        return {
            name, 
            value: value ? (value.substring(0, 40) + (value.length > 40 ? '...' : '')) : ''
        };
    });
    console.table(currentCookies);
    
    // ==========================================
    // 步骤 4: 下一步提示
    // ==========================================
    console.log('\n%c💡 下一步操作:', 'color: #2196F3; font-size: 14px; font-weight: bold;');
    console.log('1️⃣  刷新页面 (按 F5 或 Ctrl+R)');
    console.log('2️⃣  检查是否已登录');
    console.log('3️⃣  如果仍未登录，可能需要重新获取最新的 Cookie');
    
    if (failCount > 0) {
        console.log('\n%c⚠️ 注意:', 'color: #FF9800; font-size: 14px; font-weight: bold;');
        console.log('部分 Cookie 可能因 httpOnly 或其他限制无法设置');
        console.log('刷新页面后，这些 Cookie 会由服务器自动设置');
    }
    
    console.log('\n%c🎉 全部完成! 请刷新页面查看效果', 'color: #4CAF50; font-size: 16px; font-weight: bold;');
    
    return {
        cleared: clearCount,
        success: successCount,
        failed: failCount,
        total: essentialCookies.length,
        results: results
    };
})();
