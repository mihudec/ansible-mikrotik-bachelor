#!/usr/bin/env python

# Converts Ansible dynamic inventory sources to static files
# Input is received via stdin from the dynamic inventory file
#   ex:
#     ec2.py --list | ansible-dynamic-inventory-converter.py

import json
import os
import sys

import pyaml

def add_vars(_type, _id, variables):
    assert _type == "group" or _type == "host"
    dir_name = "./%s_vars" % _type
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    with open('%s/%s' % (dir_name, _id), 'w') as fh:
        fh.write(pyaml.dump(variables))

def add_host_vars(host, variables):
    add_vars('host', host, variables)

def add_group_vars(group, variables):
    add_vars('group', group, variables)

def main():
    raw_json = sys.stdin.read()
    inventory = json.loads(raw_json)
    inventory_filename = "./hosts"

    with open(inventory_filename, 'w') as fh:
        for group in inventory:
            if group == "_meta":
                for host, variables in inventory[group]["hostvars"].iteritems():
                    add_host_vars(host, variables)
            if "vars" in inventory[group]:
                add_group_vars(group, inventory[group]["vars"])
            if "hosts" in inventory[group]:
                fh.write("[%s]\n" % group)
                for host in inventory[group]["hosts"]:
                    fh.write("%s\n" % host)
                fh.write("\n")
            if "children" in inventory[group]:
                fh.write("[%s:children]\n" % group)
                for child in inventory[group]["children"]:
                    fh.write("%s\n" % child)
                fh.write("\n")
if __name__ == '__main__':
    main()