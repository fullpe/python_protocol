# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day7_bakconfig.py
# @time: 2019-11-21  17:44:22


import sqlite3
import re
import hashlib
import paramiko


def qytang_ssh(ip, username, password, cmd='ls', port=22):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=port, username=username, password=password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    i = stdout.read().decode()
    return i


def get_config_md5(ip, username='admin', password='admin'):
    try:
        device_config_raw = qytang_ssh(ip, username, password, cmd='show run')
        split_result = re.split(r'\r\nhostname \S+\r\n', device_config_raw)
        device_config = device_config_raw.replace(split_result[0], '').strip()

        md5 = hashlib.md5()
        md5.update(device_config.encode())
        md5_value = md5.hexdigest()
        return device_config, md5_value
    except Exception:
        return


device_list = ['192.168.111.111']
username = 'admin'
password = 'admin'


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
                cursor.execute("update config_md5 set config=?, md5=? where ip=?",(ip_config_md5[0],
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


if __name__ == "__main__":
    # import os
    # if os.path.exists('bakconfig.db'):
    #     os.remove('bakconfig.db')
    #
    # conn = sqlite3.connect('bakconfig.db')
    # cursor = conn.cursor()
    # cursor.execute("create table config_md5 (ip varchar(40), config varchar(99999), md5 varchar(1000))")
    # conn.commit()
    # cursor.close()
    # conn.close()
    wirte_config_md5_to_db()
    '''
    # 在全局/etc/crontab 中定时执行任务,并将标准输出和错误重定向到 /root/crontab.log
    # 每分钟执行: * * * * *
    # 每秒钟执行: * * * * * sleep 10
    * * * * * root /usr/bin/python3 /tmp/pycharm_project_524/Day7_bakconfig.py >/root/day7bak.log 2>&1 &
    # 使用 tail -f 查看执行情况，可以见到log每5秒被写入一条记录
    tail -f /root/day7bak.log 
    
    # 可以一步一步的查看脚本执行的状态
    sh -x crontab_py.sh
    # 简单的linux for循环
    for i in `seq 0 5 59`; do echo $i; done
    ========================================================================
    #！/bin/bash
    for i in `seq 0 5 59`;do
            /usr/bin/python3 /tmp/pycharm_project_524/Day7_bakconfig.py;
            sleep 5;
    done
    ==========================================================================
    
    # 建议在root下使用crontab -e来写定时任务
    * * * * * /bin/bash /root/crontab_py.sh >/root/echo.log 2>&1 &  # 单> 是覆盖,双>> 是追加.
    
    # !ps 用法
    root@ubuntu:~# !ps
    ps -ef |grep crontab
    root      26799      1  0 18:31 ?        00:00:00 /bin/bash /root/crontab_py.sh
    root      26853  22998  0 18:31 pts/1    00:00:00 grep --color=auto crontab
    '''
