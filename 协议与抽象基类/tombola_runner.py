"""
此处是doctes运行脚本示例：
运行测试的方法主要为 doctest.testfile()，其参数：
TEST_FILE 测试文档（单独的rst文件）
globs参数，表示强制使用自己的执行上下文。此例中是把cls参数绑定到全剧命名空间里的ConcreteTombola名称上，供doctest使用。(ConcreteTombola在rst文件中)
verbose=True为测试通过与未通过都将消息显示出来,默认为False，只显示失败信息。
"""

import doctest

from 协议与抽象基类.tombola import Tombola
import drum
import 协议与抽象基类.bingo, 协议与抽象基类.lotto, 协议与抽象基类.tombolist

TEST_FILE = 'tombola_tests.rst'
TEST_MSG = '{0:16}{1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    verbose = '-v' in argv
    real_subclass = Tombola.__subclasses__()
    """
    只有抽象基类有这个属性：_abc_registry，其值是一个WeakSet对象，即抽象基类注册时的虚拟子类的弱引用。
    这里要将WeakSet对象转换为list，这样方便与__subclasses__()结果拼接起来
    """
    # virtual_subclass = list(Tombola._abc_registry)

    for cls in real_subclass:
        test(cls, verbose)


def test(cls, verbose=False):
    res = doctest.testfile(
        TEST_FILE,
        globs={'ConcreteTombola': cls},
        verbose=verbose,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
    )
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == '__main__':
    import sys
    """  “argv” 即 “argument value” 是一个列表对象，其中存储的是在命令行调用 python 脚本是提供的 “命令行参数”。 """
    main(sys.argv)
