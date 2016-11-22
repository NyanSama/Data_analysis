#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: main.py
@time: 2016/9/8 18:01
"""

from K_means import K_means



def main():
    for i in range(2,12):
        K_means(i, 'app')
        K_means(i, 'device')
        K_means(i, 'ip')


if __name__ == '__main__':
    main()


