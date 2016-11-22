# -*- coding: utf-8 -*-


"""
@version: 0.0.1
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: Sqlfunc.py
@time: 2016/6/17 16:41
"""

#
import sqlite3 as sql
import logging as log


# import re


##########################
# Table INIT function

# init Basic data table: tDevice, tApp, tIp

def init_device(cur):
    init_str = 'CREATE TABLE tDevice\
                (name text NOT NULL primary key,\
                 times integer NOT NULL,\
                 os text,\
                 osv text,\
                 model text,\
                 app_num integer ,\
                 ip_num integer,\
                 time text)'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


def init_app(cur):
    init_str = 'CREATE TABLE tApp\
                (name text NOT NULL primary key,\
                 times integer NOT NULL,\
                 os text,\
                 osv text,\
                 model text,\
                 device_num integer ,\
                 ip_num integer,\
                 time text)'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


def init_ip(cur):
    init_str = 'CREATE TABLE tIp\
                (name text NOT NULL primary key,\
                 times integer NOT NULL,\
                 os text,\
                 osv text,\
                 model text,\
                 device_num integer ,\
                 app_num integer,\
                 time text)'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


####################
# init app-device relation table: tApp_Device_r

def init_app_device(cur):
    init_str = 'CREATE TABLE tApp_Device_r\
                (app text NOT NULL,\
                 device text NOT NULL,\
                 times integer NOT NULL,\
                 primary key(app,device))'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


####################
# init app-ip relation table: tApp_Ip_r

def init_app_ip(cur):
    init_str = 'CREATE TABLE tApp_Ip_r\
                    (app text NOT NULL,\
                     ip text NOT NULL,\
                     times integer NOT NULL,\
                     primary key(app,ip))'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


####################
# init app-ip relation table : tDevice_Ip_r

def init_device_ip(cur):
    init_str = 'CREATE TABLE tDevice_Ip_r\
                (device text NOT NULL,\
                 ip text NOT NULL,\
                 times integer NOT NULL,\
                 primary key(device,ip))'
    try:
        cur.execute(init_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


###################
#   Insert Function

def insert_basic_data(cur, table, name, times, os, osv, model, time, num1=0, num2=0):
    # insert basic data of device ,app ,ip
    if table == 'tDevice':
        insert_str = "INSERT INTO tDevice (name,times,os,osv,model,app_num,ip_num,time)\
                    values('%s',%d,'%s','%s','%s',%d, %d ,'%s')" % \
                     (name, times, os, osv, model, num1, num2, time)
    elif table == 'tApp':
        insert_str = "INSERT INTO tApp (name,times,os,osv,model,device_num,ip_num,time)\
                    VALUES('%s',%d,'%s','%s','%s',%d, %d ,'%s')" % \
                     (name, times, os, osv, model, num1, num2, time)
    elif table == 'tIp':
        insert_str = "INSERT INTO tIp (name,times,os,osv,model,app_num,device_num,time)\
                    VALUES('%s',%d,'%s','%s','%s',%d, %d ,'%s')" % \
                     (name, times, os, osv, model, num1, num2, time)
    else:
        insert_str = 'SELECT 1'
        log.error('[-] Insert Error : No Table Named %s' % table)

    try:
        cur.execute(insert_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


def insert_rl_data(cur, table, value1, value2, times):
    # insert relation values
    if table == 'device_ip':
        insert_str = "INSERT INTO tDevice_Ip_r (device,ip,times)\
                     VALUES('%s','%s',%d)" % \
                     (value1, value2, times)

    elif table == 'app_device':
        insert_str = "INSERT INTO tApp_Device_r (app,device,times)\
                     VALUES('%s','%s',%d)" % \
                     (value1, value2, times)

    elif table == 'app_ip':
        insert_str = "INSERT INTO tApp_Ip_r (app,ip,times)\
                     VALUES('%s','%s',%d)" % \
                     (value1, value2, times)

    else:
        insert_str = "SELECT 1"

    try:
        cur.execute(insert_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Init Error: ' + str(e))


########################
# update basic data table Function

def update_basic_data(cur, table, name, times, os, osv, model, time):
    update_str = "update %s set times=%d,os='%s',osv='%s',model='%s',\
                     time='%s' where name='%s'" % (table, times, os, osv, model, time, name)

    # print update_str

    try:
        cur.execute(update_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Update Error: ' + str(e))


#######################
# update relation data table

def update_rl_data(cur, table, value1, value2, times):
    if table == 'app_device':
        update_str = "UPDATE tApp_Device_r SET times = %d where app = '%s' and device = '%s'" % \
                     (times, value1, value2)
    elif table == 'app_ip':
        update_str = "UPDATE tApp_Ip_r SET times = %d where app = '%s' and ip = '%s'" % \
                     (times, value1, value2)
    elif table == 'device_ip':
        update_str = "UPDATE tDevice_Ip_r SET times = %d where device = '%s' and ip= '%s'" % \
                     (times, value1, value2)
    else:
        update_str = "SELECT 1"

    try:
        cur.execute(update_str)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error('[-] Update Error: ' + str(e))


#######################
# Search database

def search_basic_data(cur, table, name):
    search_str = "select * from %s where name = '%s'" % (table, name)
    try:
        cur.execute(search_str)
    except sql.OperationalError as e:
        log.error('[-] Search Error: No Name %s in table %s.' % (name, table))
        log.error('[--] ' + str(e))

    datalist = cur.fetchone()

    if datalist is not None:
        return datalist
    else:
        return 0


def search_rl_data(cur, table, value1, value2):
    if table == 'app_device':
        search_str = "SELECT * from tApp_Device_r where app = '%s' and device = '%s'" % \
                     (value1, value2)
    elif table == 'app_ip':
        search_str = "SELECT * from tApp_Ip_r where app = '%s' and ip = '%s'" % \
                     (value1, value2)
    elif table == 'device_ip':
        search_str = "SELECT * from tDevice_Ip_r where device = '%s' and ip = '%s'" % \
                     (value1, value2)
    else:
        search_str = 'SELECT 1'
    try:
        cur.execute(search_str)
    except sql.OperationalError as e:
        log.error('[-] Search Error: No relation %s-%s in table %s.' % (value1, value2, table))
        log.error('[--] ' + str(e))

    datalist = cur.fetchone()

    if datalist is not None:
        return datalist
    else:
        return 0


#########################
# Drop Table Function

def drop_tb(cur, tb_str):
    drop_str = 'drop table %s' % tb_str
    try:
        cur.execute(drop_str)
    except sql.InternalError as e:
        print '[-] Clear Error: ' + str(e)


################
# default test FUnction

def start():
    # conn = sql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='1234', db='click_data')
    # conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='click_data')
    conn = sql.connect('data.db')
    cur = conn.cursor()
    # init tables
    init_app(cur)
    init_device(cur)
    init_ip(cur)

    # test code for operation functions

    # close database connection
    cur.close()
    conn.commit()
    conn.close()

    return 0


#################
# clear database and init a new one
def clear():
    # conn = sql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='1234', db='click_data')
    # conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='click_data')
    conn = sql.connect('data.db')
    cur = conn.cursor()

    # drop table
    drop_tb(cur, 'device')
    drop_tb(cur, 'app')
    drop_tb(cur, 'ip')

    # init tables
    init_app(cur)
    init_device(cur)
    init_ip(cur)

    #  close database connection
    cur.close()
    conn.commit()
    conn.close()

    return 0


def test():
    # conn = sql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='click_data')
    conn = sql.connect('data.db')
    cur = conn.cursor()

    count1 = cur.execute('CREATE INDEX idx_de ON device(name,times)')
    count2 = cur.execute('CREATE INDEX idx_app ON app(name,times)')
    count3 = cur.execute('CREATE INDEX idx_ip ON ip(name,times)')

    # for raw in cur:
    #     print raw[0].split(',')[0]
    print count1, count2, count3
    cur.close()
    conn.close()


if __name__ == '__main__':
    pass
