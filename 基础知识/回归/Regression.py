#!/usr/bin/python
# coding:utf-8
from numpy import *
n

def loadDataSet(filename):
    fr = open(filename)
    numFeature = len(fr.readline().split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        ## 这里本来打算直接切片后添加到dataMat中，后来想想觉得float强制类型
        ## 转换还是不能丢
        lineArr= []
        for i in range(numFeature):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


def standRegres(xArr, yArr):
    xMat = mat(xArr)
    yMat = mat(yArr)
    xTx = xMat.T * xMat
    """
    原作者在这对xTx是否是奇异阵进行了，判断，这里处于
    对计算稳定的要求，改为计算伪逆
    """
    ws = linalg.pinv(xTx) * (xMat.T * yMat)
    return ws

## 下面是局部加权线性回归
## 实际用应该是均匀取点，使用时类似样条函数，
## 但从效果来过，应该可以用来作为数据清理，将整个数据变得更平滑
def lwlr(testPoint, xArr, yArr, k=1.0):
    xMat = mat(xArr)
    yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):
        diffMat = testPoint - xMat[j, :]
        weights[j, j] = exp(diffMat * diffMat.T/(-2.0 * k **2))
    xTx = xMat.T * (weights * xMat)
    ws = linalg.pinv(xTx) * (xMat.T * (weights * yMat))
    return testPoint * ws


def lwlrTest(testArr, xArr, yArr, k=1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i], xArr, yArr, k)
    return yHat


def ridgeRegres(xMat, yMat, lam=0.2):
    ## 手推时，为lam^2不是lam
    ## 很气，明天想想为什么
    xTx = xMat.T * xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    ws = linalg.pinv(denom) * (xMat.T * yMat)
    return ws


## 前向逐步回归
def stageWise(xArr, yArr, eps=0.01, numIt=100):
    xMat = mat(xArr)
    yMat = mat(yArr)
    yMean = mean(yMat, 0)
    yMat = yMat - yMean
    xMean = mean(xMat, 0)
    xVar = var(xMat, 0)
    xMat = (xMat - xMean) / xVar
    m, n = shape(xMat)
    ws = zeros((n, 1))
    wsTest = ws.copy()
    wsMax = ws.copy()
    for i in range(numIt):
        lowestError = inf
        for j in range(n):
            for sign in [-1, 1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMat * wsTest
                rssE = ((yTest - yMat)**2).sum()
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
    return ws
