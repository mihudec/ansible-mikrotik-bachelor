#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_brctl
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

                names=dict(required=True, type='list'),
                admin_mac=dict(required=False, type='str', choices=["true", "false"]),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                mtu=dict(required=False, type='int'),
                priority=dict(required=False, type='int'),
                comment=dict(required=False, type='str'),

                interfaces=dict(required=False, type='list'),
                auto_isolate=dict(required=False, type='str', choices=["true", "false"]),
                point_to_point=dict(required=False, type='str', choices=["true", "false", "auto"]),
                path_cost=dict(required=False, type='int'),



        ),

        supports_check_mode=False,

)
"""


# Debugging Section
class AnsibleModule:
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "names": ["bridge0"], "port": 8728, "disabled": "false", "interfaces": ["ether2"]}


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
switch = True  # Glabal switch


def toRawCommand(params):
    rawcmd = []
    for key in params.keys():
        if (key not in privkeys) and (params[key] is not None):
            rawcmd.append("=" + digestArg(key) + "=" + str(params[key]))


def main():  # main logic

    exitmessage = []

    while True:
        changed = False
        # Required params
        privkeys = ["hostname", "username", "password", "port", "path", "action"]


        # Section for Bridge management
        brparams=["admin_mac", "disabled", "mtu", "priority", "comment"]

        # For each bridge name
        if ansible.params["names"] is not None:
            # Create common command
            brcommand = {}
            for key in ansible.params.keys():
                if (key not in privkeys) and (key in brparams) and (ansible.params[key] is not None):
                    brcommand[digestArg(key)] = str(ansible.params[key])
            if DEBUG: print brcommand



            for bridge in ansible.params["names"]:
                brcommand["name"] = bridge
                response = API(path="/interface/bridge/", action="add", username=username, password=password,\
                        hostname=hostname, port=port, command=brcommand)
                if response['failed']:
                    if DEBUG: print bridge + " failed."
                    if response["msg"] == "Login failed":
                        ansible.fail_json(failed=True, changed=False, msg=response["msg"])
                    else:
                        ansible.fail_json(failed=True, changed=False, msg=["Configuring " + bridge + " failed.", \
                                          exitmessage])
                if response['changed']:
                    if DEBUG: print bridge + " was configured to desired state."
                    exitmessage.append(bridge + " was configured to desired state;")
                    changed = True
                else:
                    if DEBUG: print bridge + " is already in desired state."
                    exitmessage.append(bridge + " is already in desired state;")


        # Section for ports management

        intparams = ["auto_isolate", "point_to_point", "path_cost"]

        if ansible.params["interfaces"] is not None:
            # Create common command
            intcommand = {}
            for key in ansible.params.keys():
                if (key not in privkeys) and (key in intparams) and (ansible.params[key] is not None):
                    intcommand[digestArg(key)] = str(ansible.params[key])
            if DEBUG: print intcommand



            for interface in ansible.params["interfaces"]:
                intcommand["interface"] = interface
                intcommand["bridge"] = ansible.params["names"][0] # Add ports to first specified bridge
                response = API(path="/interface/bridge/port/", action="add", username=username, password=password,\
                        hostname=hostname, port=port, command=intcommand)
                if response['failed']:
                    if DEBUG: print interface + " failed."
                    ansible.fail_json(failed=True, changed=False, msg=["Configuring " + interface + " failed.", \
                                      exitmessage])

                if response['changed']:
                    if DEBUG: print interface + " was configured to desired state."
                    exitmessage.append(interface + " was configured to desired state;")
                    changed = True
                else:
                    if DEBUG: print interface + " is already in desired state."
                    exitmessage.append(interface + " is already in desired state;")








        message = "Already in desired state." + str(exitmessage)
        if changed: message = "Configured to desired state by Ansible." + str(exitmessage)

        ansible.exit_json(failed=False, changed=changed, msg=message)


from ansible.module_utils.basic import *

main()
