#! /usr/bin/env python
# A small script for cdp devices discovery

import sys
import pcapy
import socket
import getopt
import binascii
import simplejson


from dpkt import ethernet
from dpkt import cdp



def gather_options(argv):
    global interface

    help = "CDP discovery script help: \n" \
           "usage:  cdp_discovery.py -i <interface>"
    try:
        opts, args = getopt.getopt(argv, "h:i:r:",["help=", "interface=", "raw="])
    except getopt.GetoptError:
        print help
        sys.exit(2)
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print help
            sys.exit()
        elif opt in ["-i", "--interface"]:
            interface = arg



def discover_neighbors(interface, timeout=100, DEBUG=False):
    global escape

    try:
        pcap = pcapy.open_live(interface, 65535, 1, timeout)
        pcap.setfilter('ether[20:2] == 0x2000')  # CDP filter

        try:
            while not escape:
                # this is more responsive to  keyboard interrupts
                pcap.dispatch(1, on_cdp_packet)
        except KeyboardInterrupt, e:
            pass
    except Exception, e:
        print e


def on_cdp_packet(header, data):
    global inventory
    global escape
    global numpackets
    global debug

    numpackets += 1
    if debug: print "Captured %d packets" % numpackets
    ether_frame = ethernet.Ethernet(data)
    cdp_packet = ether_frame["cdp"]


    src = binascii.hexlify(ether_frame["src"])
    src_mac = ':'.join(src[i:i+2] for i in range(0,12,2))


    cdp_info = {}
    for info in cdp_packet.data:
        cdp_info.update({info['type']: info['data']})


    if cdp.CDP_ADDRESS in cdp_info.keys():
        addresses = [socket.inet_ntoa(x.data) for x in cdp_info[cdp.CDP_ADDRESS]]
        if len(addresses) < 2:
            address = addresses[0]
    else:
        address = ""

    output = {'ID': cdp_info[cdp.CDP_DEVID], 'IP': address, 'Port': cdp_info[cdp.CDP_PORTID], \
              'Version': cdp_info[cdp.CDP_VERSION], \
              'Platform':cdp_info[cdp.CDP_PLATFORM], "Source_MAC": src_mac}
    if debug: print output

    if output["Source_MAC"] in inventory.keys(): # if there is record in inventory
        if output == inventory[output["Source_MAC"]]: # if records are identical
            escape = True
            if debug: print "Captured duplicate packet. Exiting."
    else:
        inventory[output["Source_MAC"]] = output



inventory = {}
escape = False
numpackets = 0
debug = False
interface = "eth1" # try default interface if no supplied
option = ""



def main():
    global interface
    global option
    global debug
    global inventory

    args = sys.argv
    #gather_options(args[0:2])
    if "--list" in args:
        option = "list"
    if "-D" in args:
        debug = True
    if debug: print "Waiting for CDP packets..."

    discover_neighbors(interface=interface,\
                       DEBUG=debug, timeout=100)
    # Decide if output should be sorted by ID or Src-MAC
    duplicate = False
    ids = []
    for key in inventory.keys():
        if inventory[key]["ID"] not in ids:
            ids.append(inventory[key]["ID"])
            if debug: print ids
        else:
            if debug: print "\n Duplicate ID detected, sorting by Src-MAC instead..."
            duplicate = True
            break


    # Generate inventory for JSON output
    raw_inventory = {"_meta":{"hostvars":{}}, "mikrotiks":{"hosts":[], "vars": {}}}
    if duplicate:
        for key in inventory.keys():
            raw_inventory["_meta"]["hostvars"][key] = inventory[key]
            raw_inventory["mikrotiks"]["hosts"].append(key)

    else:
        for key in inventory.keys():
            raw_inventory["_meta"]["hostvars"][inventory[key]["ID"]] = inventory[key]
            raw_inventory["mikrotiks"]["hosts"].append(inventory[key]["ID"])

    # Add default variables
    raw_inventory["mikrotiks"]["vars"]["default_user"] = "admin"
    raw_inventory["mikrotiks"]["vars"]["default_password"] = ""
    output =  simplejson.dumps(raw_inventory, separators=("," , ":"), indent=2, sort_keys=True)
    print output

if __name__ == '__main__':
    main()