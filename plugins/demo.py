#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re

from lib.core import log

def expInfo():
    expInfo={}
    expInfo["appName"] = "PHP"
    expInfo["appVersion"] = "1230"
    expInfo["author"] = "123"
    expInfo["description"] = "PH1424/down.php SQL Injection"
    expInfo["references"] = "http://124.xyz/"

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


def yourDefinition():

    return "test_plugin"

def exploit(target, headers=None):
    log.process("Requesting target site:"+ target)
    return yourDefinition()