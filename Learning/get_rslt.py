#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: get_rslt.py
@time: 2016/9/8 18:25
"""
import numpy as np
import logging as log
import os
import sqlite3 as sql

def get_result(num,target,dirs,filename,n_cluster):

    work_dir = "D:/backup/data_%d/" % num
    file_path = work_dir + "%s.csv" % target
    target_dir = work_dir + dirs
    cal_file = target_dir + filename

    conn = sql.connect(work_dir + dirs +"2D_10_labels.db")
    cur = conn.cursor()
    init_str = "CREATE Table label(name text primary key,times int,num1 int,num2 int,label int)"
    try:
        cur.execute(init_str)
    except (sql.OperationalError,sql.InternalError) as e:
        print e


    or_file = open(file_path,'r')
    cl_file = open(cal_file,'r')

    for line1,line2 in zip(or_file,cl_file):
        name = line1.split(',')[0]

        try :
            times = int(line1.split(',')[1])
            num1 = int(line1.split(',')[2])
            num2 = int(line1.split(',')[3])
            label = int(line2)
        except ValueError as e:
            print e
            continue

        insert_str = "INSERT INTO label (name,times,num1,num2,label)\
            VALUES('%s','%d','%d','%d','%d')" % (name,times,num1,num2,label)
        try:
            cur.execute(insert_str)
        except (sql.OperationalError, sql.InternalError) as e:
            print e

    conn.commit()

    # ###############
    # # K-means
    for i in range(n_cluster):
        name_path = target_dir + "2D_10_rslt_%d" % i
        name_file = open(name_path,'w+')
        cur.execute("SELECT * from label where label=%d" % i)
        for raw in cur:
            rlst_str = raw[0].encode('utf-8')
            for x in range(1,len(raw)):
                rlst_str = rlst_str + ',' + str(raw[x])
            rlst_str.strip(',')
            rlst_str = rlst_str + '\n'
            name_file.writelines(rlst_str)
        cur.execute("SELECT sum(times) from label where label=%d" % i)
        tl_str = "totalnum = %d \n" % cur.fetchone()[0]
        name_file.writelines(tl_str)
        name_file.close()

    ##############
    # DBSCAN
    # for i in range(-1,n_cluster):
    #     name_path = target_dir + "2D_rslt_%d" % i
    #     name_file = open(name_path,'w+')
    #     cur.execute("SELECT * from label where label=%d" % i)
    #     for raw in cur:
    #         rlst_str = raw[0].encode('utf-8')
    #         for x in range(1,len(raw)):
    #             rlst_str = rlst_str + ',' + str(raw[x])
    #         rlst_str.strip(',')
    #         rlst_str = rlst_str + '\n'
    #         name_file.writelines(rlst_str)
    #     cur.execute("SELECT sum(times) from label where label=%d" % i)
    #     tl_str = "totalnum = %d \n" % cur.fetchone()[0]
    #     name_file.writelines(tl_str)
    #     name_file.close()



def main():

    get_result(1,'device','device_Kmeans/','2d_10.csv',10)

if __name__ == '__main__':
    main()


