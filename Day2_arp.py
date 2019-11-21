# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day2_arp.py
# @time: 2019-11-14  10:01:03


import logging
import platform
import time
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *
from Day1_GET_MAC_netifaces import get_mac_address    # 获取本机MAC地址


def get_ifname(ifname='WLAN'):
    if platform.system() == "Linux":
        return ifname
    elif platform.system() == "Windows":
        from Day1_WIN_IFNAMES import win_from_name_get_id
        return win_from_name_get_id(ifname)
    else:
        return None


def scapy_iface(os_name):
    if platform.system() == "Linux":
        return os_name
    elif platform.system() == "Windows":
        for x, y in ifaces.items():
            # print(x, y)
            if y.pcap_name is not None:
                # print(y.pcap_name)
                if get_ifname(os_name) == ('{' + y.pcap_name.split('{')[1]):
                    return x
                else:
                    pass


def gratuitous_arp(ip_address, ifname='ens33'):
    localmac = get_mac_address(ifname)
    print(localmac)
    gratuitous_arp_pkt = Ether(src=localmac, dst='ff:ff:ff:ff:ff:ff') / ARP(op=2,
                                                                            hwsrc=localmac,
                                                                            hwdst=localmac,
                                                                            psrc=ip_address,
                                                                            pdst=ip_address)
    while True:

        sendp(gratuitous_arp_pkt, iface=scapy_iface(ifname), verbose=False)
        # time.sleep(2)


if __name__ == "__main__":
    # print(scapy_iface('WLAN'))
    print(gratuitous_arp('192.168.111.200', ifname='test01'))
