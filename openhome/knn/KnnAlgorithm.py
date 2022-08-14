#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


# In[2]:


class KneighborsClassifier(object):
    '''
        自定义KNN分类器
    '''
    
    def __init__(self, n_neighbors=5):
        '''设置超参数'''
        self.n_neighbors=n_neighbors
        
    def fit(self, X, y):
        '''
            模型的训练，KNN算法作为惰性算法，这里没有任何训练逻辑
        '''
        self.X = np.array(X)
        self.y = np.array(y)
    
    def predict(self, X):
        '''
            模型的预测
            1.找到k个最近的邻居
            2.统计这k个邻居的类别情况
            3.计算出出现次数最多的类别
        '''
        X = np.array(X)
        if X.ndim!=2:
            raise Exception("默认是批量预测，X的维度应该为2维...")
            
        result = []
        for x in X:
            # 求测试数据和样本之间的欧式距离
            dist = np.sqrt(((self.X-x)**2).sum(axis=1))
            # 排序取前5个最接近样本的索引
            args = np.argsort(dist)[:self.n_neighbors]
            # 根据索引取样本的标签
            labels = self.y[args]
            # 取出现次数最多的标签，添加到结果集
            result.append(max(set(labels), key=labels.tolist().count))
        return np.array(result)
            
            
        
    


# In[3]:


'''
    测试KNN分类器
'''
# 加载测试数据集（鸢尾花卉数据集）
X,y = load_iris(return_X_y=True)

# 样本数据 ，测试数据，样本标签，测试标签
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2)
# print(y_train)
# print(len(y_train))
# print(y_test)
# print(len(y_test))

#构建模型
knn = KneighborsClassifier(n_neighbors=5)

#模型训练
knn.fit(X=X_train,y=y_train)

#模型预测
y_pred = knn.predict(X=X_test)
print("预测结果: ", end='')
print(y_pred)
print("实际结果: ", end='')
print(y_test)
print("准确率: ", end='')
acc = (y_pred==y_test).mean()
print(acc)


# In[ ]:




