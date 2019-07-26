#coding: utf-8
import multiprocessing
import time

def func(msg):
    print("msg:", msg)
    time.sleep(3)
    print("end")
    return "done"+msg

if __name__ == "__main__":
    pool = multiprocessing.Pool(3)
    result = []
    for i in range(4):
        msg = "hello %d" % i
        result.append(pool.apply_async(func, (msg, )))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    for res in result:
        print(":::",res.get())
    print("Sub-process(es) done.")