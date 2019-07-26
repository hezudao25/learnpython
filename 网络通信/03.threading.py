import time
import threading


def sing():
    """唱歌"""
    for i in range(5):
        print("我要唱歌...")
        time.sleep(1)


def dance():
    """跳舞"""
    for i in range(5):
        print("跳舞了...")
        time.sleep(1)




def main():
    t1 = threading.Thread(target=sing)
    t2 = threading.Thread(target=dance)
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(10)

    print(threading.enumerate())


if __name__ == "__main__":
    main()