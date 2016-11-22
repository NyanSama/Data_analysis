#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
@version: ??
@author: Nyansama
@contact: Nyansama@163.com
@site: http://www.nyansama.com
@software: PyCharm Community Edition
@file: K_means.py
@time: 2016/9/7 18:06
"""

import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
import logging as log
from plot import plot_Kmeans_3d
from plot import plot_Kmeans_2d
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN


def normalized(data):
    """
    :param data:
    :type data:np.ndarray
    :return:
    """
    r_data = np.zeros(data.shape)
    for i in range(len(data[0, :])):
        data_max = data.max(0)[i]
        data_min = data.min(0)[i]
        delta = data_max - data_min
        r_data[:, i] = (data[:, i] - data_min) / delta

    return r_data


def K_means(num, target):
    """
    :param num: 1~11
    :param target: app/device/ip
    :return:
    """
    work_dir = "D:/backup/data_%d/" % num
    file_path = work_dir + "%s.csv" % target
    target_dir = work_dir + '%s_Kmeans/' % target
    try:
        os.mkdir(target_dir)
    except WindowsError as e:
        print target_dir + " is already exit!"

    data_file = open(file_path, 'rb')
    data = np.loadtxt(data_file, delimiter=',', skiprows=1, usecols=(1, 2, 3))

    ####################
    # 3-dimension cluster
    # print data.shape

    X_3d = normalized(data)
    inertias = np.zeros(9)
    for n in range(2, 11):
        label_path = target_dir + "3d_%d.csv" % n
        lable_file = open(label_path, 'w')
        fig_path = target_dir + "3d_%d.png" % n
        fig_b_path = target_dir + "3d_%d_b.png" % n
        fig_in_path = target_dir + "3d_in.png"

        #########
        # 3-Dimension cluster
        est_3d = KMeans(n_clusters=n).fit(X_3d)
        label = est_3d.labels_
        inertias[n - 2] = est_3d.inertia_
        np.savetxt(lable_file, label.astype(np.int).reshape(-1, 1), header="label", fmt='%d')
        lable_file.close()

        # plot

        plot_Kmeans_3d(X_3d, label, target, fig_path, fig_b_path)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    clu_num = range(2, 11)
    ax.plot(clu_num, inertias, c='k')
    ax.scatter(clu_num, inertias, s=10, c='k')
    plt.savefig(fig_in_path)
    plt.close()
    ########
    # 3-Dimensions Cluster end
    ########

    ########
    # 2-Dimensions Cluster : times/num1,times/num2

    X_2d = np.zeros([data.shape[0],2])
    X_2d[:,0] = data[:,0] / data[:,1]
    X_2d[:,1] = data[:,0] / data[:,2]
    # X_2d[:,0] = data[:,1]/data[:,2]
    # X_2d[:,1] = data[:,1]/data[:,2]

    X_2d_r = normalized(X_2d)
    inertia_2d = np.zeros(9)
    fig_in_path = target_dir + "2d_in.png"

    for n in range(2, 11):
        label_path = target_dir + "2d_%d.csv" % n
        lable_file = open(label_path, 'w')
        fig_path = target_dir + "2d_%d.png" % n
        fig_b_path = target_dir + "2d_%d_b.png" % n

        #########
        # 2-Dimension kmeans
        est_2d = KMeans(n_clusters=n).fit(X_2d_r)
        label_2d = est_2d.labels_
        inertia_2d[n - 2] = est_2d.inertia_
        np.savetxt(lable_file, label_2d.astype(np.int).reshape(-1, 1), header="label", fmt='%d')
        lable_file.close()

        plot_Kmeans_2d(X_2d, label_2d, target, fig_path, fig_b_path)

    plt.figure(figsize=(8, 8))
    clu_num = range(2, 11)
    plt.plot(clu_num, inertia_2d, c='k')
    plt.scatter(clu_num, inertia_2d, s=10, c='k')
    plt.savefig(fig_in_path)
    plt.close()

    ########
    # 2-Dimensions Cluster End

def fDBSCAN(num,target):

    work_dir = "D:/backup/data_%d/" % num
    file_path = work_dir + "%s.csv" % target
    target_dir = work_dir + '%s_DBSCAN_t/' % target
    try:
        os.mkdir(target_dir)
    except WindowsError as e:
        print target_dir + " is already exit!"

    data_file = open(file_path, 'rb')
    data = np.loadtxt(data_file, delimiter=',', skiprows=1, usecols=(1, 2, 3))

    ########
    ## 3D cluster

    # init path
    label_path = target_dir + "3d.csv"
    lable_file = open(label_path, 'w')

    # fig_in_path = target_dir + "3d_in.png"

    # spslit data
    data_mask = np.zeros(data.shape[0],dtype=bool)
    for i,x in zip(range(data.shape[0]),data):
        data_mask[i] = (x[0] > 28 and (x[0] <100 or x[0] ==100) and (x[1]!=1 or x[2]!=1))

    r_data = data[data_mask]

    r_2d_data = np.zeros([r_data.shape[0],2])
    r_2d_data[:,0] = r_data[:,0] / r_data[:,1]
    r_2d_data[:,1] = r_data[:,0] / r_data[:,2]

    data_2d = np.zeros([data.shape[0],2])
    data_2d[:,0] = data[:,0] / data[:,1]
    data_2d[:,1] = data[:,0] / data[:,2]

    #####
    # data plot
    # fig = plt.figure(figsize=(10,10))
    # ax = fig.gca(projection='3d')
    # ax.scatter(data[:,0],data[:,1],data[:,2],c='k',marker='o')
    # ax.set_xlabel("times")
    # ax.set_ylabel("device_num")
    # ax.set_zlabel("app_num")
    # fig_path = target_dir + "3d_real.png"
    # plt.savefig(fig_path)
    # ax.set_xlim(0,1000)
    # ax.set_ylim(0,1000)
    # ax.set_zlim(0,30)
    # fig_path = target_dir + "3d_real_b.png"
    # plt.savefig(fig_path)
    # plt.close()
    #
    # fig = plt.figure(figsize=(10,10))
    # ax = fig.gca()
    # ax.scatter(data_2d[:,0],data_2d[:,1],s=10,c='k')
    # ax.set_xlabel("times per device_num")
    # ax.set_ylabel("tiems per app_num")
    # fig_path = target_dir + "2d_real.png"
    # plt.savefig(fig_path)
    # ax.set_xlim(-50,500)
    # ax.set_ylim(-50,500)
    # fig_path = target_dir + "2d_real_b.png"
    # plt.savefig(fig_path)
    # plt.close()









    # data

    X_3d = MinMaxScaler().fit_transform(r_data)
    if target == 'app':
        X_3d = MinMaxScaler().fit_transform(data)
    else:
        X_3d = MinMaxScaler().fit_transform(r_data)

    if target == 'app':
        X_2d = MinMaxScaler().fit_transform(data_2d)
    else:
        X_2d = MinMaxScaler().fit_transform(r_2d_data)


    #X_3d_s = normalized(data)
    X_3d = StandardScaler().fit_transform(X_3d)
    X_2d = StandardScaler().fit_transform(X_2d)

    ###########
    ## 3d data
    eps = 0.5
    min_samples = 50

    if target == 'app':
        eps = 0.03
        min_samples = 10
    elif target == 'device':
        eps = 0.35
        min_samples = 10
    elif target == 'ip':
        eps = 0.35
        min_samples = 10
    else:
        exit()

    db_3d = DBSCAN(eps=eps,min_samples=min_samples).fit(X_3d)
    core_samples_mask = np.zeros_like(db_3d.labels_,dtype=bool)
    core_samples_mask[db_3d.core_sample_indices_] = True
    labels = db_3d.labels_
    or_labels = np.zeros([data.shape[0],1])
    j = 0
    for i in range(np.shape(data_mask)[0]):
        if data_mask[i] == True:
            or_labels[i] = labels[j]
            j = j + 1
        else:
            or_labels[i] = -2

    np.savetxt(lable_file, or_labels.astype(np.int).reshape(-1, 1), header="3d_labels", fmt='%d')
    lable_file.close()
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X_3d, labels))

    ################################################################
    # plot
    fig = plt.figure(figsize=(10,10))
    ax = fig.gca(projection='3d')
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    markers = ['x', '+', '*', 'o', 4, 5, 6, 7, 's', 'd']
    mark = 'o'
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
            mark = 'x'

        class_member_mask = (labels == k)



        xy = X_3d[class_member_mask & core_samples_mask]
        ax.scatter(xy[:, 0], xy[:, 1], xy[:,2], c=col,s=14,marker=mark)

        xy = X_3d[class_member_mask & ~core_samples_mask]
        ax.scatter(xy[:, 0], xy[:, 1], xy[:,2],s=8, c=col, marker=mark)

        fig_c_path = target_dir + "3d_cluster_%d.png" % k
        plt.savefig(fig_c_path)

    ax.set_xlim(xmax=10)
    ax.set_ylim(ymin=1)
    ax.set_zlim(zmax=6)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    fig_path = target_dir + "3d_total.png"
    plt.savefig(fig_path)


    plt.show()
    plt.close()
    ###################
    #    3D data finished
    #################################################

    ##################
    # 2D data
    label_path = target_dir + "2d.csv"
    lable_file = open(label_path, 'w')

    if target == 'app':
        eps = 0.03
        min_samples = 10
    elif target == 'device':
        eps = 0.1
        min_samples = 10
    elif target == 'ip':
        eps = 0.35
        min_samples = 10
    else:
        exit()

    db_2d = DBSCAN(eps=eps,min_samples=min_samples).fit(X_2d)
    core_samples_mask = np.zeros_like(db_2d.labels_,dtype=bool)
    core_samples_mask[db_2d.core_sample_indices_] = True
    labels = db_2d.labels_
    or_labels = np.zeros([data.shape[0],1])
    j = 0
    for i in range(np.shape(data_mask)[0]):
        if data_mask[i] == True:
            or_labels[i] = labels[j]
            j = j + 1
        else:
            or_labels[i] = -2
    np.savetxt(lable_file, or_labels.astype(np.int).reshape(-1, 1), header="2d_labels", fmt='%d')
    lable_file.close()
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X_2d, labels))

    ################################################################
    # plot
    fig = plt.figure(figsize=(10,10))
    ax = fig.gca()
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    markers = ['x', 'o', '*', '+', 4, 5, 6, 7, 's', 'd']
    mark = 'o'
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
            mark = 'x'

        class_member_mask = (labels == k)



        xy = X_2d[class_member_mask & core_samples_mask]
        ax.scatter(xy[:, 0], xy[:, 1], c=col,s=14,marker=mark)

        xy = X_2d[class_member_mask & ~core_samples_mask]
        ax.scatter(xy[:, 0], xy[:, 1], s=8, c=col, marker=mark)

        fig_c_path = target_dir + "2d_cluster_%d.png" % k
        plt.savefig(fig_c_path)

    ax.set_xlim(xmin=0)
    ax.set_ylim(ymin=0)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    fig_path = target_dir + "2d_total.png"
    plt.savefig(fig_path)


    plt.show()
    plt.close()



def graph_test():
    #####
    # read data

    file_path = "D:/backup/data_1/ip.csv"
    data_file = open(file_path, 'rb')
    data = np.loadtxt(data_file, delimiter=',', skiprows=1, usecols=(1, 2, 3))

    #####
    # normalized data
    # print data.shape
    X = normalized(data)

    inertias = np.zeros(9)

    for n in range(2, 11):

        fig_path = "D:/backup/data_1/d_Kmeans_3d_%d.png" % n
        fig_b_path = "D:/backup/data_1/d_Kmeans_3d_%d_b.png" % n
        fig_in_path = "D:/backup/data_1/d_Kmeans_3d_in.png"
        # fig_file = open(fig_path,'w')
        # fig_b_file = open(fig_b_path,'w')

        est = KMeans(n_clusters=n).fit(X)
        label = est.labels_
        inertias[n - 2] = est.inertia_

        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca(projection='3d')

        shape = ['o', '+', '*', 'x', 4, 5, 6, 7, 's', 'd']
        unique_labels = set(label)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            class_mem_mask = (label == k)
            xy = X[class_mem_mask]
            ax.scatter(xy[:, 0], xy[:, 1], c='k', marker=shape[k])

        ax.set_xlabel('times')
        ax.set_ylabel('app_num')
        ax.set_zlabel('ip_num')
        # plt.show()
        plt.savefig(fig_path)

        ax.set_xlim3d(0.0, 0.2)
        ax.set_ylim3d(0.1, 0.6)
        ax.set_zlim3d(0.0, 0.2)

        # plt.show()

        plt.savefig(fig_b_path)

    plt.clf()
    plt.cla()
    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    clu_num = range(2, 11)
    ax.plot(clu_num, inertias, c='k')
    ax.scatter(clu_num, inertias, s=10, c='k')
    plt.savefig(fig_in_path)


def main():
    for i in range(1, 12):
        K_means(i, 'app')
        K_means(i, 'device')
        K_means(i, 'ip')


if __name__ == '__main__':
    # K_means(1,'device')
    # graph_test()
    fDBSCAN(7,'ip')
