from GeomBase import *               # 导入GeomBase模块所有东西
class Ray:
    def __init__(self, P, V):
        self.P = P.clone()               # 直线经过的点，类型为Point3D
        self.V = V.clone().normalized()              # 直线方向向量，类型为Vector3D，单位向量
    def __str__(self):
        return "Ray\nP %s\nV %s\n" %(str(self.P), str(self.V))
pass