def getNum(n):
    print("执行程序")
    i = 0
    while i < n:
        m = yield i
        print("m = ", m)
        i += 1


a = getNum(5)
print(next(a))
print(a.send("yield测试"))
print(a.__next__())
print(a.__next__())
