#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_dhcp_net
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

# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),
                network_address=dict(required=False, type='str'),
                gateway=dict(required=False, type='str'),
                dns_server=dict(required=False, type='str'),
                netmask=dict(required=False, type='str'),
                domain=dict(required=False, type='str'),
                ntp_server=dict(required=False, type='str'),

        ),
        supports_check_mode=False,

)


def main():  # main logic

    from ansible.module_utils.RosAPI import *

    # Initialize phase
    # Required parameters

    hostname = ansible.params['hostname']
    username = ansible.params['username']
    password = ansible.params['password']
    port = ansible.params['port']

    while True:

        # DHCP Server
        path = "/ip/dhcp-server/network/"
        action = ""

        command = {}

        if ("hostname" in ansible.params.keys()) and (ansible.params['hostname'] != None):
            hostname = ansible.params['hostname']
        if ("username" in ansible.params.keys()) and (ansible.params['username'] != None):
            username = ansible.params['username']
        if ("password" in ansible.params.keys()) and (ansible.params['password'] != None):
            password = ansible.params['password']
        if ("network_address" in ansible.params.keys()) and (ansible.params['network_address'] != None):
            command["address"] = ansible.params['network_address']
        if ("gateway" in ansible.params.keys()) and (ansible.params['gateway'] != None):
            command["gateway"] = ansible.params['gateway']
        if ("dns_server" in ansible.params.keys()) and (ansible.params['dns_server'] != None):
            command["dns-server"] = ansible.params['dns_server']
        if ("netmask" in ansible.params.keys()) and (ansible.params['netmask'] != None):
            command["netmask"] = ansible.params['netmask']
        if ("domain" in ansible.params.keys()) and (ansible.params['domain'] != None):
            command["domain"] = ansible.params['domain']
        if ("ntp_server" in ansible.params.keys()) and (ansible.params['ntp_server'] != None):
            command["ntp-server"] = ansible.params['ntp_server']

        # Let RosAPI do the rest
        response = API(path, action, hostname, username, password, command=command, port=port)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])


from ansible.module_utils.basic import *
main()