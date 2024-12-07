"""
这里用代码举例说明协程的应用
离散仿真出租车队运营
taxi_process 协程。（一辆出租车用一个协程表示）
Simulator 类。（保存出租车及其事件）

"""
from collections import namedtuple
import queue
import random

DEPARTURE_INTERNAL = 5
SEARCH_DURATION = 5
TRIP_DURATION = 20

Event = namedtuple('Event', 'time proc action')


def taxi_process(ident, trips, start_time=0):
    """
    创建出租车协程，事件类型为：出车库、客人上车、客人下车、回家，其中客人上车或下车的事件与行程数量相关。
    :param ident: 出租车编号
    :param trips: 出租车回家之前的行程数量
    :param start_time: 出租车离开车库的时间
    """
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')
    yield Event(time, ident, 'going home')


def compute_duration(previous_action):
    """
    计算某一种事件的随机等待时间，随机数按照指数分布。
    需要用到Python的random.expvariate(1/interval)，参数interval表示所需的等待时间间隔的平均值。
    """
    if previous_action in ['leave garage', 'drop off passenger']:
        # new state is prowling
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # new state is trip
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1 / interval)) + 1


class Simulator:

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()  # 初始化一个空的优先队列，存放的是Event。取出时是按照item[0]的顺序依次取出的。
        self.procs = dict(procs_map)  # 存放协程。为了在修改procs属性时不修改传入的参数procs_map，需要新建一个字典作为入参的副本。

    def run(self, end_time):
        """排定并显示事件，直到时间结束"""
        # 排定各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):
            first_event = next(proc)
            self.events.put(first_event)  # 把各个事件添加到self.event属性表示的优先队列中，顺序无要求

        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():  # 如果队列中没有未完成的事件，则退出。
                print('**** end of events ***')
                break

            current_event = self.events.get()  # 从优先队列中取出时间最早的事件作为当前事件
            sim_time, proc_id, previous_action = current_event  # 对元组拆包
            print('taxi: ', proc_id, proc_id * '  ', current_event)
            active_proc = self.procs[proc_id]  # 根据current_event事件的proc_id，找到该事件对应的协程
            next_time = sim_time + compute_duration(previous_action)
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


if __name__ == '__main__':
    # 创建由协程组成的taxis组，每一项对应一辆出租车对应一个协程。
    num_taxis = 3
    taxis = {
        i: taxi_process(i, (i + 1) * 2, i * DEPARTURE_INTERNAL) for i in range(num_taxis)
    }
    # 由仿真类实例sim的run方法调用taxis协程组
    sim = Simulator(taxis)
    end_time = 100
    sim.run(end_time)
