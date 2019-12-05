# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: diff_config.py
# @time: 2019-12-04  14:09:29


import sqlite3
import re
import hashlib
import paramiko
import time
from difflib import *


# def qytang_ssh(ip, username, password, cmd='ls', port=22):
#     ssh = paramiko.SSHClient()
#     ssh.load_system_host_keys()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(ip, port=port, username=username, password=password, timeout=5, compress=True)
#     stdin, stdout, stderr = ssh.exec_command(cmd)
#     i = stdout.read().decode()
#     return i

def ssh_multicmd(ip, username, password, cmd_list=['show run'], enable='enable', wait_time=3, port=22, verbose=True, timeout=10, compress=True):
    # 创建SSH Client
    ssh = paramiko.SSHClient()
    # 加载本地密钥
    ssh.load_system_host_keys()
    # 设置自动添加远程主机名及其密钥到本地
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # SSH 连接
    ssh.connect(ip, username=username, password=password, port=port, timeout=timeout, compress=compress)
    # 开始交互式会话连接
    chan = ssh.invoke_shell()
    time.sleep(1)
    x = chan.recv(4096).decode()

    if enable and '>' in x:
        chan.send('enable'.encode())
        chan.send(b'\n')
        chan.send(enable.encode())
        chan.send(b'\n')
        time.sleep(1)
        chan.send('termina length 0'.encode())
        chan.send(b'\n')
        time.sleep(wait_time)
    else:
        print('错误! 请检查enable密码')
        return

    for cmd in cmd_list:
        chan.send(b'\n')
        chan.send(cmd.encode())
        chan.send(b'\n')
        time.sleep(wait_time)
        # x = chan.recv(40960).decode()
        while True:
            # 接受数据
            received_message = ''  # 预定义接受信息变量
            received_message_fragment = chan.recv(1024).decode()
            # 接收到的数据缓存到received_message_fragment中
            if len(received_message_fragment) < 1024:  # 如果接受的数据小于1024,代表数据量小于1024
                received_message = received_message_fragment  # 直接传递给received_message
                x = received_message
                break
            else:
                while len(received_message_fragment) == 1024:  # 等于1024 表示后续还有数据!
                    received_message = received_message + received_message_fragment  # 先把接收到的信息分片重组下
                    received_message_fragment = chan.recv(1024).decode()  # 继续接收后面的的数据
                else:
                    received_message = received_message + received_message_fragment
                x = received_message
                break
        if verbose:
            return(x)
    # 结束交互式会话连接
    chan.close()
    # 结束ssh连接
    ssh.close()


def get_config_md5(ip, username='admin', password='admin'):
    try:
        device_config_raw = ssh_multicmd(ip, username, password)
        split_result = re.split(r'\r\nhostname \S+\r\n', device_config_raw)
        device_config = device_config_raw.replace(split_result[0], '').strip()

        md5 = hashlib.md5()
        md5.update(device_config.encode())
        md5_value = md5.hexdigest()
        return device_config, md5_value
    except Exception:
        return

device_list = ['10.10.10.31']
username = 'admin'
password = "admin"


def wirte_config_md5_to_db():

    conn = sqlite3.connect('bakconfig.db')
    cursor = conn.cursor()
    for device in device_list:
        ip_config_md5 = get_config_md5(ip=device, username=username, password=password)
        cursor.execute('select * from config_md5 where ip=?', (device,))
        md5_result = cursor.fetchall()
        if not md5_result:
            cursor.execute("insert into config_md5(ip, config, md5) values (?, ?, ?)", (device,
                                                                                        ip_config_md5[0],
                                                                                        ip_config_md5[1]))
            conn.commit()
        else:
            if ip_config_md5[1] != md5_result[0][2]:
                cursor.execute("update config_md5 set config=?, md5=? where ip=?", (ip_config_md5[0],
                                                                                   ip_config_md5[1],
                                                                                   device))
                conn.commit()
            else:
                continue
    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()
    for x in all_result:
        print(x[0], x[2])
    conn.close()


def diff_file(file1,file2):
    txt1 = open(file1, 'r').readlines()
    txt2 = open(file2, 'r').readlines()
    result = Differ().compare(txt1, txt2)
    return_result = '\r\n'.join(list(result))
    return return_result


def diff_txt(txt1, txt2):
    txt1_list = txt1.split('\r\n')
    txt2_list = txt2.split('\r\n')
    result = Differ().compare(txt1_list, txt2_list)
    returun_result = '\r\n'.join(list(result))
    return returun_result





if __name__ == "__main__":
    # import os
    # if os.path.exists('bakconfig.db'):
    #     os.remove('bakconfig.db')

    # conn = sqlite3.connect('bakconfig.db')
    # cursor = conn.cursor()
    # cursor.execute("create table config_md5 (ip varchar(40), config varchar(99999), md5 varchar(1000))")
    # conn.commit()
    # cursor.close()
    # conn.close()
    # wirte_config_md5_to_db()
    print(get_config_md5('10.10.10.31', 'admin', 'admin'))
    # print(ssh_multicmd('10.10.10.31', 'admin', 'admin', cmd_list=['show run']))
    # txt_1 = "\r\nprint(ssh_multicmd('10.10.10.31', 'admin', 'admin', cmd_list=['show run']))\r\n\r\n(ip varchar(40), config varchar(99999), md5 varchar(1000)))"
    # txt_2 = "\r\nprint(ssh_multicmd('10.10.10.31', 'admin', 'admin', cmd_l)\r\n\r\n(ip varchar(40), config varchar(99999), md5 varchar(1000)))"
    # print(diff_txt(txt_1, txt_2))