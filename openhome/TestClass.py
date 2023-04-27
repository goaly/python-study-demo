# 定义类
class Bike:
    compose = ['frame', 'wheel', 'pedal']

    def __init__(self):
        """默认的初始化方法"""
        self.other = 'seat'

    def use(self, distance):
        print('you ride {}m'.format(distance))


# 类的继承


class ShareBike(Bike):
    """共享单车"""
    price = 1.2

    def cost(self, hour):
        print('you ride {} hours, need ${}'.format(hour, self.price * hour))


my_bike = Bike()
you_bike = Bike()

my_bike.other = 'basket'
print(my_bike.compose)
print(my_bike.other)

print(you_bike.compose)
print(you_bike.other)

my_bike.use(100)

share_bike1 = ShareBike()
print(share_bike1.compose)
share_bike1.cost(2)
