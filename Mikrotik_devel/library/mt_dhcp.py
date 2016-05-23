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

                network_address=dict(required=False, type='str'),
                gateway=dict(required=False, type='str'),
                dns_server=dict(required=False, type='str'),
                domain=dict(required=False, type='str'),
                ntp_server=dict(required=False, type='str'),
                network_comment=dict(required=False, type='str'),

                pool_name=dict(required=False, type='str'),
                pool_ranges=dict(required=False, type='str'),

                disabled=dict(required=True, type='str', choices=['true', 'false']),
                address_pool=dict(required=True, type='str'),
                interface=dict(required=True, type='str'),
                name=dict(required=True, type='str'),


        ),
        supports_check_mode=False,

)



"""
# Debugging Section
class AnsibleModule:  # Provides Ansible-like parameters
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", "port": 8728,\
              "network_address": "192.168.50.0/24", "gateway": "192.168.50.1", "dns_server": "192.168.60.1",\
              "network_comment": "NET1", "pool_name": "POOL1",\
              "pool_ranges": "192.168.50.100-192.168.50.220",\
              "address_pool": "POOL1", "interface": "bridge-local", "name": "SRV1", "srv_comment": "SRV1",\
              }

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


def cutParams(beggining, command):
    newcommand = {}
    length = len(beggining)
    for key in command.keys():
        if key[:length] == beggining:
            newcommand[key[length:]] = command[key]
        else:
            newcommand[key] = command[key]
    return newcommand


def main():

    #IP Pool Section
    poolcommands = ["pool-name", "pool-ranges"]
    poolcommand = {}
    for key in moduleparams:
        if key not in privkeys and key in poolcommands:
            poolcommand[key] = moduleparams[key]
    poolcommand = cutParams("pool-", poolcommand)

    response = API(hostname=hostname, username=username, password=password, port=port,\
                   path="/ip/pool/", command=poolcommand, DEBUG=DEBUG)
    if DEBUG: print response
    exitmessage.append(response["msg"])
    if response["failed"]:
        ansible.fail_json(failed=response["failed"], changed=response["changed"], msg=exitmessage)

    # Network Section
    netcommands = ["network-address", "gateway", "dns-server",\
                   "domain", "ntp-server", "network-comment"]
    netcommand = {}
    for key in moduleparams:
        if key not in privkeys and key in netcommands:
            netcommand[key] = moduleparams[key]
    print "Netcommand: "+str(netcommand)
    netcommand = cutParams("network-", netcommand)
    print "Netcommand: "+str(netcommand)


    response = API(hostname=hostname, username=username, password=password, port=port,\
                   path="/ip/dhcp-server/network/", command=netcommand, DEBUG=DEBUG)
    exitmessage.append(response["msg"])
    if response["failed"]:
        ansible.fail_json(failed=response["failed"], changed=response["changed"], msg=exitmessage)

    # Server Section
    srvcommands = ["disabled", "address-pool", "interface", "name"]
    srvcommand = {}
    for key in moduleparams:
        if key not in privkeys and key in srvcommands:
            srvcommand[key] = moduleparams[key]
    srvcommand = cutParams("srv-", srvcommand)

    response = API(hostname=hostname, username=username, password=password, port=port,\
                   path="/ip/dhcp-server/", command=srvcommand, DEBUG=DEBUG)
    exitmessage.append(response["msg"])
    if response["failed"]:
        ansible.fail_json(failed=response["failed"], changed=response["changed"], msg=exitmessage)



    ansible.exit_json(failed=response["failed"], changed=response["changed"], msg=exitmessage)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()