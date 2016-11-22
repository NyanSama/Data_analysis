#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: 0.0.2
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: main.py
@time: 2016/6/17 16:41
"""

from getdata import *
from DataType import basetype as basedata
from Sqlfunc import *
import logging as log
import time as timefuc


# from utils import *


################
# Save sql data to data structure
def list_to_data(data_list):
    data = basedata(data_list[0].encode('utf-8'), data_list[1], data_list[2].encode('utf-8'),
                    data_list[3].encode('utf-8'), data_list[4].encode('utf-8'), data_list[7].encode('utf-8'))
    return data


def insertlistdata(data_list, os, osv, model, time):
    """
    :param time:
    :param model:
    :param osv:
    :param os: os
    :type data_list: basedata
    """
    data_list.os.insertdata(os)
    data_list.osv.insertdata(osv)
    data_list.model.insertdata(model)
    data_list.time.insertdata(time)

    return data_list


######################
# Basic process
def basic_process(cur, table, name, os, osv, model, time):
    """

    """
    sql_data_list = search_basic_data(cur, table, name)

    if sql_data_list is 0:
        insert_basic_data(cur, table, name, 1, os, osv, model, time)

    else:
        # Base data process
        old_data = list_to_data(sql_data_list)
        old_data = insertlistdata(old_data, os, osv, model, time)
        old_data.times += 1

        update_basic_data(cur, table, name, old_data.times, old_data.os.getstr(), old_data.osv.getstr(),
                          old_data.model.getstr(), old_data.time.getstr())


#################
# Relation process

def relation_process(cur, table, value1, value2):
    sql_data_list = search_rl_data(cur, table, value1, value2)

    if sql_data_list is 0:
        insert_rl_data(cur, table, value1, value2, 1)

    else:
        times = sql_data_list[2] + 1
        update_rl_data(cur, table, value1, value2, times)


def countline(path):
    """
    :type read_file: file
    """
    count = 0
    start_time = timefuc.time()
    read_file = open(path, 'r')

    for line in read_file:
        if line:
            count += 1

    log_str = 'Count lines time : %s' % (timefuc.time() - start_time)
    log.info(log_str)

    read_file.close()
    return count


def main():
    # Start time
    # start_time = timefuc.time()

    # log setting
    log.basicConfig(level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d %b %Y %H:%M:%S',
                    filename='data.log', filemode='w+')
    # conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='click_data')

    for num in range(2,11):

        read_file_path = 'F:/Working/DATA/original/%d' % (num + 1)
        db_file_path = 'data_%d.db' % (num + 1)

        log.info("================= File %d Running Begin =================" % (num + 1))
        log.info("File Path : %s " % read_file_path)
        log.info("Database Name : %s " % db_file_path)

        try:
            datafile = open(read_file_path, 'r')
        except IOError as e:
            log.error('[-] Original Data Not Found')
            log.error(e)
            quit()

        conn = sql.connect(db_file_path)

        max_count = countline(read_file_path)
        log.info("Total Lines : %d " % max_count)

        cur = conn.cursor()

        init_app(cur)
        init_ip(cur)
        init_device(cur)

        init_app_device(cur)
        init_app_ip(cur)
        init_device_ip(cur)

        # set cursor
        count = 0
        start_time = or_time = timefuc.time()

        # read data
        for line in datafile:
            if not line:
                log.error('[-] Original Data is Empty Now!')

            datalist = read_data_from_line(line)

            if datalist[0] is None:
                count += 1
                continue

            # save data to data structure
            name = datalist[0]
            os = datalist[1]
            osv = datalist[2]
            model = datalist[3]
            app_name = datalist[4]
            ip = datalist[5]
            time = datalist[6]

            ############


            # device
            basic_process(cur, 'tDevice', name, os, osv, model, time)

            # app
            basic_process(cur, 'tApp', app_name, os, osv, model, time)

            # ip
            basic_process(cur, 'tIp', ip, os, osv, model, time)

            ############
            #  relation data process

            # app-device
            relation_process(cur, 'app_device', app_name, name)

            # app-ip
            relation_process(cur, 'app_ip', app_name, ip)

            # device-ip
            relation_process(cur, 'device_ip', name, ip)

            if count % 100000 == 0:
                end_time = timefuc.time()
                log.info(count)
                log.info("Circul time : %s " % (end_time - start_time))

                start_time = end_time

            count += 1
            if count > max_count:
            #if count > 10000:
                end_time = timefuc.time()
                log.info("TOTAL TIME : %s" % (end_time - or_time))
                log.info(line[0:40])
                break

        # close file
        datafile.close()

        # commit & close database
        cur.close()
        conn.commit()
        conn.close()
        log.info("================= File %d Runing End    =================" % (num + 1))


if __name__ == '__main__':
    main()
