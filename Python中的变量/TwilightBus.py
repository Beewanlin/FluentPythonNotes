class TwilightBus:
    """
    以此为例，说明 可变对象作为函数参数的危险之处（即使该参数默认值设置为了None，能够解决HauntedBus的问题，但还有新的问题）
    要避免直接将可变对象参数赋值给实例变量。
    """
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            """
            self.passengers = passengers会有问题。
            因为参数 basketball_team 是可变对象，直接赋值给变量 self.passengers，会导致后面修改self.passengers变量时，也会修改到 basketball_team。 
            因此需要注意，复制作为参数的可变对象为新对象，用新对象这个副本再赋值给self.passengers变量。这样就不会影响到传入的参数其本身了。
            """
            # self.passengers = passengers
            self.passengers = passengers[:]   # 复制列表对象，可以操作为 list(待复制对象)、待复制对象[:]、copy.copy(待复制对象)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


if __name__ == '__main__':
    basketball_team = ['Sue', 'Tina', 'Maya', 'Diana',  'Pat']
    print('篮球队的队员们有：' + str(basketball_team))
    bus = TwilightBus(basketball_team)
    print('篮球队的队员们上公交车了。\n公交车上的乘客有：' + str(bus.passengers))
    bus.drop('Tina')
    print('Tina 下车了')
    print('公交车上的乘客有：' + str(bus.passengers))
    print('篮球队的队员们有：' + str(basketball_team))
    bus.drop('Pat')
    print('Pat 下车了')
    print('公交车上的乘客有：' + str(bus.passengers))
    print('篮球队的队员们有：' + str(basketball_team))