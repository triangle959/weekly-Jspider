#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/21 16:19
# @Author  : zjz
import json
import re
import time

import execjs
import requests
from bs4 import BeautifulSoup


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

if __name__ == '__main__':
    headers = """
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: no-cache
Cookie: _ga=GA1.2.1806556551.1579420043; footprints=eyJpdiI6IlpNdE9vZTdYVkxoMzE5eEtsQ2Jjanc9PSIsInZhbHVlIjoiK1ZVRWk4dW5hZTVFMEJMV0E0UXJveHpFdDNVT0tKSHlBZzRvQlJIWXpQUitQTnM5SUE1clRFUU9CY3BPVE9RTiIsIm1hYyI6IjlhMjQxNTFhZDAzZTExZTVmNTQ5NmM2MWNhZjg2Mzk2YWM0NmI1OGJjNDI2NmFjNWFhMzZjZTdkZmMyNWM4ZWMifQ%3D%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IlVpZHZWK2RCYyszeEpcL1wvUTlcL0VnVUE9PSIsInZhbHVlIjoidkZFZEJoeFRhVnB6XC8rR1c5NkVxTTBDSEc4Z1VIRmdYRURVUjZIOXZXdnZqNEgwUTVDVDJwOGZocHNveCsyRUVMZ09OY3pMWGpuazVxazMxMUpwN1JOeFdKcUJSRjBNMWRrVGRjUStiempBU1wvckl3cnFhcGtjUncwNHd6Z1JXRkwrOXNNcCtYNnNacTAzVnIwMlNBR0hpZEo4M245bEd3dEtUSTBTK3hpVlU9IiwibWFjIjoiNGQ4MjAyMzQwMjJjNzEyYjQxMzBiOGRmZjY5OGE4ODNiOGRiY2NlN2YwOWMyMjAxYWNkNDJhYTQxZWQ1Y2NlNSJ9; Hm_lvt_020fbaad6104bcddd1db12d6b78812f6=1583835732,1583890405,1584069053,1584494337; _gid=GA1.2.1257378577.1584927464; _gat_gtag_UA_75859356_3=1; XSRF-TOKEN=eyJpdiI6InZlM0NqWHhmamRHYnJucHU2bXRlWXc9PSIsInZhbHVlIjoiZklGQkpmMHExOW9VeVZQVGFOY2F2UGxISTIzaFdBekFjYkhKNkJRVG9Dbjd1RzVRc1wveFlZekFQSTBnTVduYzYiLCJtYWMiOiJhMTA2MDgyN2NlOGM4NWZhYzRiZWUxODIyMDE1ZTI1MzMyNjZhMDc4Y2IwNTRkYzMxMTgxNjI4YWJiMTQyNGI2In0%3D; glidedsky_session=eyJpdiI6InExTVlxM0c3eDBma21kV0RxWXVHMUE9PSIsInZhbHVlIjoidHhyelB3YmZuWjBJRnNtRWdqUmIyZGsxaTZrSFdmbEFYMzVWbnVTUTJFdzRWUVViZDRqK1lkenIxK04rNVdHaiIsIm1hYyI6IjNjMWMxM2NlOTc3MjQxZDc1NjQ3ZjAyOTA3YzQ0YWNkNzYxNDcwNmRlZmVmNWFmMTNhYzU0M2QyNzQ4MTYxZTEifQ%3D%3D; Hm_lpvt_020fbaad6104bcddd1db12d6b78812f6=1584927469
Host: www.glidedsky.com
Pragma: no-cache
Proxy-Connection: keep-alive
Referer: http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
"""
    total = 0
    headers = format_headers(headers)
    for page in range(1, 1001):
        url1 = "http://www.glidedsky.com/level/web/crawler-javascript-obfuscation-1?page=%s" % str(page)
        res = requests.get(url1, headers=headers)
        t = int(re.search('" t="(.*?)">',res.text).group(1))
        parma = get_js_function('sign.js', 'get_sign', t)
        url2 = "http://www.glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page=%s&t=%s&sign=%s" % (str(page), parma["t"], parma["sign"])
        res = requests.get(url2, headers=headers)
        result = json.loads(res.text)
        for num in result["items"]:
            total = total + num
        print("now page is " + str(page), "now total is " + str(total))
