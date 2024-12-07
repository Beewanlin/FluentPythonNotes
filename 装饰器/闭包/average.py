"""
这里举例实现 计算移动平均值的高阶函数（基于闭包的实现）

闭包：在该例中，闭包是 内层的averager函数和其外层的自由变量series 组成的。
自由变量：未在外层函数本地作用域中绑定的变量，其绑定会在内层函数被保留（虽然定义作用域不可用了，但是绑定还是可用的）

只有嵌套在其他函数中的函数才可能需要处理不在全局作用域中的外部变量，如该例中的 averager。
"""


def make_average():
    series = []

    def averager(value):
        series.append(value)
        total = sum(series)
        return total / len(series)

    return averager


if __name__ == '__main__':
    avg = make_average()  # 返回 averager 可调用对象。此时make_average的调用已经结束，那么series的历史值是保存在哪里的呢？
    print(avg.__code__.co_varnames)  # 查看 averager函数对象的局部变量名
    print(avg.__code__.co_freevars)  # 查看 averager函数对象的自由变量名
    print(avg.__closure__)  # 查看 averager函数对象的自由变量值（这些值是cell对象，可以通过contens属性查看到内容）
    print('当前自由变量的值为', avg.__closure__[0].cell_contents)  # 通过.cell_contents查看averager函数对象的自由变量值的属性
    res1 = avg(10)
    print('当前移动平均值为：', res1)
    print('当前自由变量的值为', avg.__closure__[0].cell_contents)
    res2 = avg(11)
    print('当前移动平均值为：', res2)
    print('当前自由变量的值为', avg.__closure__[0].cell_contents)


