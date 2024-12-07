"""
基于已实现的策略模式，找出最佳的策略的 另一种思路：
在一个单独的模块中保存所有的策略函数，把best_promo排除在外，然后对Order实例，使用内省单独的promotions模块，构建promos列表。
这里使用到了inspect模块。
inspect模块：用来收集对象的信息

什么是内省模块？

"""
import inspect
from collections import namedtuple
from 策略模式 import promotions

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


# 寻找最佳策略的方法-构建promos列表的方法三：
promos = [func for name, func in inspect.getmembers(promotions, inspect.isfunction)]


# 与 promos 结合，比较并返回最佳策略
def best_promo(order):
    return max(promo(order) for promo in promos)


if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, 0.05), LineItem('apple', 5, 1.5), LineItem('watermellon', 5, 5.0)]
    print(Order(joe, cart, best_promo))
    print(Order(joe, cart, best_promo))
    print(Order(ann, cart, best_promo))
    banana_cart = [LineItem('banbana', 30, 0.5), LineItem('apple', 10, 1.5)]
    print(Order(joe, banana_cart, best_promo))
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, long_order, best_promo))
    print(Order(joe, cart, best_promo))
