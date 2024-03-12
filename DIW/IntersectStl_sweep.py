from Plane import *
from StlModel import *
from Layer import *
from GeomAlgo import *
# from SliceAlgo import *
import time

class SweepPlane:
    def __init__(self):
        self.triangles = []
    pass

class IntersectStl_sweep:
    def __init__(self, stlModel, layerThk):
        self.stlModel = stlModel
        self.layerThk = layerThk
        self.layers = []
        self.intersect()

    def intersect(self):
        triangles = self.stlModel.triangles
        triangles.sort(key = lambda t : t.zMinPnt().z)
        zs = self.genLayerHeights()

        k = 0
        sweep = SweepPlane()
        for z in zs:
            for i in range(len(sweep.triangles) - 1, -1, -1):   # 先从sweep上移除元素
                if z > sweep.triangles[i].zMaxPnt().z:
                    del sweep.triangles[i]

            for i in range(k, len(triangles)):                  # 往sweep上添加元素
                tri = triangles[i]
                if z >= tri.zMinPnt().z and z <= tri.zMaxPnt().z:
                    sweep.triangles.append(tri)
                elif tri.zMinPnt().z > z:
                    k = i
                    break

            layer = Layer(z)
            for triangle in sweep.triangles:
                seg = intersectTriangleZPlane(triangle, z)
                if seg is not None:
                    layer.segments.append(seg)
            self.layers.append(layer)

    def genLayerHeights(self):
        xMin, xMax, yMin, yMax, zMin, zMax = self.stlModel.getBounds()
        zs = []
        z = zMin + self.layerThk
        while z < zMax:
            zs.append(z)
            z += self.layerThk
        return zs



from VtkAdaptor import *
if __name__ == '__main__':
    stlModel = StlModel()
    stlModel.readStlFile('E:\\man head.STL')

    print('face count:', stlModel.getFacetNumber())

    start_CPU = time.clock()
    layers = IntersectStl_sweep(stlModel, 0.1).layers
    end_CPU = time.clock()
    print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))

    start_CPU = time.clock()
    layers1 = intersectStl_brutal(stlModel, 0.1)
    end_CPU = time.clock()
    print("Method 2: %f CPU seconds" % (end_CPU - start_CPU))

    print(len(layers))


    va = VtkAdaptor()

    for layer in layers:
        #segmentsToContours_brutal(layer)
        for contour in layer.contours:
            va.drawPolyline(contour).GetProperty().SetColor(0, 0, 0)
            pass

    va.display()







