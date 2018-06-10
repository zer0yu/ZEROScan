# ZEROScan

[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/crates/l/rustc-serialize.svg)](https://github.com/zer0yu/ZEROScan/blob/master/LICENSE)

## 简介

ZEROScan 是多线程漏洞检测框架，通过它可以很容易地获取或者开发漏洞检测插件，来对目标进行渗透测试。界面和使用方式借鉴了metasploit-framework框架，很容易上手使用和开发插件。

## 特点

- 支持多线程并发模式  
- 极简式脚本编写，无需参考文档  
- 支持Linux, Windows, Mac OSX, BSD

## 安装

```
$ git clone https://github.com/zer0yu/ZEROScan.git
```

或者你可以下载最新的zip源码包进行解压安装:

```
$ wget https://codeload.github.com/zer0yu/ZEROScan/zip/master
$ unzip ZEROScan-master.zip
```

## 使用

```bash
➜  ZEROScan git:(master) ✗ python z-console.py

  ____________ _____   ____   _____
 |___  /  ____|  __ \ / __ \ / ____|
    / /| |__  | |__) | |  | | (___   ___ __ _ _ __
   / / |  __| |  _  /| |  | |\___ \ / __/ _` | '_ \
  / /__| |____| | \ \| |__| |____) | (_| (_| | | | |
 /_____|______|_|  \_\\____/|_____/ \___\__,_|_| |_|

+ -- --=[ ZEROScan - 1.0 ]
#执行help命令你可以查看每一个参数的说明。
ZEROScan > help

Core Commands
=============

Command                       Description
-------                       -----------
run                           Run current plugin
help                          Help menu
use <plugin>                  Select a plugin by name
update                        Update the framework
search <keyword>              Search plugin names and descriptions
set <option> <value>          Set a variable to a value
info <plugin>                 Display information about one plugin
list                          List all plugins
version                       Show the framework version numbers
exit                          Exit the console
options                       Display options for current plugin
#使用list命令显示当前所有的插件
ZEROScan > list
\Modules
=======

expName    appName      appVersion  description
---------  ---------  ------------  -----------------------------
demo       PHP                1230  PH1424/down.php SQL Injection
#可以使用info命令来查看对应插件的详情信息
ZEROScan > info demo

appName: PHP
appVersion: 1230
Author:
	123

Description:
	PH1424/down.php SQL Injection

Reference:
	http://124.xyz/
#使用use命令来指定要调用的插件
ZEROScan > use demo
#使用options命令来查看此插件需要设置的对应项
ZEROScan exploit(demo) > options
#批量扫描的文件需要放置于target目录下
#批量扫描的文件直接设置参数url为文件名即可(不需要加txt结尾)
Name    Current Setting      Required  Description
------  -----------------  ----------  --------------------------
URL                                 1  URL or URL file
Thread  1                           0  Threads
Cookie                              0  Cookie
Report  False                       0  do you need a html report?
#使用set命令来设置
ZEROScan exploit(demo) > set URL ww.baidu.com
URL => ww.baidu.com
#run命令来执行对应的插件
ZEROScan exploit(demo) > run
[!]exploit target:'ww.baidu.com'
[!]Requesting target site:ww.baidu.com
+--------------+------------+-------------+
| target-url   | poc-name   | status      |
+==============+============+=============+
| ww.baidu.com | demo       | test_plugin |
+--------------+------------+-------------+
success : 1
#最终结果会保存在output目录下的txt文件中
ZEROScan exploit(demo) >
```

## 插件编写

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
from lib.core import log
#可以从thirdparty中导入requests库
#from thirdparty import requests

#expInfo()为必须的函数，在此处要填写以下信息
def expInfo():
    expInfo={}
    expInfo["appName"] = "PHP"
    expInfo["appVersion"] = "123"
    expInfo["author"] = "Z3r0yu"
    expInfo["description"] = "PHPxxx/down.php SQL Injection"
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

#在插件中你可以随意定义你所需要的函数
def yourDefinition():

    return "test_plugin"
#exploit(target, headers=None)为执行函数，是必须有的，并且需要给予两个参数
#target参数用于指定目标，headers可以用于实现随机UA
def exploit(target, headers=None):
    log.process("Requesting target site:"+ target)
#return你想要的信息
#但是框架会将有return值的一次扫描定义为成功扫描并给予显示
    return yourDefinition()
```

## 更新日志

- v1.0.0
  - 优化了整体的结构
- v0.0.1
  - 初出茅庐

## 联系作者

- mail:zeroyu.xyz@gmail.com

## 声明

本软件仅供学习交流使用，请勿用于非法用途，否则造成的后果于作者无关。