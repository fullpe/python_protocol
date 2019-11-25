# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day9_mem_rdb.py
# @time: 2019-11-25  15:45:48


import sqlite3
from dateutil import parser
from datetime import datetime, timedelta
from Day6_mat_plot import mat_line


def mem_read_db(dbname, last_mine=1):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    now = datetime.now()
    before_last_min = now - timedelta(minutes=last_mine)
    print(before_last_min)
    cursor.execute("select mem_time, mem_percent from routerdb where mem_time > '{0}'".format(before_last_min))
    yourrults = cursor.fetchall()
    print('=' * 80, '\n', yourrults[1])

    return [[parser.parse(i[0]), i[1]] for i in yourrults]
    # print([[parser.parse(i[0]), i[1]] for i in yourrults])


if __name__ == "__main__":
    # print(cpu_read_db('deviceinfo.sqlite3', 1))
    mat_line(mem_read_db('deviceinfo.sqlite3', 10))