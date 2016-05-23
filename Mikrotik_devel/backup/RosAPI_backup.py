#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
from ansible.module_utils.RosCore import *


class Auth:

    def __init__(self, host, hostsfile="/etc/ansible/hosts", DEBUG=False):
        hostsfile = open(hostsfile, mode='r')
        DEBUG = False
        # Determine number of lines in the file
        num_lines = sum(1 for line in hostsfile)
        if DEBUG: print num_lines
        hostsfile.seek(0)


        hostsdict = {}
        # Create dictionary from file lines
        for i in range(0, num_lines):
            workline = hostsfile.readline()
            if DEBUG: print workline
            # If line isn't empty
            if workline and workline[0] != '[':

                linearray = workline.split(' ')
                if DEBUG: print linearray
                linedict = dict(host=linearray[0].strip())
                linearray.remove(linearray[0])
                for i in range(0, len(linearray)):
                    if DEBUG: print linearray[i].split('=')
                    linedict[linearray[i].split('=')[0].strip()] = linearray[i].split('=')[1].strip()
                    hostsdict[linedict['host']] = linedict

                if DEBUG: print linedict
                if host in hostsdict.keys():
                    if 'hostname' in hostsdict[host].keys():
                        self.hostname = hostsdict[host]['hostname']
                    if 'username' in hostsdict[host].keys():
                        self.username = hostsdict[host]['username']
                    if 'password' in hostsdict[host].keys():
                        self.password = hostsdict[host]['password']

def changeCheck(response, command, DEBUG=False):
    priv_params = ["name", "comment"]
    while True:
        r = {"exists": "", "isSame": True}
        decision = []
        if len(response) > 1:
            decision = [0] * (len(response) - 1)
            # Decide which response has most common arguments
            for i in range(0, len(decision), 1):
                for key in command.keys():
                    if str("=" + key) in response[i][1].keys():
                        if (command[key] == response[i][1]["=" + key]):
                            decision[i] += 1
                            if key in priv_params:
                                decision[i] += 9

            if DEBUG == True: print decision, response

        elif len(response) == 1:
            r["exists"] = False
            r["isSame"] = False
            return r

        """Check if object with most common values is truly unique, otherwise
          object does not yet exist and will be created with ADD"""
        # If there is more than 1 object
        if len(decision) > 1:

            if sorted(decision)[-1] > sorted(decision)[-2]:
                r["exists"] = True
                # Get ID of object with most common values for SET option
                r["id"] = response[decision.index(max(decision))][1]["=.id"]
            else:
                r["exists"] = False
        # If there are no objects
        # If there is exactly 1 object
        elif len(decision) == 1:
            if decision[0] == 0:
                r["exists"] = False
            else:
                r["exists"] = True

            if "=.id" in response[0][1].keys():
                r["id"] = response[0][1]["=.id"]

        """If at least one value doesn't match command, it is NOT the same
         - we'll either ADD new or SET existing to match all values """
        for key in command.keys():
            if str("=" + key) in response[decision.index(max(decision))][1].keys():
                if command[key] != response[decision.index(max(decision))][1]["=" + key]:
                    r["isSame"] = False

        return r

def replyCheck(r):
    reply = {"success": True}
    for i in range(0,len(r)-1):
        if r[i][0] == "!trap":
            if '=message' in r[i][1].keys():
                reply["message"] = r[i][1]['=message']
            reply["success"] = False
            break
    return reply

def intCheck(interface_name, hostname, username, password, port=8728):
    # Checks if desired interface exists

    while True:
        # Check if interface exists
        response = API("/interface/", "print", hostname, username=username, password=password)

        if response["msg"] == "Login failed":
            return {"msg": "Login Failed", "Exists": "Unknown"}

        interfaces = [0] * (len(response["response"]) - 1)

        for i in range(0, len(interfaces)):
            interfaces[i] = response["response"][i][1]["=name"]

        if interface_name in interfaces:
            interfaceExists = True
            return {"msg": "Interface with specified name exists.", "Exists": True}

        else:
            interfaceExists = False
            return {"msg": "Interface with specified name does not exists.", "Exists": False}


def digestArg(argument, backwards=False):
    l = list(argument)
    if backwards:
        # Hyphens to underscores
        for i in range(0, len(argument) - 1):
            if l[i] == "-":  # Find
                l[i] = "_"  # Replace with
    else:
        # Underscores to hyphens
        for i in range(0, len(argument) - 1):
            if l[i] == "_":  # Find
                l[i] = "-"  # Replace with
    newarg = "".join(l)
    return newarg

def digestArgs(arguments):
    newargs = {}
    for key in arguments.keys():
        if arguments[key] is not None:
            newargs[digestArg(key)] = arguments[key]
    return newargs

def stripResponse(response):
    strippedresponse = {}
    for key in response.keys():
        strippedresponse[key[1:]] = response[key]
    return strippedresponse

def API(path, action, hostname="", username="admin", password="", command=None, port=8728, DEBUG=False):
    changed = False
    lst = []

    while True:

        # Connect
        mikrotik = Core(hostname, DEBUG=DEBUG)
        login = mikrotik.login(username, password)
        # Check if login is correct
        if login[0][0] == '!trap':
            if DEBUG == True:
                print login

            return {"failed": True, "changed": False, "msg": "Login failed"}

        else:
            if DEBUG == True:
                print login



        response = mikrotik.talk([path + "print"])
        if DEBUG == True: print response



        if action == "print":
            return {"failed": False, "changed": changed, "msg": "No changes were made", "response": response, "isSame": None}

        r = changeCheck(response, command, DEBUG=DEBUG)
        if r["isSame"]:
            mikrotik.close_connection()
            return {"failed": False, "changed": changed, "msg": "Already in desired state."}

        else:
            # In case that similar object already exists
            if r["exists"] == True:

                # Create list for arguments
                if "id" in r.keys():
                    namematch = True
                    if "name" in command.keys():
                        for i in range(0, len(response)-1):
                            if response[i][1]["=.id"] == r["id"]:
                                namematch = (command["name"] == response[i][1]["=name"])

                                break
                        if namematch:
                            lst = [path + "set", "=.id=" + r["id"]]
                        else:
                            lst = [path + "add"]
                        del command["name"]
                    else:
                        lst = [path + "set", "=.id=" + r["id"]]
                else:
                    lst = [path + "set"]

            # In case there's no similar object
            elif r["exists"] == False:
                # Create list for arguments
                # Allow force set by module
                if action == "set":
                    lst = [path + "set"]
                else:
                    lst = [path + "add"]


        # Add commands to argument string
        for key in command.keys():
            lst.append("=" + key + "=" + str(command[key]))




        # Apply changes
        mikrotik.talk(lst)
        # Check if changes were actually applied
        if changeCheck(mikrotik.talk([path + "print"]), command, DEBUG=DEBUG)["isSame"]:
            changed = True

            mikrotik.close_connection()
            return {"failed": False, "changed": changed, "msg": "Configured to desired state by Ansible"}

        else:
            mikrotik.close_connection()
            return {"failed": True, "changed": changed, "msg": "Something went wrong..."}

