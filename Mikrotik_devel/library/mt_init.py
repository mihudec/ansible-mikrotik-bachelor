#!/usr/bin/python
# -*- coding: UTF-8 -*-
# THIS IS ANSIBLE MODULE USED FOR CONFIGUTING MIKROTIK ROUTEROS DEVICES
# This module uses mactelnet to connect to end devices to perform initial config to enable API access


from ansible.module_utils.basic import *
from subprocess import *

# Import Ansible module parameters
"""
ansible = AnsibleModule(
        argument_spec=dict(
                mac_address=dict(required=False, type='str', aliases=["host"]),
                username=dict(required=True, type='str', aliases=["user"]),
                password=dict(required=True, type='str', aliases=["pass"]),
                new_user=dict(required=True, type='str'),
                new_password=dict(required=True, type='str'),
                ip=dict(required=True, type='str'),
                identity=dict(required=True, type='str', aliases=["id"])
        ),
        supports_check_mode=False,

)
"""

def main():  # main logic
    import os
    import select
    import shutil
    import subprocess
    import fcntl
    import getpass

    # Define variables
    mac_address = "00:0c:29:7f:41:3f"
    username = "admin"
    password = ""
    new_user = "ansible"
    new_password = "ansible"
    ip = "192.168.116.110/24"
    identity = "VirtualClone"



from ansible.module_utils.basic import *

main()
