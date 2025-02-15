一、【可迭代对象】

序列可以迭代的原因：__iter__方法

Python解释器需要调用可迭代对象x时，会自动调用iter(x)。调用逻辑如下：
如果对象实现了__iter__方法，就会调用它，获取一个迭代器；
如果对象没有实现__iter__方法，但实现了__getitem__方法，就会创建一个迭代器并尝试从0开始获取元素；
如果对象既没有实现__iter__方法，也没有实现__getitem__方法，Python就会抛出TypeError异常，通常提示对象不可迭代。
——因此，实现可迭代对象的标准方式是实现__iter__方法，或者实现向后兼容的__getitem__方法；（分别对应下面白鹅类型和鸭子类型的定义方法）

定义可迭代对象的两种方法是：
1）鸭子类型判断对象是否可迭代，是根据是否实现了__iter__方法或者__getitem__方法（且该方法的参数是从0开始的整数）；
2）白鹅类型判断对象是否可迭代，是根据是否实现了__iter__方法（有点像鸭子类型，因为abc.iterable类实现了__subclasshook__方法）
建议不要对可迭代对象进行显示检查，而是让其先执行，抛出异常后再处理。

可迭代对象与迭代器的关系：
Python解释器从可迭代对象中获取迭代器。





二、【迭代器】

标准的迭代器接口有2个函数：
__next__：返回序列的下一个元素，如果没有下一个元素则抛出StopIteration异常。
__iter__：返回迭代器实例本身。
检查对象是否是【迭代器】的最好的方式是调用 isinstance(x, abc.Iterator)




在使用迭代器的场景中，还有优化的实现方式，是使用【生成器】，节省内存。（迭代器实际上是生成器对象）
相比于迭代器预先将所有元素生成存储在可迭代对象中；生成器的改进之处在于每次需要的时候调用生成器时再生成当前所需的元素，然后暂停，等待下一次调用时再继续执行。

三、【生成器函数】及【生成器对象】及【生成器表达式】

【生成器函数】与【生成器对象】
函数定义体中有yield关键字的就是生成器函数。调用一个【生成器函数】，会返回一个【生成器对象】。
生成器函数可以没有return语句，它会自动返回一个生成器对象；
而且生成器函数永远不会抛出StopIteration异常，生成完全部值之后直接退出；但生成器函数外层的生成器对象会抛出StopIteration异常（与迭代器一致）。

因为生成器是迭代器：
所以可以调用生成器对象的.next()方法获取yield生成的下一个元素；当所有元素生成完以后/没有下一个元素了，调用.next()会抛出StopIteration异常。
迭代生成器时（例如 for g in gen，其中gen是生成器），for的机制等于 g=iter(gen())，用于获取生成器对象g，之后每次迭代则调用next(g)方法获取生成器函数gen中每次yield生成的值。

【生成器表达式】是一种简化代码的语法糖，与生成器函数的效果一样，如果需要 任何生成器函数都可以转化为生成器表达式。
只是有时候用函数更灵活，便于实现复杂逻辑。





四、【内置的和itertools库的生成器函数】
了解这些函数，避免重复造轮子
