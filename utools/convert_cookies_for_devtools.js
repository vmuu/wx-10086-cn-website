// 将 cooike_user2.json 转换为可在浏览器中使用的格式
const fs = require('fs');

const cookies = JSON.parse(fs.readFileSync('user2/cooike_user2.json', 'utf8'));

// 转换为 Chrome DevTools 可以使用的格式
const chromeCookies = cookies.map(cookie => ({
    name: cookie.name,
    value: cookie.value,
    domain: cookie.domain,
    path: cookie.path,
    expires: cookie.expirationDate,
    httpOnly: cookie.httpOnly,
    secure: cookie.secure,
    sameSite: cookie.sameSite || 'Lax'
}));

console.log(JSON.stringify(chromeCookies, null, 2));

