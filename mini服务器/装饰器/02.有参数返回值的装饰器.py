import time

def set_func(func):
    def call_func(num):
        start_time = time.time()
        func(num)
        stop_time = time.time()
        print("alltimeis %f" % (stop_time - start_time))
    return call_func


@set_func # 等价于 test1 = set_func(test1)
def test1(num):
    print("----test1-----%d" % num)
    for i in range(10000):
        pass

#test1 = set_func(test1)

test1(100)

test1(200)