#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: sum.py
@time: 2016/9/7 19:26
"""
import sqlite3 as sql
import logging as log


def main():

    log.basicConfig(level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d %b %Y %H:%M:%S',
                    filename='D:/backup/sum.log', filemode='a')

    for i in range(2,12):
        conn_s = sql.connect("D:/backup/data_sum.db")
        cur_s = conn_s.cursor()
        cur_u = conn_s.cursor()
        add_db_path = "D:/backup/data_%d.db" % i
        conn_a = sql.connect(add_db_path)
        cur_a = conn_a.cursor()

        log.info("========== sum db %d Begin ==========" % i)

        ###################
        #

        log.info("========== db %d tDevice Begin ==========" % i)
        count = 0
        cur_a.execute("SELECT name,times,app_num,ip_num from tDevice")
        for raw in cur_a:
            count += 1
            name = raw[0].encode('utf-8')
            times = raw[1]

            if times == 1:
                continue

            num1 = raw[2]
            num2 = raw[3]

            cur_s.execute("SELECT times,app_num,ip_num from tDevice where name='%s'" % name)
            data_list = cur_a.fetchone()
            if data_list is not None:
                times = times + data_list[0]
                num1 = times + data_list[1]
                num2 = times + data_list[2]
                u_str = "UPDATE tDevice set times=%d,app_num=%d,ip_num=%d where name='%s'" % (times,num1,num2,name)
                cur_u.execute(u_str)

            else:
                i_str = "INSERT INTO tDevice (name,times,app_num,ip_num) values('%s',%d,%d,%d)" % (name,times,num1,num2)
                cur_u.execute(i_str)

        log.info("========== db %d tDevice END ==========" % i)

        ###################
        #

        log.info("========== db %d tApp Begin ==========" % i)
        count = 0
        cur_a.execute("SELECT name,times,device_num,ip_num from tApp")
        for raw in cur_a:
            count += 1
            name = raw[0].encode('utf-8')
            times = raw[1]

            if times == 1:
                continue

            num1 = raw[2]
            num2 = raw[3]

            cur_s.execute("SELECT times,device_num,ip_num from tApp where name='%s'" % name)
            data_list = cur_a.fetchone()
            if data_list is not None:
                times = times + data_list[0]
                num1 = times + data_list[1]
                num2 = times + data_list[2]
                u_str = "UPDATE tApp set times=%d,device_num=%d,ip_num=%d where name='%s'" % (times, num1, num2, name)
                cur_u.execute(u_str)

            else:
                i_str = "INSERT INTO tApp (name,times,device_num,ip_num) values('%s',%d,%d,%d)" % (
                name, times, num1, num2)
                cur_u.execute(i_str)

        log.info("========== db %d tApp END ==========" % i)

        ###################
        #

        log.info("========== db %d tIp Begin ==========" % i)
        count = 0
        cur_a.execute("SELECT name,times,app_num,device_num from tIp")
        for raw in cur_a:
            count += 1
            name = raw[0].encode('utf-8')
            times = raw[1]

            if times == 1:
                continue

            num1 = raw[2]
            num2 = raw[3]

            cur_s.execute("SELECT times,app_num,device_num from tIp where name='%s'" % name)
            data_list = cur_a.fetchone()
            if data_list is not None:
                times = times + data_list[0]
                num1 = times + data_list[1]
                num2 = times + data_list[2]
                u_str = "UPDATE tIpD set times=%d,app_num=%d,device_num=%d where name='%s'" % (times, num1, num2, name)
                cur_u.execute(u_str)

            else:
                i_str = "INSERT INTO tIp (name,times,app_num,device_num) values('%s',%d,%d,%d)" % (
                name , times, num1, num2)
                cur_u.execute(i_str)

        log.info("========== db %d tIp END ==========" % i)

        conn_a.commit()
        conn_s.commit()
        conn_a.close()
        conn_s.close()
        log.info("========== sum db %d End ==========" % i)










if __name__ == '__main__':
    main()


