#!/bin/usr/python
from ansible.module_utils.RosCore import *

# Global Variables
privkeys = ["hostname", "username", "password", "port" "path"]
# Initialize phase
# Required parameters
hostname = "192.168.116.100"
username = "admin"
password = ""
port = 8728
DEBUG = False  # This is only for debugging, if set to True Ansible will crash
switch = True  # Global switch

def API(path="/", action=None, hostname="", username="admin", password="", command=None, port=8728, DEBUG=DEBUG):

    while True:
        failed = False
        changed = True
        sentence = [path + "print"]
        reply = {"failed": False, "changed": False, "msg": []}
        exitmsg = []
        info = ""




        # Connect
        mikrotik = Core(hostname, DEBUG=DEBUG)
        login = mikrotik.login(username, password)
        # Check if login is correct
        if login[0][0] == '!trap':
            if DEBUG: print login

            return {"failed": True, "changed": False, "msg": "Login failed"}

        else:
            if DEBUG: print login

        # Create command, proplist and propstring
        rawcommand = []
        proplist = []
        propstr = ""
        if (command is not None) and (len(command) > 0):
            for key in command.keys():
                if key not in privkeys:
                    rawcommand.append("="+key+"="+str(command[key]))
                    proplist.append(key)
                    propstr = propstr + key + ","
            propstr = propstr + ".id"

        if DEBUG: print "Rawcommand: "+str(rawcommand)+" \nProplist: "+str(proplist)+" \nPropstr: "+propstr
        printsentence = sentence[:]
        printsentence.append("=.proplist="+propstr)
        if DEBUG: print "Printsentence: "+str(printsentence)
        # Get response
        response = mikrotik.talk(printsentence)
        if DEBUG: print "PRINT response: "+str(response)
        response = digestResponse(response)
        if DEBUG: print "Digested PRINT response: "+str(response)
        if response != "noObjects":

            common = commonParams(response, command)
            if DEBUG: print "Common: "+ str(common)

            # Decide if SET or add
            if common["max"]["hasmax"]:
                maxno = common["max"]["maxno"]
                maxpos = common["max"]["maxpos"]
                if maxno == len(command):
                    # All specified attributes match, do nothing
                    info = "All desired atributes are already present."

                    reply["failed"] = False
                    reply["changed"] = False
                    reply["msg"].append(info)


                    if DEBUG: print info
                    exitmsg.append(info)
                    if DEBUG: print reply
                    mikrotik.close_connection()
                    return reply

                else:
                    # Some atributes are incorrect, use SET
                    if ("comment" in proplist):

                        if ("comment" in response[maxpos].keys()):

                            if (response[maxpos]["comment"] == command["comment"]):
                                # Comments match, use SET ID
                                id = common["max"]["maxid"]
                                action = "set"
                                sentence = [path + action, "=.id="+id]
                                # Has ID use set with ID
                                info = "Maximum with ID and matching comment exists, using SET ID..."
                                if DEBUG: print info
                                exitmsg.append(info)

                                reply["failed"] = False
                                reply["changed"] = True
                                reply["msg"].append(info)

                            else:
                                # Comments don't match, use ADD
                                action = "add"
                                info = "Comments don't match, using ADD..."
                                if DEBUG: print info
                                exitmsg.append(info)
                                sentence = [path + action]

                                reply["failed"] = False
                                reply["changed"] = True
                                reply["msg"].append(info)
                        else:
                            # Exists, but has no ID. Use SET without ID
                            action = "set"
                            sentence = [path + action]
                            info = "Maximum exists without comment, using SET..."
                            if DEBUG: print info
                            exitmsg.append(info)

                            reply["failed"] = False
                            reply["changed"] = True
                            reply["msg"].append(info)
                    else:
                        # No comment in proplist
                        if maxno == len(command):
                            info = "Already in desired state."
                            if DEBUG: print info
                            exitmsg.append(info)
                            reply["changed"] = False
                            reply["msg"] = exitmsg
                            reply["failed"] = False
                            return reply
                        else:
                            action = "set"
                            info = "No comment supplied, found max, using SET." + str(response) + str(common) + str(command)
                            reply["changed"] = True
                            exitmsg.append(info)
                            reply["msg"] = exitmsg
                            if DEBUG: print info





            else:
                if len(response) >= 1:
                    if ".id" in response[0].keys():
                        action = "add"
                        info = "Maximum does not exist, using ADD..."
                    else:
                        action = "set"
                        info = "Object wit no ID, using SET..."
                reply["changed"] = True
                if DEBUG: print info
                exitmsg.append(info)
                sentence = [path + action]

                reply["failed"] = False
                reply["changed"] = True
                reply["msg"].append(info)
        else:
            # No objects exist, use ADD
            action = "add"
            info = "No objects exist, using ADD..."
            if DEBUG: print info
            exitmsg.append(info)
            sentence = [path + action]

            reply["failed"] = False
            reply["changed"] = True
            reply["msg"].append(info)



        sentence = [path + action]
        if DEBUG: print "Sentence: " + str(sentence)
        if DEBUG: print rawcommand

        for item in rawcommand:
            sentence.append(item)
        if DEBUG: print "Full sentence: " + str(sentence)
        response = mikrotik.talk(sentence)
        if DEBUG: print "Response: "+str(response)
        if response[0][0] == "!done":
            reply["failed"] = False
        else:
            reply["failed"] = True
        if DEBUG: print reply
        mikrotik.close_connection()
        return reply















def digestResponse(response):
    newresponse = {}
    if len(response) > 1:
        response = response[:-1]
        for i in range(0, len(response)):
            newresponse[i] = {}
            for key in response[i][1].keys():
                newresponse[i][key[1:]] = response[i][1][key]
        return newresponse
    return "noObjects"

def commonParams(digresponse, command):

    common = {}
    num = 0
    for i in range(0, len(digresponse)):
        for key in command.keys():
            if (key in digresponse[i].keys()) and (str(command[key]) == digresponse[i][key]):
                num += 1
        common[i] = num
        num = 0
    maxi = {"hasmax": True}
    maximum = []
    for j in range(0, len(common)):
        maximum.append(common[j])


    if maximum.count(max(maximum)) != 1:
        # Has no true maximum
        maxi["hasmax"] = False
    elif maximum.count(max(maximum)) == 1:
        maxi["hasmax"] = True
        maxi["maxno"] = max(maximum)
        maxi["maxpos"] = maximum.index(max(maximum))
        if ".id" in digresponse[maxi["maxpos"]].keys():
            maxi["maxid"] = digresponse[maxi["maxpos"]][".id"]
        if maxi["maxno"] == 0:
            maxi["hasmax"] = False

    common["max"] = maxi
    return common

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



if __name__ == '__main__':

    path = "/ip/pool/"
    command = {"ranges": "192.168.100.1-192.168.100.100", "name": "pool1"}

    API(path=path, command=command, hostname=hostname)