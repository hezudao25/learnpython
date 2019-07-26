import time

def set_func(func):
    def call_func(*args, **kwargs):
        print("---这是权限验证---")
        func(*args, **kwargs)

    return call_func


@set_func # 等价于 test1 = set_func(test1)
def test1(num, *args, **kwargs):
    print("----test1-----%d" % num)
    print("----test1-----", args)
    print("----test1-----", kwargs)


test1(100)
test1(100, 200)
test1(100, 200, 300 ,mm=100)


