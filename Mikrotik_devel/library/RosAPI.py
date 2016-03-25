#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#


class Core:
    """Core part of Router OS API It contains methods necessary to extract raw data from the router.
    If object is instanced with DEBUG = True parameter, it runs in verbosity mode.
    Core part is taken mostly from http://wiki.mikrotik.com/wiki/Manual:API#Example_client."""

    def __init__(self, hostname, port=8728, DEBUG=False):
        import socket
        self.DEBUG = DEBUG
        self.hostname = hostname
        self.port = port
        self.currenttag = 0
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sk.connect((self.hostname, self.port))

    def login(self, username, pwd):
        import binascii
        from hashlib import md5

        for repl, attrs in self.talk(["/login"]):
            chal = binascii.unhexlify(attrs['=ret'])
        md = md5()
        md.update('\x00')
        md.update(pwd)
        md.update(chal)
        r = self.talk(["/login", "=name=" + username, "=response=00" + binascii.hexlify(md.digest())])
        return r

    def talk(self, words):
        if self.writeSentence(words) == 0: return
        r = []
        while 1:
            i = self.readSentence()
            if len(i) == 0: continue
            reply = i[0]
            attrs = {}
            for w in i[1:]:
                j = w.find('=', 1)
                if (j == -1):
                    attrs[w] = ''
                else:
                    attrs[w[:j]] = w[j + 1:]
            r.append((reply, attrs))
            if reply == '!done': return r

    def writeSentence(self, words):
        ret = 0
        for w in words:
            self.writeWord(w)
            ret += 1
        self.writeWord('')
        return ret

    def readSentence(self):
        r = []
        while 1:
            w = self.readWord()
            if w == '':
                return r
            r.append(w)

    def writeWord(self, w):
        if self.DEBUG:
            print "<<< " + w
        self.writeLen(len(w))
        self.writeStr(w)

    def readWord(self):
        ret = self.readStr(self.readLen())
        if self.DEBUG:
            print ">>> " + ret
        return ret

    def writeLen(self, l):
        if l < 0x80:
            self.writeStr(chr(l))
        elif l < 0x4000:
            l |= 0x8000
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x200000:
            l |= 0xC00000
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        elif l < 0x10000000:
            l |= 0xE0000000
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))
        else:
            self.writeStr(chr(0xF0))
            self.writeStr(chr((l >> 24) & 0xFF))
            self.writeStr(chr((l >> 16) & 0xFF))
            self.writeStr(chr((l >> 8) & 0xFF))
            self.writeStr(chr(l & 0xFF))

    def readLen(self):
        c = ord(self.readStr(1))
        if (c & 0x80) == 0x00:
            pass
        elif (c & 0xC0) == 0x80:
            c &= ~0xC0
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xE0) == 0xC0:
            c &= ~0xE0
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xF0) == 0xE0:
            c &= ~0xF0
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        elif (c & 0xF8) == 0xF0:
            c = ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
            c <<= 8
            c += ord(self.readStr(1))
        return c

    def writeStr(self, str):
        n = 0;
        while n < len(str):
            r = self.sk.send(str[n:])
            if r == 0: raise RuntimeError, "connection closed by remote end"
            n += r

    def readStr(self, length):
        ret = ''
        while len(ret) < length:
            s = self.sk.recv(length - len(ret))
            if s == '': raise RuntimeError, "connection closed by remote end"
            ret += s
        return ret

    def response_handler(self, response):
        """Handles API response and remove unnessesary data"""

        # if respons end up successfully
        if response[-1][0] == "!done":
            r = []
            # for each returned element
            for elem in response[:-1]:
                # if response is valid Mikrotik returns !re, if error !trap
                # before each valid element, there is !re
                if elem[0] == "!re":
                    # take whole dictionary of single element
                    element = elem[1]
                    # with this loop we strip equals in front of each keyword
                    for att in element.keys():
                        element[att[1:]] = element[att]
                        element.pop(att)
                    # collect modified data in new array
                    r.append(element)
        return r

    def run_interpreter(self):
        import select, sys
        inputsentence = []

        while 1:
            r = select.select([self.sk, sys.stdin], [], [], None)
            if self.sk in r[0]:
                # something to read in socket, read sentence
                x = self.readSentence()

            if sys.stdin in r[0]:
                # read line from input and strip off newline
                l = sys.stdin.readline()
                l = l[:-1]

                # if empty line, send sentence and start with new
                # otherwise append to input sentence
                if l == '':
                    self.writeSentence(inputsentence)
                    inputsentence = []
                else:
                    inputsentence.append(l)
        return 0

    def close_connection(self):
        self.sk.close()


def prettify(data):
    for x in data:
        for y in x.keys():
            print "%-20s: %50s" % (y, x[y])


def changeCheck(response, command, DEBUG=False):

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


def intCheck(interface_name, hostname, username, password, port=8728):
    # Checks if desired interface exists

    while True:
        # Check if interface exists
        response = API("/interface/", "print", hostname, username=username, password=password)

        if response["msg"] == "Login failed":
            return {"msg": "Login Failed", "Exists": "Unknown"}

        interfaces = [0] * (len(response["response"]) - 1)

        for i in range(0, len(interfaces), 1):
            interfaces[i] = response["response"][i][1]["=name"]

        if interface_name in interfaces:
            interfaceExists = True
            return {"msg": "Interface with specified name exists.", "Exists": True}

        else:
            interfaceExists = False
            return {"msg": "Interface with specified name does not exists.", "Exists": False}


def API(path, action, hostname, username="admin", password="", command=None, port=8728, DEBUG=False):
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

        # Check if there's need to change anything
        response = mikrotik.talk([path + "print"])
        if DEBUG == True: print response
        if action == "print":
            return {"failed": False, "changed": changed, "msg": "No changes were made", "response": response}

        r = changeCheck(response, command, DEBUG=DEBUG)

        if r["isSame"]:
            mikrotik.close_connection()
            return {"failed": False, "changed": changed, "msg": "Already in desired state"}

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
