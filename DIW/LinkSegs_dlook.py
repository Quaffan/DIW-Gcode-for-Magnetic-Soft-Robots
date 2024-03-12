
from LinkPoint import LinkPoint
import pprint

class LinkSegs_dlook:
    def __init__(self, segs):
        self.segs = segs
        self.contours = []
        self.polys = []
        self.link()

    def createLpDic(self):
        dic = {}
        for seg in self.segs:
            lp1, lp2 = LinkPoint(seg.A), LinkPoint(seg.B)
            lp1.other, lp2.other = lp2, lp1

            if (lp1.x, lp1.y) not in dic.keys():
                dic[(lp1.x, lp1.y)] = []
            dic[(lp1.x, lp1.y)].append(lp1)

            if (lp2.x, lp2.y) not in dic.keys():
                dic[(lp2.x, lp2.y)] = []
            dic[(lp2.x, lp2.y)].append(lp2)
        return dic

    def findUnusedPnt(self, dic):
        for pnts in dic.values():
            for pnt in pnts:
                if pnt.used == False:
                    return pnt
        return None

    def findNextPnt(self, p, dic):
        other = p.other
        pnts = dic[(other.x, other.y)]
        difPnt = None
        for pnt in pnts:
            if pnt is not other:
                difPnt = pnt
        return difPnt

    def link(self):
        dic = self.createLpDic()
        #pprint.pprint(dic)

        while True:
            p = self.findUnusedPnt(dic)
            if p is None:
                break

            poly = Polyline()

            while True:
                poly.addPoint(p.toPoint3D())
                p.used, p.other.used = True, True
                p = self.findNextPnt(p, dic)

                if poly.isClosed():
                    self.contours.append(poly)
                    break
                if p is None:
                    self.polys.append(poly)
                    break


        # link not closed contours





from VtkAdaptor import *
from StlModel import *
import time
from SliceAlgo import *
from LinkSegs_dorder import *

if __name__ == '__main__':

    for i in range(10):
        print(i/10)

    src = vtk.vtkSTLReader()
    src.SetFileName("E:\\STL\\monk.stl")
    stlModel = StlModel()
    stlModel.extractFromVtkStlReader(src)


    print('bounds:', stlModel.getBounds())
    print('face count:', stlModel.getFacetNumber())


    layers = IntersectStl_sweep(stlModel, 1.200001).layers

    print('finished: intersect STL')

    start_CPU = time.clock()

    segCount = 0
    for layer in layers:
        layer.contours = LinkSegs_dlook(layer.segments).contours

        #linkSegs_brutal(layer)

        segCount += len(layer.segments)

    end_CPU = time.clock()
    print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))

    print('total segment count:', segCount)
    print('avg segment count per layer:', segCount / len(layers))


    va = VtkAdaptor((1,1,1))

    for layer in layers:
        #segmentsToContours_brutal(layer)
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
            pass


    #va.drawPdSrc(src).GetProperty().SetOpacity(0.8)
    va.display()
