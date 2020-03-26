function get_sign(parma) {
    const sha1 = require("sha1");
    let t = Math.floor((parma - 99) / 99);
    let sign = sha1('Xr0Z-javascript-obfuscation-1' + t);
    return {"t": t, "sign":sign}
}