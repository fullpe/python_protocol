# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: Day4_matplotlib.py
# @time: 2019-11-18  14:05:24


from matplotlib import pyplot as plt
import matplotlib.font_manager
# matplotlib.use('GTK3Agg')
import matplotlib


print(matplotlib.matplotlib_fname())
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = ['sans-serif']


def mat_bing(size_list, name_list):
    plt.figure(figsize=(6, 6))
    patches, label_text, percent_text = plt.pie(size_list,
                                                labels=name_list,
                                                labeldistance=1.1,
                                                autopct='%3.1f%%',
                                                shadow=False,
                                                startangle=90,
                                                pctdistance=0.6)
    for l in label_text:
        l.set_size = 30,
    for p in percent_text:
        p.set_size = 20
    plt.axis('equal')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    counters = [30, 53, 12, 45]
    protocols = ['http协议', 'ftp协议', 'rdp协议', 'qq协议']
    mat_bing(counters, protocols)
