"""
这个例子是想举例说明，弱引用是什么。
所指对象还存在强引用时，其弱引用也存在（非None）返回所指对象；所指对象不存在强引用时，其弱引用返回None。
注意所有的print语句需要转换为在控制台里直接输入print内容，因为控制台的输出结果会绑定在_变量上。因此该例一个强引用是控制台变量_。

其实 weakref.ref一般不会被使用。常用的是弱引用集合，包括：WeakValuesDictionary、WeakKeysDictionary、Weakset、finalize。
而不是手动创建并使用weakref.ref实例。
"""
import weakref

a_set = {0, 1, 2}
wref = weakref.ref(a_set)
print(wref)
print(wref())
a_set = {2, 3, 4}
print(wref())
print(wref() is None)
print(wref() is None)
