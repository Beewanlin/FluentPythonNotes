"""
实现Order类。

主要记录订单信息。
支持插入式折扣策略。需要建一个抽象基类，作为抽象策略；然后继承给子类用于实现其抽象方法以实现不同的具体策略。
"""
from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')  # 顾客信息，包括顾客姓名、积分。用具名元组实现。不可修改。


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
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        """修改了类默认描述"""
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC):
    """抽象基类。在该例中，表示待为实现的抽象策略"""

    @abstractmethod
    def discount(self, order):
        """返回折扣金额，抽象方法 待实现。"""


class FidelityPromo(Promotion):
    """策略1：为积分1000以上的顾客提供5%折扣"""

    def discount(self, order):
        if order.customer.fidelity >= 1000:
            return order.total() * 0.05
        else:
            return 0


class BulkItemPromo(Promotion):
    """策略2：单个商品为20个或以上时，为该商品提供10%折扣"""

    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity > 20:
                discount += item.total() * 0.1
        return discount


class LargeOrderPromo(Promotion):
    """策略3： 订单中的不同商品的种类数量达到10个或以上时提供7%具体折扣"""

    def discount(self, order):
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
    print(Order(joe, cart, FidelityPromo()))
    print(Order(joe, cart, FidelityPromo()))
    print(Order(ann, cart, FidelityPromo()))
    banana_cart = [LineItem('banbana', 30, 0.5), LineItem('apple', 10, 1.5)]
    print(Order(joe, banana_cart, BulkItemPromo()))
    long_order = [LineItem(str(item_code), 1, 1.0) for item_code in range(10)]
    print(Order(joe, long_order, LargeOrderPromo()))
    print(Order(joe, cart, LargeOrderPromo()))
