# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: test.py
# @time: 2019-11-19  15:48:11




if __name__ == "__main__":
    # cmd_list = ['show run']
    # print(ssh_multicmd('10.10.10.31', 'admin', 'admin', cmd_list, enable='enable'))
    print(get_config_md5('10.10.10.31', 'admin', 'admin', cmd))
