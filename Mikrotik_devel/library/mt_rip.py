#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES

DOCUMENTATION = '''
---
module: mt_rip
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
                distribute_default=dict(required=False, type='str', choices=["always", "never", "if-installed"]),
                redistribute_static=dict(required=False, type='str', choices=["true", "false"]),
                redistribute_connected=dict(required=False, type='str', choices=["true", "false"]),
                redistribute_ospf=dict(required=False, type='str', choices=["true", "false"]),
                redistribute_bgp=dict(required=False, type='str', choices=["true", "false"]),
                metric_default=dict(required=False, type='int'),
                metric_static=dict(required=False, type='int'),
                metric_connected=dict(required=False, type='int'),
                metric_ospf=dict(required=False, type='int'),
                metric_bgp=dict(required=False, type='int'),
                timeout_timer=dict(required=False, type='str'),
                garbage_timer=dict(required=False, type='str'),
                update_timer=dict(required=False, type='str'),
                networks=dict(required=False, type='list'),
                interfaces=dict(required=False, type='list'),
                send=dict(required=False, type='str', choices=["v1", "v1-2", "v2"]),
                receive=dict(required=False, type='str', choices=["v1", "v1-2", "v2"]),
                authentication=dict(required=False, type='str', choices=["none", "md5", "simple"]),
                authentication_key=dict(required=False, type='str'),
                comment=dict(required=False, type='str'),
                disabled=dict(required=False, type='str', choices=["true", "false"]),
                passive=dict(required=False, type='str', choices=["true", "false"]),


        ),

        supports_check_mode=False,

)
"""


# Debugging Section
class AnsibleModule:
    params = {"username": "admin", "hostname": "192.168.116.100", "password": "", \
              "interfaces": ["ether1", "ether2"], "networks": ["192.168.116.0/24"], \
              "send": "v2", "receive": "v2", "authentication": "md5", "authentication_key": "mikrotik", "port": 8728}


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
DEBUG = False # This is only for debugging, if set to True Ansible will crash
switch = True  # Glabal switch


def toRawCommand(params):
    rawcmd = []
    for key in params.keys():
        if (key not in privkeys) and (params[key] is not None):
            rawcmd.append("=" + digestArg(key) + "=" + str(params[key]))



def main():  # main logic



    while True:

        path = "/routing/rip/"
        action = "set"
        changed = False
        # Required params
        privkeys = ["hostname", "username", "password", "port", "path", "action"]

        # Commands for RIP global setup
        ripglparams = ["distribute_default", "redistribute_static", "redistribute_connected", "redistribute_ospf", \
                       "redistribute_bgp", "metric_static", "metric_connected", "metric_ospf", "metric_bgp", ""]
        switch = False
        for key in ansible.params.keys():  # Determine if this section should be configured
            if key in ripglparams: switch = True

        if DEBUG:
            if switch:
                print "RIP global setup will now be checked..."
            else:
                print "No arguments for RIP global setup, skipping..."

        if switch:
            ripcmd = {}
            for key in ansible.params.keys():
                if (key not in privkeys) and (key in ripglparams) and (ansible.params[key] is not None):
                    ripcmd[digestArg(key)] = str(ansible.params[key])

            if len(ripcmd) > 0:
                response = API(path, action, hostname, username, password, command=ripcmd, port=port)
                if response['failed']:
                    ansible.fail_json(failed=True, msg="Failed to set RIP global parameters.")
                    if DEBUG: print "Failed to set RIP global parameters."
                if response["changed"] or changed: changed = True
                if DEBUG:
                    if response["changed"]:
                        print "Global RIP configuration has been changed."
                    else:
                        print "Global RIP configuration is already in desired state."

        # Commands for RIP Network setup
        if ansible.params["networks"] is not None:
            if DEBUG: print "RIP network setup will now be checked..."
            path = "/routing/rip/network/"
            action = "add"
            for network in ansible.params["networks"]:
                ripnetcmd = {"network": network}
                response = API(path, action, hostname, username, password, command=ripnetcmd, port=port)
                if response['failed']:
                    ansible.fail_json(failed=True, msg="Failed to add RIP network.")
                    if DEBUG: print "Failed to add RIP network."
                elif DEBUG:
                    if response["changed"]:
                        print "RIP Network added."
                    else:
                        print "RIP network already configured..."

                if response["changed"] or changed: changed = True

        else:
            print "No arguments for RIP network setup, skipping..."

        # Command for RIP interface setup
        ripintparams = ["send", "receive", "authentication", "authentication_key", \
                        "comment", "disabled", "passive"]

        switch = False
        for key in ansible.params.keys():  # Determine if this section should be configured
            if key in ripintparams: switch = True
        if DEBUG:
            if switch:
                print "RIP interface setup will now be checked..."
            else:
                print "No arguments for RIP interface setup, skipping..."
        # Separate sentence for each interface:

        if ansible.params["interfaces"] is not None:
            # Execute call for each interface
            proplist = []
            ripintcmd = []
            for key in ansible.params.keys():
                if (key not in privkeys) and (key in ripintparams) and (ansible.params[key] is not None):
                    ripintcmd.append("=" + digestArg(key) + "=" + str(ansible.params[key]))
                    proplist.append(digestArg(key))
            if DEBUG: print ripintcmd

            for interface in ansible.params["interfaces"]:
                ripintcmdfull = ripintcmd[:]
                ripintcmdfull.append("=interface=" + interface)

                response = RosRaw("/routing/rip/interface/", "add", hostname, username, password, command=ripintcmdfull,
                                  port=port)
                if DEBUG: print "Interface " + interface + " response: " + str(response)
                if response["response"][0][0] == "!trap":
                    if response["response"][0][1]["=message"] == "failure: only one config per interface allowed":
                        if DEBUG: print "Interface " + interface + " exists, checking it's configuration..."
                        # This means that interface exists, but might not be configured in desired way
                        # Time to do print and check
                        propstr = ""
                        isSame = True
                        for prop in proplist:  # Build proplist
                            propstr = propstr + prop + ","
                        propstr = propstr + ".id"
                        response = RosRaw("/routing/rip/interface/", "print", hostname, username, password, \
                                          command=['?interface=' + interface, '=.proplist=' + propstr], port=port)
                        response = stripResponse(response["response"][:-1][0][1])
                        if DEBUG: print response
                        id = response[".id"]
                        for prop in proplist:
                            if ansible.params[digestArg(prop, True)] != response[prop]:
                                isSame = False
                        if not isSame:
                            if DEBUG: print "Interface " + interface + " has different configuration, using SET..."
                            changed = True
                            ripintcmdfull = ripintcmd[:]
                            ripintcmdfull.append("=.id=" + id)
                            response = RosRaw("/routing/rip/interface/", "set", \
                                              hostname, username, password, command=ripintcmdfull, port=port)
                            if DEBUG: print response
                        else:
                            if DEBUG: print "Interface " + interface + " is already in desired state"





                    else:
                        if DEBUG: print "Unhandled exception, configuring interface " + interface + " failed."
                        ansible.fail_json(failed=True, msg="Failed to setup RIP interface.")
                elif response["response"][0][0] == "!done":
                    # This means interface was succefully added
                    changed = True

        message = "Already in desired state."
        if changed: message = "Configured to desired state by Ansible."

        ansible.exit_json(failed=False, changed=changed, msg=message)


from ansible.module_utils.basic import *

main()
