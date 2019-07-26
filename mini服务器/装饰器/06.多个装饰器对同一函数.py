def set_func(func):
    print("---开始进行装饰权限功能----")
    def call_func(*args, **kwargs):
        print("---这是权限验证---")
        return func(*args, **kwargs)
    return call_func


def set_func2(func):
    print("---进行XXX的装饰----")
    def call_func(*args, **kwargs):
        print("---这是XXXX证---")
        return func(*args, **kwargs)
    return call_func


@set_func
@set_func2
def test1():   # 多个装饰器 作用从上到下
    print("----test1-----")



test1()