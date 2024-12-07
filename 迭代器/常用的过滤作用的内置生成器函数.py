"""
该文档演示用于过滤的生成器函数，返回具有过滤作用的生成器
"""
import itertools


def vowel(c):
    return c.lower() in 'aeiou'


if __name__ == '__main__':
    it = 'Aardvark'
    """ filter(predicate, it) it的每个元素传给predicate，若为真则产出该元素，若predicate为None，也只产出真值元素"""
    res = list(filter(vowel, it))
    print(res)
    """ itertools.filterfalse(predicate, it) 与filter逻辑相反，产出it中传入predicate为假的元素"""
    res = list(itertools.filterfalse(vowel, it))
    print(res)
    """ itertools.dropwhile(predicate, it) 跳过传入predicate为真的元素，直到传入predicate为假 然后直接产出剩下的元素（不会对剩下的元素继续进一步检查了）"""
    res = list(itertools.dropwhile(vowel, it))
    print(res)
    """ itertools.takewhile(predicate, it) 产出传入predicate为真的元素，直到直到传入predicate为假 然后直接停止（不会继续判断后续的元素了）"""
    res = list(itertools.takewhile(vowel, it))
    print(res)
    """ itertools.compress(it, selector_it) 并行迭代处理it和selector_it，如果selector_it当前元素为假则不产出it中对应的元素，如果为真则产出。"""
    res = list(itertools.compress(it, (1, 0, 1, 1, 0, 1)))
    print(res)
    """ itertools.islice(it, stop) 产出it的切片，作用类似于s[:stop]或s[start:stop:step]。it可以是任何可迭代对象。该实现方式是惰性的。"""
    res1 = list(itertools.islice(it, 4))
    print(res1)
    res2 = list(itertools.islice(it, 4, 7))
    print(res2)
    res3 = list(itertools.islice(it, 1, 7, 2))
    print(res3)

