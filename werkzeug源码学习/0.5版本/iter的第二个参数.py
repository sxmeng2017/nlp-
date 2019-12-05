import random

"""
即iter的第二个参数给定时，iter会持续调用第一个参数的__call__方法
直到__call__返回产生和第二个参数一致时。停止运行
"""
class IterTest:

    def __init__(self):
        self.a = [1,2,3,4,5]

    def __iter__(self):
        print('__iter__')
        return iter(self.a)

    def __call__(self):
        print('ok')
        return random.randint(0,10)
it = IterTest()
for i in iter(it, 3):
    print(i)
