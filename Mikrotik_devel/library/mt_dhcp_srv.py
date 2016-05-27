#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_dhcp_srv
author: Miroslav Hudec
version_added: ""
short_description: Sets DHCP server on interface
requirements: [ RosAPI ]
description:
    - Sets DHCP server on desired interface. This requires having IP pool defined.
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
                disabled=dict(required=True, type='str', choices=['true', 'false']),
                address_pool=dict(required=True, type='str'),
                interface=dict(required=True, type='str'),
                name=dict(required=True, type='str'),


        ),
        supports_check_mode=False,

)


def main():  # main logic

    from ansible.module_utils.RosAPI import API
    from ansible.module_utils.RosAPI import intCheck
    # Initialize phase
    # Required parameters

    hostname = ansible.params['hostname']
    username = ansible.params['username']
    password = ansible.params['password']
    port = ansible.params['port']

    while True:

        # DHCP Server
        path = "/ip/dhcp-server/"
        action = ""
        command = {"name": ansible.params['name'], "address-pool": ansible.params['address_pool'], "interface": ansible.params['interface'], "disabled": ansible.params["disabled"]}


        # Check if interface exists
        response = intCheck(command["interface"], hostname, username, password, port)
        interfaceExists = response["Exists"]
        if not interfaceExists:
            ansible.fail_json(failed=True, changed=False, msg=response["msg"])
            break

        response = API(path, action, hostname, username, password, command=command, port=port)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])



from ansible.module_utils.basic import *
main()