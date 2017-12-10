#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from collections import namedtuple
from lib.core import log
from thirdparty import requests

def expInfo():
    expInfo={}
    expInfo["appName"] = "File Leakage"
    expInfo["appVersion"] = "every"
    expInfo["author"] = "Z3r0yu"
    expInfo["description"] = "try to find thef file leakage"
    expInfo["references"] = "https://github.com/wonderkun/python_tools/blob/master/coinfo.py"

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


class CollectionInfo(object):
    """docstring for CoInfo.
        .hg  https://github.com/kost/dvcs-ripper
        index.bak
        index.php.bak
        index.php.
        .index.php
        index.php~
        index.pyc
        .index.php.swp
        .index.php.swpx
        .index.php.swm
        index.tar.gz
        index.rar
        index.zip
        www.rar
        www.zip
        .svn   https://pan.baidu.com/s/1mrNpB
        .git
        .DS_Store  https://github.com/lijiejie/ds_store_exp
        .index.php.swo
        .index.php.swn
        robots.txt
        phpstorm/   .idea/workspace.xml
        CVS http://www.am0s.com/CVS/Root 返回根信息 http://www.am0s.com/CVS/Entries 返回所有文件的结构
        bk clone http://url/name dir
        WEB-INF/web.xml 

    """
    def __init__(self,url=''):

        self.url = url
        self.fileBackList = ['.bak','.','~','.pyc','.swp','.swpx','.swm','.swo','.swn']
        self.fileList = ['.viminfo','index.bak','index.tar.gz','index.zip','index.rar','www.tar.gz','www.rar','www.zip','.svn','.git','.DS_Store',
        'robots.txt','.idea/','.hg','www.7z','WEB-INF/web.xml','WEB-INF/classes/','WEB-INF/lib/','WEB-INF/src/',
        'WEB-INF/database.properties','CVS/','CVS/Root','CVS/Entries','phpMyAdmin','phpmyadmin']
        self.vimBackList = ['','~','.swp','.swpx','.swm','.swo','.swn']
        self.UrlList = []
        self.getUrlList()
        self.table = []

    def getUrlList(self):
        for file in self.fileList:
            self.UrlList.append(self.url.rstrip('/')+'/'+file)

    def sendRequest(self,cookies="",agent=""):
        cookies = cookies
        User_Agent = agent if agent is not  "" else "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
        header = {
        "User-Agent":User_Agent,
        "Cookie":cookies
        }
        for  url in self.UrlList:
            res = requests.get(url,headers=header)
            if res.status_code != 404:
                self.table.append(url)
        return str(self.table)

def exploit(target, headers=None):
    coll = CollectionInfo(target)
    return coll.sendRequest()