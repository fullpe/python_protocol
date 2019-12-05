# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day14_mail.py
# @time: 2019-12-03  17:40:28


import pymysql
from paramiko_ssh import qytang_ssh
import re
import hashlib
from diff_config import diff_txt
from smtp_send_mail_attachments import qyt_smtp_attachment

# Device Info
device_list = ['192.168.5.4', '192.168.5.1']
username = 'admin'
password = 'cug@2018'


def get_config_md5(ip, username, password):
    try:
        cfg = qytang_ssh(ip, username, password, cmd='show running')
        cfg_parsed = re.findall(r'(hostname[\w\W]*\r\nend)', cfg.strip())[0]
    except Exception:
        return

    m = hashlib.md5()
    m.update(cfg_parsed.encode())
    md5_val = m.hexdigest()

    return cfg_parsed, md5_val


def write_cfg_md5_to_db():
    mydb = pymysql.connect('192.168.64.131', 'lijian', 'rootdb', database='ljdb')
    cursor = mydb.cursor()

    for device in device_list:
        config_and_md5 = get_config_md5(device, username, password)
        config = config_and_md5[0]
        md5_val = config_and_md5[1]
        cursor.execute("select * from config_md5 where ip = '%s'" % device)
        md5_result = cursor.fetchall()
        if not md5_result:
            cursor.execute("insert into config_md5 values (%s, %s, %s)", (device, config, md5_val))
            # cursor.execute("insert into config_md5 values ('%s', '%s', '%s')"%(device, config, md5_val))
        else:
            if md5_result[0][2] == md5_val:  # fetchall() returns a tuple of tuples, so two indexes should be used
                continue  # Must user 'continue' not break
            else:
                # Must add the where condition, or the whole table will be updated to one entry
                subject = f'Router{device}Config changed'
                old_config = md5_result[0][1]
                body = diff_txt(old_config, config)
                body = 'Config changes as below:\n' + body
                qyt_smtp_attachment('smtp-mail.outlook.com',
                                    'orchidv524@outlook.com',
                                    'xxxxxxxx',
                                    'orchidv524@outlook.com',
                                    '1594541942@qq.com',
                                    subject,
                                    body)

                cursor.execute("update config_md5 set config = '%s', md5_config = '%s' where ip = '%s'"%(config, md5_val, device))

    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()
    for x in all_result:
        print(x[0], x[2])

    mydb.commit()

if __name__ == '__main__':
    write_cfg_md5_to_db()
