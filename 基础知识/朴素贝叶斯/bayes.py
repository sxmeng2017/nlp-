from numpy import *

def loadDataSet():
    """
    创建数据集
    :return: 单词列表postingList, 所属类别classVec
    """
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'], #[0,0,1,1,1......]
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec

def createVocabList(dataSet):
    """
    制作词汇表
    :param dataSet:分类使用的数据集
    :return: 返回数据集中使用的全部单词
    """
    vocabSet = set([])
    for doucument in dataSet:
        vocabSet = vocabSet | set(doucument)
    return list(vocabSet)

def word2vec(vocabList, words):
    """
    将输入的words句子，根据给出的单词词汇，转换为词向量
    :param vocabList: 单词词汇表
    :param words:句子
    :return:词向量
    """
    vect = [0 for i in range(len(vocabList))]
    for word in words:
        if word in vocabList:
            vect[vocabList.index(word)] = 1
    return vect

def train(trainMatrix, trainCategory):
    """
    使用已经转换完毕的词矩阵，和预先给出的分类结果，训练分类模型
    :param trainMatrix: 词矩阵
    :param trainCategory: 分类
    :return: 不是垃圾话的条件概率，垃圾话的条件概率，整体分类中垃圾话的概率。
    """
    num_samples = len(trainMatrix)
    num_words = len(trainMatrix[0])
    p_abuse = sum(trainCategory)/num_samples
    p0num = ones(num_words)
    p1num = ones(num_words)

    p0stat = 2.0
    p1stat = 2.0

    for i in range(num_samples):
        if trainCategory[i] == 1:
            p1num += trainMatrix[i]
            p1stat += sum(trainMatrix[i])
        else:
            p0num += trainMatrix[i]
            p0stat += sum(trainMatrix[i])
    p1prob = log(p1num / p1stat)
    p0prob = log(p0num/ p0stat)
    return p0prob, p1prob, p_abuse


def classifyNB(vecClassify, p0Vect, p1Vect, pClass1):
    """
    将需要分类的句子转换为词向量后，使用训练好的条件概率结果进行分类
    :param vecClassify: 词向量
    :param p0Vect: 不是垃圾话的条件概率向量
    :param p1Vect: 是垃圾话的条件概率向量
    :param pClass1: 垃圾话的概率
    :return: 分类结果
    """
    p1 = sum(vecClassify * p1Vect) + log(pClass1)
    p0 = sum(vecClassify * p0Vect) + log(1 - pClass1)
    if p0 > p1:
        return 0
    else:
        return 1

