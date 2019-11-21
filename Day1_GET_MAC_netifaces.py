# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author : zunsi
# @File   : Day1_GET_MAC_netifaces.py.py
# @Time   : 2019-11-12  21:13:55

import netifaces
import platform
import pprint
pp = pprint.PrettyPrinter(indent=4)


def get_mac_address(ifname):
    if platform.system() == "Linux":
        # pp.pprint(netifaces.ifaddresses(ifname))
        # 所有地址信息 2 为IPv4, 10 为IPv6, 17 为以太网
        # {   2: [   {   'addr': '10.1.1.80',
        #                'broadcast': '10.1.1.255',
        #                'netmask': '255.255.255.0'}],
        #     10: [   {'addr': '2001:1::80', 'netmask': 'ffff:ffff:ffff:ffff::/64'},
        #             {   'addr': 'fe80::250:56ff:feab:2508%ens33',
        #                 'netmask': 'ffff:ffff:ffff:ffff::/64'}],
        #     17: [{'addr': '00:50:56:ab:25:08', 'broadcast': 'ff:ff:ff:ff:ff:ff'}]}

        # AF_LINK表示以太网
        # print(netifaces.AF_LINK)  # 17
        try:
            return netifaces.ifaddresses(ifname)[netifaces.AF_LINK][0]['addr']
        except ValueError:
            return None
    elif platform.system() == "Windows":
        from Day1_WIN_IFNAMES import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        if not if_id:
            return None
        else:
            return netifaces.ifaddresses(if_id)[netifaces.AF_LINK][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == '__main__':
    print(get_mac_address("WLAN"))
    print(get_mac_address("test01"))
