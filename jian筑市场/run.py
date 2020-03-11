#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/20 10:07
# @Author  : zjz
import json
from Crypto.Cipher import AES
import requests


class AESDecrypt:
    iv = '0123456789ABCDEF'
    key = 'jo8j9wGw%6HbxfFn'

    @classmethod
    def _pkcs7unpadding(cls, text):
        length = len(text)
        unpadding = -ord(text[length-1])
        return text[0: length-unpadding]

    @classmethod
    def decrypt(cls, content):
        key = bytes(cls.key, encoding='utf-8')
        iv = bytes(cls.iv, encoding='utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_bytes = cipher.decrypt(bytes.fromhex(content))
        result = str(decrypt_bytes, encoding='utf-8')
        result = cls. _pkcs7unpadding(result)
        return result


class JianzhuSpider:
    def __init__(self):
        self.parse_url = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/project/list?projectRegionId=161612111212&pg=0&pgsz=15&total=0"

    def _request(self, url):
        # 前端仅显示0-29页
        res = requests.get(url)
        if res.status_code == 200:
            result = AESDecrypt().decrypt(res.text)
            result = json.loads(result.replace('',"").replace('',""))
            print(result)
        return res.text

    def parse_list(self):
        url = self.parse_url
        result = self._request(url)

if __name__ == '__main__':
    JianzhuSpider().parse_list()