class HauntedBus:
    """
    以此为例，说明 函数参数的默认值为可变对象的危险之处。
    """

    def __init__(self, passengers=[]):  # 设置 passengers 的默认参数为[]
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


if __name__ == '__main__':
    bus1 = HauntedBus(['Alice', 'Nick', 'James'])
    print('bus1_initial: ' + str(bus1.passengers))
    bus2 = HauntedBus()
    print('bus2_initial: ' + str(bus2.passengers))
    print('bus1_(after initiate bus2): ' + str(bus1.passengers))  # bus1不受影响
    bus2.pick('Rose')
    print('bus2_(after pick Rose): ' + str(bus2.passengers))
    print('bus1_(after pick Rose): ' + str(bus1.passengers))
    bus3 = HauntedBus()
    print('bus3_initial: ' + str(bus3.passengers))  # bus3初始化就带了bus2的Rose
    print('bus1_(after initiate bus3): ' + str(bus1.passengers))  # bus1不受影响
    print('bus2_(after initiate bus3): ' + str(bus2.passengers))
    bus3.pick('John')
    print('bus3_(after pick John): ' + str(bus3.passengers))
    print('bus1_(after pick John): ' + str(bus1.passengers))  # bus1不受影响
    print('bus2_(after pick John): ' + str(bus2.passengers))  # bus2也被新增了John


