#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: plot.py
@time: 2016/9/8 19:18
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_Kmeans_3d(X, label, target, fig_path, fig_b_path):
    #########
    # plot
    fig = plt.figure(figsize=(10, 10))
    ax = fig.gca(projection='3d')

    shape = ['o', '+', '*', 'x', 4, 5, 6, 7, 's', 'd']
    unique_labels = set(label)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        class_mem_mask = (label == k)
        xy = X[class_mem_mask]
        ax.scatter(xy[:, 0], xy[:, 1], xy[:, 2], c='k', marker=shape[k])

    ax.set_xlabel('times')

    if target == 'app':

        ax.set_ylabel('device_num')
        ax.set_zlabel('ip_num')
        plt.savefig(fig_path)
        ax.set_xlim3d(0.0, 0.4)
        ax.set_ylim3d(0.0, 0.2)
        ax.set_zlim3d(0.0, 0.2)
    elif target == 'device':
        ax.set_ylabel('app_num')
        ax.set_zlabel('ip_num')
        plt.savefig(fig_path)
        ax.set_xlim3d(0.0, 0.15)
        ax.set_ylim3d(0.0, 0.4)
        ax.set_zlim3d(0.0, 0.15)
    elif target == 'ip':
        ax.set_ylabel('device_num')
        ax.set_zlabel('app_num')
        plt.savefig(fig_path)
        ax.set_xlim3d(0.0, 0.2)
        ax.set_ylim3d(0.0, 0.3)
        ax.set_zlim3d(0.0, 0.2)

    # plt.show()

    plt.savefig(fig_b_path)
    plt.close()


def plot_Kmeans_2d(X_2d, label_2d, target, fig_path, fig_b_path):
    fig = plt.figure(figsize=[10, 10])
    ax = fig.gca()
    shape = ['o', '+', '*', 'x', 4, 5, 6, 7, 's', 'd']
    unique_labels = set(label_2d)

    for k in unique_labels:
        class_mem_mask = (label_2d == k)
        xy = X_2d[class_mem_mask]
        ax.scatter(xy[:, 0], xy[:, 1], c='k', marker=shape[k])

    if target == 'app':
        plt.xlabel("times per device")
        plt.ylabel("app per ip")
        plt.savefig(fig_path)
        plt.xlim(-50, 800)
        plt.ylim(-50, 600)
        plt.savefig(fig_b_path)
        plt.close()
    elif target == 'device':
        plt.xlabel("times per app")
        plt.ylabel("times per ip")
        plt.savefig(fig_path)
        plt.xlim(-100, 2000)
        plt.ylim(-100, 2000)
        plt.savefig(fig_b_path)
        plt.close()
    elif target == 'ip':
        plt.xlabel("times per device")
        plt.ylabel("times per app")
        plt.savefig(fig_path)
        plt.xlim(-100, 2000)
        plt.ylim(-100, 2000)
        plt.savefig(fig_b_path)
        plt.close()


def plot_DBSCAN_3d():
    pass


if __name__ == '__main__':
    pass
