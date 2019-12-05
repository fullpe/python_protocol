# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day13_tcpsocket_server.py
# @time: 2019-12-03  10:51:40


import json
from socket import *
import os
import base64


def Server_JSON(ip, port):
    # 创建TCP Socket, AF_INET为ipv4, SOCK_STREAM 为 TCP
    sockobj = socket(AF_INET, SOCK_STREAM)
    # 绑定地址，地址为（host, port) 的元组
    sockobj.bind((ip, port))
    # 在拒绝链接前，操作系统可以挂起的最大链接数量， 一般配置为5
    sockobj.listen(5)

    while True:    # 循环接受链接请求
        try:
            # 接受TCP链接，并返回（conn, address)的元组， conn为新的套接字对象， 可以用来接受和发送数据，address是接受客户端数据的地址
            connetcion, address = sockobj.accept()
            # conn.settimeout(5.0)   # 设置链接超时
            # 打印链接客户端地址ip地址
            print('Server Connected by', address)
            received_message = b''  # 预定义接受信息变量
            received_message_fragment = connetcion.recv(1024)
            if len(received_message_fragment) < 1024:

                received_message = received_message_fragment
                obj = json.loads(received_message.decode())
            else:
                while len(received_message_fragment) == 1024:
                    received_message = received_message + received_message_fragment
                    received_message_fragment = connetcion.recv(1024)
                else:
                    received_message = received_message + received_message_fragment
                obj = json.loads(received_message.decode())
            if 'exec_cmd' in obj.keys():
                obj.update({'cmd_result': os.popen(obj.get('exec_cmd')).read()})
                return_data = obj
            elif 'upload_file' in obj.keys():
                # 上传时应该考虑文件名
                fp = open('upload_file.py', 'wb')
                fp.write(base64.b64decode(obj.get('file_bit').encode()))
                fp.close()
                print('上传文件{}'.format(obj.get('upload_file')))
                return_data = {'message': 'Upload Success!'}
            elif 'download_file' in obj.keys():
                file_bit = base64.b64encode(open(obj.get('download_file'), 'rb').read()).decode()
                obj.update({'file_bit': file_bit})
                return_data = obj
            connetcion.send(json.dumps(return_data).encode())
            connetcion.close()
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    Server_IP = '0.0.0.0'
    Server_Port = 6668
    Server_JSON(Server_IP, Server_Port)
