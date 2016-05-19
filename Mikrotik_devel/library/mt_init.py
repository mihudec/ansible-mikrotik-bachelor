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
<<<<<<< HEAD
    import pexpect

    # Define variables
    mac_address = "00:0c:29:7f:41:3f"
    username = "admin"
    password = ""
=======

    # Define variables
    mac_address = "00:0c:29:7f:41:3f"
    username = "ansible"
    password = "ansible"
>>>>>>> origin/ansible-mikrotik-bachelor
    new_user = "ansible"
    new_password = "ansible"
    ip = "192.168.116.110/24"
    identity = "VirtualClone"

<<<<<<< HEAD
    child = pexpect.spawn("mactelnet " + mac_address)
    child.logfile = sys.stdout
    child.expect("Login:")
    child.sendline("admin")
    child.expect("Password:")
    child.sendline("")
    child.expect("done")
    time.sleep(2)
    child.send("\r")
    time.sleep(2)
    child.sendline("/system reboot\r")
    child.expect("[y/N]")
    child.sendline("y")
    child.terminate()



=======
>>>>>>> origin/ansible-mikrotik-bachelor


from ansible.module_utils.basic import *

main()
