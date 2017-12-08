#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import socket
import os

from lib.core.data import kb
from lib.core.data import conf
from lib.core import log
from lib.core.common import getFileItems
from lib.core.common import safeExpandUser
from lib.core.common import getPublicTypeMembers
from lib.core.exception import ZEROScanFilePathException
from lib.core.exception import ZEROScanSyntaxException
from thirdparty.oset.pyoset import oset


def initializeKb():
    kb.targets = Queue.Queue()#kb.targets.put(url)入队；kb.targets.get()出队，先进先出
    kb.exps = {}
    kb.results = oset()#有序集合[]

def setMultipleTarget():
    #urlFile
    if not conf.urlFile:
        target_urls = []
        #c段地址
        if conf.url.endswith('/24'):
            try:
                socket.inet_aton(conf.url.split('/')[0])
                base_addr = conf.url[:conf.url.rfind('.') + 1]
                target_urls = ['{}{}'.format(base_addr, i)
                                for i in xrange(1, 255 + 1)]
            except socket.error:
                errMsg = 'only id address acceptable'
                log.error(errMsg)
        else:
            target_urls = conf.url.split(',')

        for url in target_urls:
            if url:
                kb.targets.put((url))
        return
    #安全载入文件，防止出现编码错误
    conf.urlFile = safeExpandUser(conf.urlFile)
    infoMsg = "parsing multiple targets list from '%s'" % conf.urlFile
    log.process(infoMsg)

    #检查编码是否错误
    if not os.path.isfile(conf.urlFile):
        errMsg = "the specified file does not exist"
        raise ZEROScanFilePathException(errMsg)
    #将conf.urlFile路径中存储的文件读出
    for line in getFileItems(conf.urlFile):
        kb.targets.put(line.strip())