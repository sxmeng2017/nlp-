from __future__ import print_function
from numpy import *
import operator
from os import listdir
from collections import Counter

"""
完成knn算法
"""

def createDataSet():
    """
    创建数据集和标签
     调用方式
     import kNN
     group, labels = kNN.createDataSet()
    """
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify(inx, dataSet, labels, k):
    """

    :param inx: 需要分类的数据
    :param dataSet: 分类号的数据集合
    :param labels: 数据集中数据的分类
    :param k: 选择的最近邻居数目
    :return: inx对应的类别
    """
    ## 计算inx到各个点的距离
    dataSize = dataSet.shape[0]
    delta_ = tile(inx, (dataSize, 1)) - dataSet
    distance = delta_ ** 2
    distance = (distance.sum(axis=1)) ** 0.5
    sorted_dis_index = distance.argsort()

    ## 找出距离最小的k个点,记录其类别
    Count = {}
    for i in range(k):
        label = labels[sorted_dis_index[i]]
        Count[label] = Count.get(label, 0) + 1

    ## 返回数量最多的类别
    maxCount = max(Count, key=Count.get)
    return maxCount

"""
以下为数据处理用函数
"""
# -------------------------------------------------------------------
def file2matrix(filename):
    """
    将文件数据读取出来，注意该文件必须用/t作为分隔符
    :param filename:
    :return:
    """
    fr = open(filename)
    temp = fr.readlines()
    number_of_lines = len(temp)
    number_of_columns = len(temp[0].strip().split('\t')) - 1
    Matrix = zeros((number_of_lines, number_of_columns))
    class_labels = []
    index = 0
    fr = open(filename)
    for line in fr.readlines():
        line = line.strip()
        list_form = line.split("\t")
        Matrix[index, :] = list_form[:3]
        class_labels.append(int(list_form[-1]))
        index += 1

    return Matrix, class_labels

def autoNorm(dataSet):
    """
    这里的归一化使用最大-最小值归一化
    :param dataSet:数据集
    :return:返回归一化的数据集
    """
    min_val = dataSet.min(axis=0)
    max_val = dataSet.max(axis=0)

    ranges = max_val - min_val
    dataSet_size = dataSet.shape[0]
    norm_date_set = zeros(shape(dataSet))
    norm_date_set = dataSet - tile(min_val, (dataSet_size, 1))
    norm_date_set = norm_date_set / ranges

    return norm_date_set

def img2vector(filename):
    """
    将图片转换为向量
    :param filename:
    :return:
    """
    IMG_FLATTEN_SIZE = 1024
    return_vect = zeros((1, IMG_FLATTEN_SIZE))
    fr = open(filename)
    length = int(IMG_FLATTEN_SIZE ** 0.5)
    for i in range(length):
        line = fr.readline()
        for j in range(length):
            return_vect[0, 32 * i + j] = int(line[j])
    return return_vect




