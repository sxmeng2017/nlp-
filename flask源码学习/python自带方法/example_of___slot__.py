"""
__slot__方法，slot方法用于缩减程序所需内存

如果无__slot__，类中的所有实例属性会以字典的形式保存下来，这允许类随意创建自己的新
属性。但如果类的属性已知。这就非常消耗内存。python不能再对象创建时直接分配一个固定量
的内存来保存所用属性。使用slot方法会告诉python不要使用字典。而且只给一个固定集合
的属性来分配空间。
"""

class limit:
    __slots__ = ['name', 'age', 'job']
    def __init__(self):
        # self.grade = 100
        # AttributeError: 'limit' object has no attribute 'grade'
        # 类内的赋值会受到限制。
        pass


if __name__ == '__main__':
    l = limit()
    limit.name = 'hi'
    print(limit.name)
    limit.grade = '100' #现在在外面这样赋值是可行的会自动添加到__dict__
    print(limit.grade)
    print(limit.__dict__)
    print(limit.age)