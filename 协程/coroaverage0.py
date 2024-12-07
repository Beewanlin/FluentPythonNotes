"""
示例：使用协程计算移动平均值。

移动平均值：对一组测定值，按顺序取一定数量的数据并算得其全部算术平均值，得到的数据就叫做移动平均值
"""
from inspect import getgeneratorstate  # 该方法可以获取协程的状态。


def averager():
    total = 0
    count = 0
    average = 0
    while True:  # 虽然这是一个无限循环，但仅当协程调用.send()时，才会产出值。停止循环的方式是调用协程averager时调用.close()方法。
        value = yield average  # 赋值表达式先执行右边，先产生当前average，再接收新增值value
        total += value
        count += 1
        average = total / count


if __name__ == '__main__':

    coroaverage = averager()  # 定义一个协程（此时协程处于GEN_CTRATED状态）

    print('此时协程状态：'+getgeneratorstate(coroaverage))

    next(coroaverage)  # 预激活协程，使其执行到第一个yield之前

    print('此时协程状态：'+getgeneratorstate(coroaverage))  # 预激活后，协程执行到yield暂停

    res = coroaverage.send(10)  # （此时协程处于暂停GEN_SUSPENDED状态）可以传递值给yield表达式

    print(res)

    res = coroaverage.send(11)

    print(res)

    coroaverage.close()  # 仅当调用方在协程上调用.close()方法，或则没有对协程的引用而被垃圾回收程序回收时，协程才会终止。

    print('此时协程状态：'+getgeneratorstate(coroaverage))  # 协程已关闭（此时协程的状态为GEN_CLOSED）
