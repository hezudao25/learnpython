import time

class Classname(object):
    def __init__(self):
        self.names = list()
        self.current_num = 0

    def add(self, name):
        self.names.append(name)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_num < len(self.names):
            ret =self.names[self.current_num]
            self.current_num += 1
            return ret
        else:
            raise StopIteration

classname= Classname()
classname.add("wadg")
classname.add("dfsdf")
classname.add("zhangwu")

#print("判断classname是否可以迭代的对象：", isinstance(classname, Iterable))
#classname_iterator = iter(classname)
#print("判断classname_iterator是否迭代器：", isinstance(classname_iterator, Iterator))
#print(next(classname_iterator))

for temp in classname:
    print(temp)
    time.sleep(1)

