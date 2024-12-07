def factorial(n):
    """
    定义一个求阶乘的函数
    :param n: 表示要求n的阶乘
    :return: 返回n的阶乘结果
    """
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    print(factorial.__doc__)  # 该函数其实也是对象，是function类的实例。函数对象有__doc__属性，是函数的帮助文档，即定义函数时的注释。
    print(help(factorial))  # 等价于上式
    fact = factorial  # 函数的别名/引用
    print(fact)  # 输出的是对象的内存地址
