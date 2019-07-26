import gevent
import time
from gevent import monkey

monkey.patch_all

def func1(func):
    print("start func1")
    gevent.sleep(1)
    print("end func1",func)


def func2(func):
    print("start func2")
    gevent.sleep(1)
    print("end func2",func)

gevent.joinall(
    [
        gevent.spawn(func1, "func1"),
        gevent.spawn(func2, "func2")
    ]
)