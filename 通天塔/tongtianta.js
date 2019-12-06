/*
通天塔JS
传入参数t,e分别为请求网页返回的cookie所带有的user_id=24497; access_token=vf9HTrLEuuRjGtlwV9ionjIFIGnmunF1
通过本JS计算得到所需请求的参数nonce_str以及sign
*/
function get_parma(t, e){
    function get_sign(e, n) {
        var t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
          , n = {
            rotl: function(e, t) {
                return e << t | e >>> 32 - t
            },
            rotr: function(e, t) {
                return e << 32 - t | e >>> t
            },
            endian: function(e) {
                if (e.constructor == Number)
                    return 16711935 & n.rotl(e, 8) | 4278255360 & n.rotl(e, 24);
                for (var t = 0; t < e.length; t++)
                    e[t] = n.endian(e[t]);
                return e
            },
            randomBytes: function(e) {
                for (var t = []; e > 0; e--)
                    t.push(Math.floor(256 * Math.random()));
                return t
            },
            bytesToWords: function(e) {
                for (var t = [], n = 0, r = 0; n < e.length; n++,
                r += 8)
                    t[r >>> 5] |= e[n] << 24 - r % 32;
                return t
            },
            wordsToBytes: function(e) {
                for (var t = [], n = 0; n < 32 * e.length; n += 8)
                    t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
                return t
            },
            bytesToHex: function(e) {
                for (var t = [], n = 0; n < e.length; n++)
                    t.push((e[n] >>> 4).toString(16)),
                    t.push((15 & e[n]).toString(16));
                return t.join("")
            },
            hexToBytes: function(e) {
                for (var t = [], n = 0; n < e.length; n += 2)
                    t.push(parseInt(e.substr(n, 2), 16));
                return t
            },
            bytesToBase64: function(e) {
                for (var n = [], r = 0; r < e.length; r += 3)
                    for (var o = e[r] << 16 | e[r + 1] << 8 | e[r + 2], a = 0; a < 4; a++)
                        8 * r + 6 * a <= 8 * e.length ? n.push(t.charAt(o >>> 6 * (3 - a) & 63)) : n.push("=");
                return n.join("")
            },
            base64ToBytes: function(e) {
                e = e.replace(/[^A-Z0-9+\/]/gi, "");
                for (var n = [], r = 0, o = 0; r < e.length; o = ++r % 4)
                    0 != o && n.push((t.indexOf(e.charAt(r - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | t.indexOf(e.charAt(r)) >>> 6 - 2 * o);
                return n
            }
        };
        var t = n
        , r = {
            stringToBytes: function(e) {
                e = unescape(encodeURIComponent(e))
                for (var t = [], n = 0; n < e.length; n++)
                    t.push(255 & e.charCodeAt(n));
                return t
            },
            bytesToString: function(e) {
                return decodeURIComponent(escape(n.bin.bytesToString(e)))
            }
        }
        , o = function(e) {
            return null != e && (n(e) || r(e) || !!e._isBuffer)
        }
        , a = {
            stringToBytes: function(e) {
                for (var t = [], n = 0; n < e.length; n++)
                    t.push(255 & e.charCodeAt(n));
                return t
            },
            bytesToString: function(e) {
                for (var t = [], n = 0; n < e.length; n++)
                    t.push(String.fromCharCode(e[n]));
                return t.join("")
            }
        }
        , i = function(e, n) {
            e.constructor == String ? e = n && "binary" === n.encoding ? a.stringToBytes(e) : r.stringToBytes(e) : o(e) ? e = Array.prototype.slice.call(e, 0) : Array.isArray(e) || (e = e.toString());
            for (var l = t.bytesToWords(e), s = 8 * e.length, u = 1732584193, c = -271733879, f = -1732584194, p = 271733878, d = 0; d < l.length; d++)
                l[d] = 16711935 & (l[d] << 8 | l[d] >>> 24) | 4278255360 & (l[d] << 24 | l[d] >>> 8);
            l[s >>> 5] |= 128 << s % 32,
            l[14 + (s + 64 >>> 9 << 4)] = s;
            for (var h = i._ff, m = i._gg, v = i._hh, y = i._ii, d = 0; d < l.length; d += 16) {
                var g = u
                , b = c
                , w = f
                , x = p;
                u = h(u, c, f, p, l[d + 0], 7, -680876936),
                p = h(p, u, c, f, l[d + 1], 12, -389564586),
                f = h(f, p, u, c, l[d + 2], 17, 606105819),
                c = h(c, f, p, u, l[d + 3], 22, -1044525330),
                u = h(u, c, f, p, l[d + 4], 7, -176418897),
                p = h(p, u, c, f, l[d + 5], 12, 1200080426),
                f = h(f, p, u, c, l[d + 6], 17, -1473231341),
                c = h(c, f, p, u, l[d + 7], 22, -45705983),
                u = h(u, c, f, p, l[d + 8], 7, 1770035416),
                p = h(p, u, c, f, l[d + 9], 12, -1958414417),
                f = h(f, p, u, c, l[d + 10], 17, -42063),
                c = h(c, f, p, u, l[d + 11], 22, -1990404162),
                u = h(u, c, f, p, l[d + 12], 7, 1804603682),
                p = h(p, u, c, f, l[d + 13], 12, -40341101),
                f = h(f, p, u, c, l[d + 14], 17, -1502002290),
                c = h(c, f, p, u, l[d + 15], 22, 1236535329),
                u = m(u, c, f, p, l[d + 1], 5, -165796510),
                p = m(p, u, c, f, l[d + 6], 9, -1069501632),
                f = m(f, p, u, c, l[d + 11], 14, 643717713),
                c = m(c, f, p, u, l[d + 0], 20, -373897302),
                u = m(u, c, f, p, l[d + 5], 5, -701558691),
                p = m(p, u, c, f, l[d + 10], 9, 38016083),
                f = m(f, p, u, c, l[d + 15], 14, -660478335),
                c = m(c, f, p, u, l[d + 4], 20, -405537848),
                u = m(u, c, f, p, l[d + 9], 5, 568446438),
                p = m(p, u, c, f, l[d + 14], 9, -1019803690),
                f = m(f, p, u, c, l[d + 3], 14, -187363961),
                c = m(c, f, p, u, l[d + 8], 20, 1163531501),
                u = m(u, c, f, p, l[d + 13], 5, -1444681467),
                p = m(p, u, c, f, l[d + 2], 9, -51403784),
                f = m(f, p, u, c, l[d + 7], 14, 1735328473),
                c = m(c, f, p, u, l[d + 12], 20, -1926607734),
                u = v(u, c, f, p, l[d + 5], 4, -378558),
                p = v(p, u, c, f, l[d + 8], 11, -2022574463),
                f = v(f, p, u, c, l[d + 11], 16, 1839030562),
                c = v(c, f, p, u, l[d + 14], 23, -35309556),
                u = v(u, c, f, p, l[d + 1], 4, -1530992060),
                p = v(p, u, c, f, l[d + 4], 11, 1272893353),
                f = v(f, p, u, c, l[d + 7], 16, -155497632),
                c = v(c, f, p, u, l[d + 10], 23, -1094730640),
                u = v(u, c, f, p, l[d + 13], 4, 681279174),
                p = v(p, u, c, f, l[d + 0], 11, -358537222),
                f = v(f, p, u, c, l[d + 3], 16, -722521979),
                c = v(c, f, p, u, l[d + 6], 23, 76029189),
                u = v(u, c, f, p, l[d + 9], 4, -640364487),
                p = v(p, u, c, f, l[d + 12], 11, -421815835),
                f = v(f, p, u, c, l[d + 15], 16, 530742520),
                c = v(c, f, p, u, l[d + 2], 23, -995338651),
                u = y(u, c, f, p, l[d + 0], 6, -198630844),
                p = y(p, u, c, f, l[d + 7], 10, 1126891415),
                f = y(f, p, u, c, l[d + 14], 15, -1416354905),
                c = y(c, f, p, u, l[d + 5], 21, -57434055),
                u = y(u, c, f, p, l[d + 12], 6, 1700485571),
                p = y(p, u, c, f, l[d + 3], 10, -1894986606),
                f = y(f, p, u, c, l[d + 10], 15, -1051523),
                c = y(c, f, p, u, l[d + 1], 21, -2054922799),
                u = y(u, c, f, p, l[d + 8], 6, 1873313359),
                p = y(p, u, c, f, l[d + 15], 10, -30611744),
                f = y(f, p, u, c, l[d + 6], 15, -1560198380),
                c = y(c, f, p, u, l[d + 13], 21, 1309151649),
                u = y(u, c, f, p, l[d + 4], 6, -145523070),
                p = y(p, u, c, f, l[d + 11], 10, -1120210379),
                f = y(f, p, u, c, l[d + 2], 15, 718787259),
                c = y(c, f, p, u, l[d + 9], 21, -343485551),
                u = u + g >>> 0,
                c = c + b >>> 0,
                f = f + w >>> 0,
                p = p + x >>> 0
            }
            return t.endian([u, c, f, p])
        };
        i._ff = function(e, t, n, r, o, a, i) {
            var l = e + (t & n | ~t & r) + (o >>> 0) + i;
            return (l << a | l >>> 32 - a) + t
        }
        ,
        i._gg = function(e, t, n, r, o, a, i) {
            var l = e + (t & r | n & ~r) + (o >>> 0) + i;
            return (l << a | l >>> 32 - a) + t
        }
        ,
        i._hh = function(e, t, n, r, o, a, i) {
            var l = e + (t ^ n ^ r) + (o >>> 0) + i;
            return (l << a | l >>> 32 - a) + t
        }
        ,
        i._ii = function(e, t, n, r, o, a, i) {
            var l = e + (n ^ (t | ~r)) + (o >>> 0) + i;
            return (l << a | l >>> 32 - a) + t
        }
        ,
        i._blocksize = 16,
        i._digestsize = 16;
        var r = wordsToBytes(i(e, n));
        return n && n.asBytes ? r : n && n.asString ? a.bytesToString(r) : t.bytesToHex(r)

    }
    function wordsToBytes(e) {
        for (var t = [], n = 0; n < 32 * e.length; n += 8)
            t.push(e[n >>> 5] >>> 24 - n % 32 & 255);
        return t
    }
    function o(e) {
        for (var t = "", n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"], r = 0; r < e; r++) {
            t += n[Math.round(Math.random() * (n.length - 1))]
        }
        return t
    }
    n = o(50)
    sign = get_sign(t + e + n, undefined)
    console.log(n);
    console.log(sign);
    return {"nonce_str": n, "sign":sign}
}
