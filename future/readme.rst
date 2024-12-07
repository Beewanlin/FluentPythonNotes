future示例中的服务端：
https://www.fluentpython.com/data/flags/

Future对象 代表一个异步执行的操作。

通过concurrent.futures框架或asyncio框架实例化future对象（不要自己实现future对象），
例如，Excutor.submit(fn, *args, **kwargs)，fn是需要异步执行的函数，args,kwargs:为给函数传递的参数。该方法排定可调用对象fn的执行时间，然后返回一个future，表示一个待执行的异步操作。

框架内大多数函数都不会直接返回future对象，而是返回future对象的结果。
例如 Excutor.map(func, <iterable>) 返回一个迭代器，迭代器的__next__方法调用各个future的result方法，因此得到的是future执行完的结果（而不是future本身）。
最后需要用future.result()来获取future运行结束返回的结果。


实现并发。
对于线程来说，适用于I/O密集型的场景。
可用concurrent.futures模块，常用方法是：
futures.ThreadPoolExecutor(maxworkers=?)（与with结构连用）进行future的实例化；
Executor.map(fn, <iterable>)
Executor.submit(fn, *args)
futures.as_completed(<iterable>)
futures.result()
futures.done()
对于进程来说，可用futures.ProcessExecutor模块可以绕开GIL，适用于CPU密集型的场景。

