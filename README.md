# ZEROScan

## 简介

ZEROScan 是漏洞利用框架，通过它可以很容易地获取、开发漏洞利用插件并对目标应用进行渗透测试。界面和使用借鉴了msf框架，很容易上手使用和开发插件。

## 安装

本框架采用 Python 语言开发，并且第三方依赖包都已打包，只需要下载就可以直接进行使用。

## 使用

首先打开终端切换到ZEROScan目录

```Shell
➜  ZEROScan git:(master) ✗ python z-console.py

　　......(\_/)
　　......( '_')
　　..../""""""""""""\======░ ▒▓▓█D
　　/"""""""""""""""""""\
　　\_@_@_@_@_@_@_@_@_@_/

+ -- --=[ ZEROScan - 2017/04/08 ]
+ -- --=[ 2 CMS                 ]
+ -- --=[ 2 Plugins             ]
#输入help可以显示当前的命令以及详情
ZEROScan > help

Core Commands
=============

Command                       Description
-------                       -----------
help                          Help menu
use <plugin>                  Select a plugin by name
vulns                         List all vulnerabilities in the database
update                        Update the framework
vulns -d                      Clear all vulnerabilities in the database
exploit                       Run current plugin
vulns -o <plugin>             Save vulnerabilities to file
search <keyword>              Search plugin names and descriptions
set <option> <value>          Set a variable to a value
info <plugin>                 Display information about one plugin
rebuild                       Rebuild the database
list                          List all plugins
version                       Show the framework version numbers
exit                          Exit the console
options                       Display options for current plugin
#list则显示目前可用的模块(当然你可以自己编写模块)
ZEROScan > list
\Modules
=======

Name                                    Scope                                   Description
----                                    -----                                   -----------
corem_whatweb                           All CMS                                 CMS 识别
phpcms_down_sqli                        PHPCMS <= 9.6.0                         PHPCMS content/down.php SQL Injection
#使用use <模块名称>就是加载相应的模块
ZEROScan > use corem_whatweb
#输入options查看插件需要的参数
ZEROScan exploit(corem_whatweb) > options

	Name                Current Setting                         Required  Description
	----                ---------------                         --------  -----------
	URL                                                         True      网站地址
	Thread              50                                      True      线程数

#使用set命令对相应的参数进行设置
ZEROScan exploit(corem_whatweb) > set URL https://www.wpdaxue.com/
URL => https://www.wpdaxue.com/
#输入exploit命令就可以执行相应的模块
ZEROScan exploit(corem_whatweb) > exploit
[!]https://www.wpdaxue.com: wordpress
[!]vuln is exist!
#模块执行后的结果会存在数据库中，使用vulns命令进行查看
ZEROScan exploit(corem_whatweb) > vulns

Vulns
=====

Plugin                                  Vuln
------                                  ----
corem_whatweb                           https://www.wpdaxue.com: wordpress

ZEROScan exploit(corem_whatweb) >
```

以上便是基本的使用方法。

## 插件开发

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from lib.core import logger
from lib.thirdparty import requests

author = "Z3r0yu"
scope = "Demo <一般在此填写cms对应的版本号等一些信息>"
description = "模块 Demo <一般在此填写漏洞类型>"
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

def poc(url):
    #可以定义任意的函数
    pass


#exploit函数是框架的入口，必须带URL和Thread这两个参数
def exploit(URL, Thread):
    #return的信息将被保存在数据库中
    #使用vulns进行查看
    return "URL"
```

开发后的模块应放置在相应的cms文件夹路径下，之后在z-console中执行build命令对数据库进行重构

## 作者

Author：Z3r0yu

Blog：    http://zeroyu.xyz/

Mail:       zeroyu@protonmail.com

<PS:欢迎提交bug和修改建议>

## 更新

2017.04.09—修改了框架，更新了whatweb可以对国内几十种CMS进行识别

2017.04.09—增加phpcms9.6.0 SQL注入漏洞