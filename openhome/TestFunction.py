# code:UTF-8
# 测试函数定义
def change_number(number):
    hiding_num = number.replace(number[3:7], '*' * 4)
    return hiding_num


print(change_number('13207113160'))
