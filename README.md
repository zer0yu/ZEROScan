# ZEROScan

## 简介

ZEROScan 是漏洞利用框架，通过它可以很容易地获取、开发漏洞利用插件并对目标应用进行渗透测试。界面和使用借鉴了msf框架，很容易上手使用和开发插件。

## 安装

本框架采用 Python 语言开发，并且第三方依赖包都已打包，只需要下载就可以直接进行使用。

## 使用

框架内输入 ```help``` 可查看详细的帮助信息

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



## 作者

Author：Z3r0yu

Blog：    http://zeroyu.xyz/

Mail:       zeroyu@protonmail.com

<PS:欢迎提交bug和修改建议>

## 更新

2017.04.09—修改了框架，更新了whatweb可以对国内几十种CMS进行识别

2017.04.09—增加phpcms9.6.0 SQL注入漏洞