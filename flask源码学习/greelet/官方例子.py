from greenlet import greenlet
def tet1():
    print(12)
    gr2.switch()
    print(34)

def tet2():
    print(56)
    gr1.switch()
    print(78)
if __name__ == '__main__':

    gr1 = greenlet(tet1)
    gr2 = greenlet(tet2)
    gr1.switch()