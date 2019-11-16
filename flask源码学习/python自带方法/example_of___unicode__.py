"""
简而言之就是__str__,方法保证str（class）的结果。
__unicode__能保证str和unicode两个的结果。
"""
class str1():
    def __str__(self):
        return "str1"

class str2():
    def __unicode__(self):
        return u"str2"

"""
在werkzeug中有
def implements_to_string(cls):
    cls.__unicode__ = cls.__str__
    cls.__str__ = lambda x: x.__unicode__().encode("utf-8")
    return cls
这个是用于做装饰器，将装饰的类的方法进行改写。
"""

if __name__ == '__main__':
    t1 = str1()
    print(str(t1))# str1
    # print(unicode(t1))# str1

    t2 = str2()
    print(str(t2)) # <__main__.str2 instance
    # print(unicode(t2))#str2
    ## py3中两者的区别被废除
    ## 所以结果为
    ## str1
    ## <__main__.str2 object at 0x106479908>