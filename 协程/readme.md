【协程】
指的是与调用方协作并产出由调用方提供的值的过程。
协程与生成器类似，都包含yield。yield在协程中的用法由生成器进化而来，与迭代或迭代器毫无关系。
在生成器中，yield的作用是 产出值 和 执行暂停；在协程中，yield的作用是接收值 和 执行暂停。
相比于原来的生成器API，协程多了.send(datum)、.throw(…) .close()几个方法，分别用于 传递数据给yield表达式、抛出异常、终止协程。

协程有4个状态，可以由inspect.getgeneratorstatus(…)来获取。
'GEN_CREATED' 等待开始执行
'GEN_RUNNING' 解释器正在执行
'GEN_SUSPENDED' 在yield表达式处暂停
'GEN_CLOSED' 执行结束**

注意，只有协程处于暂停状态时，才可以send值给yield表达式。
而根据生成器的执行过程：
一开始，协程处于'GEN_CREATE'状态；
调用next(生成器对象)后，函数定义体才会执行到yield之前，协程处于'GEN_SUSPENDED'状态（这一步调用next，通常称为"预激协程"，即让协程前进到第一yield表达式暂停，准备好作为活跃的线程使用）；
此时，调用send()才能将数值传给yield表达式；(若yield右边也有式子，由于赋值语句的右边会先执行，暂停在yield左式之前会先执行右式产出值)


协程也可以有返回值。
根据Python文档建议的方法，要获取协程的返回值，需要通过捕获StopIteration异常获取其value值以获取协程的返回值。
可以在调用协程时编写try/else语句块来手工捕获StopIteration异常，当然更好的方法是 通过yield from结构来自动捕获StopIteration异常。

回顾yield from，它的一大重要作用是简化for循环中的yield表达式。但其实它更重要的作用是"把职责委托给子生成器"。
yield from <iterable> 的原理是，调用<iterable>的iter方法获取迭代器。