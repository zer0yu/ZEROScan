#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import tempfile
from textwrap import dedent
from lib.core.settings import REPORT_HTMLBASE
from lib.core.settings import REPORT_TABLEBASE
from lib.core.data import paths
from lib.core.exception import ZEROScanSystemException
from lib.core.exception import ZEROScanMissingPrivileges
from lib.core.common import getUnicode
from lib.core.common import reIndent
from lib.core.common import normalizeUnicode
from lib.core import log
from lib.core.data import conf
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
from lib.core.threads import runThreads
from lib.core.pluginbase import PluginBase
from thirdparty.python_tabulate.tabulate import tabulate


def start():
    #kb.targets是队列
    if kb.targets and kb.targets.qsize() > 1:
        infoMsg = "ZEROScan got a total of %d targets" % kb.targets.qsize()
        log.process(infoMsg)

    #多线程函数，线程数，函数
    runThreads(conf.threads, expThreads)

    if not kb.results:
        return

    toNum = 0
    tmp = []
    for _ in kb.results:
        if _:
            toNum += 1
            tmp.append(list(_))

    print tabulate(tmp,["target-url", "poc-name", "status"],tablefmt="grid")
    print "success : {}".format(toNum)

    _createTargetDirs()
    _setRecordFiles()

    if conf.report:
        _setReport()


def expThreads():
    """
    @function multiThread executing
    """
    zsp = PluginBase(package='zsplugins')
    plugin_zsp = zsp.make_plugin_source(searchpath=[paths.ZEROSCAN_PLUGINS_PATH])
    zspi = plugin_zsp.load_plugin('%s'%(kb.CurrentPlugin))

    while not kb.targets.empty() and kb.threadContinue:
        target = kb.targets.get()
        infoMsg = "exploit target:'%s'" % (target)
        log.process(infoMsg)
        # TODO
        result = zspi.exploit(target, headers=conf.httpHeaders)
        #插件中没有返回值就默认是失败
        if not result:
            continue
        output = (target, kb.CurrentPlugin, result)

        kb.results.add(output)
        if isinstance(conf.timeout, (int, float)) and conf.timeout > 0:
            time.sleep(conf.timeout)


def _createTargetDirs():
    """
    Create the output directory.
    """
    if not os.path.isdir(paths.ZEROSCAN_OUTPUT_PATH):
        try:
            if not os.path.isdir(paths.ZEROSCAN_OUTPUT_PATH):
                os.makedirs(paths.ZEROSCAN_OUTPUT_PATH, 0755)
            warnMsg = "using '%s' as the output directory" % paths.ZEROSCAN_OUTPUT_PATH
            log.error(warnMsg)
        except (OSError, IOError), ex:
            try:
                tempDir = tempfile.mkdtemp(prefix="ZEROScanoutput")
            except Exception, _:
                errMsg = "unable to write to the temporary directory ('%s'). " % _
                errMsg += "Please make sure that your disk is not full and "
                errMsg += "that you have sufficient write permissions to "
                errMsg += "create temporary files and/or directories"
                raise ZEROScanSystemException(errMsg)

            warnMsg = "unable to create regular output directory "
            warnMsg += "'%s' (%s). " % (paths.ZEROSCAN_OUTPUT_PATH, getUnicode(ex))
            warnMsg += "Using temporary directory '%s' instead" % getUnicode(tempDir)
            log.error(warnMsg)

            paths.POCUSITE_OUTPUT_PATH = tempDir


def _setRecordFiles():
    for (target, expname, result) in kb.results:
        outputPath = os.path.join(getUnicode(paths.ZEROSCAN_OUTPUT_PATH), normalizeUnicode(getUnicode(target)))

        if not os.path.isdir(outputPath):
            try:
                os.makedirs(outputPath, 0755)
            except (OSError, IOError), ex:
                try:
                    tempDir = tempfile.mkdtemp(prefix="ZEROScantoutput")
                except Exception, _:
                    errMsg = "unable to write to the temporary directory ('%s'). " % _
                    errMsg += "Please make sure that your disk is not full and "
                    errMsg += "that you have sufficient write permissions to "
                    errMsg += "create temporary files and/or directories"
                    raise ZEROScanSystemException(errMsg)

                warnMsg = "unable to create output directory "
                warnMsg += "'%s' (%s). " % (outputPath, getUnicode(ex))
                warnMsg += "Using temporary directory '%s' instead" % getUnicode(tempDir)
                log.warn(warnMsg)

                outputPath = tempDir

        filename = str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())+".txt")
        recordFile = os.path.join(outputPath, filename)

        if not os.path.isfile(recordFile):
            try:
                with open(recordFile, "w") as f:
                    f.write("target,expname,result")
            except IOError, ex:
                if "denied" in getUnicode(ex):
                    errMsg = "you don't have enough permissions "
                else:
                    errMsg = "something went wrong while trying "
                errMsg += "to write to the output directory '%s' (%s)" % (paths.ZEROSCAN_OUTPUT_PATH, ex)

                raise ZEROScanMissingPrivileges(errMsg)

        try:
            with open(recordFile, "a+") as f:
                f.write("\n" + ",".join([target, expname, result]))
        except IOError, ex:
            if "denied" in getUnicode(ex):
                errMsg = "you don't have enough permissions "
            else:
                errMsg = "something went wrong while trying "
            errMsg += "to write to the output directory '%s' (%s)" % (paths.ZEROSCAN_OUTPUT_PATH, ex)

            raise ZEROScanMissingPrivileges(errMsg)


def _setReport():
    tdPiece = thStr = ""
    for _ in ("target-url", "exp-name", "status"):
        tdPiece += " <td>%s</td> "
        thStr += " <th>%s</td> " % _
    td = "<tr class='status' onclick='showDetail(this)'>%s</tr>" % tdPiece
    detail = "<tr class=\"result0\"><td colspan=\"6\">%s</td></tr>"
    tables = ""
    reportTable = dedent(REPORT_TABLEBASE)
    reportHtml = dedent(REPORT_HTMLBASE)
    for _ in kb.results:
        tdStr = td % _[:-2]
        detailStr = ""
        if _[-1]:
            result_obj = eval(_[-1])
            if result_obj:
                detailStr = "<dl>"
                for outkey in result_obj.keys():
                    items = "<dt>%s</dt>" % (outkey)
                    vals = result_obj.get(outkey)
                    for innerkey in vals.keys():
                        items += "<dd>%s: %s</dd>" % (innerkey, vals.get(innerkey))
                    detailStr += items
                detailStr += "</dl>"
        if detailStr:
            tdStr += detail % detailStr
        tables += reportTable % reIndent(tdStr, 4)
    html = reportHtml % (reIndent(thStr, 19), reIndent(tables, 16))

    with open(conf.report, 'w') as f:
        f.write(html)
