#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 14:26
# @Author  : zjz
import json
import re
import time
import requests

# 需要查找的id
id = '3007689648'
s = requests.Session()
# 一个cookie过期时间还未定
headers = {
    "Host": "capi.tianyancha.com",
    "Connection": "keep-alive",
    "Origin": "https://dis.tianyancha.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://dis.tianyancha.com/dis/tree?graphId={}&origin=https%3A%2F%2Fwww.tianyancha.com&mobile=&time=15753515647237b28&full=1".format(
        id),
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "TYCID=d9727140157e11eaab41691f9a51d2ed; undefined=d9727140157e11eaab41691f9a51d2ed; ssuid=8686323904; bannerFlag=undefined; RTYCID=26963f4845324e7f8aaf1c9ca2159104; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1575344515; aliyungf_tc=AQAAAG/4CAKdyAcAnUEYdNm5vLgCnTNI; CLOUDID=756cffe2-228f-42ef-8e3f-528816e86384; CT_TYCID=20b71739a88447dd98725c23c08efc0f; _ga=GA1.2.199777249.1575344515; _gid=GA1.2.1748072841.1575344515; _gat_gtag_UA_123487620_1=1; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1575351565;"
}
# js里有段默认值t.default,这里直接debug拿到默认值转换的数组
default_list = [
    ["6", "b", "t", "f", "2", "z", "l", "5", "w", "h", "q", "i", "s", "e", "c", "p", "m", "u", "9", "8", "y", "k", "j",
     "r", "x", "n", "-", "0", "3", "4", "d", "1", "a", "o", "7", "v", "g"],
    ["1", "8", "o", "s", "z", "u", "n", "v", "m", "b", "9", "f", "d", "7", "h", "c", "p", "y", "2", "0", "3", "j", "-",
     "i", "l", "k", "t", "q", "4", "6", "r", "a", "w", "5", "e", "x", "g"],
    ["s", "6", "h", "0", "p", "g", "3", "n", "m", "y", "l", "d", "x", "e", "a", "k", "z", "u", "f", "4", "r", "b", "-",
     "7", "o", "c", "i", "8", "v", "2", "1", "9", "q", "w", "t", "j", "5"],
    ["x", "7", "0", "d", "i", "g", "a", "c", "t", "h", "u", "p", "f", "6", "v", "e", "q", "4", "b", "5", "k", "w", "9",
     "s", "-", "j", "l", "y", "3", "o", "n", "z", "m", "2", "1", "r", "8"],
    ["z", "j", "3", "l", "1", "u", "s", "4", "5", "g", "c", "h", "7", "o", "t", "2", "k", "a", "-", "e", "x", "y", "b",
     "n", "8", "i", "6", "q", "p", "0", "d", "r", "v", "m", "w", "f", "9"],
    ["j", "h", "p", "x", "3", "d", "6", "5", "8", "k", "t", "l", "z", "b", "4", "n", "r", "v", "y", "m", "g", "a", "0",
     "1", "c", "9", "-", "2", "7", "q", "e", "w", "u", "s", "f", "o", "i"],
    ["8", "q", "-", "u", "d", "k", "7", "t", "z", "4", "x", "f", "v", "w", "p", "2", "e", "9", "o", "m", "5", "g", "1",
     "j", "i", "n", "6", "3", "r", "l", "b", "h", "y", "c", "a", "s", "0"],
    ["d", "4", "9", "m", "o", "i", "5", "k", "q", "n", "c", "s", "6", "b", "j", "y", "x", "l", "a", "v", "3", "t", "u",
     "h", "-", "r", "z", "2", "0", "7", "g", "p", "8", "f", "1", "w", "e"],
    ["7", "-", "g", "x", "6", "5", "n", "u", "q", "z", "w", "t", "m", "0", "h", "o", "y", "p", "i", "f", "k", "s", "9",
     "l", "r", "1", "2", "v", "4", "e", "8", "c", "b", "a", "d", "j", "3"],
    ["1", "t", "8", "z", "o", "f", "l", "5", "2", "y", "q", "9", "p", "g", "r", "x", "e", "s", "d", "4", "n", "b", "u",
     "a", "m", "c", "h", "j", "3", "v", "i", "0", "-", "w", "7", "k", "6"],
]

def getfnstr(data):
    fnstr = ""
    for i in data.split(','):
        fnstr += chr(int(i))
    return fnstr

def getSogo(default_list, id):
    r = str(ord(id[0]))
    return default_list[int(r[1])]

def getfxckStr(fxck, window_sogo):
    fxckStr = ""
    for i in fxck.split(','):
        fxckStr += window_sogo[int(i)]
    return fxckStr

# 获取前置参数 random为13位时间戳
res1 = s.get("https://capi.tianyancha.com/cloud-equity-provider/v4/qq/name.json?id={}?random={}".format(id, str(
    int(time.time() * 1000))), headers=headers)
data_dict = json.loads(res1.content)["data"]


# 调用加密函数,获取cloud_token 以及cloud_utm
fnstr = getfnstr(data_dict.get('v'))
cookie_token = re.search('cookie=\'cloud_token\=(.*?)\;', fnstr).group(1)
wtf_return = re.search('return\'(.*?)\'', fnstr).group(1)
window_sogo = getSogo(default_list, id)
# cloud_utm
fxckStr = getfxckStr(wtf_return, window_sogo)
headers["Cookie"] = headers["Cookie"] + " cloud_utm=" + fxckStr + "; cloud_token=" + cookie_token + ';'
res2 = s.get('https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id={}'.format(id),
             headers=headers)
text = json.loads(res2.text)
print(text)

