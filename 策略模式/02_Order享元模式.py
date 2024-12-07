"""
对Order的折扣策略的实现进行改进。

改进原因：
1.从上一个Order策略模型.py中可以看到，每个策略都是一个类，且只有一个discount函数。
这看起来就像普通的函数，的确，直接用函数也可以实现策略，而且由于函数比类轻量，能够使用更少的代码实现相同的功能。
2.另外，对于场景：多个order对象计算促销策略时，使用同一种促销策略，也会创建多个同种策略的类实例。
因此，如果我们把策略类转换为独立与类的公共函数实现，就可以大大减少这种消耗。
3.应用策略也更简单了，Order类不需要通类对象再调用其方法来计算策略，只需直接调用策略方法即可；同样的Order实例要应用策略，直接将策略函数作为参数即可。


--------
这种设计模式叫做 享元模式。
策略函数在此叫做 "享元"，即 可共享的对象，可以同时在多个上下文中使用。

"""

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')  # 顾客信息，包括顾客姓名、积分。用具名元素实现。不可修改。


class LineItem:
    """
    LineItem翻译过来就是行款项，意为包含项目、单价、数量、总价的一行记录。
    在这个例子中可以理解为一项商品及其购买信息。
    """

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.quantity * self.price


# 上下文
class Order:
    """
    订单类。
    每个订单的元素有：
    【顾客】（具名元组：包括<顾客姓名>、<顾客积分>两个参数，每个订单对应一个顾客信息）、
    【购物车】（列表结构，包括 该订单上 所有商品的LineItem实例）、
    【促销方式】（在当前订单上所要实施的促销策略）
    每个订单需要有一个计算原价总价的函数 和 一个计算促销后总价格的函数。
    """

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer  # 顾客信息。是包括顾客、积分的具名元组。
        self.cart = cart  # 购物车。是LineItem集合的List。
        self.promotion = promotion  # 促销方式

    def total(self):  # 计算购物车内商品的原价总额
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):  # 计算应付费用
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        """修改了类默认描述"""
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


# 独立的策略函数们：
def FidelityPromo(order):
    """策略1：为积分1000以上的顾客提供5%折扣"""
    if order.customer.fidelity >= 1000:
        return order.total() * 0.05
    else:
        return 0


def BulkItemPromo(order):
    """策略2：单个商品为20个或以上时，为该商品提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity > 20:
            discount += item.total() * 0.1
    return discount


def LargeOrderPromo(order):
    """策略3： 订单中的不同商品的种类数量达到10个或以上时提供7%具体折扣"""
    # 使用集合筛选不重复的项
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * 0.07
    else:
        return 0


if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, 0.05), LineItem('apple', 5, 1.5), LineItem('watermellon', 5, 5.0)]
    print(Order(joe, cart, FidelityPromo))
    print(Order(joe, cart, FidelityPromo))
    print(Order(ann, cart, FidelityPromo))
    banana_cart = [LineItem('banbana', 30, 0.5), LineItem('apple', 10, 1.5)]
    print(Order(joe, banana_cart, BulkItemPromo))
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, long_order, LargeOrderPromo))
    print(Order(joe, cart, LargeOrderPromo))
