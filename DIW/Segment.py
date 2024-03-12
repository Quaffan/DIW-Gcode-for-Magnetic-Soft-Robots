from GeomBase import *

class Segment:
    def __init__(self, A, B):
        self.A = A.clone()
        self.B = B.clone()

    def __str__(self):
        return "Segment\nA %s\nB %s\n" %(str(self.A), str(self.B))

    def __mul__(self, m : Matrix3D):
        self.A *= m
        self.B *= m
        return Segment(self.A, self.B)

    def __round__(self, n=1): # 圆整坐标，保留n位小数
        return "Segment\nA %s\nB %s\n" %(str(round(self.A, n)), str(round(self.B, n)))

    def length(self):
        return self.A.distance(self.B)

    def direction(self):
        return self.A.pointTo(self.B)

    def swap(self):
        self.A, self.B = self.B, self.A

    def multiply(self, m):
        self.A = self.A.multiplied(m)
        self.B = self.B.multiplied(m)

    def multiplied(self, m):
        seg = Segment(self.A, self.B)
        seg.multiply(m)
        return seg

    pass

if __name__ == '__main__':
    A = Point3D(1,2,4)
    B = Point3D(2,3,4)
    seg = Segment(A, B)
    print(seg)
    seg.swap()
    print(seg)