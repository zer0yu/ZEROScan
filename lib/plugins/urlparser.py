#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urlparse

def GetDomain(url):
    """
    得到标准的URL
    Use:
    GetDomain('http://www.baidu.com/index.php?username=guol')
    Return:
    'http://www.baidu.com'
    """
    u = urlparse.urlparse(url)
    return urlparse.urlunsplit([u.scheme, u.netloc, '', '', ''])


def IteratePath(OriStr):
    """
    返回解析之后的URL列表
    Use:
    IteratePath('http://www.baidu.com/jsp/index.php?username=guol')
    Return:
    ['http://www.baidu.com/index.php?username=guol',
     'http://www.baidu.com/'
     'http://www.baidu.com/jsp',
     'http://www.baidu.com/jsp/index.php?username=guol']

    """
    parser = urlparse.urlparse(OriStr)
    _path_list = parser.path.replace('//', '/').strip('/').split('/')
    _ans_list = set()
    _ans_list.add(OriStr)

    if not _path_list[0]:
        return _ans_list

    _ans_list.add(GetDomain(OriStr))
    s = ''
    for each in _path_list:
        s += '/' + each
        _ans_list.add(urlparse.urljoin(OriStr, s))
    return _ans_list