#!/usr/bin/env python
# -*- coding:utf-8 -*-

import copy
import os
from lib.core.data import kb
from lib.core.data import conf
from lib.core.common import paths
from lib.core.pluginbase import PluginBase
from lib.controller.controller import start
from lib.core.option import setMultipleTarget


def ListPlugins():
    """
    @function show all plugins
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
    @function search plugins
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
    @function show the plugin infomations
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
    @function show the plugin options
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
    @function set the plugin options
    :param option: string, 设置项名称
    :param value: string, 设置值
    :return:
    """
    #TODO
    #目标如果在txt文件中，必须将文件放在targets目录下
    if option.upper() == "URL":
        path_files = os.listdir(paths.ZEROSCAN_TARGET_PATH)
        for tmp_path_file in path_files:
            if str(value) in tmp_path_file:
                tmp_str = str(value)
                if tmp_str[-4:] == '.txt':
                    conf.urlFile = str(value)
                    return "%s => %s" % (option, value)
                else:
                    conf.urlFile = str(value)+'.txt'
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
    @function clear var
    :return:
    """
    conf.urlFile = ""
    conf.url = ""
    conf.threads = 1
    conf.cookie = ""
    conf.report = False

def ExecPlugin():
    """
    @function exec the plugin
    :return:
    """
    setMultipleTarget()
    start()