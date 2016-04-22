#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_dns
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

# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),
                remote_requests=dict(required=False, type='str'),
                servers=dict(required=False, type='str'),

        ),
        supports_check_mode=False,

)


def main():  # main logic
    from ansible.module_utils.RosAPI import API
    # Initialize phase
    # Required parameters

    hostname = ansible.params['hostname']
    username = ansible.params['username']
    password = ansible.params['password']
    port = ansible.params['port']

    path = "/ip/dns/"
    # This module forces SET option
    action = "set"

    command = {}

    if ("servers" in ansible.params.keys()) and (ansible.params['servers'] != None):
        command["servers"] = ansible.params['servers']

    if ("remote_requests" in ansible.params.keys()) and (ansible.params['remote_requests'] != None):
        command["allow-remote-requests"] = ansible.params['remote_requests']



    while True:
        response = API(path, action, hostname, port=port, username=username, password=password, command=command)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])
        break

from ansible.module_utils.basic import *

main()
