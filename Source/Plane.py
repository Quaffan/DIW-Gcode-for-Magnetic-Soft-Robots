# Plane class
# Written by Lin Zhiwei
# Started on 2019/2/9

from GeomBase import *
from Line import *

# A plane is infinite, it is defined by
# a point and a normal vector passing through it
class Plane:
    def __init__(self, P, N):
        self.P = P.clone()
        self.N = N.clone().normalized()

    def __str__(self):
        return "Plane\n%s\n%s\n" % (str(self.P), str(self.N))

    @staticmethod
    def zPlane(z):
        return Plane(Point3D(0, 0, z), Vector3D(0, 0, 1.0))

    def toFormula(self):
        A, B, C = self.N.dx, self.N.dy, self.N.dz
        D = -self.N.dx * self.P.x - self.N.dy * self.P.y - self.N.dz * self.P.z
        return A, B, C, D

    def intersect(self, other):
        dir = self.N.crossProduct(other.N)
        if dir.isZeroVector():
            return None
        else:
            x, y, z = 0, 0, 0
            A1, B1, C1, D1 = self.toFormula()
            A2, B2, C2, D2 = other.toFormula()
            if B2*C1 - B1*C2 != 0:
                y = -(-C2*D1 + C1*D2)/(B2*C1 - B1*C2)
                z = -(B2*D1 - B1*D2)/(B2*C1 - B1*C2)
            elif A2*C1 - A1*C2 != 0:
                x = -(-C2*D1 + 1*D2)/(A2*C1 - A1*C2)
                z = -(A2*D1 - A1*D2)/(A2*C1 - A1*C2)
            elif A2*B1 - A1*B2 != 0:
                x = -(-B2*D1 + B1*D2)/(A2*B1 - A1*B2)
                y = -(A2*D1 - A1*D2)/(A2*B1 - A1*B2)
            else:
                return None
            return Line(Point3D(x, y, z), dir.normalized())



def zPlane(z):
    p = Plane(Point3D(0, 0, z), Vector3D(0, 0, 1.0))
    return p