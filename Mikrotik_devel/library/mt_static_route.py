#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_dhcp_server
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
                dst_address=dict(required=True, type='str'),
                gateway=dict(required=True, type='str'),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                comment=dict(required=False, type='str'),

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

    while True:

        # DHCP Server
        path = "/ip/route/"
        action = ""

        command = {}

        if ("dst_address" in ansible.params.keys()) and (ansible.params['dst_address'] != None):
            command["dst-address"] = ansible.params['dst_address']
        if ("gateway" in ansible.params.keys()) and (ansible.params['gateway'] != None):
            command["gateway"] = ansible.params['gateway']


        # Let RosAPI do the rest
        response = API(path, action, hostname, username, password, command=command, port=port)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])



from ansible.module_utils.basic import *
main()