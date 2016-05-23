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

#from ansible.module_utils.basic import *
from ansible.module_utils.RosAPI import *
from ansible.module_utils.RosRaw import *

"""
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
                comment=dict(required=False, type='str'),



        ),

        supports_check_mode=False,

)
"""


# Debugging Section
class AnsibleModule:
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "in_interface": "ether1", "port": 8728, "disabled": "false", "chain": "forward",\
              "connection_state": "established,related", "log": "false", "action": "accept"}


ansible = AnsibleModule

# Global Variables
privkeys = ["hostname", "username", "password", "port", "path", "action"]
# Initialize phase
# Required parameters
hostname = ansible.params['hostname']
username = ansible.params['username']
password = ansible.params['password']
port = ansible.params['port']
DEBUG = True # This is only for debugging, if set to True Ansible will crash
switch = True  # Glabal switch


def main():  # main logic

    arguments = digestArgs(ansible.params)
    exitmessage = []

    while True:
        changed = False
        # Required params
        privkeys = ["hostname", "username", "password", "port", "path", "action"]
        command = {}

        for key in arguments.keys():
            if key not in privkeys:
                command[key] = arguments[key]
        # Call API
        response = API(path="/ip/firewall/filter/", action="add", username=username, hostname=hostname, \
                       password=password, command=command, port=port, DEBUG=DEBUG)
        print response







        message = "Already in desired state." + str(exitmessage)
        if changed: message = "Configured to desired state by Ansible." + str(exitmessage)

        ansible.exit_json(failed=False, changed=changed, msg=message)


from ansible.module_utils.basic import *

main()
