#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 列表测试
# 列表长度是动态的,可任意添加删除元素.
# 用索引可以很方便访问元素,甚至返回一个子列表
# 更多方法请参考Python的文档

word = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
a = word[2]
print('a is : ' + a)
b = word[1:3]

# # end=''作为print()的一个参数，会使该函数关闭“在输出中自动包含换行”的默认行为
# print('b is : ', end='')
# print(b)
# c = word[:2]
# print("c is: ", end='')
# print(c)
# d = word[1:]
# print("d is: ", end='')
# print(d)

# 列表可以合并
e = word[:2] + word[2:]
print("列表可以合并 e = word[:2] + word[2:] is:", e)

# The last elements of word.
f = word[-1]
print("word[-1] is:", f)

# The last two elements.
h = word[-2:]
print("word[-2:] is:", h)

# Everything except the last two characters
i = word[:-2]
print("Everything except the last two characters word[:-2] ->", i)

length = len(word)
print("Length of word is: " + str(length))
print("Adds new element 'h'")
word.append('h')
print(word)

# 删除元素
print("删除元素 [0]")
del word[0]
print(word)
print("删除元素 [1:3]")
del word[1:3]
print(word)
