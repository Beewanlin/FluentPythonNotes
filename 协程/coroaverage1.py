from 协程.coroutil import coroutine


@coroutine
def averager():
    total = 0
    count = 0
    average = 0
    while True:
        value = yield average
        total += value
        count += 1
        average = total/count


if __name__ == '__main__':
    # 该例使用了预激活装饰器装饰协程，所以生成协程后，直接传值即可
    coroaverage = averager()
    print(coroaverage.send(10))
    res = coroaverage.send(20)
    print(res)