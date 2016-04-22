#!/usr/bin/python
# -*- coding: UTF-8 -*-


DOCUMENTATION = '''
---
module: mt_ip
author: Miroslav Hudec
version_added: ""
short_description: Sets IP addresses on Mikrotik's interfaces
requirements: [ RosAPI ]
description:
    - Sets IP addresses on Mikrotik's interfaces
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
    address:
        required: True
        aliases: ["ip", "addr"]
    interface:
        aliases: ["int"]
        required: True
    disabled:
        required: True
        choices: ['yes', 'no']

'''

from ansible.module_utils.basic import *


# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),
                address=dict(required=False, type='str', aliases=['ip', 'addr']),
                interface=dict(required=True, type='str', aliases=['int']),
                disabled=dict(required=False, type='str', choices=['true', 'false'])

        ),
        supports_check_mode=False,
)



def main():
    from ansible.module_utils.RosAPI import API
    from ansible.module_utils.RosAPI import intCheck
    # Initialize phase
    # Required parameters
    hostname = ansible.params['hostname']
    username = ansible.params['username']
    password = ansible.params['password']
    port = ansible.params['port']
    command = {"address": ansible.params['address'], "interface": ansible.params['interface']}
    path = "/ip/address/"
    action = ""


    while True:

        # Check if interface exists
        response = intCheck(command["interface"], hostname, username, password, port)
        interfaceExists = response["Exists"]
        if not interfaceExists:
            ansible.fail_json(failed=True, changed=False, msg=response["msg"])
            break

        # Let RosAPI do the rest
        response = API(path, action, hostname, username, password, command=command, port=port)

        # Enable or disable interface
        if (not response['failed']) and ('disabled' in ansible.params.keys()):
            command["disabled"] = ansible.params['disabled']
            response = API(path, action, hostname, username, password, command=command, port=port)

        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])
        break


from ansible.module_utils.basic import *
main()