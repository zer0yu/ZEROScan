#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import sys

from lib.core.revision import getRevisionNumber

VERSION = "1.0dev"
REVISION = getRevisionNumber()
VERSION_STRING = "zerosacn/%s%s" % (VERSION, "-%s" % REVISION if REVISION else "-nongit-%s" % time.strftime("%Y%m%d", time.gmtime(os.path.getctime(__file__))))

IS_WIN = subprocess.mswindows

PLATFORM = os.name
PYVERSION = sys.version.split()[0]

ISSUES_PAGE = "https://github.com/zer0yu/ZEROScan/issues"
GIT_REPOSITORY = "git@github.com:zer0yu/ZEROScan.git"
GIT_PAGE = "https://github.com/zer0yu/ZEROScan"

LEGAL_DISCLAIMER = "Usage of zeroscan for attacking targets without prior mutual consent is illegal."


BANNER = """
  ____________ _____   ____   _____                 
 |___  /  ____|  __ \ / __ \ / ____|                
    / /| |__  | |__) | |  | | (___   ___ __ _ _ __  
   / / |  __| |  _  /| |  | |\___ \ / __/ _` | '_ \ 
  / /__| |____| | \ \| |__| |____) | (_| (_| | | | |
 /_____|______|_|  \_\\\____/|_____/ \___\__,_|_| |_|
 
+ -- --=[ ZEROScan - %s ]
""" % (VERSION)

# Encoding used for Unicode data
UNICODE_ENCODING = "utf-8"
# Format used for representing invalid unicode characters
INVALID_UNICODE_CHAR_FORMAT = r"\?%02x"

USAGE = "pocsuite [options]"

INDENT = " " * 2

POC_ATTRS = ( "appName", "appVersion", "author", "description", "references")


HTTP_DEFAULT_HEADER = {
    "Accept": "*/*",
    "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Referer": "http://www.baidu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0"
}



REPORT_TABLEBASE = """\
    <tbody>
    %s
    </tbody>
    """

REPORT_HTMLBASE = """\
    <!DOCTYPE html>
    <html lang="zh-cn">
        <head>
            <meta charset="utf-8">
            <title></title>
            <style type="text/css">
            caption{padding-top:8px;padding-bottom:8px;color:#777;text-align:left}th{text-align:left}.table{width:100%%;max-width:100%%;margin-bottom:20px}.table>thead>tr>th,.table>tbody>tr>th,.table>tfoot>tr>th,.table>thead>tr>td,.table>tbody>tr>td,.table>tfoot>tr>td{padding:8px;line-height:1.42857143;vertical-align:top;border-top:1px solid #ddd}.table>thead>tr>th{vertical-align:bottom;border-bottom:2px solid #ddd}.result0{display:none}.result1{}.status{cursor: pointer;}
            </style>
            <script>
                function showDetail(dom){
                    parent = dom.parentElement;
                    detail = parent.children[1];
                    if (detail == undefined){
                        return;
                    };
                    if (detail.className == 'result0'){
                        detail.className = 'result1';
                    }else{
                        detail.className = 'result0';
                    };
                }
            </script>
        </head>
        <body>
            <div class="container">
                <table class="table">
                    <thead>
    %s
                    </thead>
    %s
                </table>
            </div>
        </body>
    </html>
    """
