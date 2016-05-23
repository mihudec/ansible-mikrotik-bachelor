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
from ansible.module_utils.RosRaw import *



# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),
                address=dict(required=False, type='str', aliases=['ip', 'addr']),
                interface=dict(required=True, type='str', aliases=['int']),
                comment=dict(required=False, type='str'),


        ),
        supports_check_mode=False,
)

"""
# Debugging Section
class AnsibleModule:  # Provides Ansible-like parameters
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "interface": "!bridge-local", "port": 8728, "address": "192.168.201.1/24"}

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


    moduleparams = digestArgs(ansible.params)
    exitmessage = []
    changed = False
    path = "/ip/address/"
    action = "add"
    command = {}
    commandstr = []
    proplist = []
    propstr = ""

    for key in moduleparams.keys():
        if key not in privkeys:
            if moduleparams[key][0] == "!":
                command[key] = moduleparams[key][1:]
                commandstr.append("="+key+"="+moduleparams[key][1:])
            else:
                command[key] = moduleparams[key]
                commandstr.append("="+key+"="+moduleparams[key])
            proplist.append(key)

    for item in proplist:
        propstr = propstr + item + ","
    propstr = propstr + ".id"



    if DEBUG: print "Command: " + str(command) +"\nCommandstr: " + str(commandstr) + "\n"

    while True:

        # Check if interface exists
        response = RosRaw(hostname=hostname, username=username, password=password, port=port,\
                          path="/interface/", action="print", command=["=.proplist=name,.id,type"])
        response = response["response"][:-1]
        interfacelist = {}

        for i in range(0, len(response)):
            interfacelist[response[i][1]["=name"]] = [response[i][1]["=.id"], response[i][1]["=type"]]
        if DEBUG: print str(response) + "\nInterfacelist: " + str(interfacelist)
        intExists = False
        if (moduleparams["interface"] in interfacelist.keys()) or (moduleparams["interface"][1:] in interfacelist.keys()):
            intExists = True
        if intExists:
            exitmessage.append("Interface "+ moduleparams["interface"] + " exists.")
            if DEBUG: print "Interface "+ moduleparams["interface"] + " exists."
        else:
            exitmessage.append("Interface "+ moduleparams["interface"] + " does not exist.")
            if DEBUG: print "Interface "+ moduleparams["interface"] + " does not exist."
            ansible.fail_json(failed=True, msg=exitmessage)




        # Check current IP addresses


        response = RosRaw(hostname=hostname, username=username, password=password, port=port,\
                          path="/ip/address/", action="print", command=["=.proplist=interface,address,.id,network,netmask"])
        response = response["response"][:-1]
        if DEBUG: print "IP address PRINT: " + str(response)
        addresslist = {}
        ipinterfacelist = {}
        for i in range(0, len(response)):
            addresslist[response[i][1]["=address"]] = response[i][1]["=interface"]
            ipinterfacelist[response[i][1]["=interface"]] = [response[i][1]["=address"], response[i][1]["=.id"]]
        if DEBUG: print "Addresslist: " + str(addresslist) + "\nIPinterfacelist: " + str(ipinterfacelist)

        #Remove interface address
        remove = {"remove": False, "interface": {}}



        if (moduleparams["interface"][0] == "!"):
            remove["remove"] = True

            if (moduleparams["interface"][1:] in ipinterfacelist):



                interface = moduleparams["interface"][1:]
                if DEBUG: print "Removing interface: " + interface
                moduleparams["interface"] = moduleparams["interface"][1:]

                remove["interface"][interface] = {}
                remove["interface"][interface][".id"] = ipinterfacelist[interface][1]
                if DEBUG: print "Remove: " + str(remove)
                # Talk
                response = RosRaw(hostname=hostname, username=username, password=password, port=port,\
                          path="/ip/address/", action="remove", command=["=.id="+ remove["interface"][interface][".id"]])
                response = response["response"]
                if DEBUG: print "Remove response: " + str(response)
                if response[0][0] == "!done":
                    changed = True
                    if DEBUG: print "Interface IP address of " + interface + " was removed by Ansible"
                    exitmessage.append("Interface IP address of " + interface + " was removed by Ansible")
                    break



            else:
                exitmessage.append("Iterface " + moduleparams["interface"][1:] + " does not have IP address, cannot remove.")
                if DEBUG: print "Iterface " + moduleparams["interface"][1:] + " does not have IP address, cannot remove."
                ansible.fail_json(failed=True, msg=exitmessage)






        if remove["remove"] == False:
            if moduleparams["address"] in addresslist.keys():
                if addresslist[moduleparams["address"]] == moduleparams["interface"]:
                    # Already in desired state
                    if DEBUG: print "Specified IP address " + moduleparams["address"] + \
                                    " is already configured at " + addresslist[moduleparams["address"]]
                    exitmessage.append("Specified IP address " + moduleparams["address"] + " is already configured at " + addresslist[moduleparams["address"]])
                    break
                else:
                    if DEBUG: print "Specified IP address " + moduleparams["address"] + \
                                    " is already configured at " + addresslist[moduleparams["address"]]
                    exitmessage.append("Specified IP address " + moduleparams["address"] + " is already configured at " + addresslist[moduleparams["address"]])
                    ansible.fail_json(failed=True, msg=["Configuring IP address failed", exitmessage])

            if moduleparams["interface"] in ipinterfacelist.keys():
                # SET IP address
                commandstr.append("=.id="+ipinterfacelist[moduleparams["interface"]][1])
                response = RosRaw(hostname=hostname, username=username, password=password, port=port,\
                              path="/ip/address/", action="set",\
                              command=commandstr)
                if response["response"][0][0] == "!done":
                    if DEBUG: print "IP address " + moduleparams["address"] + \
                                " was SET by Ansible on interface " + moduleparams["interface"]
                    exitmessage.append("IP address " + moduleparams["address"] + " was SET by Ansible on interface " + moduleparams["interface"])
                    changed = True
                    break
                else:
                    if DEBUG: print "Failed to SET IP address " + moduleparams["address"] + " on " + moduleparams["interface"]
                    exitmessage.append("Failed to SET IP address " + moduleparams["address"] + " on " + moduleparams["interface"])
                    ansible.fail_json(failed=True, msg=exitmessage)


            else:
                # ADD IP interface

                response = RosRaw(hostname=hostname, username=username, password=password, port=port,\
                              path="/ip/address/", action="add", command=commandstr)
                if DEBUG: print "ADD response: " + str(response)
                if response["response"][0][0] == "!done":
                    #Success, added
                    if DEBUG: print "IP address " + moduleparams["address"] + \
                                " was ADDed by Ansible on interface " + moduleparams["interface"]
                    exitmessage.append("IP address " + moduleparams["address"] + " was ADDed by Ansible on interface " + moduleparams["interface"])
                    changed = True
                    break
                else:
                    if DEBUG: print "Failed to ADD IP address " + moduleparams["address"] + " on " + moduleparams["interface"]
                    exitmessage.append("Failed to ADD IP address " + moduleparams["address"] + " on " + moduleparams["interface"])
                    ansible.fail_json(failed=True, msg=[exitmessage, response])

    message = "Already in desired state."
    if changed: message = "Configured to desired state by Ansible."
    ansible.exit_json(failed=False, changed=changed, msg=[message, exitmessage])



from ansible.module_utils.basic import *
main()