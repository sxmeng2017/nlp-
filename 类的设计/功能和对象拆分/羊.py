class Animal:
    """
    Animal类作为所有动物的抽象类。只提供最基本的是否为哺乳动物的属性和判断
    """
    def __init__(self, is_mammal=True):
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
        self.name = name
        self.sex = sex
        self.horn = horn
        self.color = color
        self.tail = tail


#********************************* 功能类 ***********************************#
class Run:

    def __init__(self, speed=10, step=10):
        self.name = None
        self.speed = speed
        self.step = step

    def run(self):
        print('{} is running'.format(self.name))


#******************************** 最上层 ************************************#
class sheep(AbstractSheep, Run):

    def __init__(self, name):
        super(sheep, self).__init__(name)


if __name__ == '__main__':
    s = sheep('sheep1')
    s.run()