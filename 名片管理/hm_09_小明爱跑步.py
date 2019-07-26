class Peison:

    def __init__(self,name,weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return  "我的名字叫%s 体重是%s 公斤" % (self.name,self.weight)

    def run(self):
        print("%s 爱跑步，跑步锻炼身体" % self.name)
        self.weight -=0.5

    def eat(self):
        print("%s 爱吃东西" % self.name)
        self.weight +=1



xiaoming = Peison("小明",60)
xiaoming.run()
xiaoming.eat()
print(xiaoming)

xiaomei = Peison("小美",45)
xiaomei.eat()
xiaomei.run()
print(xiaomei)