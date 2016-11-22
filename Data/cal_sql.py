# coding=utf-8
import logging as log
import sqlite3 as sql
import time as timefunc

def creat_index(cur):
    index_ad_a = "CREATE INDEX 'iApp_Device_r_app' ON 'tApp_Device_r' ('app')"
    index_ad_d = "CREATE INDEX 'iApp_Device_r_device' ON 'tApp_Device_r' ('device')"
    index_ai_a = "CREATE INDEX 'iApp_Ip_r_app' ON 'tApp_Ip_r' ('app')"
    index_ai_i = "CREATE INDEX 'iApp_Ip_r_ip' ON 'tApp_Ip_r' ('ip')"
    index_di_d = "CREATE INDEX 'iDevice_Ip_r_device' ON 'tDevice_Ip_r' ('device')"
    index_di_i = "CREATE INDEX 'iDevice_Ip_r_ip' ON 'tDevice_Ip_r' ('ip')"

    try:
        cur.execute(index_ad_a)
        cur.execute(index_ad_d)

    except (sql.InternalError, sql.OperationalError) as e:
        log.error("[-]Create index Error: " + str(e))

    log.info("[+] tApp_Device_r Index success.")

    try:
        cur.execute(index_ai_a)
        cur.execute(index_ai_i)
    except (sql.InternalError, sql.OperationalError) as e:
        log.error("[-]Create index Error: " + str(e))

    log.info("[+] tApp_Ip_r Index success.")

    try:
        cur.execute(index_di_d)
        cur.execute(index_di_i)

    except (sql.InternalError, sql.OperationalError) as e:
        log.error("[-]Create index Error: " + str(e))

    log.info("[+] tDevice_Ip_r Index success.")



def count_data(cur,table,name):
    count_str = "SELECT COUNT(*) from %s where device = '%s'" % (table, name)
    cur.execute(count_str)
    count = cur.fetchone()
    return count


def update_lb_data(cur,table,name,num,target):
    update_str = "UPDATE %s set %s = %d where name = '%s'" % (table,target,num,name)





def main():
    db_path = 'D:/backup/data_11.db'
    td = 'tDevice'
    ta = 'tApp'
    ti = 'tIp'
    ta_d_r = 'tApp_Device_r'
    ta_i_r = 'tApp_Ip_r'
    td_i_r = 'tDevice_Ip_r'

    conn = sql.connect(db_path)

    cur = conn.cursor()
    cur_r = conn.cursor()

    log.basicConfig(level=log.DEBUG, format='%(asctime)s: %(message)s', datefmt='%d %b %Y %H:%M:%S',
                    filename='D:/backup/cal_data11.log', filemode='a')

    log.info("=== Create SQl Index ===")
    creat_index(cur)
    log.info("=== create Index end ===")

    ###############
    #  cal for Device
    log.info("=== Cal For tDevice begin ===")
    or_time = start_time = timefunc.time()
    select_str = 'SELECT name,times from %s' % td
    cur.execute(select_str)
    count = 0

    for raw in cur:

        name = raw[0].encode('utf-8')
        times = raw[1]
        if times == 1:
            continue

        else:
            count_str = "SELECT COUNT(*) from %s where device = '%s'" % (ta_d_r, name)
            cur_r.execute(count_str)
            num1 = cur_r.fetchone()
            update_str = "UPDATE %s set app_num = %d where name = '%s'" % (td,num1[0],name)
            cur_r.execute(update_str)

            count_str = "SELECT COUNT(*) from %s where device = '%s'" % (td_i_r, name)
            cur_r.execute(count_str)
            num2 = cur_r.fetchone()
            update_str = "UPDATE %s set ip_num = %d where name = '%s'" % (td,num2[0],name)
            cur_r.execute(update_str)

        if count % 50000 == 0:
            log.info(count)
            end_time = timefunc.time()
            log.info("Circul time : %s " % (end_time-start_time))
            start_time = end_time

        count += 1
    end_time = timefunc.time()
    log.info("Total Time : %s " % (end_time - or_time))
    conn.commit()
    log.info("=== Cal for tDevice End ===")

    ##############
    #  cal for App

    log.info("=== Cal For tApp begin ===")
    or_time = start_time = timefunc.time()
    select_str = 'SELECT name,times from %s' % ta
    cur.execute(select_str)
    count = 0

    for raw in cur:

        name = raw[0].encode('utf-8')
        times = raw[1]
        if times == 1:
            continue

        else:
            count_str = "SELECT COUNT(*) from %s where app = '%s'" % (ta_d_r, name)
            cur_r.execute(count_str)
            num1 = cur_r.fetchone()
            update_str = "UPDATE %s set device_num = %d where name = '%s'" % (ta,num1[0],name)
            cur_r.execute(update_str)

            count_str = "SELECT COUNT(*) from %s where app = '%s'" % (ta_i_r, name)
            cur_r.execute(count_str)
            num2 = cur_r.fetchone()
            update_str = "UPDATE %s set ip_num = %d where name = '%s'" % (ta,num2[0],name)
            cur_r.execute(update_str)

        if count % 2000 == 0:
            log.info(count)
            end_time = timefunc.time()
            log.info("Circul time : %s " % (end_time-start_time))
            start_time = end_time

        count += 1
    end_time = timefunc.time()
    log.info("Total Time : %s " % (end_time - or_time))
    conn.commit()
    log.info("=== Cal for tApp End ===")

    ##############
    #  cal for Ip

    log.info("=== Cal For tIp begin ===")
    or_time = start_time = timefunc.time()
    select_str = 'SELECT name,times from %s' % ti
    cur.execute(select_str)
    count = 0

    for raw in cur:

        name = raw[0].encode('utf-8')
        times = raw[1]
        if times == 1:
            continue

        else:
            count_str = "SELECT COUNT(*) from %s where ip = '%s'" % (td_i_r, name)
            cur_r.execute(count_str)
            num1 = cur_r.fetchone()
            update_str = "UPDATE %s set device_num = %d where name = '%s'" % (ti,num1[0],name)
            cur_r.execute(update_str)

            count_str = "SELECT COUNT(*) from %s where ip = '%s'" % (ta_i_r, name)
            cur_r.execute(count_str)
            num2 = cur_r.fetchone()
            update_str = "UPDATE %s set app_num = %d where name = '%s'" % (ti,num2[0],name)
            cur_r.execute(update_str)

        if count % 50000 == 0:
            log.info(count)
            end_time = timefunc.time()
            log.info("Circul time : %s " % (end_time-start_time))
            start_time = end_time

        count += 1

    end_time = timefunc.time()
    log.info("Total Time : %s " % (end_time - or_time))

    log.info("=== Cal for tIp End ===")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
