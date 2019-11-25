# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day8_cpu_rdb.py
# @time: 2019-11-25  14:48:25


import sqlite3
from dateutil import parser
from datetime import datetime, timedelta
from Day6_mat_plot import mat_line

def cpu_read_db(dbname, last_mine=1):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    now = datetime.now()
    before_last_min = now - timedelta(minutes=last_mine)
    cursor.execute("select time, cpu from routerdb where time > '{0}'".format(before_last_min))
    yourrults = cursor.fetchall()

    return [[parser.parse(i[0]), i[1]] for i in yourrults]

if __name__ == "__main__":
    # print(cpu_read_db('deviceinfo.sqlite3', 1))
    mat_line(cpu_read_db('deviceinfo.sqlite3', 10))