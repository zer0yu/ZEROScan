#!/usr/bin/env python
# -*- coding:utf-8 -*-

from thirdparty.colorama import init,Fore

def error(string):
    """
    retun a error information
    :param string: string, the string you want to print
    :return:
    """
    init(autoreset=True) 
    print(Fore.RED + "[!]"+string)


def success(string):
    """
    retun a success information
    :param string: string, the string you want to print
    :return:
    """
    init(autoreset=True) 
    print(Fore.GREEN + "[!]"+string)


def process(string):
    """
    retun the process information
    :param string: string, the string you want to print
    :return:
    """
    init(autoreset=True) 
    print(Fore.BLUE + "[!]"+string)

def warn(string):
    """
    retun a warning information
    :param string: string, the string you want to print
    :return:
    """
    init(autoreset=True) 
    print(Fore.YELLOW + "[!]"+string)