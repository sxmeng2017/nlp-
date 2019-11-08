"""
我原以为树回归，是不同特征有不同回归，作者给出的方式更直接。
不同的特征有不同的均值，最后结果会分类结果的均值。这相当于聚类

作者剪枝部分的代码用来归并排序的思想很厉害。
"""

from numpy import *


def loadDataSet(filename):
    """
    加载数据，数据文件中数据以tab键作为分隔符。然后将每行的内容保存为
    一组浮点数。
    :param filename: 数据文件
    :return: 提取的数据，类型为list。
    """
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat


def binSplitDataSet(dataSet, feature, value):
    """
    给定数据集，分割特征，分割特征的值，依据分割特证，对特征的值进行划分，界线为value
    :param dataSet: 数据集
    :param feature: 用于分割的特征
    :param value: 分割特征用来分割的值
    :return: 分割后的两个数据集
    """
    mat0 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0, mat1

# 返回叶节点的均值
def regLeaf(dataSet):
    return mean(dataSet[:, -1])

# 作者的理解是求一组数据的方差，通过决策树进行划分，可以让差距大数据分到同一类
# 我的理解是划分度量是误差的平方和，而var是平方和的总数分之一。所以要乘总量。
# 这个划分标准会使划分不仅往平方和小的划分方式走，还会尝试将样本划分的更细，这样可以避免
# 出现大量方差小的一组数据，由于结果是返回均值，而对于较大的定义域中的结果返回同一个值。
def regErr(dataSet):
    return var(dataSet[:, -1]) * shape(dataSet)[0]

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    """
    寻找切分数据集的最佳方式和生成叶子节点
    :param dataSet: 数据集
    :param leafType: 叶子节点类型，建立叶子节点的函数
    :param errType: 误差计算函数
    :param ops: 【容许误差下降值， 切分的最少样本数】
    :return: bestIndex 最佳切分feature的index坐标
             bestValue 切分的最优值
    """
    tolS = ops[0]
    tolN = ops[1]

    if len(set(dataSet[:, -1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)
    m, n = shape(dataSet)
    S = errType(dataSet)
    bestS, bestIndex, bestValue = inf, 0, 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:, featIndex].T.toindex()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
                continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                beatValue = splitVal
                beatS = newS
    if S - beatS < tolS:
        return None, leafType(dataSet)
    if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
        return None, leafType(dataSet)
    return bestIndex, beatValue

#这课树的叶子节点具有right和left两半，到了最后的叶子节点，其只有right和left，无spInd，spVal
# left和righ中的数据大小不一定相等
def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
    if feat is None:
        return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree

# 判断是否是字典（叶子节点）
def isTree(obj):
    return (type(obj).__name__=='dict')

# 这个方法的成立是由叶子节点必然有left和right两个项来保证的
# 但left和right的大小不一定相等，所以这里的均值只是近似
# 这里的剪枝为从底向下剪
def getMean(tree):
    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2.0

def prune(tree, testData):
    if shape(testData)[0] == 0:
        return getMean(tree)
    if isTree(tree['right']) or isTree(tree['left']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    # 如果是左边分枝是字典，就传入左边的数据集和左边的分枝，进行递归
    if isTree(tree['left']):
        tree['left'] = prune(tree['left'], lSet)
    # 如果是右边分枝是字典，就传入左边的数据集和左边的分枝，进行递归
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rSet)

    ## 上一步将整个数据拆到最小组成，后面开始整合，这个过程相当于归并排序的思想
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])

    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        errorNoMerge = sum(power(lSet[:, -1] - tree['left'], 2)) + sum(power(rSet[:, -1] - tree['right'], 2))
        treeMean = (tree['left'] + tree['right'])/2.0
        errorMerge = sum(power(testData[:, -1] - treeMean, 2))
        if errorMerge < errorNoMerge:
            print("merging")
            return treeMean
        else:
            return tree
    else:
        return tree


def modelLeaf(dataSet):
    ws, X, Y = linearSolve(dataSet)

def modelErr(dataSet):
    ws, X, Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat, 2))

def linearSolve(dataSet):
    m, n = shape(dataSet)
    X = mat(ones((m, n)))
    Y = mat(ones((m, n)))
    X[:, 1: n] = dataSet[:, 0: n-1]
    Y = dataSet[:, -1]

    xTx = X.T * X
    ws = linalg.pinv(xTx) *(X.T * Y)
    return ws, X, Y




