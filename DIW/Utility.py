import math
from GeomBase import *

def makeListLinear(lists):
    outList = []
    _makeListLinear(lists, outList)
    return outList

def _makeListLinear(inList, outList):
    for a in inList:
        if type(a) != list:
            outList.append(a)
        else:
            _makeListLinear(a, outList)


def radToDeg(rad):
    return rad * 180.0 / math.pi

def degToRad(deg):
    return deg * math.pi / 180.0


if __name__ == '__main__':
    a = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, [12,34]], [1, 2, 3, 4]]
    print(makeListLinear(a))
    pow(1,2)



