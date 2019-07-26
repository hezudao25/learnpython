import time
import threading

g_num = 0

def test1(temp):
    global g_num
    dext.acquire()
    for i in range(temp):
        g_num += 1
    dext.release()
    print("---in test1 num=%d---" % g_num)


def test2(temp):
    global g_numdfsdf df请输入内容:dfsdfsdf 请输入内容:
    dext.acquire()
    for i in range(temp):
        g_num += 1
    dext.release()
    print("---in test2 num=%d---" % g_num)

#定义互拆锁
dext = threading.Lock()


def main():
    t1 = threading.Thread(target=test1,args=(10000000,))
    t2 = threading.Thread(target=test2,args=(10000000,))
    t1.start()

    t2.start()

    time.sleep(2)

    print("--- in test temp=%s---" % str(g_num))



if __name__ == "__main__":
    main()
    print("")
