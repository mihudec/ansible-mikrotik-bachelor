#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_dhcp_server
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
                mode=dict(required=False, type='str', choices=["ftp", "http", "https"]),
                src_path=dict(required=False, type='str'),
                dst_path=dict(required=False, type='str'),
                keep_result=dict(required=False, type='str', choices=["True", "False"]),
                connection_username=dict(required=False, type='str', aliases=["con_user"]),
                connection_password=dict(required=False, type='str', aliases=["con_pass"]),
                upload=dict(required=False, type='str', choices=["True", "False"]),
                url=dict(required=False, type='str'),
                address=dict(required=False, type='str', aliases=["addr"])
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
        path = "/tool/fetch"
        action = "raw"

        command = {}

        if ("hostname" in ansible.params.keys()) and (ansible.params['hostname'] != None):
            hostname = ansible.params['hostname']
        if ("username" in ansible.params.keys()) and (ansible.params['username'] != None):
            username = ansible.params['username']
        if ("password" in ansible.params.keys()) and (ansible.params['password'] != None):
            password = ansible.params['password']
        if ("mode" in ansible.params.keys()) and (ansible.params['mode'] != None):
            command["mode"] = ansible.params['mode']
        if ("src_path" in ansible.params.keys()) and (ansible.params['src_path'] != None):
            command["src-path"] = ansible.params['src_path']
        if ("dst_path" in ansible.params.keys()) and (ansible.params['dst_path'] != None):
            command["dst-path"] = ansible.params['dst_path']
        if ("keep_result" in ansible.params.keys()) and (ansible.params['keep_result'] != None):
            command["keep-result"] = ansible.params['keep_result']
        if ("domain" in ansible.params.keys()) and (ansible.params['domain'] != None):
            command["domain"] = ansible.params['domain']
        if ("connection_username" in ansible.params.keys()) and (ansible.params['connection_username'] != None):
            command["user"] = ansible.params['connection_username']
        if ("connection_password" in ansible.params.keys()) and (ansible.params['connection_password'] != None):
            command["password"] = ansible.params['connection_password']
        if ("url" in ansible.params.keys()) and (ansible.params['url'] != None):
            command["url"] = ansible.params['url']
        if ("address" in ansible.params.keys()) and (ansible.params['address'] != None):
            command["address"] = ansible.params['address']

        # Let RosAPI do the rest
        response = API(path, action, hostname, username, password, command=command, port=port)
        ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])


from ansible.module_utils.basic import *
main()