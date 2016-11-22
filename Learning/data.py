#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: data.py
@time: 2016/9/7 11:07
"""

import sqlite3 as sql
import numpy as np
import pandas as pd
import csv
import os


# class Getdata:
#     def __init__db(self,db_path):
#         self._conn = sql.connect(db_path)
#         self._cur = self._conn.cursor()
#
#     def __init__(self,db_path):
#         self.__init__db(db_path)
#
#     def save_csv(self,dir_path):


def getdata():

    for i in range(1,12):

        db_path = "D:/backup/data_%d.db" % i
        os.mkdir("D:/backup/data_%d" % i)
        device_path = "D:/backup/data_%d/device.csv" % i
        app_path = "D:/backup/data_%d/app.csv" % i
        ip_path = "D:/backup/data_%d/ip.csv" % i

        device_file = open(device_path,'wb')
        app_file = open(app_path,'wb+')
        ip_file = open(ip_path,'wb')

        conn = sql.connect(db_path)

        cur = conn.cursor()

        cur.execute("SELECT name,times,app_num,ip_num from tDevice where times>1")
        device_write = csv.writer(device_file)
        device_write.writerow(['name','times','app_num','ip_num'])
        for raw in cur:
            device_write.writerow(raw)
        device_file.close()

        cur.execute("SELECT name,times,device_num,ip_num from tApp where times>1")
        app_write = csv.writer(app_file)
        app_write.writerow(['name','times','device_num','ip_num'])
        for raw in cur:
            app_write.writerow([raw[0].encode('utf-8'),raw[1],raw[2],raw[3]])
        app_file.close()

        cur.execute("SELECT name,times,device_num,app_num from tIp where times>1")
        ip_write = csv.writer(ip_file)
        ip_write.writerow(['name','times','device_num','app_num'])
        for raw in cur:
            ip_write.writerow(raw)
        ip_file.close()





if __name__ == '__main__':
    getdata()


