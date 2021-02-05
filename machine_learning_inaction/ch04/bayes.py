# 《机器学习实战》
# 朴素贝叶斯
# --------------------------------
# ---------- 2021.1.15 ----------
# --------------------------------
from numpy import *


# 词表到向量的转换函数
def loadDataSet():
    # 切分的词条
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    # 1 代表侮辱性文字、0代表正常言论
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


# 创建一个包含在所有文档中出现的不重复词的列表
# ['my', 'flea', 'posting', 'dog', 'has', 'dalmation', 'not',
# 'problems', 'steak', 'stupid', 'I', 'help', 'buying', 'licks',
# 'him', 'so', 'garbage', 'how', 'to', 'park', 'quit', 'maybe',
# 'take', 'worthless','cute', 'is', 'food', 'ate', 'love', 'please', 'mr', 'stop']
def createVocabList(dataSet):
    vocabSet = set([])  # 创建一个空集
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # 创建两个集合的并集
    return list(vocabSet)


# 检查词汇表中的单词在输入文档中是否出现
# 朴素贝叶斯词集模型
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)  # 创建一个其中所含元素都为0的元素
    for word in inputSet:  # 遍历每个词条
        if word in vocabList:  # 如果词条存在于词汇表中，则置1
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec  # 返回文档向量


# 朴素贝叶斯分类器训练函数
def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)  # 计算训练的文档数目
    numWords = len(trainMatrix[0])  # 计算每篇文档的词条数
    # 1是侮辱类 0是非侮辱类
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 文档属于侮辱类的概率

    # 词条出现数初始化
    # p0Num = zeros(numWords)
    p0Num = ones(numWords)
    # p1Num = zeros(numWords)
    p1Num = ones(numWords)

    # 分母初始化
    # p0Denom = 0.0
    p0Denom = 2.0
    # p1Denom = 0.0
    p1Denom = 2.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:  # 统计属于侮辱类的条件概率，即P(w0|1)、P(w1|1)、P(w2|1)...
            p1Num += trainMatrix[i]  # 将统计所有侮辱类每个单词出现个数
            p1Denom += sum(trainMatrix[i])  # 所有侮辱类文档中所有单词出现个数
        else:  # 统计属于非侮辱类的条件概率，即P(w0|0)、P(w1|0)、P(w2|0)...
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # 对每个元素做除法
    # 这里使用log是因为用python乘许多很小的数，最终四舍五入等于0
    # p1Vect = p1Num / p1Denom
    p1Vect = log(p1Num / p1Denom)  # 所有侮辱类文档中每个单词出现概率即P(wi|1)
    # p0Vect = p0Num / p0Denom
    p0Vect = log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive


# 朴素贝叶斯公式计算
# 这里假设所有词都是互相独立的，P(ci|wi)=P(wi|ci)P(ci)
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)  # 元素相乘
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


# 朴素贝叶斯分类函数
def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))

    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))


# 朴素贝叶斯词袋模型
def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec


if __name__ == '__main__':
    # listOPosts, listClasses = loadDataSet()
    # myVocalList = createVocabList(listOPosts)
    # print(myVocalList)
    # for postinDoc in listOPosts:
    #     print(postinDoc)
    #     print(setOfWords2Vec(myVocalList, postinDoc))

    # trainMat = []
    # for postinDoc in listOPosts:
    #     trainMat.append(setOfWords2Vec(myVocalList, postinDoc))
    # p0V, p1V, pAb = trainNB0(trainMat, listClasses)
    # print(pAb)  # 文档属于侮辱类的概率P(c1)
    # print(p0V)  # 所有侮辱类文档中每个单词出现的概率，即P(wi|c1)
    # print(p1V)  # 所有非侮辱类文档中每个单词出现的概率P，即(wi|c0)

    testingNB()
