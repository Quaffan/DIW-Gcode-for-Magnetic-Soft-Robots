# Trangle class
# Written by Lin Zhiwei
# Started on 2019/2/9


from GeomBase import *
from Line import *
from Segment import *
from VtkAdaptor import *

class Triangle:
    def __init__(self, A, B, C, N = Vector3D(0,0,0)):
        self.A = A.clone()
        self.B = B.clone()
        self.C = C.clone()
        self.N = N.clone()
        self.zs = [] # 存储切片的高度

    def __str__(self):
        s1 = ">>> Triangle\nA: %s, %s, %s\nB: %s, %s, %s\nC: %s, %s, %s\n" %(self.A.x, self.A.y, self.A.z, self.B.x, self.B.y, self.B.z, self.C.x, self.C.y, self.C.z)
        s2 = "N: %s, %s %s\n" %(self.N.dx, self.N.dy, self.N.dz)
        s = s1 + s2
        return s

    # 计算三角面片的法向量
    def calcNormal(self):
        v1 = self.A.pointTo(self.B)
        v2 = self.A.pointTo(self.C)
        n = v1.crossProduct(v2)
        self.N = n.normalized()
        return self.N

    def lowestPnt(self):
        zMin = self.A.z
        pntMin = self.A
        if (self.B.z < zMin):
            zMin = self.B.z
            pntMin = self.B
        if (self.C.z < zMin):
            pntMin = self.C
        return pntMin

    def highestPnt(self):
        zMax = self.A.z
        pntMax = self.A
        if (self.B.z > zMax):
            zMax = self.B.z
            pntMax = self.B
        if (self.C.z > zMax):
            pntMax = self.C
        return pntMax

    def zMinPnt(self): return self.lowestPnt()
    def zMaxPnt(self): return self.highestPnt()

    def draw(self, va):
        va.drawSegment(Segment(self.A, self.B))
        va.drawSegment(Segment(self.A, self.C))
        va.drawSegment(Segment(self.C, self.B))

if __name__ == "__main__":
    t = Triangle(Point3D(0, 0, 0), Point3D(100, 100, 0), Point3D(50, 200, 0), Vector3D(0, 0, 1))
    print(t)
    va = VtkAdaptor()
    va.drawAxes()
    va.setBackgroundColor(0, 0, 0)
    t.draw(va)
    va.display()