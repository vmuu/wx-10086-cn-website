// ==========================================
// 通过浏览器开发者工具设置 httpOnly Cookie
// 使用方法：在 Application → Storage → Cookies 中运行
// ==========================================

// 必要的 Cookies（包括 httpOnly）
const cookies = [
    {
        name: 'clientId',
        value: '2d716501-5442-4d9b-9553-1cdb704be5c2',
        domain: 'wx.10086.cn',
        path: '/',
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
        expirationDate: 1768453584
    },
    {
        name: 'shareToken',
        value: 'm-gp5A.ybB2rH-SvcwSmu627Lr0hC4WSMjs_e2FJA2VnjLtQqqpniUspaD53By-8tfKAyw-2VtAJxqxdVxaiLgnnwbn9eJlWwla3jpvizJ_q0IVJWpnBFUftdWHq8PD-nFeuWMQgNBUxuKl.Mme7Jd8FpVT9L80+LC1jnizd0rOPuTaeXhK0Riew5MMRciLG+ceuAcBAK0Mc7EZbNddVLjoctH7eU4SeXyZ7yQ==',
        domain: 'wx.10086.cn',
        path: '/',
        httpOnly: true,  // 这个需要特殊处理
        secure: false,
        sameSite: 'Lax',
        expirationDate: 1765872956
    },
    {
        name: 'riskToken',
        value: '6940e7d4h8TfdNBFh64W2HN3epAMLUumjHx7drh1',
        domain: 'wx.10086.cn',
        path: '/',
        httpOnly: true,  // 这个需要特殊处理
        secure: false,
        sameSite: 'Lax',
        expirationDate: 1765947986
    },
    {
        name: 'uuid',
        value: '8a0e9d48-3dea-4ce9-81e4-3f5b0a27cedb',
        domain: 'wx.10086.cn',
        path: '/',
        httpOnly: false,
        secure: false,
        sameSite: 'Lax',
        expirationDate: 1768510147
    }
];

// 使用说明
console.log('%c📝 Cookie 手动导入指南', 'font-size: 16px; font-weight: bold; color: #4CAF50;');
console.log('\n由于 shareToken 和 riskToken 是 httpOnly Cookie，需要手动添加：\n');
console.log('方法 1 - 使用浏览器扩展（推荐）:');
console.log('  1. 安装 "EditThisCookie" 或 "Cookie-Editor" 扩展');
console.log('  2. 点击扩展图标');
console.log('  3. 导入下面的 Cookie JSON\n');

console.log('方法 2 - 手动在开发者工具添加:');
console.log('  1. F12 → Application → Storage → Cookies');
console.log('  2. 选择 https://wx.10086.cn');
console.log('  3. 双击空白处，手动添加每个 Cookie\n');

console.log('方法 3 - 使用 Puppeteer/Playwright 脚本（高级）\n');

console.log('%c复制以下 JSON 到扩展中:', 'font-weight: bold; color: #2196F3;');
console.log(JSON.stringify(cookies, null, 2));

console.log('\n%c或者逐个复制以下值:', 'font-weight: bold; color: #2196F3;');
cookies.forEach(c => {
    console.log(`\n${c.name}:`);
    console.log(`  值: ${c.value}`);
    console.log(`  域名: ${c.domain}`);
    console.log(`  路径: ${c.path}`);
    console.log(`  httpOnly: ${c.httpOnly}`);
});

