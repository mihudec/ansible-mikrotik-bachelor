#!/usr/bin/python
# -*- coding: UTF-8 -*-

from RosRaw import *

if __name__ == '__main__':
    response = RosRaw(path="/system/package/", action="print", hostname="192.168.1.100", \
        username="admin", password="Epuak3578@", DEBUG=True, command=["?name=ipv6"])

    print response



