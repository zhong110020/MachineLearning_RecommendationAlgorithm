# -*- coding:utf-8 -*-
import numpy as np
from random import normalvariate    #正态分布
from sklearn.preprocessing import MinMaxScaler as MM    #可将特征缩放到给定的最小值和最大值之间
import pandas as pd

data_train = pd.read_csv('diabetes_train.txt', header=None)
data_test = pd.read_csv('diabetes_test.txt', header=None)

# 数据处理
def preprocessing(data_input):
    standardopt = MM()
    data_input.iloc[:, -1].replace(0, -1, inplace=True) #把数据集中的0转为-1
    feature = data_input.iloc[:, :-1]                   #除了最后一列之外，其余均为特征
    feature = standardopt.fit_transform(feature)        #将特征转换为0与1之间的数
    feature = np.mat(feature)                  #传回来的是array，如果要dataframe那用dataframe
    label = np.array(data_input.iloc[:, -1])    #最后一列是标签，表示有无糖尿病。1:有, 0:无
    return feature, label     #返回特征，标签

# 分类器
def sigmoid(x): #定义sigmoid函数
    return 1.0/(1.0 + np.exp(-x))

# 模型训练
def sgd_fm(datamatrix, label, k, iter, alpha):
    '''
    k：分解矩阵的长度
    datamatrix：数据集特征
    label：数据集标签
    iter:迭代次数
    alpha:学习率
    '''
    m, n = np.shape(datamatrix) #m:数据集特征的行数，n:数据集特征的列数
    w0 = 0.0 #初始化w0为0
    w = np.zeros((n, 1)) #初始化w
    v = normalvariate(0, 0.2) * np.ones((n, k))
    for it in range(iter):
        for i in range(m):
            # inner1 = datamatrix[i] * w
            inner1 = datamatrix[i] * v #对应公式进行计算
            inner2 = np.multiply(datamatrix[i], datamatrix[i]) * np.multiply(v, v)
            jiaocha = np.sum((np.multiply(inner1, inner1) - inner2), axis=1) / 2.0
            ypredict = w0 + datamatrix[i] * w + jiaocha
            # print(np.shape(ypredict))
            # print(ypredict[0, 0])
            yp = sigmoid(label[i]*ypredict[0, 0])
            loss = 1 - (-(np.log(yp)))
            w0 = w0 - alpha * (yp - 1) * label[i] * 1
            for j in range(n):
                if datamatrix[i, j] != 0:
                    w[j] = w[j] - alpha * (yp - 1) * label[i] * datamatrix[i, j]
                    for k in range(k):
                        v[j, k] = v[j, k] - alpha * ((yp - 1) * label[i] * \
                                  (datamatrix[i, j] * inner1[0, k] - v[j, k] * \
                                  datamatrix[i, j] * datamatrix[i, j]))
        print('第%s次训练的误差为：%f' % (it, loss))
    return w0, w, v

# 预测
def predict(w0, w, v, x, thold):
    inner1 = x * v
    inner2 = np.multiply(x, x) * np.multiply(v, v)
    jiaocha = np.sum((np.multiply(inner1, inner1) - inner2), axis=1) / 2.0
    ypredict = w0 + x * w + jiaocha
    y0 = sigmoid(ypredict[0,0])
    if y0 > thold:
        yp = 1
    else:
        yp = -1
    return yp

# 评估
def calaccuracy(datamatrix, label, w0, w, v, thold):
    error = 0
    for i in range(np.shape(datamatrix)[0]):
        yp = predict(w0, w, v, datamatrix[i], thold)
        if yp != label[i]:
            error += 1
    accuray = 1.0 - error/np.shape(datamatrix)[0]
    return accuray

datamattrain, labeltrain = preprocessing(data_train) #将训练集进行预处理，datamattrain存放训练集特征，labeltrain存放训练集标签
datamattest, labeltest = preprocessing(data_test)#将测试集进行预处理，datamattest存放训练集特征，labeltest存放训练集标签
w0, w, v = sgd_fm(datamattrain, labeltrain, 20, 500, 0.01)#分解矩阵的长度为20，迭代次数为300次，学习率为0.01
maxaccuracy = 0.0
tmpthold = 0.0
for i in np.linspace(0.4, 0.6, 201):
    #print(i)
    accuracy_test = calaccuracy(datamattest, labeltest, w0, w, v, i)
    if accuracy_test > maxaccuracy:
        maxaccuracy = accuracy_test
        tmpthold = i
print("准确率:",accuracy_test)