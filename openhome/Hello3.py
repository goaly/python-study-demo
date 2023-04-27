from sys import argv

# 需要在运行时加入一个参数，如：python hello3.py tom
# 通过sys模块argv列表获取命令行参数，sys.arg[0]保存的是源码文件名，命令行参数从sys.arg[1]开始引用
print('哈啰！', argv[1], '!')
