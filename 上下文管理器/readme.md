上下文管理器

什么是上下文？
定义上来说，上下文是指代码执行过程中的环境和状态；
但感性理解上来说，某个语句块的前后被执行的语句，就是该语句块的上下文。

什么是上下文管理器？
上下文管理器协议是 __enter__() 和 __exit__() 接口。满足了该协议的，就是上下文管理器。
上下文管理器就是为了管理with语句块的，而with语句块的作用是简化try/finnaly。

Python有自带的上下文管理器，例如：open() 打开文件方法。
该上下文管理器的__enter__方法返回其自身，这样当with open() as f 时会将文件绑定到f上；
该上下文管理器的__exit__方法把文件关闭。


自定义实现上下文管理器的方式有：
（1）自定义一个实现了__enter__方法和__exit__方法的类。但需注意：
__enter__方法：传入参数可以仅有self，也可以根据实际场景传入多个
__exit__方法：最好处理异常，然后返回True（因为__exit__方法会向上冒泡异常）
（2）最常用的方法：使用@contextmanager装饰器，装饰一个生成器函数。
该函数中的yield并不起迭代器的作用，而起类似协程的作用，使得程序执行在yield语句暂停后，让客户代码先运行，再可从暂停点继续执行。




其他知识点：else语句块可以在if、while、try中使用