from GeomBase import *
from Polyline import *
from LinkPoint import LinkPoint
import functools



def cmp_pntSmaller(lp1, lp2):
    if (lp1.x < lp2.x):
        return -1
    elif (lp1.x == lp2.x and lp1.y < lp2.y):
        return -1
    elif (lp1.x == lp2.x and lp1.y == lp2.y and lp1.z < lp2.z):
        return -1
    elif (lp1.x == lp2.x and lp1.y == lp2.y and lp1.z == lp2.z):
        return 0
    else:
        return 1


class LinkSegs_dorder:
    def __init__(self, segs):
        self.segs = segs
        self.contours = []
        self.polys = []
        self.link()
        pass

    def createLpList(self):
        lpnts = []
        for seg in self.segs:
            lp1, lp2 = LinkPoint(seg.A), LinkPoint(seg.B)
            lp1.other, lp2.other = lp2, lp1
            lpnts.append(lp1)
            lpnts.append(lp2)
        lpnts.sort(key=functools.cmp_to_key(cmp_pntSmaller))

        for i in range(len(lpnts)):
            lpnts[i].index = i

        return lpnts

    def findUnusedPnt(self, lpnts):
        startIndex = -1
        for lpnt in lpnts:
            if lpnt.used == False:
                startIndex = lpnt.index
                break
        return startIndex

    def link(self):
        lpnts = self.createLpList()


        cnt = len(lpnts)
        while True:
            startIndex = self.findUnusedPnt(lpnts)
            if startIndex == -1:
                break

            p = lpnts[startIndex]
            poly = Polyline()
            while True:
                poly.addPoint(p.toPoint3D())
                p.used, p.other.used = True, True
                if poly.isClosed():
                    self.contours.append(poly)
                    break

                index = p.other.index
                if index - 1 >= 0 and p.other.toPoint3D().isCoincide(lpnts[index - 1].toPoint3D()):
                    p = lpnts[index - 1]
                elif index + 1 < cnt and p.other.toPoint3D().isCoincide(lpnts[index + 1].toPoint3D()):
                    p = lpnts[index + 1]
                else:
                    self.polys.append(poly)
                    break



'''
       while True:
            startIndex = -1
            for i in range(cnt):
                if lpnts[i].used == False:
                    startIndex = i
                    break

            if startIndex == -1:
                break

            poly = Polyline()
            poly.addPoint(lpnts[startIndex].toPoint3D())
            poly.addPoint(lpnts[startIndex].other.toPoint3D())

            crtPnt = lpnts[startIndex].other.toPoint3D()
            index = lpnts[startIndex].other.index

            lpnts[startIndex].used = True
            lpnts[startIndex].other.used= True

            while True:
                if index - 1 >= 0 and crtPnt.isCoincide(lpnts[index - 1].toPoint3D()):
                    # poly.addPoint(linkedPnts[index-1].toPoint3D())
                    lpnts[index - 1].used = True
                    lpnts[index - 1].other.used = True

                    poly.addPoint(lpnts[index - 1].other.toPoint3D())
                    crtPnt = lpnts[index - 1].other.toPoint3D()
                    index = lpnts[index - 1].other.index


                elif index + 1 < cnt and crtPnt.isCoincide(lpnts[index + 1].toPoint3D()):
                    # poly.addPoint(linkedPnts[index+1].toPoint3D())
                    lpnts[index + 1].used = True
                    lpnts[index + 1].other.used = True

                    poly.addPoint(lpnts[index + 1].other.toPoint3D())
                    crtPnt = lpnts[index + 1].other.toPoint3D()
                    index = lpnts[index + 1].other.index

                if poly.isClosed():
                    break

            self.contours.append(poly)


'''

from VtkAdaptor import *
from StlModel import *
import time
from SliceAlgo import *

if __name__ == '__main__':
    stlModel = StlModel()
    stlModel.readStlFile('E:\\STL\\man head.STL')

    print('face count:', stlModel.getFacetNumber())


    layers = IntersectStl_sweep(stlModel, 0.2).layers


    start_CPU = time.clock()

    for layer in layers:
        layer.contours = LinkSegs_dorder(layer.segments).contours


    end_CPU = time.clock()
    print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))



    va = VtkAdaptor()

    for layer in layers:
        #segmentsToContours_brutal(layer)
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
            pass

    va.display()

