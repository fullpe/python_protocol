# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day8_cpu_wdb.py
# @time: 2019-11-25  11:10:51


import os
import sqlite3
#from snmpv2_get import snmpv2_get
import datetime
import time
from pysnmp.hlapi import *


def snmpv2_get(ip, community, oid, port=161):
    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    errorIndication, errorStatus, errorindex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),  # 配置community
               UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
               ContextData(),
               ObjectType(ObjectIdentity(oid))  # 读取的OID
               )
    )
    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus,
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )
    # 如果返回结果有多行,需要拼接后返回
    result = ""
    for varBind in varBinds:
        result = result + varBind.prettyPrint() # 返回结果！
    # 返回的为一个元组,OID与字符串结果
    # return result.split("=")[0].strip(), result.split("=")[1].strip()
    return result.split("=")[1].strip()


def get_info_wirtedb(ip, rocommunity, dbname, seconds):
    if os.path.exists(dbname):
        os.remove(dbname)
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    cursor.execute("create table routerdb(id INTEGER PRIMARY KEY AUTOINCREMENT, time timestamp, cpu int)")

    while seconds > 0:
        cpu_info = snmpv2_get(ip, rocommunity, '1.3.6.1.4.1.9.9.109.1.1.1.1.3.7')
        time_info = datetime.datetime.now()
        cursor.execute("insert into routerdb (time, cpu) values ('{0}', {1})".format(time_info, int(cpu_info)))

        time.sleep(5)
        seconds -= 5
        conn.commit()


if __name__ == "__main__":
    # # 使用Linux解释器 & WIN解释器
    # # 系统描述
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.2.1.1.1.0", port=161))
    # # 联系人
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.2.1.1.4.0", port=161))
    # # 主机名
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.2.1.1.5.0", port=161))
    # # 地点
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.2.1.1.6.0", port=161))
    # # cpmCPUTotal5sec
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161))
    # # cpmCPUMemoryUsed
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161))
    # # cpmCPUMemoryFree
    # print(snmpv2_get("192.168.111.111", "public", "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161))
    get_info_wirtedb('192.168.111.111', 'public', "deviceinfo.sqlite3", 1000)
