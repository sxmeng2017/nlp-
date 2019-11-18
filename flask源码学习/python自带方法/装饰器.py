"""
看着装饰器很有趣，但一直没写过多写几个放这
"""
import time

def implement_of_time_cost(f):
    def decorator(*args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        print(end - start)
    return decorator

def implement_of_name(f):
    def decorator(*args, **kwargs):
        print('it is time to start {}'.format(f.__name__))
        f(*args, **kwargs)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('{} have finished at {}'.format(f.__name__, t))
    return decorator

def f(a,b):
    return a + b

@implement_of_time_cost
def f1(a,b):
    return a + b

@implement_of_name
def f2(a,b):
    return a + b
if __name__ == '__main__':
    f(1,2)
    f1(1, 2)
    f2(1, 2)