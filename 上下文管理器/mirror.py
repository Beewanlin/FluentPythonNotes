"""
这里实现一个LookingGlass类，是一个上下文管理器类。
"""


class LookingGlass:

    def __enter__(self):  # 解释器调用__enter__方法时，除了隐式的self，不会传入其他参数。
        import sys
        self.original_writer = sys.stdout.write
        sys.stdout.write = self.reverse_write  # 打猴子补丁。运行时修改标准输出函数为自定义的反响输出函数。
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_writer(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):  # 这三个参数是 异常类、异常实例、traceback对象。可以为空，说明无异常。
        import sys  # 重复导入模块不会消耗很多资源，Python会缓存导入的模块
        sys.stdout.write = self.original_writer
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero')
            return True  # 告诉解释器，异常已处理
        # 如果__exit__方法返回None，或者True之外的值，with块中的任何异常都会向上冒泡


if __name__ == '__main__':
    # 测试LookingGlass上下文管理器类
    with LookingGlass() as what:  # 上下文管理器是LookingGlass实例，此时调用了LookingGlass实例的__enter__方法，该方法返回了'JABBERWOCKY'赋给了what
        print('Alice, Kitty and Snowdrop')  # 打印字符串。但由于上下文管理器的__enter__方法给标准输出sys.stdout.write打了猴子补丁，变成了逆向输出。
        print(what)  # 打印what变量。同样也是逆序打印。
    print(what)  # 此时执行完了with语句块，调用了上下文管理器LookingGlass实例的__exit__方法，该方法中还原了标准输出方法为原来的方法。因此输出的what是顺序的。
    print('Back to normal')  # 输出也是顺序的。
    # 在with之外使用LookingGlass类
    manager = LookingGlass()
    print(manager)
    monster = manager.__enter__()  # 预期输出是顺序的
    print(monster == 'JABBERWOCKY')  # 预期输出是逆序的
    print(monster)  # 预期输出是逆序的
    print(manager)  # 预期输出是逆序的
    manager.__exit__(None, None, None)
    print(monster)  # 预期输出是顺序的
