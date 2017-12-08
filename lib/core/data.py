#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.core.datatype import AttribDict
from lib.core.defaults import defaults

# object to share within function and classes command
# line options and settings
conf = AttribDict()

# Dictionary storing
# (1)targets<队列形式的目标>, (2)targetName<options中的值>, (3) CurrentPlugin<当前插件的信息>
# (4)results, (5)expNumbers<插件数目>
# (6)multiThreadMode \ threadContinue \ threadException
kb = AttribDict()

registeredPocs = {}

# zeroscan paths，本质上还是个字典类型
paths = AttribDict()

defaults = AttribDict(defaults)

savedReq = AttribDict()
