"""
该demo是为了体现装饰器的一个应用场景，优化商品促销策略。

该例也是对【策略模式】用装饰器改进选择最优策略的一种方法的说明。
通过对每个策略方法应用注册装饰器，使得自动统计已有的策略函数，便于最后选择最佳策略时避免遗漏的遍历并比较选择。
此外，该方法还有一个优点，不必限制策略函数的命名了（自省方法统计，需要根据类型对象的属性即函数命名来筛选）。
"""
# 用一个列表记录商品促销策略处理函数
promos = []


# 装饰器 promotion，作用是 登记每一个已创建的促销策略函数
def promotion(promo_func):
    promos.append(promo_func)
    return promos


@promotion
def bulk_item(order):
    """单个商品购买20个以上，提供10%折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * 0.1
    return discount


@promotion
def large_order(order):
    """订单的不同商品达到10个或以上时提供7%折扣"""
    discount_items = {item.product for item in order.cart}
    if len(discount_items) >= 10:
        return order.total() * 0.07
    return 0


def best_promo(order):
    """选择最佳的折扣方式"""
    return max(promo(order) for promo in promos)
