# !/usr/bin/env python3
# -*- coding=utf-8 -*-
# @Author  : zunsi
# @file: test.py
# @time: 2019-11-19  15:48:11


import random
num = []
for i in range(1, 21):
    if i < 10:
        x = random.randrange(15, 100, 7)
        num.append(x)
    else:
        break

# print(num)


from datetime import datetime, timedelta
now = datetime.now() - timedelta(hours=12)
time = [now]
for i in range(1, 25):
    if i < 25:
        a = now -timedelta(hours=1)
        time.append(a)
    else:
        break
# print(time)

time_list = {}
for time_list in time, num:
    print(time_list[0])