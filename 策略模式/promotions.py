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

