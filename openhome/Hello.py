# code:UTF-8

name = input('名称：')

if __name__ == '__main__':
    # 单独运行时，才执行以下代码
    print('Hello!', name, '!')

    # strip方法去除字符串两侧的空格
    a = '!***python *is *good**!*@*!'
    print(a.strip('*!'))

print('__name__:',__name__)

