#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from modules.useragent import *
from thirdparty import requests

def expInfo():
    expInfo={}
    expInfo["appName"] = "ScanWebHost"
    expInfo["appVersion"] = "ALL"
    expInfo["author"] = "z3r0yu"
    expInfo["description"] = "Detect WebServer by spider"
    expInfo["references"] = "https://github.com/zer0h/httpscan/"

    expInfo["options"] = [
        {
            "Name": "URL",
            "Current Setting": "",
            "Required": True,
            "Description": "URL or URL file"
        },
        {
            "Name": "Thread",
            "Current Setting": "1",
            "Required": False,
            "Description": "Threads"
        },
        {
            "Name": "Cookie",
            "Current Setting": "",
            "Required": False,
            "Description": "cookie"
        },
        {
            "Name": "Report",
            "Current Setting": "",
            "Required": False,
            "Description": "do you need a html report?"
        },
    ]
    return expInfo

#User-Agent
ua = get_random_agent()
header = {'User-Agent' : ua,'Connection':'close'}
TimeOut = 5  #request timeout

def sacn(target):
    try:
        r = requests.Session().get(str(target),headers=header,timeout=TimeOut)
        status = r.status_code
        title = re.search(r'<title>(.*)</title>', r.text) #get the title
        if title:
            title = title.group(1).strip().strip("\r").strip("\n")[:30]
        else:
            title = "None"
        banner = ''
        try:
            banner += r.headers['Server'][:20] #get the server banner
        except:
            pass
        return "Status>%s|Server>%s|Title>%s" % (status,banner,title)
    except Exception,e:
        pass

def exploit(target, headers=None):
    if 'http://' in target or 'https://' in target:
        result = sacn(target)
        return result
    else:
        try:
            target = 'http://'+target
            result = sacn(target)
            return result
        except:
            target = 'https://'+target
            result = sacn(target)
            return result