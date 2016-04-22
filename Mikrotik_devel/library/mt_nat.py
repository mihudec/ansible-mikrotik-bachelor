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
                out_interface=dict(required=False, type='str'),
                chain=dict(required=True, type='str', choices=["srcnat", "dstnat"]),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                comment=dict(required=False, type='str'),
                action=dict(required=True, type='str', choices=["masquerade", "dst-nat"]),
                dst_port=dict(required=False, type='str'),
                dst_address=dict(required=False, type='str'),
                to_addresses=dict(required=False, type='str'),
                protocol=dict(required=False, type='str', choices=["tcp", "udp"]),
                to_ports=dict(required=False, type='str')

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
        path = "/ip/firewall/nat/"
        action = ""
        # Required params
        command = {"action": ansible.params['action'], "chain": ansible.params['chain']}
        # Optional params
        if ("disabled" in ansible.params.keys()) and (ansible.params['disabled'] != None):
            command["disabled"] = ansible.params['disabled']
        if ("comment" in ansible.params.keys()) and (ansible.params['comment'] != None):
            command["comment"] = ansible.params['comment']
        if ("out_interface" in ansible.params.keys()) and (ansible.params['out_interface'] != None):
            command["out-interface"] = ansible.params['out_interface']
        if ("to_addresses" in ansible.params.keys()) and (ansible.params['to_addresses'] != None):
            command["to-addresses"] = ansible.params['to_addresses']
        if ("protocol" in ansible.params.keys()) and (ansible.params['protocol'] != None):
            command["protocol"] = ansible.params['protocol']
        if ("to_ports" in ansible.params.keys()) and (ansible.params['to_ports'] != None):
            command["to-ports"] = ansible.params['to_ports']
        if ("dst_address" in ansible.params.keys()) and (ansible.params['dst_address'] != None):
            command["dst-address"] = ansible.params['dst_address']
        if ("dst_port" in ansible.params.keys()) and (ansible.params['dst_port'] != None):
            command["dst-port"] = ansible.params['dst_port']


        # Let RosAPI do the rest
        response = API(path, action, hostname, username, password, command=command, port=port)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])



from ansible.module_utils.basic import *
main()