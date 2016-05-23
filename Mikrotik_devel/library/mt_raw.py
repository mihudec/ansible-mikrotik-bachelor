#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#

DOCUMENTATION = '''
---
module: mt_raw
author: Miroslav Hudec
version_added: ""
short_description: Sets information provided by DHCP server
requirements: [ RosAPI ]
description:
    - Sets information provided by DHCP server, such as default gateway, DNS servers, domain name etc...
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
    port:
        required: False
        description:
        - Port used to connect to MikroTik's API, default 8728


'''






from ansible.module_utils.basic import *
from ansible.module_utils.RosRaw import *
from ansible.module_utils.RosAPI import *

# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),
                path=dict(required=True, type='str'),
                action=dict(required=True, type='str', ),
                command=dict(required=False, type='list'),
                query=dict(required=False, type='str'),

        ),
        supports_check_mode=False,

)
"""

# Debugging Section
class AnsibleModule:
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", "port": 8728, \
              "command": [], "path": "/system/", "action": "reboot"}


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

def main():  # main logic

    # Initialize phase
    # Required parameters
    privkeys = ["hostname", "username", "password", "port", "path", "action"]
    command = []
    path = ansible.params["path"]
    action = ansible.params["action"]
    while True:
        if ansible.params["command"] is not None:

            for item in ansible.params["command"]:
                command.append("=" + item)



        response = RosRaw(path, action, hostname, username, password, command=command, port=port, DEBUG=DEBUG)
        creply = replyCheck(response)
        if not creply["success"]:
            ansible.fail_json(failed=True, changed=False, msg=str(response))
        else:
            ansible.exit_json(failed=False, changed=True, msg=str(response))


from ansible.module_utils.basic import *

main()
