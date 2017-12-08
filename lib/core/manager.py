#!/usr/bin/env python
# -*- coding:utf-8 -*-

import binascii
import json
import sqlite3
import copy
from os import walk

from lib.core import log
from lib.core.data import kb
from lib.core.data import conf
from lib.core.common import paths
from lib.core.pluginbase import PluginBase
from lib.controller.controller import start
from lib.core.option import setMultipleTarget
from lib.core.option import initializeKb
from thirdparty import requests


def ListPlugins():
    """
    显示插件列表
    :return: list(dict) expName,appName, appVersion, description
    """
    list_plugin_info = []
    plugin_info = {}
    zsp = PluginBase(package='zsplugins')
    plugin_zsp = zsp.make_plugin_source(searchpath=[paths.ZEROSCAN_PLUGINS_PATH])
    expNames = plugin_zsp.list_plugins()
    for expName in expNames:
        plugin_tmp = InfoPlugin(expName)
        plugin_info["expName"] = expName
        plugin_info["appName"] = plugin_tmp["appName"]
        plugin_info["appVersion"] = plugin_tmp["appVersion"]
        plugin_info["description"] = plugin_tmp["description"]
        pi_tmp = copy.deepcopy(plugin_info)#python的优化造成必须使用deepcopy
        list_plugin_info.append(pi_tmp)
    return list_plugin_info


def SearchPlugin(keyword):
    """
    搜索插件
    :param keyword: string, 插件信息
    :return: list, 插件列表
    """
    return_list = []
    plugin_info = {}
    zsp = PluginBase(package='zsplugins')
    plugin_zsp = zsp.make_plugin_source(searchpath=[paths.ZEROSCAN_PLUGINS_PATH])
    expNames = plugin_zsp.list_plugins()
    for expName in expNames:
        if keyword in expName:
            plugin_tmp = InfoPlugin(expName)
            plugin_info["expName"] = expName
            plugin_info["appName"] = plugin_tmp["appName"]
            plugin_info["appVersion"] = plugin_tmp["appVersion"]
            plugin_info["description"] = plugin_tmp["description"]
            pi_tmp = copy.deepcopy(plugin_info)#python的优化造成必须使用deepcopy
            return_list.append(pi_tmp)
    return return_list

def InfoPlugin(plugin):
    """
    显示插件信息
    :param plugin: string, 插件名
    :return: dict, 所有的插件信息
    """
    zsp = PluginBase(package='zsplugins')
    plugin_zsp = zsp.make_plugin_source(searchpath=[paths.ZEROSCAN_PLUGINS_PATH])
    zspi = plugin_zsp.load_plugin('%s'%plugin)
    zspi_tmp = zspi.expInfo()
    return zspi_tmp


def ShowOptions():
    """
    显示插件设置项
    kb.CurrentPlugin
    :return:插件的options
    """
    zspi_to_re = []
    zspi_dict_tmp = {}
    zsp = PluginBase(package='zsplugins')
    plugin_zsp = zsp.make_plugin_source(searchpath=[paths.ZEROSCAN_PLUGINS_PATH])
    zspi = plugin_zsp.load_plugin('%s'%(kb.CurrentPlugin))
    zspi_tmp = zspi.expInfo()
    for list_tmp in zspi_tmp["options"]:
        if list_tmp["Name"] == "URL":
            if conf.url:
                zspi_dict_tmp["Name"] = "URL"
                zspi_dict_tmp["Current Setting"] = conf.url
                zspi_dict_tmp["Required"] = True
                zspi_dict_tmp["Description"] = "URL or URL file"
            elif conf.urlFile:
                zspi_dict_tmp["Name"] = "URL"
                zspi_dict_tmp["Current Setting"] = conf.urlFile
                zspi_dict_tmp["Required"] = True
                zspi_dict_tmp["Description"] = "URL or URL file"
            else:
                zspi_dict_tmp["Name"] = "URL"
                zspi_dict_tmp["Current Setting"] = ""
                zspi_dict_tmp["Required"] = True
                zspi_dict_tmp["Description"] = "URL or URL file"
        if list_tmp["Name"] == "Thread":
            zspi_dict_tmp["Name"] = "Thread"
            zspi_dict_tmp["Current Setting"] = conf.threads
            zspi_dict_tmp["Required"] = False
            zspi_dict_tmp["Description"] = "Threads"
        if list_tmp["Name"] == "Cookie":
            zspi_dict_tmp["Name"] = "Cookie"
            zspi_dict_tmp["Current Setting"] = conf.cookie
            zspi_dict_tmp["Required"] = False
            zspi_dict_tmp["Description"] = "Cookie"
        if list_tmp["Name"] == "Report":
            zspi_dict_tmp["Name"] = "Report"
            zspi_dict_tmp["Current Setting"] = conf.report
            zspi_dict_tmp["Required"] = False
            zspi_dict_tmp["Description"] = "do you need a html report?"
        _=copy.deepcopy(zspi_dict_tmp)
        zspi_to_re.append(_)
    return zspi_to_re

def SetOption(option, value):
    """
    设置插件选项
    :param option: string, 设置项名称
    :param value: string, 设置值
    :return:
    """
    #TODO
    #目标如果在文件中，必须将文件放在targets目录下
    if option.upper() == "URL":
        if "targets" in option:
            conf.urlFile = str(value)
            return "%s => %s" % (option, value)
        else:
            #这个是要check的
            conf.url = str(value)
            return "%s => %s" % (option, value)
    elif option == "Thread":
        conf.threads = value
        return "%s => %s" % (option, value)
    elif option == "Cookie":
        conf.cookie = str(value)
        return "%s => %s" % (option, value)
    elif option == "Report":
        conf.report = value
        return "%s => %s" % (option, value)
    else:
        return "Invalid option: %s" % option

def ClearConf():
    """
    清除变量
    :return:
    """
    conf.urlFile = ""
    conf.url = ""
    conf.threads = 1
    conf.cookie = ""
    conf.report = False

def ExecPlugin():
    """
    执行插件
    :return:
    """
    setMultipleTarget()
    start()


def DownPluginList(self):
    """
    获取远程插件列表
    :param dirs: 所有插件目录
    :return: list, 远程插件列表
    """
    BaseUrl = "https://api.github.com/repos/zer0yu/" \
                "ZEROScan/contents/"
    PluginDirs = []
    RemotePlugins = []

    def DownPluginDirs():
        """
        获取远程插件目录
        :return:
        """
        r = requests.get(BaseUrl+"modules")
        r.close()
        j = json.loads(r.text)
        for i in j:
            PluginDirs.append(i["path"])

    def DownSingleDir(PluginDir):
        """
        下载单个目录插件列表
        :param plugin_dir: list, 插件目录
        """
        RemotePlugins = []
        r = requests.get(BaseUrl+PluginDir)
        r.close()
        j = json.loads(r.text)
        for i in j:
            RemotePlugins.append(i["path"])
        return RemotePlugins

    def log(request, result):
        """
        threadpool callback
        """
        RemotePlugins.extend(result)

    DownPluginDirs()
    pool = threadpool.ThreadPool(10)
    reqs = threadpool.makeRequests(DownSingleDir, PluginDirs, log)
    for req in reqs:
        pool.putRequest(req)
    pool.wait()
    return RemotePlugins

def GetLocalPluginList(self):
    """
    获取本地插件列表
    :return:
    """
    LocalPlugins = []
    for dirpath, dirnames, filenames in walk("modules/"):
        if dirpath == "modules/":
            continue
        for fn in filenames:
            if fn.endswith(".py"):
                LocalPlugins.append(dirpath+"/"+fn)
    return LocalPlugins

def DownPlugins(self, RemotePlugins, LocalPlugins):
    """
    下载插件
    :param RemotePlugins: list, 远程插件列表
    :param LocalPlugins: list, 本地插件列表
    :return: list, 新增插件列表
    """
    def down_single_plugin(plugin):
        """
        下载单个插件
        :return:
        """
        BaseUrl = "https://api.github.com/repos/zer0yu/" \
                    "ZEROScan/contents/"
        r = requests.get(BaseUrl+plugin)
        r.close()
        j = json.loads(r.text)
        data = binascii.a2b_base64(j["content"])
        with open(plugin, "w") as f:
            f.write(data)

    for plugin in LocalPlugins:
        if plugin in RemotePlugins:
            RemotePlugins.remove(plugin)
    pool = threadpool.ThreadPool(10)
    reqs = threadpool.makeRequests(down_single_plugin, RemotePlugins)
    for req in reqs:
        pool.putRequest(req)
    pool.wait()
    return RemotePlugins