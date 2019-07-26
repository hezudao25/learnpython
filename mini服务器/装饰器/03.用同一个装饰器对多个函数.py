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

@set_func # 等价于 test2 = set_func(test2)
def test2(num):
    print("----test2-----%d" % num)

#test1 = set_func(test1)

test1(100)

test2(200)