from GeomAlgo import *
from Layer import *
from StlModel import *
from IntersectStl_sweep import *

class IntersectStl_match:
    def __init__(self, stlModel, layerThk):
        self.stlModel = stlModel
        self.layerThk = layerThk
        self.layers = []
        self.excute()
        pass

    def matchFacetZs_brutal(self, zs):
        for triangle in self.stlModel.triangles:
            zMin, zMax = triangle.zMinPnt().z, triangle.zMaxPnt().z
            for z in zs:
                if z > zMax:
                    break
                if z >= zMin and z <= zMax:
                    triangle.zs.append(z)

    '''
    def matchFacetZs_bisection(self, zs):
        zs.append(zs[-1] + layerThickness*100)
        zs.insert(0, zs[0] - layerThickness*100)
        zCount = len(zs)
        for triangle in self.stlModel.triangles:
            zMin, zMax = triangle.zMinPnt().z, triangle.zMaxPnt().z
            startIndex, stopIndex = 0, 0

            low, up = 0, zCount -1
            while up - low > 1:
                mid = int((low + up)/2)
                if zs[mid] < zMin:
                    low = mid
                else:
                    up = mid
            startIndex = int((low + up) / 2)


            low, up = 0, zCount - 1
            while up - low > 1:
                mid = int((low + up)/2)
                if zs[mid] < zMax:
                    low = mid
                else:
                    up = mid
            stopIndex = int((low + up)/2)


            for i in range(startIndex, stopIndex+1, 1):
                triangle.zs.append(zs[i])
        pass
    '''

    def matchFacetZs_bisection(self, zs):
        n = len(zs)
        for tri in self.stlModel.triangles:
            zMin, zMax = tri.zMinPnt().z, tri.zMaxPnt().z

            low, up, mid = 0, n - 1, 0
            while up - low > 1:
                mid = int((low + up)/2)
                if zs[mid] < zMin:
                    low = mid
                else:
                    up = mid
            start = up
            if zs[mid] == zMin:
                start = low

            low, up = 0, n - 1	
            while up - low > 1:
                mid = int((low + up)/2)
                if zs[mid] < zMax:
                    low = mid
                else:
                    up = mid
            stop = low
            if zs[mid] == zMax:
                stop = up

            for i in range(start, stop + 1, 1):
                tri.zs.append(zs[i])
        pass

    def excute(self):
        zs, layerDic = self.genLayerHeights()
        self.matchFacetZs_bisection(zs)

        for triangle in self.stlModel.triangles:
            for z in triangle.zs:
                seg = intersectTriangleZPlane(triangle, z)
                if seg is not None:
                    layerDic[z].segments.append(seg)

        for layer in layerDic.values():
            self.layers.append(layer)

    def genLayerHeights(self):
        xMin, xMax, yMin, yMax, zMin, zMax = self.stlModel.getBounds()
        zs, layerDic = [], {}
        z = zMin + self.layerThk
        while z < zMax:
            z = round(z, 3)            # 必须要加上，否则会有字典可能找不到
            zs.append(z)
            layerDic[z] = Layer(z)
            z += self.layerThk
        return zs, layerDic



from VtkAdaptor import *
if __name__ == '__main__':

    xx = [1,2,3]
    xx.insert(0, 0)
    print(xx)


    stlModel = StlModel()
    stlModel.readStlFile('E:\\man head.STL')

    print('face count:', stlModel.getFacetNumber())

    layerThk = 2

    start_CPU = time.clock()
    #layers1 = IntersectStl_sweep(stlModel, layerThk).layers
    end_CPU = time.clock()
    print("Method sweep: %f CPU seconds" % (end_CPU - start_CPU))

    start_CPU = time.clock()
    layers2 = IntersectStl_match(stlModel, layerThk).layers
    end_CPU = time.clock()
    print("Method smart: %f CPU seconds" % (end_CPU - start_CPU))

    start_CPU = time.clock()
    #layers3= intersectStl_brutal(stlModel, layerThk)
    end_CPU = time.clock()
    print("Method brutal: %f CPU seconds" % (end_CPU - start_CPU))

    #print(len(layers1))


    va = VtkAdaptor()

    for layer in layers2:
        linkSegments_brutal(layer)
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
            pass

    va.display()

