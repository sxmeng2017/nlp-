from __future__ import print_function
from math import *


"""
一样，看完原理，默代码。学习的代码作者使用递归而不是循环很有意思。
"""

def createDateSet():
    """DateSet 基础数据集
        Args:
            无需传入参数
        Returns:
            返回数据集和对应的label标签
        """
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    # dataSet = [['yes'],
    #         ['yes'],
    #         ['no'],
    #         ['no'],
    #         ['no']]
    # labels  露出水面   脚蹼
    labels = ['no surfacing', 'flippers']
    # change to discrete values
    return dataSet, labels


def calcShannonEnt(dataSet):
    """
    该函数用于计算一个数据集中香农熵
    :param dataSet: 数据集
    :return: 熵
    """
    numbers = len(dataSet)
    labelCounter = {}
    for item in dataSet:
        label = item[-1]
        labelCounter[label] = labelCounter.get(label, 0) + 1
    """
    计算每个label的数目，用于计算比例
    """
    shannon = 0.0
    for key in labelCounter:
        prob = float(labelCounter[key])/numbers
        shannon -= prob * log(prob, 2)
    return shannon


def splitDataSet(dataSet, index, value):
    """
    将数据集用指定特征值的value值进行划分
    :param dataSet: 数据集
    :param index: 特征值在单组数据中的位置
    :param value: 划分使用的特征的值
    :return: 指定特征为指定值的数据组
    """
    retData = []
    for item in dataSet:
        if item[index] == value:
            res = item[:index] + item[index+1:]
            ## 这里要把指定特征从数据中去除，因为后续划分已经知道了该信息
            ## 同时后续操作会删去该特征，避免出错
            retData.append(res)
    return retData


def chooseBestFeatureTosplit(dataSet):
    """
    寻找最佳的划分特征
    :param dataSet:数据集
    :return: 最佳的划分特征
    """
    numFeature = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestGain, beatFeature = 0.0, -1
    for i in range(numFeature):
        featureValue = [item[i] for item in dataSet]
        uniqueValue = set(featureValue)
        newEntropy = 0.0
        for value in uniqueValue:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = float(len(subDataSet))/len(dataSet)
            newEntropy += prob * calcShannonEnt(subDataSet)
        gain = baseEntropy - newEntropy
        if gain > bestGain:
            bestGain = gain
            beatFeature = i
    return beatFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    # 倒叙排列classCount得到一个字典集合，然后取出第一个就是结果（yes/no），即出现次数最多的结果
    sortedClassCount = sorted(classCount.items(), key=lambda x:x[1], reverse=True)
    # print 'sortedClassCount:', sortedClassCount
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)

    bestFeature = chooseBestFeatureTosplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    Tree = {bestFeatureLabel:{}}
    del labels[bestFeature]
    featureValue = [item[bestFeature] for item in dataSet]
    uniqueValue = set(featureValue)
    for value in uniqueValue:
        subLabels = labels
        Tree[bestFeatureLabel][value] = createTree(splitDataSet(dataSet, bestFeature, value), subLabels)
    return Tree








