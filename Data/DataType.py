# -*- coding: utf-8 -*-


"""
@version: 0.0.1
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: DataType.py
@time: 2016/6/17 16:41
"""


# import re



class basetype(object):
    """

    """

    def __init__(self, name, times, os, osv, model, time):
        self.name = name
        self.times = times
        self.os = listtype(os)
        self.osv = listtype(osv)
        self.model = listtype(model)
        self.time = listtype(time)


class listtype(object):
    """

    """

    def __init__(self, datastr):
        self.__data = datastr.split(',')

    def insertdata(self, datastr):

        try:
            self.__data.index(datastr)
        except ValueError:
            self.__data.append(datastr)

    def getstr(self):
        datastr = ''
        for i in range(len(self.__data)):
            datastr = self.__data[i] + ',' + datastr
        datastr = datastr.strip(',')
        return datastr
