#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_firewall
author: Miroslav Hudec
version_added: ""
short_description: Manage Mikrotik Routers
requirements: [ RosAPI ]
description:
    - Manage Mikrotik RouterOS devices.
options:
    hostname:
        required: True
        aliases: ["host"]
        description:
        - Hostname or IP address of Mikrotik device
    username:
        required: True
        aliases: ["user"]
        description:
        - Username used to login to Mikrotik's API
    password:
        required: True
        aliases: ["pass"]
        description:
        - Password used to login to Mikrotik's API


'''

from ansible.module_utils.basic import *
from ansible.module_utils.RosAPI import *
from ansible.module_utils.RosRaw import *


# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),

                chain=dict(required=True, type='str', choices=["input", "output", "forward"]),
                action=dict(required=True, type='str', choices=["accept", "reject", "drop"]),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                in_interface=dict(required=False, type='str'),
                out_interface=dict(required=False, type='str'),
                connection_state=dict(required=False, type='str'),
                connection_nat_state=dict(required=False, type='str'),
                protocol=dict(required=False, type='str'),
                src_address=dict(required=False, type='str'),
                dst_address=dict(required=False, type='str'),
                src_port=dict(required=False, type='str'),
                dst_port=dict(required=False, type='str'),
                log=dict(required=False, type='str', choices=["true", "false"]),
                log_prefix=dict(required=False, type='str'),
                comment=dict(required=True, type='str'),



        ),

        supports_check_mode=False,

)
"""


# Debugging Section
class AnsibleModule:
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "in_interface": "ether1", "port": 8728, "disabled": "false", "chain": "forward",\
              "connection_state": "established,related", "log": "false", "action": "accept", "comment": "rule1"}


ansible = AnsibleModule
"""
# Global Variables
privkeys = ["hostname", "username", "password", "port", "path", "action"]
# Initialize phase
# Required parameters
hostname = ansible.params['hostname']
username = ansible.params['username']
password = ansible.params['password']
port = ansible.params['port']
DEBUG = False # This is only for debugging, if set to True Ansible will crash



def main():  # main logic

    moduleparams = digestArgs(ansible.params)
    exitmessage = []

    while True:
        changed = False
        # Required params
        privkeys = ["hostname", "username", "password", "port", "path", "action"]
        rawcommand = []
        command = {}
        proplist = []
        propstr = ""

        for key in moduleparams.keys():
            if key not in privkeys:
                command[key] = moduleparams[key]
                proplist.append(key)
                propstr = propstr + key + ","
                rawcommand.append("=" + key + "=" + moduleparams[key])
        propstr = propstr + ".id"
        printcommand = ["=.proplist=" + propstr]


        # Call print
        response = RosRaw(path="/ip/firewall/filter/", action="print", username=username, hostname=hostname, \
                       password=password, command=printcommand, port=port, DEBUG=DEBUG)
        response = digestResponse(response["response"])
        if DEBUG: print "Print response: " + str(response)
        newresponse = {}
        # checkresponse
        isSame = True
        hascomment = False
        matchingresponse = {}
        id = ""

        if response != "noObjects":

            for i in range(0, len(response)):
                if command["comment"] == response[i]["comment"]:
                    if not hascomment:
                        hascomment = True
                        id = response[i][".id"]
                        matchingresponse = response[i]
                        info = "Found matching comment at ID "+ id
                        if DEBUG: print info
                        exitmessage.append(info)
                    else:
                        info = "Found multiple matching comments, cannot continue..."
                        if DEBUG: print info
                        exitmessage.append(info)
                        ansible.fail_json(failed=True, changed=False, msg="Module failed" + str(exitmessage))

        if hascomment:
            for item in proplist:
                if command[item] != matchingresponse[item]:
                    isSame = False
            if isSame:
                # Already in desired state
                info = "Matching rule with specified parameters already exists with ID: " + id
                exitmessage.append(info)
                if DEBUG: print info
                ansible.exit_json(failed=False, changed=False, msg="Already in desired state" + str(exitmessage))
            else:
                # SET
                rawcommand.append("=.id=" + id)
                response = RosRaw(path="/ip/firewall/filter/", action="set", username=username, hostname=hostname, \
                       password=password, command=rawcommand, port=port, DEBUG=DEBUG)
                if DEBUG: print "SET response: " + str(response)
                if response["response"][0][0] == "!done":
                    info = "Specified rule was SET by Ansible with ID "+id
                    if DEBUG: print info
                    exitmessage.append(info)
                    ansible.exit_json(Failed=False, changed=True, msg="Configured to desired state by Ansible." + str(exitmessage))
                else:
                    info = "Failed to SET rule."
                    if DEBUG: print info
                    exitmessage.append(info)
                    ansible.exit_json(Failed=True, changed=False, msg="Something went wrong." + str(exitmessage))

        else:
            # ADD
            response = RosRaw(path="/ip/firewall/filter/", action="add", username=username, hostname=hostname, \
                       password=password, command=rawcommand, port=port, DEBUG=DEBUG)
            if DEBUG: print "ADD response: "+str(response)
            if response["response"][0][0] == "!done":
                info = "Specified rule was ADDed by Ansible with ID "+response["response"][0][1]["=ret"]
                if DEBUG: print info
                exitmessage.append(info)
                ansible.exit_json(Failed=False, changed=True, msg="Configured to desired state by Ansible." + str(exitmessage))
            else:
                info = "Failed to ADD rule."
                if DEBUG: print info
                exitmessage.append(info)
                ansible.exit_json(Failed=True, changed=False, msg="Something went wrong." + str(exitmessage))



















from ansible.module_utils.basic import *

main()
