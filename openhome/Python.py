def get_num(n):
    print("执行程序")
    i = 0
    while i < n:
        m = yield i
        print("m = ", m)
        i += 1


a = get_num(3)
print(next(a))
print(a.send("yield测试"))
print(a.__next__())
