#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: 0.0.1
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: getdata.py
@time: 2016/6/18 13:42
"""


def get_data(datastr, key1, key2):
    lenth = len(key1)
    s = datastr.find('"' + key1 + '"')
    l = datastr.find('"' + key2 + '"')
    if s > -1 and l > -1:
        return datastr[s + 2 + lenth:l].strip('":{},[]')
    else:
        return None


def read_data_from_line(line):
    line = line.replace(r'\"', '"')
    line = line.replace("'", "_")

    time = line[11:19]
    timelist = time.split(':')
    time = int(timelist[0]) * 6300 + int(timelist[1]) * 60 + int(timelist[2])

    name = get_data(line, 'dpidsha1', 'user')
    os = get_data(line, 'os', 'sw')
    osv = get_data(line, 'osv', 'sh')
    model = get_data(line, 'model', 'connectiontype')
    app_name = get_data(line, 'name', 'paid')
    ip = get_data(line, 'ip', 'js')


    return [name, os, osv, model, app_name, ip, str(time)]


if __name__ == '__main__':
    pass
