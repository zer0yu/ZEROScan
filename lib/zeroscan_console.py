#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from lib.core.common import getUnicode
from lib.core.common import setPaths
from lib.core.data import kb
from lib.core.data import paths
from lib.core.consoles import initializeExp
from lib.core.consoles import baseConsole
from lib.core.option import initializeKb

def main():
    #文件根目录的绝对路径
    #/Users/zeroyu/Desktop/ZEROScan-1.0/
    paths.ZEROSCAN_ROOT_PATH = modulePath()
    #初始化路径
    setPaths()
    #{1: u'/Users/zeroyu/Desktop/ZEROScan-1.0/plugins/test_plugin.py'}
    kb.unloadedList = {}
    #初始化：目标，exp，结果
    initializeKb()
    initializeExp()
    #load的时候先记录插件名称，然后在exec的时候去执行相应的函数
    zs = baseConsole()
    zs.cmdloop()




def modulePath():
    """
    @function the function will get us the program's root directory
    """
    return getUnicode(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), sys.getfilesystemencoding())