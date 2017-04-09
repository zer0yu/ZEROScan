#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.core.settings import *
from lib.utils import versioncheck
from lib.zeroscan_console import Interface

def main():

    interface = Interface()
    print BANNER % (interface.version(),
                  "%d CMS" % interface.CMSNum(),
                  "%d Plugins" % interface.PluginsNum())
    while True:
        try:
            interface.cmdloop()
        except KeyboardInterrupt:
            print "Interrupt: use the 'exit' command to quit"

if __name__ == "__main__":
    main()