from Triangle import *

import vtk
import math

class StlModel:
    def __init__(self):
        self.triangles = []
        self.xMin = self.xMax = self.yMin = self.yMax = self.zMin = self.zMax = 0

    def getFacetNumber(self):
        return len(self.triangles)

    def getCoords(self, line):
        strs = line.lstrip().split(' ')
        cnt = len(strs)
        return float(strs[cnt-3]), float(strs[cnt-2]), float(strs[cnt-1])

    def readStlFile(self, filepath):
        f = None
        try:
            f = open(filepath, 'r')
            while True:
                line = f.readline().strip('\n')
                if line is None or line == '':
                    break
                if 'facet normal' in line:
                    dx, dy, dz = self.getCoords(line)
                    N = Vector3D(dx,dy,dz)
                    f.readline()
                    A, B, C = Point3D(), Point3D(), Point3D()
                    A.x, A.y, A.z = self.getCoords(f.readline())
                    B.x, B.y, B.z = self.getCoords(f.readline())
                    C.x, C.y, C.z = self.getCoords(f.readline())
                    triangle = Triangle(A, B, C, N)
                    self.triangles.append(triangle)
        except Exception as ex:
            print(ex)
        finally:
            if f: f.close()



    def extractFromVtkStlReader(self, vtkStlReader): # 从 vtk stlreader 中提取三角面片信息
        vtkStlReader.Update()
        polydata = vtkStlReader.GetOutput()
        cells = polydata.GetPolys()
        cells.InitTraversal()
        while True:
            idList = vtk.vtkIdList()
            res = cells.GetNextCell(idList)
            if res == 0:
                break
            pnt3ds = []
            for i in range(idList.GetNumberOfIds()):
                id = idList.GetId(i)
                x, y, z = polydata.GetPoint(id)
                pnt3ds.append(Point3D(x, y, z))
            triangle = Triangle(pnt3ds[0], pnt3ds[1],pnt3ds[2])
            triangle.calcNormal()
            self.triangles.append(triangle)

    def getBounds(self):
        cnt = len(self.triangles)
        if (cnt == 0):
            return self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax
        else:
            self.xMin = self.xMax = self.triangles[0].A.x
            self.yMin = self.yMax = self.triangles[0].A.y
            self.zMin = self.zMax = self.triangles[0].A.z
            for t in self.triangles:
                self.xMin = min(t.A.x, t.B.x, t.C.x, self.xMin)
                self.yMin = min(t.A.y, t.B.y, t.C.y, self.yMin)
                self.zMin = min(t.A.z, t.B.z, t.C.z, self.zMin)
                self.xMax = max(t.A.x, t.B.x, t.C.x, self.xMax)
                self.yMax = max(t.A.y, t.B.y, t.C.y, self.yMax)
                self.zMax = max(t.A.z, t.B.z, t.C.z, self.zMax)
            return self.xMin, self.xMax, self.yMin, self.yMax, self.zMin, self.zMax

    def multiply(self, m):
        for t in self.triangles:
            t.A, t.B, t.C, t.N = t.A * m, t.B * m, t.C * m, t.N * m

    def multiplied(self, m):
        model = StlModel()
        for t in self.triangles:
            triangle = Triangle(t.A * m, t.B * m, t.C * m, t.N * m)
            model.triangles.append(triangle)
        return model

    def rotate(self, a, b, c):
        mx = Matrix3D.createRotateMatrix('X', a)
        my = Matrix3D.createRotateMatrix('Y', b)
        mz = Matrix3D.createRotateMatrix('Z', c)
        m = mx * my * mz
        self.multiply(m)

    def rotated(self, a, b, c):
        mx = Matrix3D.createRotateMatrix('X', a)
        my = Matrix3D.createRotateMatrix('Y', b)
        mz = Matrix3D.createRotateMatrix('Z', c)
        m = mx * my * mz
        return self.multiplied(m)


from VtkAdaptor import *
# main function
if __name__ == "__main__":

    va = VtkAdaptor()
    va.setBackgroundColor(0, 0, 0)

    stlModel = StlModel()
    stlModel.readStlFile("E:\\STL\\3DP.STL")


    for tri in stlModel.triangles:
        tri.draw(va)

    print(stlModel.getBounds())

    va.display()