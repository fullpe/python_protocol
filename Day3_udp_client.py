# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day3_UDP.py
# @time: 2019-11-18  11:03:13


import socket
import struct
import hashlib
import pickle


def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1
    for x in data_list:
        # ---header设计---
        # 2 字节 版本 1
        # 2 字节 类型 1为请求 2为响应(由于UDP是单向流量!本次实验只有请求)
        # 4 字节 ID号
        # 4 字节 长度
        #
        # ---变长数据部分---
        # 使用pickle转换数据
        #
        # ---HASH校验---
        # 16字节 MD5值

        send_data = pickle.dumps(x)
        header = struct.pack('>HHLL', version, pkt_type, seq_id, len(send_data))
        m = hashlib.md5()
        m.update(header + send_data)
        md5_value = m.digest()

        s.sendto(header + send_data + md5_value, address)

        seq_id += 1
    s.close()


if __name__ == "__main__":
    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}]
    udp_send_data('10.10.202.25', 16666, user_data)
