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
from ansible.module_utils.RosAPI import *




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



"""
# Debugging Section
class AnsibleModule:  # Provides Ansible-like parameters
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", "port": 8728,\
              "chain": "dstnat",  "action": "dst-nat", "comment": "SSH", "dst-port": 2022,\
            "to-addresses": "192.168.200.112", "to-ports": 22, "protocol": "tcp"}

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
DEBUG = False  # This is only for debugging, if set to True Ansible will crash
moduleparams = digestArgs(ansible.params)
exitmessage = []
changed = False


def main():

    command = {}
    for key in moduleparams:
        if key not in privkeys:
            command[key] = moduleparams[key]

    response = API(hostname=hostname, username=username, password=password, port=port,\
                   path="/ip/firewall/nat/", command=command, DEBUG=DEBUG)
    if DEBUG: print response
    ansible.exit_json(failed=response["failed"], changed=response["changed"], msg=response["msg"])

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()