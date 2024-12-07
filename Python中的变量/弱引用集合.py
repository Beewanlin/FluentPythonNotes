"""
该例说明 弱引用集合如何使用。但是 不太清楚弱引用的作用是什么？？类似缓存。
"""


import weakref


class Cheese:
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%s)' % self.kind


if __name__ == '__main__':
    stock = weakref.WeakValueDictionary()
    # stock = {}
    catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Paramesan')]
    for cheese in catalog:
        stock[cheese.kind] = cheese
    print('Original stock: ' + str(list(stock)))
    print('Sorted stock: ' + str(list(sorted(stock.keys()))))
    del catalog
    print('Delete catalog, Now stock is: ' + str(list(sorted(stock.keys()))))
    print('临时变量存在：' + str(cheese))
    del cheese
    print('Delete cheese, Now stock is: ' + str(list(sorted(stock.keys()))))
