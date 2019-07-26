


# 一个函数中有yield语句，那么这个不是函数，而是一个生成器的模板
def create_num(all_num):
    print()
    # a = 0
    # b = 1
    a, b = 0, 1
    current_num = 0
    while current_num < all_num:
        #print(a)
        ret = yield a
        print("...ret...", ret)
        a, b = b, a+b
        current_num += 1
# 如果在调用craete_num时候，发现这个函数有yield那么此时，不是调用函数，而是创建一个生成器对象

obj = create_num(10)
print(next(obj))

print(obj.send("haha"))

print(next(obj))
#for i in obj:
    #print(i)