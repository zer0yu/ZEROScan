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
from lib.core.common import paths
from lib.core.exception import ZEROScanFilePathException
from thirdparty.oset.pyoset import oset


def initializeKb():
    kb.targets = Queue.Queue()
    kb.exps = {}
    kb.results = oset()

def setMultipleTarget():
    #urlFile
    if not conf.urlFile:
        target_urls = []
        if conf.url:
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
        else:
            errMsg = 'the url needs to be set'
            log.error(errMsg)
        return
    if paths.ZEROSCAN_TARGET_PATH in conf.urlFile:
        conf.urlFile = safeExpandUser(conf.urlFile)
        infoMsg = "parsing multiple targets list from '%s'" % conf.urlFile
        log.process(infoMsg)
    else:
        conf.urlFile = paths.ZEROSCAN_TARGET_PATH +'/'+ conf.urlFile
        conf.urlFile = safeExpandUser(conf.urlFile)
        infoMsg = "parsing multiple targets list from '%s'" % conf.urlFile
        log.process(infoMsg)

    if not os.path.isfile(conf.urlFile):
        errMsg = "the specified file does not exist"
        raise ZEROScanFilePathException(errMsg)
    for line in getFileItems(conf.urlFile):
        kb.targets.put(line.strip())