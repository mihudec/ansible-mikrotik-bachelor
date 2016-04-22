#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#

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
                path=dict(required=True, type='str'),
                action=dict(required=True, type='str', ),
                command=dict(required=False, type='list'),
                query=dict(required=False, type='str'),

        ),
        supports_check_mode=False,

)


def main():  # main logic

    from ansible.module_utils.RosRaw import RosRaw
    from ansible.module_utils.RosAPI import *
    # Initialize phase
    # Required parameters

    hostname = ansible.params['hostname']
    username = ansible.params['username']
    password = ansible.params['password']
    port = ansible.params['port']

    while True:

        #For cases when we want to change some properties based on query
        if ansible.params.has_key("query"):

            path = ansible.params["path"]
            action = "print"
            command = ansible.params["query"]


        command = ansible.params["command"]

        raw_reply = RosRaw(path, action, hostname, username, password, command=command, port=port)

        if raw_reply.has_key("failed"):
            ansible.exit_json(failed=raw_reply["failed"], changed=raw_reply["changed"], msg=raw_reply["msg"])

        elif raw_reply.has_key("response"):
            creply = replyCheck(raw_reply)

            if creply["success"]:

                response = {"failed": False, "changed": True, "msg": "RAW command ended successfully."}

            else:

                response = {"failed": True, "changed": False, "msg": "RAW command failed..."}

            ansible.exit_json(failed=response['failed'], changed=response['changed'], msg=response['msg'])


from ansible.module_utils.basic import *

main()
