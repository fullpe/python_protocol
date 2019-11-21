# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day3_udp_server.py
# @time: 2019-11-18  11:15:38


import socket
import sys
import struct
import hashlib
import pickle

address = ('10.10.202.25', 16666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP简单服务器启动!等待数据')
while True:
    try:
        recv_source_data = s.recvfrom(2048)
        # print(recv_source_data)
        rdata, addr = recv_source_data
        header = rdata[:12]
        uppack_header = struct.unpack('>HHLL', header)
        version = uppack_header[0]
        pkt_type = uppack_header[1]
        seq_id = uppack_header[2]
        length = uppack_header[3]

        rdata = rdata[12:]
        data = rdata[:length]
        md5_recv = rdata[length:]

        m = hashlib.md5()
        m.update(header + data)
        md5_value = m.digest()

        if md5_recv == md5_value:
            print('=' * 80)
            print("{0:<30}:{1:<30}".format('数据源自于', str(addr)))
            print("{0:<30}:{1:<30}".format('数据序列号', seq_id))
            print("{0:<30}:{1:<30}".format('数据长度为', length))
            print("{0:<30}:{1:<30}".format('数据源自于', str(pickle.loads(data))))
    except KeyboardInterrupt:
        sys.exit()


# if __name__ == "__main__":
#     pass