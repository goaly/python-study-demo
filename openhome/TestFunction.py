# code:UTF-8
def change_number(number):
    hiding_num = number.replace(number[3:7], '*' * 4)
    print(hiding_num)


change_number('13207113160')
