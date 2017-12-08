# ZEROScan

## 简介

ZEROScan 是漏洞利用框架，通过它可以很容易地获取、开发漏洞利用插件并对目标应用进行渗透测试。界面和使用借鉴了msf框架，很容易上手使用和开发插件。

此版本的ZEROScan致力于更好的批量化插件扫描。

## 安装

本框架采用 Python 语言开发，并且基础的第三方依赖包都已打包，只需要下载就可以直接进行使用。

(PS:但是如果插件有额外的需要模块，还需使用pip安装)

## 使用

```bash
➜  ZEROScan git:(master) ✗ python z-console.py

　　......(\_/)
　　......( '_')
　　..../\======░ ▒▓▓█D
　　/"\
　　\_@_@_@_@_@_@_@_@_@_/
+ -- --=[ ZEROScan - 1.0.0dev ]
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
ZEROScan > list
\Modules
=======

expName    appName      appVersion  description
---------  ---------  ------------  -----------------------------
demo       PHP                1230  PH1424/down.php SQL Injection
ZEROScan > info demo

appName: PHP
appVersion: 1230
Author:
	123

Description:
	PH1424/down.php SQL Injection

Reference:
	http://124.xyz/

ZEROScan > use demo
ZEROScan exploit(demo) > options

Name    Current Setting      Required  Description
------  -----------------  ----------  --------------------------
URL                                 1  URL or URL file
Thread  1                           0  Threads
Cookie                              0  Cookie
Report  False                       0  do you need a html report?
ZEROScan exploit(demo) > set URL ww.baidu.com
URL => ww.baidu.com
ZEROScan exploit(demo) > run
[!]exploit target:'ww.baidu.com'
[!]Requesting target site:ww.baidu.com
+--------------+------------+-------------+
| target-url   | poc-name   | status      |
+==============+============+=============+
| ww.baidu.com | demo       | test_plugin |
+--------------+------------+-------------+
success : 1
ZEROScan exploit(demo) >
```

