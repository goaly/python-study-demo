# code:UTF-8

name = input('请输入名称：')

# 程序入口
if __name__ == '__main__':
    # 单独运行时，才执行以下代码
    print('Hello! ', name, '. Python is easy to learn, let\'s get started\n', sep='')

    print('示例1：打印程序入口 __name__:', __name__, '\n')

    # strip方法去除字符串两侧的空格
    a = '    !***python *is *good**!*@*!  '
    print('示例2：strip方法去除字符串两侧的空格 a:', a.strip(' '), '\n', sep='')

    # import wheel.pep425tags as w
    # print(w.get_supported(archive_root='C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python38'))

    l_tuple = [i for i in range(10)]
    print('示例3：通过 for in 生成集合 l_tuple:', l_tuple, '\n')

    print('示例4：通过将列表转换成集合，去除生重复的元素')
    brand_list = ['xiaomi', 'huawei', 'xiaomi']
    brand_set = set(brand_list)
    print('brand_list：', brand_list)
    print('brand_set：', brand_set, '\n')

