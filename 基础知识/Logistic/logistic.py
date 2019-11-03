from numpy import *

def loadDataSet(filename):
    """
    从文件中加载数据，这里的数据就两个特征。
    :param filename:文件名
    :return:返回数据矩阵和标签矩阵
    """
    data = []
    labels = []
    fr = open(filename)
    for line in fr.readlines():
        temp = line.strip().split()
        if len(temp) == 1:
            continue
        data.append([float(temp[0]), float(temp[1])])
        labels.append([int(temp[-1])])
    return data, labels


def sigmod(inX):
    ## 这里是tanh（滑稽）
    return 2 * 1.0/(1 + exp(-2*inX)) - 1


def gradAscent(dataMatIn, classLabels):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    m, n = dataMatrix.shape[0], dataMatrix.shape[1]
    alpha = 0.001
    maxCycles = 500
    weight = ones((n, 1))
    for k in range(maxCycles):
        h = sigmod(dataMatrix * weight)
        error = labelMat - h
        weight = weight + alpha * dataMatrix.transpose() * error
        ## 这里的推导过程为求导取0，原代码所在网站没有仔细提。简化说明
        ## 就是先写出是和否的概率表达，然后写成似然函数，最后求导。
    return array(weight)


## 随机梯度下降
## 思路很简单，从样本里选取一个例子来进行权重更新
def stocGradAscent(dataMatrix, classLabels):
    m, n = dataMatrix.shape[0], dataMatrix.shape[1]
    weight = ones((n, 1))
    alpha = 0.001
    for k in range(m):
        h = sigmod(sum(dataMatrix[i] * weight))
        error = classLabels[i] - h
        weight = weight + alpha * error * dataMatrix[i]
    return weight

## 随机梯度下降（随机版）
def stocGradAscent1(dataMatrix, classLabels, numIter=150):
    m, n = dataMatrix.shape[0], dataMatrix.shape[1]
    weight = ones((n, 1))
    for k in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0 + k + i)
            randIndex = random.randint(0, len(dataIndex) -1)
            h = sigmod(sum(dataMatrix[randIndex] * weight))
            error = classLabels[randIndex] - h
            weight = weight + alpha * error * dataMatrix[randIndex]
            del (dataIndex[randIndex])
    return weight



