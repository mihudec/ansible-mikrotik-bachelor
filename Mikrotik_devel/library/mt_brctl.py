#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_brctl
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
from ansible.module_utils.RosAPI import *
from ansible.module_utils.RosRaw import *



# Import Ansible module parameters
ansible = AnsibleModule(
        argument_spec=dict(
                hostname=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=False, type='str', aliases=["user"]),
                password=dict(required=False, type='str', aliases=["pass"]),
                port=dict(required=False, type='int', default=8728),

                names=dict(required=True, type='list'),
                admin_mac=dict(required=False, type='str', choices=["true", "false"]),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                mtu=dict(required=False, type='int'),
                priority=dict(required=False, type='int'),
                comment=dict(required=False, type='str'),

                interfaces=dict(required=False, type='list'),
                auto_isolate=dict(required=False, type='str', choices=["true", "false"]),
                point_to_point=dict(required=False, type='str', choices=["true", "false", "auto"]),
                path_cost=dict(required=False, type='int'),



        ),

        supports_check_mode=False,

)
"""


# Debugging Section
class AnsibleModule:  # Provides Ansible-like parameters
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "names": ["bridge-local"], "port": 8728, "disabled": "false", "interfaces": ["!ether2", "!ether3"]}


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
switch = True  # Global switch


def toRawCommand(params):
    rawcmd = []
    for key in params.keys():
        if (key not in privkeys) and (params[key] is not None):
            rawcmd.append("=" + digestArg(key) + "=" + str(params[key]))


def main():  # main logic
    moduleparams=digestArgs(ansible.params)
    if DEBUG: print "moduleparams: " + str(moduleparams)
    exitmessage = []

    while True:
        changed = False
        # Required params
        privkeys = ["hostname", "username", "password", "port", "path", "action"]

        # Section for Bridge management
        brparams = ["admin_mac", "disabled", "mtu", "priority", "comment"]

        # For each bridge name
        if moduleparams["names"] is not None:
            # Create common command
            brcommand = {}
            for key in moduleparams.keys():
                if (key not in privkeys) and (key in brparams) and (moduleparams[key] is not None):
                    brcommand[digestArg(key)] = str(moduleparams[key])
            if DEBUG: print brcommand

            for bridge in moduleparams["names"]:
                brcommand["name"] = bridge
                response = API(path="/interface/bridge/", action="add", username=username, password=password, \
                               hostname=hostname, port=port, command=brcommand)
                if response['failed']:
                    if DEBUG: print bridge + " failed."
                    if response["msg"] == "Login failed":
                        ansible.fail_json(failed=True, changed=False, msg=response["msg"])
                    else:
                        ansible.fail_json(failed=True, changed=False, msg=["Configuring " + bridge + " failed.", \
                                                                           exitmessage])
                if response['changed']:
                    if DEBUG: print bridge + " was configured to desired state."
                    exitmessage.append(bridge + " was configured to desired state;")
                    changed = True
                else:
                    if DEBUG: print bridge + " is already in desired state."
                    exitmessage.append(bridge + " is already in desired state;")

        # Section for ports management

        intparams = ["auto_isolate", "point_to_point", "path_cost"]

        if (moduleparams["interfaces"] is not None) and (len(moduleparams["interfaces"]) > 0):

            # Remove interface if requested:
            remove = {"remove": False, "interfaces": {}}
            # Check which interfaces should be removed
            for interface in moduleparams["interfaces"]:
                if interface[0] == "!":
                    interface = interface[1:]
                    remove["remove"] = True
                    remove["interfaces"][interface] = {}

            # Remove "to-be-removed" interfaces from interface list
            for interface in remove["interfaces"].keys():
                moduleparams["interfaces"].remove("!" + interface)


            if DEBUG: print "Remove: " + str(remove)

            if remove["remove"]:
                response = RosRaw(path="/interface/bridge/port/", action="print", username=username, password=password, \
                                  hostname=hostname, port=port, command=["=.proplist=bridge,interface,.id"])
                if DEBUG: print "Remove section PRINT response: " + str(response)
                response = response["response"][:-1]
                for interface in remove["interfaces"].keys():

                    for i in range(0, len(response)):

                        if (response[i][1]["=interface"] == interface) and (response[i][1]["=bridge"] == moduleparams["names"][0]):
                            remove["interfaces"][interface]["id"] = response[i][1]["=.id"]
                            # Remove interface
                            if DEBUG: print "Removing " + interface + " from bridge " + \
                                            response[i][1][
                                                "=bridge"]
                            rep = RosRaw(path="/interface/bridge/port/", action="remove", username=username,
                                         password=password, \
                                         hostname=hostname, port=port,
                                         command=["=.id=" + remove["interfaces"][interface]["id"]])
                            if DEBUG: print "Remove reply: " + str(rep)
                            if rep["response"][0][0] == "!done":
                                exitmessage.append(
                                    "Interface " + interface + " successfully removed from " +
                                    response[i][1]["=bridge"])
                                remove["interfaces"][interface]["removed"] = True
                                changed = True
                                if DEBUG:
                                    print "Interface " + response[i][1]["=interface"] + " successfully removed from " + \
                                          response[i][1]["=bridge"]
                            else:
                                if DEBUG: print "Unhandled exception, failed to remove " + interface
                                exitmessage.append(
                                    "Unhandled exception, failed to remove " + interface)
                                ansible.fail_json(failed=True, msg=exitmessage)
                    if "removed" not in remove["interfaces"][interface].keys():
                        if DEBUG: print "Interface " + interface + " is not port of " + moduleparams["names"][0]
                        exitmessage.append("Interface " + interface + " is not port of " + moduleparams["names"][0])


        if len(moduleparams["interfaces"]) > 0:
            # Create common command
            intcommand = {}
            intrawcommand = []
            intproplist = []
            for key in moduleparams.keys():
                if (key not in privkeys) and (key in intparams) and (moduleparams[key] is not None):
                    intcommand[digestArg(key)] = str(moduleparams[key])
                    intrawcommand.append("=" + digestArg(key) + "=" + str(moduleparams[key]))
                    intproplist.append(digestArg(key))
            if DEBUG: print intcommand, intproplist

            propstr = ""
            for item in intproplist:
                propstr = propstr + item + ","

            for interface in moduleparams["interfaces"]:
                intcommand["interface"] = interface
                intcommand["bridge"] = moduleparams["names"][0]  # Add ports to first specified bridge
                intrawcommandfull = intrawcommand[:]
                intrawcommandfull.append("=interface=" + interface)
                intrawcommandfull.append("=bridge=" + moduleparams["names"][0])

                response = RosRaw(path="/interface/bridge/port/", action="add", username=username, password=password, \
                                  hostname=hostname, port=port, command=intrawcommandfull)

                response = response["response"][0]
                if DEBUG: print "Response for " + interface + " :" + str(response)
                if response[0] == "!trap":
                    if response[1]["=message"] == "failure: device already added as bridge port":
                        # Port is already added, check it's properties...
                        propstrfull = propstr[:] + "bridge,.id"

                        response = RosRaw(path="/interface/bridge/port/", action="print", username=username,
                                          password=password, \
                                          hostname=hostname, port=port,
                                          command=['?interface=' + interface, '=.proplist=' + propstrfull])
                        if DEBUG: print "Interface " + interface + " PRINT output: " + str(response)
                        response = stripResponse(response["response"][:-1][0][1])
                        id = response[".id"]

                        isSame = True
                        for prop in intproplist:
                            if moduleparams[digestArg(prop, True)] != response[prop]:
                                isSame = False

                        if DEBUG: print interface + " properties: " + str(response), " isSame=" + str(isSame)
                        if isSame:
                            exitmessage.append(
                                    "Interface " + interface + " with ID " + id + " is already in desired state.")
                            if DEBUG: print "Interface " + interface + " with ID " + id + " is already in desired state."

                        else:
                            intrawcommandfull.append("=.id=" + id)
                            response = RosRaw(path="/interface/bridge/port/", action="set", username=username,
                                              password=password, \
                                              hostname=hostname, port=port, command=intrawcommandfull)
                            if DEBUG: print "Response for interface " + interface + " SET commnad: " + str(response)
                            if response["response"][0][0] == "!done":
                                if DEBUG: print "Interface " + interface + " with ID " + id + " already existed, Ansible changed it's properties."
                                changed = True
                                exitmessage.append(
                                        "Interface " + interface + " with ID " + id + " already existed, Ansible changed it's properties.")
                            else:
                                if DEBUG: print "Failed to SET interface " + interface + " with ID " + id + " to desired state."
                                exitmessage.append(
                                        "Failed to SET interface " + interface + " with ID " + id + " to desired state.")
                                ansible.fail_json(failed=True, message=exitmessage)
                                changed = True
                    else:
                        if DEBUG: "Unhandled exception, RosRaw returned: " + str(response)
                        exitmessage.append("Unhandled exception." + str(response) + str(len(moduleparams["interfaces"])))
                        ansible.fail_json(failed=True, msg=exitmessage)

                elif response[0] == "!done":
                    if DEBUG: print "Interface " + interface + " added as " + moduleparams["names"][0] + " port."
                    exitmessage.append("Interface " + interface + " added as " + moduleparams["names"][0] + " port.")
                    changed = True

        message = "Already in desired state." + str(exitmessage)
        if changed: message = "Configured to desired state by Ansible." + str(exitmessage)

        ansible.exit_json(failed=False, changed=changed, msg=message)


from ansible.module_utils.basic import *

main()
