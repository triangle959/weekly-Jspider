#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/20 15:36
# @Author  : zjz
import re
import time

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
Cookie: UM_distinctid=170c8979d2483d-046df15f1c2248-4313f6a-1fa400-170c8979d255b5; CNZZDATA1254317176=616657727-1583912404-%7C1583912404
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
Cookie: UM_distinctid=170c8979d2483d-046df15f1c2248-4313f6a-1fa400-170c8979d255b5; CNZZDATA1254317176=616657727-1583912404-%7C1583912404
Host: www.aqistudy.cn
Referer: https://www.aqistudy.cn/html/city_realtime.php?v=2.3
Pragma: no-cache
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
"""
headers1 = format_headers(headers1)
headers2 = format_headers(headers2)
def get_Common():
    for i in range(3):
        url_first = "https://www.aqistudy.cn/html/city_realtime.php?v=2.3"
        res = requests.get(url=url_first, headers=headers1)
        js_key = re.search("encrypt_(.*?)\.", res.text).group(1)
        url = "https://www.aqistudy.cn/js/encrypt_%s.min.js?t=%s" % (js_key, str(int(time.time())))
        res = requests.get(url=url, headers=headers2)
        text = re.search("127,'(.*?)'",res.text).group(1)
        result = text.split('|')
        if result[124] == 'aqistudyapi':
            continue
        return result


def make_request(url, parma, parma_key='parma'):
    res = requests.post(url, data={parma_key: parma})
    return res.text



if __name__ == '__main__':
    data_obj = {"city": "深圳"}

    parma_keys = get_Common()
    if parma_keys:
        # parma_keys[124] '9f7be8c7160d51c752e23a722632dd6c'
        param = get_js_function('AQI.js', 'get_parma', "GETDATA", data_obj, parma_keys[124], parma_keys[102], parma_keys[103])
        print(param)
        encryp_data = make_request('https://www.aqistudy.cn/apinew/aqistudyapi.php', param, parma_keys[121])
        print(encryp_data)
        data = get_js_function('AQI.js', 'decrypt_data', encryp_data, parma_keys[107], parma_keys[91], parma_keys[103], parma_keys[106])
        print(data)
