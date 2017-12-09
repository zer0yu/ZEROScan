#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import json
from lib.core import log
from thirdparty import requests

def expInfo():
    expInfo={}
    expInfo["appName"] = "CHECK CSM"
    expInfo["appVersion"] = "every version"
    expInfo["author"] = "Z3r0yu"
    expInfo["description"] = "To find what the web is"
    expInfo["references"] = "http://zeroyu.xyz/"

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


def whatweb(target):
	query = {"url": target}
	whatWebUrl = "http://whatweb.bugscaner.com/what/"
	response = requests.post(whatWebUrl,data=query)
	return response.text

def exploit(target, headers=None):
    log.process("whatweb target site:"+ target)
    whatcms = json.loads(whatweb(target))
    return whatcms["cms"]