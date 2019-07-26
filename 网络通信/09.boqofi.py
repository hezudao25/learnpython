import time

numlist = list()
a = 0
b = 1
i = 0

while i<10:
    numlist.append(a)
    a, b = b, a+b
    i += 1


for num in numlist:
    print(num)
    time.sleep(1)