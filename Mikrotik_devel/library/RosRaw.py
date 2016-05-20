#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#

from ansible.module_utils.RosCore import *


def RosRaw(path, action, hostname="", username="admin", password="", command="", port=8728, DEBUG=False):

    lst = [path + action]
    while True:
    # Connect
        mikrotik = Core(hostname, DEBUG=DEBUG)
        login = mikrotik.login(username, password)
        # Check if login is correct
        if login[0][0] == '!trap':
            if DEBUG == True:
                print login

            return {"failed": True, "changed": False, "msg": "Login failed"}

        else:
            if DEBUG == True:
                print login

        if len(command) != 0:
            for i in range(0, len(command)):
                lst.append(command[i])

        raw_response = mikrotik.talk(lst)
        mikrotik.close_connection()
        return {"response": raw_response}

