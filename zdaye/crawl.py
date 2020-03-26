#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/26 10:26
# @Author  : zjz
import requests
import re

url = 'https://www.zdaye.com/dayProxy.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
}


def get_arg1():
    response = requests.get(url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    arg1 = re.search("arg1='([^']+)'", response.text).group(1)
    return arg1


def unsbox(arg):
    _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd,
                 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c,
                 0x22, 0x25, 0xc, 0x24]
    _0x4da0dc = [''] * 40
    _0x12605e = ''
    for _0x20a7bf in range(0, len(arg)):
        _0x385ee3 = arg[_0x20a7bf]
        for _0x217721 in range(0, len(_0x4b082b)):
            if _0x4b082b[_0x217721] == _0x20a7bf + 0x1:
                _0x4da0dc[_0x217721] = _0x385ee3
    _0x12605e = ''.join(_0x4da0dc)
    return _0x12605e


def hexxor(_0x4e08d8, _0x23a392):
    _0x5a5d3b = ''
    _0xe89588 = 0x0
    while _0xe89588 < len(_0x23a392) and _0xe89588 < len(_0x4e08d8):
        _0x401af1 = int(_0x23a392[_0xe89588:_0xe89588 + 0x2], 16)
        _0x105f59 = int(_0x4e08d8[_0xe89588:_0xe89588 + 0x2], 16)
        _0x189e2c = hex(_0x401af1 ^ _0x105f59)
        if len(_0x189e2c) == 0x1:
            _0x189e2C = ' \x30' + _0x189e2c
        _0x5a5d3b += _0x189e2c[2:]
        _0xe89588 += 0x2
    return _0x5a5d3b


def get_arg2():
    arg1 = get_arg1()
    key = '3000176000856006061501533003690027800375'
    _0x23a392 = unsbox(arg1)
    arg2 = 'acw_sc__v2=' + hexxor(key, _0x23a392)
    return arg2


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Cookie': get_arg2()
    }
    res = requests.get(url, headers=headers, verify=False)
    print(res.text)

