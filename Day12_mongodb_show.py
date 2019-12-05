# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day12_mongodb_show.py
# @time: 2019-11-29  18:22:44




from pymongo import *
from Day12_mongodb_getif import search_info_from_mongodb
from matplotlib import pyplot as plt

client = MongoClient('mongodb://qytangadmin:Cisc0123@10.10.10.22:27017/qytang')
db = client['qytang']


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
    # write_iface_data_to_mongodb('10.10.10.22', "public")
    # print(search_info_from_mongodb('GigabitEthernet', 'out', 2))
    mat_line(search_info_from_mongodb('GigabitEthernet1', 'out', 2))
    # mat_line(search_info_from_mongodb('GigabitEthernet1', 'in', 10)[0], search_info_from_mongodb('GigabitEthernet1', 'in', 10)[1])
    # mat_line(search_info_from_mongodb('GigabitEthernet1', 'in', 10)[0], search_info_from_mongodb('GigabitEthernet1', 'in', 10)[1])
