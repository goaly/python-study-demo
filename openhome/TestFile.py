# 文件读写测试

fileName = 'D:/GitRepository/python/pythonStudy/file.txt'
# 追加写模式
f = open(fileName,'a+')
f.write('\nhello world!!!')
f.close()

f2 = open(fileName, 'r')
content = f2.read()
print(content)
f2.close()