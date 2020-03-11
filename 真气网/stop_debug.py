#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/19 11:33
# @Author  : zjz
"""
mitmproxy 脚本，去除debug
"""
import mitmproxy.http
from mitmproxy import ctx
import re

def response(flow):
    if 'www.aqistudy.cn/' in flow.request.url:
        ctx.log.warn(flow.request.url + '修改')
        flow.response.text = re.sub('endebug\(.*?}\);', "", flow.response.text, flags=re.S)
