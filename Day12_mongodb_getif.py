# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day12_mongodb_getif.py
# @time: 2019-11-29  15:01:28


import numpy as np
from SNMP_GET import snmpv2_get
from SNMP_GETBULK import snmpv2_getbulk
from datetime import datetime
from pprint import pprint
from pymongo import *
import time
from datetime import datetime,timedelta
from matplotlib import pyplot as plt

client = MongoClient('mongodb://qytangadmin:Cisc0123@10.10.10.22:27017/qytang')
db = client['qytang']


def write_db_period(interval=5, seconds=1200):
    while seconds > 0:
        write_iface_data_to_mongodb('10.10.10.31', 'public')
        time.sleep(5)
        seconds -= interval


def write_iface_data_to_mongodb(ip, community_ro):
    iface_data = {}
    # 接口名字列表
    iface_name = [y for x, y in snmpv2_getbulk(ip, community_ro, "1.3.6.1.2.1.2.2.1.2", count=25, port=161)]
    # 接口速率列表
    speed_list = [i[1] for i in snmpv2_getbulk(ip, community_ro, "1.3.6.1.2.1.2.2.1.5", port=161)]
    # 进接口字节数列表
    in_bytes_list = [i[1] for i in snmpv2_getbulk(ip, community_ro, "1.3.6.1.2.1.2.2.1.10", port=161)]
    # 出接口字节数列表
    out_bytes_list = [i[1] for i in snmpv2_getbulk(ip, community_ro, "1.3.6.1.2.1.2.2.1.16", port=161)]

    iface_name_list = []
    x = 0
    for i in iface_name:
        if 'Ethernet' in i:
            iface_data[i + '_in_bytes'] = int(in_bytes_list[x])
            iface_data[i + '_out_bytes'] = int(out_bytes_list[x])
            iface_data[i + '_speed'] = int(speed_list[x])
            x+=1
            iface_name_list.append(i)
    iface_data['if_name_list'] = iface_name_list
    iface_data['ip'] = ip
    iface_data['record_time'] = datetime.now()
    # iface_data['mem_f'] = int(snmpv2_get(ip, "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)[1])
    # iface_data['mem_u'] = int(snmpv2_get(ip, "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)[1])
    # iface_data['cpu_5s'] = snmpv2_get(ip, "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1]
    db.secie.insert_one(iface_data)


    # for obj in db.secie.find():
    #     pprint(obj)

def search_info_from_mongodb(ifname, direction, last_mins):
    if_bytes_list = []
    record_time_list = []
    for obj in db.secie.find({'record_time':{'$gte':datetime.now() - timedelta(minutes=last_mins)}}):
        # print(obj)
        if_bytes_list.append(obj[ifname + '_' + direction + '_bytes'])
        record_time_list.append(obj['record_time'])
    # print(if_bytes_list)

    # numpy的diff计算列表的差值
    # np.diff([x for x in range(5)])
    # array([1, 1, 1, 1])
    # 通过这种方式获取两次获取的字节数差值
    diff_if_bytes_list = list(np.diff(if_bytes_list))

    # 计算两次时间对象的秒数的差值，np的多态太牛逼了
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]

    # 计算速率
    # *8得到bit数
    # /1000计算Kb
    # / x[1] 计算kbs
    #  round(x, 2)保留两位小数
    # zip把字节差列表和时间差列表 压到一起
    speed_list = list(map(lambda x: round(((x[0]* 8)/(1000* x[1])), 5), zip(diff_if_bytes_list, diff_record_time_list)))
    record_time_list = record_time_list[1:]
    print('==================', speed_list,record_time_list)
    return record_time_list, speed_list

def mat_line(record_time_list, speed_list):
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 处理X轴时间格式
    import matplotlib.dates as mdate

    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M:%S')) # 设置时间标签显示格式


    # 添加主题和注释
    plt.title('路由器G1接口，in方向，2分钟速率')
    plt.xlabel('采集时间')
    plt.ylabel('速率kbps')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 实线红色
    ax.plot(record_time_list, speed_list, linestyle='solid', color='r', label='R1')
    # 虚线黑色
    # ax.plot(x, y, linestyle='dashed', color='b', label='R1')

    # 设置说明的位置
    ax.legend(loc='upper left')

    # 保存到图片
    # plt.savefig('result1.png')
    # 绘制图形
    plt.show()



if __name__ == "__main__":
    # client = MongoClient('mongodb://qytangadmin:Cisc0123@10.10.10.22:27017/qytang')
    # db = client['qytang']
    # db.secie.remove()
    # for obj in db.secie.find():
    #     print(obj)
    # write_iface_data_to_mongodb('10.10.10.22', "public")
    # print(search_info_from_mongodb('GigabitEthernet', 'out', 2))
    # mat_line(search_info_from_mongodb('GigabitEthernet1', 'in', 10)[0], search_info_from_mongodb('GigabitEthernet1', 'in', 10)[1])
    # mat_line(search_info_from_mongodb('GigabitEthernet1', 'in', 10)[0], search_info_from_mongodb('GigabitEthernet1', 'in', 10)[1])
    write_db_period(5, 1200)
    # mat_line(search_info_from_mongodb('GigabitEthernet1', 'out', 2))

