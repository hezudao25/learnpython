import time
import threading

class MyThread(threading.Thread):
    """"""
    def run(self):
        self.sing()
        self.dance()

    def sing(self):
        """唱歌"""
        for i in range(5):
            print("我要唱歌...")
            time.sleep(1)


    def dance(self):
        """跳舞"""
        for i in range(5):
            print("跳舞了...")
            time.sleep(1)




def main():
    t1 = MyThread()
    t1.start()



if __name__ == "__main__":
    main()
    print("")
