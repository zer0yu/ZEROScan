#!/usr/bin/env python
# -*- coding:utf-8 -*-

from thirdparty.colorama import init,Fore

def error(string):
    """
    输出错误信息
    :param string: string, 欲输出的信息
    :return:
    """
    init(autoreset=True) 
    print(Fore.RED + "[!]"+string)


def success(string):
    """
    输出成功信息
    :param string: string, 欲输出的信息
    :return:
    """
    init(autoreset=True) 
    print(Fore.GREEN + "[!]"+string)


def process(string):
    """
    输出进程中信息
    :param string: string, 欲输出的信息
    :return:
    """
    init(autoreset=True) 
    print(Fore.BLUE + "[!]"+string)

def warn(string):
    """
    输出进程中信息
    :param string: string, 欲输出的信息
    :return:
    """
    init(autoreset=True) 
    print(Fore.YELLOW + "[!]"+string)