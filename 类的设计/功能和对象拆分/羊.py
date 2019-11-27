"""
这里有个问题，就是__init__在多继承中，如果给予的变量已经能全部填给前面继承的类
后面的继承的类的的__init__实际上不会被执行。
所以如果要attack，run能对继承的子类有所检验，看样子最好还是在动作里检测
或者子类里面检测。
"""

class Animal:
    """
    Animal类作为所有动物的抽象类。只提供最基本的是否为哺乳动物的属性和判断
    """
    def __init__(self, is_mammal=True):
        print('ani')
        self.is_mammal = is_mammal

    def isMammal(self):
        return self.is_mammal

#******************************* 动物类 ***********************************#
class AbstractSheep(Animal):
    """
    羊的抽象类，具有羊的最基本属性
    """
    is_mammal = True

    def __init__(self, name, sex=None, horn=None, color=None, tail=None):
        super(AbstractSheep, self).__init__(is_mammal=self.is_mammal)
        print('ab')
        self.name = name
        self.sex = sex
        self.horn = horn
        self.color = color
        self.tail = tail


#********************************* 功能类 ***********************************#
class Run:

    def __init__(self, speed=10, step=10):
        print('run')
        self.name = None
        self.speed = speed
        self.step = step

    def run(self):
        print('{} is running'.format(self.name))

class Horn:

    def __init__(self, length=None, hardness=None):
        self.length = length
        self.hardness = hardness

class Attack:

    def __init__(self):
        #if self.horn:
        print('{} can attack'.format(self.name))
        #else:
        #    raise ValueError('you dont have horns')

    def attack(self):
        print('Attack!')

#******************************** 最上层 ************************************#
class sheep(AbstractSheep, Run, Attack):

    def __init__(self, name, **kwargs):
        super(sheep, self).__init__(name, **kwargs)
        print('ok')


if __name__ == '__main__':
    h = Horn()
    s = sheep('sheep0')
    s.run()
    #s.attack()