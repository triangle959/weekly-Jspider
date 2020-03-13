#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 15:36
# @Author  : zjz
import re
import time
from urllib import parse

import execjs
import requests


def get_js_function(js_path, func_name, *func_args):
    '''
    获取指定目录下的js代码, 并且指定js代码中函数的名字以及函数的参数。
    :param js_path: js代码的位置
    :param func_name: js代码中函数的名字
    :param func_args: js代码中函数的参数
    :return: 返回调用js函数的结果
    '''

    with open(js_path, encoding='utf-8') as fp:
        js = fp.read()
        ctx = execjs.compile(js)
        return ctx.call(func_name, *func_args)


def format_headers(string) -> dict:
    """
    将在Chrome上复制下来的浏览器UA格式化成字典，以\n为切割点
    :param string: 使用三引号的字符串
    :return:
    """
    string = string.strip().split('\n')
    new_headers = {}
    for key_value in string:
        key_value_list = key_value.split(': ')
        if len(key_value_list) > 2:
            new_headers.update({key_value_list[0]: ':'.join(key_value_list[1::])})
        else:
            new_headers.update({key_value_list[0]: key_value_list[1]})
    return new_headers


headers1 = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: UM_distinctid=170c8979d2483d-046df15f1c2248-4313f6a-1fa400-170c8979d255b5; CNZZDATA1254317176=616657727-1583912404-%7C1584063635
Host: www.aqistudy.cn
Pragma: no-cache
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
"""
headers2 = """
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Connection: keep-alive
Cookie: UM_distinctid=170c8979d2483d-046df15f1c2248-4313f6a-1fa400-170c8979d255b5; CNZZDATA1254317176=616657727-1583912404-%7C1584063635
Host: www.aqistudy.cn
Referer: https://www.aqistudy.cn/html/city_realtime.php?v=2.3
Pragma: no-cache
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
"""
headers1 = format_headers(headers1)
headers2 = format_headers(headers2)


def get_Common(city):
    """
    获取加密的js文件，以及调用的方法名
    :return:
    """
    url_first = "https://www.aqistudy.cn/html/city_realtime.php?v=2.3"
    headers1["Cookie"] = headers1["Cookie"] + "; dcity=" + parse.quote("深圳")
    # 第一步，请求js文件导入到本地util.js内
    res = requests.get(url=url_first, headers=headers1)
    js_key = re.search("encrypt_(.*?)\.", res.text).group(1)
    method_key = re.search("\s*(.*?)\(method", res.text).group(1)
    url = "https://www.aqistudy.cn/js/encrypt_%s.min.js?t=%s" % (js_key, str(int(time.time())))
    res = requests.get(url=url, headers=headers2)
    js = res.text.replace("eval(", 'x=')
    docjs = execjs.compile(js[:-2])
    encrype_js = docjs.eval('x')
    # 获取解密后的js进行替换$ajax
    param_key = re.search("data:{(.*?):param}", encrype_js).group(1)
    encrype_js = re.sub('\$\.ajax\({(.*?)}\)', "return param;", encrype_js)
    decrype_key = re.search("newObject}function\s(.*?)\(data\)", encrype_js).group(1)
    # 在返回的值里还需插入param的加密方法
    # encrype_keys = re.findall("(?<=const ).*?(?==)", encrype_js)[6:8]
    # new_encrypt_js = encrype_js.split("return param")[0] + "param=DES.encrypt(param,%s,%s);return param"%(encrype_keys[0],encrype_keys[1])+  encrype_js.split("return param")[1]
    with open('util.js', 'a+', encoding='utf-8') as f:
        f.write("localStorage={data: {},setItem(key, value) {this.data[key] = value;},getItem(key) {return this.data[key]; }};")
        f.write(encrype_js)
    return True, method_key, param_key, decrype_key


def make_request(url, parma, param_key='parma'):
    res = requests.post(url, data={param_key: parma}, headers=headers1)
    return res.text


if __name__ == '__main__':
    city = "深圳"
    # 每次运行后将util.js 最后一行补写的js删除
    # post请求的key 位置有两处 107 和 121
    status, method_key, param_key, decrype_key = get_Common(city)
    param = get_js_function('util.js', method_key, "GETDATA", {city: "深圳"}, None, 0.5)
    print(param)
    data = make_request('https://www.aqistudy.cn/apinew/aqistudyapi.php', param, param_key)
    print(get_js_function('util.js', decrype_key, data))

