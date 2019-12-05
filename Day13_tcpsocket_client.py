# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day13_tcpsocket_client.py
# @time: 2019-12-03  10:51:57


import json
from socket import *
import base64


def Client_JSON(ip, port, obj):
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((ip, port))

    if 'exec_cmd' in obj:
        send_obj = obj
    elif 'upload_file' in obj:
        filename = obj.get('upload_file')
        file_bit = base64.b64encode(open(filename, 'rb').read())
        obj.update({'file_bit': file_bit.decode()})
        send_obj = obj
    elif 'download_file' in obj:
        send_obj = obj

    send_message = json.dumps(send_obj).encode()
    send_message_fragment = send_message[:1024]
    send_message = send_message[1024:]

    while send_message_fragment:
        sockobj.send(send_message_fragment)
        send_message_fragment = send_message[:1024]
        send_message = send_message[1024:]
    recieved_message = b''
    recieved_message_fragment = sockobj.recv(1024)

    while recieved_message_fragment:
        recieved_message = recieved_message + recieved_message_fragment
        recieved_message_fragment = sockobj.recv(1024)

    return_data = json.loads(recieved_message.decode())
    if 'download_file' not in return_data.keys():
        print('收到确认数据:', return_data)
    else:
        print('收到确认数据:', return_data)
        fp = open('download_file.py', 'wb')
        fp.write(base64.b64decode(return_data.get('file_bit').encode()))
        fp.close()
        print('下载文件{0}保存成功!'.format(return_data.get('download_file')))
    sockobj.close()


if __name__ == '__main__':
    port = 6668
    exec_cmd = {'exec_cmd': 'pwd'}
    Client_JSON('10.10.10.21', port, exec_cmd)
    upload_file = {'upload_file': 'snmp_get1.py'}
    Client_JSON('10.10.10.21', port, upload_file)
    download_file = {'download_file': 'snmp_get1.py'}
    Client_JSON('10.10.10.21', port, download_file)
