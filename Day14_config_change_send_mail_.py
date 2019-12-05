# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day14_mail.py
# @time: 2019-12-03  17:40:28


import pymysql
import sqlite3
import re
import hashlib
from diff_config import diff_txt, ssh_multicmd
from smtp_send_mail_attachments import qyt_smtp_attachment

# Device Info
device_list = ['10.10.10.31', '10.10.10.32']
username = 'admin'
password = 'admin'
cmd = ['show run']


def get_config_md5(ip, username='admin', password='admin'):
    try:
        device_config_raw = ssh_multicmd(ip, username, password, cmd)
        split_result = re.split(r'\r\nhostname \S+\r\n', device_config_raw)
        device_config = device_config_raw.replace(split_result[0], '').strip()

        md5 = hashlib.md5()
        md5.update(device_config.encode())
        md5_value = md5.hexdigest()
        return device_config, md5_value

    except Exception:
        return


def write_cfg_md5_to_db():
    conn = sqlite3.connect('bakconfig.db')
    cursor = conn.cursor()

    for device in device_list:
        config_and_md5 = get_config_md5(device, username, password)
        config = config_and_md5[0]
        md5_val = config_and_md5[1]
        cursor.execute("select * from config_md5 where ip = '%s'" % device)
        md5_result = cursor.fetchall()



        if not md5_result:
            cursor.execute("insert into config_md5(ip, config, md5) values (?, ?, ?)", (device,
                                                                                        config,
                                                                                        md5_val))
            conn.commit()
        else:
            # if config_and_md5[1] != md5_result[0][2]:
            #     cursor.execute("update config_md5 set config = '%s', md5 = '%s' where ip = '%s'" % (config, md5_val, device))
            #     conn.commit()
            #     print(diff_txt(md5_result[0][1], config))
            if md5_result[0][2] == md5_val:
                continue
            else:
                Subj = f'Router {device} Config changed'
                old_config = md5_result[0][1]
                diff_body = diff_txt(old_config, config)
                Main_Body = 'Config changes as below:\n\n' + diff_body
                qyt_smtp_attachment('smtp.qiye.aliyun.com',
                                    'system01@zoosi.top',
                                    'Xx123123',
                                    'system01@zoosi.top',
                                    'sizun@jsonmedia.com',
                                    Subj,
                                    Main_Body)

                cursor.execute("update config_md5 set config = '%s', md5 = '%s' where ip = '%s'" %
                               (config, md5_val, device))
                conn.commit()

    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()
    for x in all_result:
        print(更新数据库:)
        print(x[0], x[2])
        print(更新完成!t)

    conn.commit()

if __name__ == '__main__':
    write_cfg_md5_to_db()
