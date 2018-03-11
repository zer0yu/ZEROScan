#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import traceback
from thread import error as threadError

from lib.core import log
from lib.core.data import kb

from lib.core.settings import PYVERSION

from lib.core.exception import ZEROScanConnectionException
from lib.core.exception import ZEROScanThreadException
from lib.core.exception import ZEROScanValueException


def runThreads(numThreads, threadFunction, forwardException=True, startThreadMsg=True):
    threads = []
    numThreads = int(numThreads)
    kb.multiThreadMode = True
    kb.threadContinue = True
    kb.threadException = False

    try:
        if numThreads > 1:
            if startThreadMsg:
                infoMsg = "starting %d threads" % numThreads
                log.process(infoMsg)

        else:
            threadFunction()
            return

        for numThread in xrange(numThreads):
            thread = threading.Thread(target=exceptionHandledFunction, name=str(numThread), args=[threadFunction])

            setDaemon(thread)

            try:
                thread.start()
            except threadError, errMsg:
                errMsg = "error occurred while starting new thread ('%s')" % errMsg
                log.error(errMsg)
                break

            threads.append(thread)

        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print
        kb.threadContinue = False
        kb.threadException = True

        if numThreads > 1:
            log.process("waiting for threads to finish (Ctrl+C was pressed)")
        try:
            while (threading.activeCount() > 1):
                pass

        except KeyboardInterrupt:
            raise ZEROScanThreadException("user aborted (Ctrl+C was pressed multiple times)")

        if forwardException:
            raise

    except (ZEROScanConnectionException, ZEROScanValueException), errMsg:
        print
        kb.threadException = True
        log.process("thread %s: %s" % (threading.currentThread().getName(), errMsg))

    except:
        from lib.core.common import unhandledExceptionMessage

        print
        kb.threadException = True
        errMsg = unhandledExceptionMessage()
        log.error("thread %s: %s" % (threading.currentThread().getName(), errMsg))
        traceback.print_exc()

    finally:
        kb.multiThreadMode = False
        kb.bruteMode = False
        kb.threadContinue = True
        kb.threadException = False

#前台线程（默认），都终止才终止；后台线程，前终止后立即终止
def setDaemon(thread):
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def exceptionHandledFunction(threadFunction):
    try:
        threadFunction()
    except KeyboardInterrupt:
        kb.threadContinue = False
        kb.threadException = True
        raise
    except Exception, errMsg:
        # thread is just going to be silently killed
        log.error("thread %s: %s" % (threading.currentThread().getName(), errMsg))
