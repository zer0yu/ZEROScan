#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from lib.thirdparty.odict.odict import OrderedDict
from lib.core.exception import *
from lib.core.data import *



def setPaths():
    paths.WEAK_PASS = "data/password-top100.txt"
    paths.LARGE_WEAK_PASS = "data/password-top1000.txt"
    paths.UA_LIST_PATH = "data/user-agents.txt"


def checkFile(filename):
    """
    function Checks for file existence and readability
    """
    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except IOError:
            valid = False

    if not valid:
        raise ToolkitSystemException("unable to read file '%s'" % filename)


def getFileItems(filename, commentPrefix='#', unicode_=True, lowercase=False, unique=False):
    """
    @function returns newline delimited items contained inside file
    """

    retVal = list() if not unique else OrderedDict()

    checkFile(filename)

    try:
        with open(filename, 'r') as f:
            for line in (f.readlines() if unicode_ else f.xreadlines()):
                # xreadlines doesn't return unicode strings when codecs.open() is used
                if commentPrefix and line.find(commentPrefix) != -1:
                    line = line[:line.find(commentPrefix)]

                line = line.strip()

                if not unicode_:
                    try:
                        line = str.encode(line)
                    except UnicodeDecodeError:
                        continue

                if line:
                    if lowercase:
                        line = line.lower()

                    if unique and line in retVal:
                        continue

                    if unique:
                        retVal[line] = True

                    else:
                        retVal.append(line)

    except (IOError, OSError, MemoryError), ex:
        errMsg = "something went wrong while trying "
        errMsg += "to read the content of file '%s' ('%s')" % (filename, ex)
        raise ToolkitSystemException(errMsg)

    return retVal if not unique else retVal.keys()