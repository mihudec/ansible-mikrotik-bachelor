#! /usr/bin/env python
# A small script for cdp devices discovery

import sys
import pcapy
import socket

from dpkt import ethernet
from dpkt import cdp


def discover_neighbors(interface, timeout=100, DEBUG=False):
    def on_cdp_packet(header, data):
        ether_frame = ethernet.Ethernet(data)
        cdp_packet = ether_frame.cdp

        cdp_info = {}
        for info in cdp_packet.data:
            cdp_info.update({info['type']: info['data']})

        if DEBUG:
            print cdp_info

        if cdp.CDP_ADDRESS in cdp_info.keys():
            addresses = [socket.inet_ntoa(x.data) for x in cdp_info[cdp.CDP_ADDRESS]]
        else:
            addresses = []

        # print "Hey, %s is at %s." % (cdp_info[cdp.CDP_DEVID], ", ".join(addresses))
        output = {'ID': cdp_info[cdp.CDP_DEVID], 'IP': addresses, 'Port': cdp_info[cdp.CDP_PORTID], \
                  'Version': cdp_info[cdp.CDP_VERSION], \
                  'Platform':cdp_info[cdp.CDP_PLATFORM]}
        print output

    try:
        pcap = pcapy.open_live(interface, 65535, 1, timeout)
        pcap.setfilter('ether[20:2] == 0x2000')  # CDP filter

        try:
            while True:
                # this is more responsive to  keyboard interrupts
                pcap.dispatch(1, on_cdp_packet)
        except KeyboardInterrupt, e:
            pass
    except Exception, e:
        print e


if __name__ == "__main__":
    discover_neighbors(interface='eth1', DEBUG=True, timeout=50)
