"""
等差数列生成器
要求：
输入参数为：begin、step、end（可选）
返回结果的类型和begin或step相同，支持int、float、Fraction、Decimal类型。

该版本使用迭代器模式实现一个类
"""


class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None表示是无穷数列

    def __iter__(self):
        # 先输出当前结果并确定数据类型。通过begin和step之和的类型，强制类型转换。
        result = type(self.begin + self.step)(self.begin)
        # 下标
        index = 0
        # 起一个标志是否是无穷数列，便于判断循环次数
        forever = self.end is None
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


if __name__ == '__main__':
    ap = ArithmeticProgression(0, 1, 3)
    print(list(ap))
    ap2 = ArithmeticProgression(0, .5, 2)
    print(list(ap2))
