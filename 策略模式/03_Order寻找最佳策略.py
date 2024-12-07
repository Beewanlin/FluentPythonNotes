"""
基于已实现的策略模式，如果我们需要找出最佳的策略。该用什么方法呢？

基本思路：
创建一个寻找最佳策略的方法，先应用每个策略，再比较各个策略的计算结果，最后返回最佳策略。
    · 简单的方法：
      先新建一个记录所有策略方法的列表，手动添加策略方法，方便维护记录 方便寻找最佳策略时遍历不遗漏
    · 厉害的方法：
      使用globals()方法，自动找出当前模块中的全部策略。内省模块的全局命名空间，构建promos列表。
    · 另一种思路：
      见 04_Order寻找最佳策略_另一种思路.py

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


# 寻找最佳策略的方法
# 方法一：先新建一个记录所有策略方法的列表，手动添加策略方法，方便维护记录 方便寻找最佳策略时遍历不遗漏
# promos = [FidelityPromo, BulkItemPromo, LargeOrderPromo]
# 方法二：使用globals()方法，自动找出当前模块中的全部策略。——globals()方法返回一个字典，表示当前的全局符号表。
promos = [globals()[name] for name in globals() if name.endswith('Promo') and name != 'best_promo']


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
