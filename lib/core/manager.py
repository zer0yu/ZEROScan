#!/usr/bin/env python
# -*- coding:utf-8 -*-

import binascii
import json
import sqlite3
from imp import find_module, load_module
from lib.thirdparty import requests
from lib.thirdparty.threadpool import threadpool
from os import walk


class PluginManager(object):
    """
    插件管理器
    """
    def __init__(self):
        self.plugins = {}
        self.conn = sqlite3.connect("lib/core/core.db")
        self.conn.text_factory = str
        self.cu = self.conn.cursor()
        self.CurrentPlugin = ""

    def version(self):
        """
        插件库版本
        :return: string, 插件库版本
        """
        self.cu.execute("select version from core")
        return self.cu.fetchone()[0]

    def CMSNum(self):
        """
        查询 CMS 数量
        :return: int, CMS 数量
        """
        self.cu.execute("select cms from modules")
        return len(set(self.cu.fetchall()))

    def PluginsNum(self):
        """
        查询插件数量
        :return: int, 插件数量
        """
        self.cu.execute("select count(*) from modules")
        return self.cu.fetchone()[0]

    def ListPlugins(self):
        """
        显示插件列表
        :return: list, 插件列表
        """
        self.cu.execute("select name, scope, description from modules")
        return self.cu.fetchall()

    def SearchPlugin(self, keyword):
        """
        搜索插件
        :param keyword: string, 插件信息
        :return: list, 插件列表
        """
        keyword = "%" + keyword + "%"
        self.cu.execute("select name, scope, description from modules where "
                        "name like ? or description like ?", (keyword, keyword))
        return self.cu.fetchall()

    def InfoPlugin(self, plugin):
        """
        显示插件信息
        :param plugin: string, 插件名
        :return: string, 插件信息
        """
        self.cu.execute("select name, author, cms, scope, description, "
                        "reference from modules where name=?", (plugin,))
        return self.cu.fetchone()

    def LoadPlugin(self, plugin):
        """
        加载插件
        :param plugin: string, 插件名
        :return:
        """
        if plugin not in self.plugins:
            self.plugins[plugin] = {}
            PluginName = plugin[plugin.index("_")+1:]
            PluginDir = "modules/" + plugin[:plugin.index("_")]
            module = load_module(PluginName,
                                 *find_module(PluginName, [PluginDir]))
            self.plugins[plugin]["options"] = module.options
            self.plugins[plugin]["exploit"] = module.exploit
        self.CurrentPlugin = plugin

    def ShowOptions(self):
        """
        显示插件设置项
        :return:
        """
        return self.plugins[self.CurrentPlugin]["options"]

    def SetOption(self, option, value):
        """
        设置插件选项
        :param option: string, 设置项名称
        :param value: string, 设置值
        :return:
        """
        for op in self.plugins[self.CurrentPlugin]["options"]:
            if op["Name"] == option:
                op["Current Setting"] = value
                return "%s => %s" % (op["Name"], value)
                break
        else:
            return "Invalid option: %s" % option

    def ExecPlugin(self):
        """
        执行插件
        :return:
        """
        #exp中的options
        options = {}
        for option in self.plugins[self.CurrentPlugin]["options"]:
            #这里的name可以是cookie，url，thread
            name = option["Name"]
            CurrentSet = option["Current Setting"]
            required = option["Required"]
            if required and not CurrentSet:
                return "%s is required!" % name
            else:
                if name == "URL":
                    if CurrentSet.endswith("/"):
                        options["URL"] = CurrentSet[:-1]
                    else:
                        options["URL"] = CurrentSet
                elif name == "Cookie":
                    options["Cookie"] = dict(
                        i.split("=", 1)
                        for i in CurrentSet.split("; ")
                    )
                elif name == "Thread":
                    options["Thread"] = int(CurrentSet)
                else:
                    options[name] = CurrentSet
        try:
            vuln = self.plugins[self.CurrentPlugin]["exploit"](**options)
            if vuln:
                self.cu.execute("insert into vulns values (?, ?)",
                                (self.CurrentPlugin, vuln))
                self.conn.commit()
                return True, vuln
            else:
                return False, "Exploit failed, perhaps not vulnerable?"
        except sqlite3.ProgrammingError:
            return True, vuln
        except Exception, e:
            return False, "%s: %s" % (self.CurrentPlugin, e.message)

    def ShowVulns(self):
        """
        显示当前漏洞信息
        :return:
        """
        self.cu.execute("select plugin, vuln from vulns")
        return self.cu.fetchall()

    def ClearVulns(self):
        """
        清空漏洞信息
        :return:
        """
        self.cu.execute("delete from vulns")
        self.conn.commit()

    def DBRebuild(self):
        """
        重建数据库
        :return:
        """
        self.cu.execute("delete from modules")
        self.conn.commit()
        for dirpath, dirnames, filenames in walk("modules/"):
            if dirpath == "modules/":
                continue
            db = {
                "cms": dirpath.split("/")[1],
                "modules": []
            }
            for fn in filenames:
                if fn.endswith("py"):
                    db["modules"].append(fn.split(".")[0])
            for module in db["modules"]:
                p = load_module(module, *find_module(module, [dirpath]))
                name = db["cms"] + "_" + module
                author = p.author
                scope = p.scope
                description = p.description
                reference = p.reference
                self.cu.execute("insert into modules values (?, ?, ?, ?, ?, ?)",
                                (name, author, db["cms"], scope, description,
                                 reference))
                self.conn.commit()

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

    def Exit(self):
        """
        退出插件管理器
        :return:
        """
        self.conn.close()
