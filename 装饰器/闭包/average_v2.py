"""
该版本基于上个版本，改进了实现，不用series列表记录所有历史值，而是记录total和count两个数字型变量。

但要注意的是，对于不可变类型只能读取不能更新。
在该例中，如果在内层函数内尝试重新绑定不可变类型变量total、count，其实会在内层函数内隐式创建局部变量，total和count变量也不再是自由变量了，因此不会保存在闭包中。
解决办法就是在内层函数中声明 变量为自由变量，那么当这些变量需要更新时，闭包中保存的绑定也会更新。
"""


def make_average():
    total = 0
    count = 0

    def averager(value):
        nonlocal total, count  # 使用nonlocal关键词声明变量为自由变量
        count += 1
        total += value
        return total / count

    return averager


if __name__ == '__main__':
    avg = make_average()  # 返回 averager 可调用对象。此时make_average的调用已经结束，那么series的历史值是保存在哪里的呢？

    print(avg.__code__.co_varnames)  # 查看 averager函数对象的局部变量名
    print(avg.__code__.co_freevars)  # 查看 averager函数对象的自由变量名

    print('当前自由变量的值为:')  # 通过.cell_contents查看averager函数对象的自由变量值的属性
    for v in avg.__closure__:
        print(v.cell_contents)

    res1 = avg(10)
    print('当前移动平均值为：', res1)

    print('当前自由变量的值为:')  # 通过.cell_contents查看averager函数对象的自由变量值的属性
    for v in avg.__closure__:
        print(v.cell_contents)

    res2 = avg(11)
    print('当前移动平均值为：', res2)

    print('当前自由变量的值为:')  # 通过.cell_contents查看averager函数对象的自由变量值的属性
    for v in avg.__closure__:
        print(v.cell_contents)
