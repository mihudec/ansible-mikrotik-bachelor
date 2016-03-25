#!/usr/bin/python
# -*- coding: UTF-8 -*-

from RosAPI import API

def main():

    # Basic variables
    path = "/ip/address/"
    action = "add"
    hostname = "192.168.116.110"
    password = ""
    command = {"interface": "ether2", "address": "192.168.110.1/24"}


    r = API(path, action, hostname, password=password, command=command, DEBUG=True)
    print r



main()