function p(t) {
    const crypto = require('crypto-js');
    var u= crypto.enc.Utf8.parse("jo8j9wGw%6HbxfFn"),
        d = crypto.enc.Utf8.parse("0123456789ABCDEF");
    e = crypto.enc.Hex.parse(t);
    a = crypto.enc.Base64.stringify(e);
    n = crypto.AES.decrypt(a, u,
    {
        iv: d,
        mode: crypto.mode.CBC,
        padding: crypto.pad.Pkcs7
    }),
    i = n.toString(crypto.enc.Utf8);
    return i;
    // return i.toString();
}

