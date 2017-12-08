#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ZEROScanBaseException(Exception):
    pass


class ZEROScanUserQuitException(ZEROScanBaseException):
    pass


class ZEROScanDataException(ZEROScanBaseException):
    pass


class ZEROScanGenericException(ZEROScanBaseException):
    pass


class ZEROScanSystemException(ZEROScanBaseException):
    pass


class ZEROScanFilePathException(ZEROScanBaseException):
    pass


class ZEROScanConnectionException(ZEROScanBaseException):
    pass


class ZEROScanThreadException(ZEROScanBaseException):
    pass


class ZEROScanValueException(ZEROScanBaseException):
    pass


class ZEROScanMissingPrivileges(ZEROScanBaseException):
    pass


class ZEROScanSyntaxException(ZEROScanBaseException):
    pass
