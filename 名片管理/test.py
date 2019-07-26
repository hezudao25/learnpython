class Cat:
    def __init__(self,name):
        print("这是初始化方法")
        # self.属性名 = 属性的初始值
        self.name = name

    def eat(self):
        print("%s吃鱼" % self.name)

    def play(self):
        print("小猫爱玩")

    def __str__(self):
        return "%s 这是啥" % self.name

    def __del__(self):
        print("%s 走了" % self.name)


#使用类名（）创建对象时，自动调用————init————方法
tom = Cat("tom")

print(tom)

