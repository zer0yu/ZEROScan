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
    paths.ZEROSCAN_ROOT_PATH = modulePath()
    setPaths()
    kb.unloadedList = {}
    initializeKb()
    initializeExp()
    zs = baseConsole()
    zs.cmdloop()




def modulePath():
    """
    @function the function will get us the program's root directory
    """
    return getUnicode(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), sys.getfilesystemencoding())