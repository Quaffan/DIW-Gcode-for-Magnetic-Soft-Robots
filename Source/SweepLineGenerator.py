"""
# 设置输出文件名
geom_name='机械样条' 

# 绘制磁编程单元轮廓
path = []

# 设置扫描线间距，单位 mm
interval = 0.35


# 设置扫描角度，单位 °
angle_deg = 0

sweep1 = SweepLineGenerator(geom_name, path, interval, angle_deg)
# sweep2 = sweep1.rotated(0,0,math.pi/3)

sweep1.addTable()
# sweep2.addTable()

sweep1.preview()
# sweep6.preview()
# 旋转矩阵采用弧度制参数

geom_name='索状花抓手'
interval = 0.35
angle_deg1 = 90
angle_deg2 = 270
path1 = [(0,0),(2,3.46),(1,6),(-1,6),(-2,3.46)]
path2 = [(1,6),(2,9.46),(1,12),(-1,12),(-2,9.46),(-1,6)]
bottom1 = SweepLineGenerator(geom_name, path1, interval, angle_deg1)
upper1 = SweepLineGenerator(geom_name, path2, interval, angle_deg2)
foot1 = bottom1 + upper1
foot2 = foot1.rotated(0,0,math.pi/3)
foot3 = foot2.rotated(0,0,math.pi/3)
foot4 = foot3.rotated(0,0,math.pi/3)
foot5 = foot4.rotated(0,0,math.pi/3)
foot6 = foot5.rotated(0,0,math.pi/3)
msr = foot1 + foot2 + foot3 + foot4 + foot5 + foot6
pressure = 0.5
print_speed = 4
firstz = 0.2
advanced_off = 1

"""



import copy
import GeomBase
from VtkAdaptor import *
from SliceAlgo import *
import Utility
from GenHatch import *
from Segment import *
import csv
import math

class SweepLineGenerator:
    def __init__(self, csv_name, path, interval, angle_deg):
        self.csv_name = csv_name
        self.path = path
        self.interval = interval
        self.angle_deg = angle_deg
        self.poly = ClipperAdaptor(0).toPoly(path)
        self.angle = Utility.degToRad(angle_deg)
        self.segs = genSweepHatches([self.poly], self.interval, self.angle)
    
    def initTable(self):
        with open("E:\\JupyterNotebook\\DIW\\CSV\\%s.csv" % self.csv_name, 'w', newline='', encoding='ANSI') as f:
            writer = csv.writer(f)
            writer.writerow(['端点 X', '端点 Y', '端点 Z', '起点 X', '起点 Y', '起点 Z'])        

    # 将磁编程块组装
    def __add__(self, other):
        answer = copy.deepcopy(self)
        answer.path += other.path
        # answer.poly += other.poly
        answer.segs += other.segs
        answer.angle_deg = [self.angle_deg, other.angle_deg]
        return answer

    # 打印扫描线段
    def getSegs(self):
        for seg in self.segs:
            print(seg)
    
    # 将现有扫描线段添加至csv表格中
    def addTable(self):
        with open("E:\\JupyterNotebook\\DIW\\CSV\\%s.csv" % self.csv_name, 'a', newline='', encoding='ANSI') as f:
            writer = csv.writer(f)
            for seg in self.segs:
            # 写入实例化的对象数据
                writer.writerow([round(seg.B.x,4), round(seg.B.y,4), round(seg.B.z,4), round(seg.A.x,4), round(seg.A.y,4), round(seg.A.z,4)])
        print("数据已添加！")
    
    # 预览效果图
    def preview(self):
        va = VtkAdaptor()
        prop = va.drawPolyline(self.poly).GetProperty()
        prop.SetColor(0, 0, 0)
        prop.SetLineWidth(2)
        for i in range(len(self.segs)):
            prop = va.drawSegment(self.segs[i]).GetProperty()
            prop.SetColor(1, 0, 0)
            prop.SetLineWidth(2)
            textSrc = vtk.vtkVectorText()
            textSrc.SetText('%d' % i)
            textActor = va.drawPdSrc(textSrc)
            textActor.SetPosition(self.segs[i].B.x, self.segs[i].B.y, self.segs[i].B.z)
            textActor.SetScale(0.1)
            textActor.GetProperty().SetColor(0, 0, 0)
        va.display()
    
    # 平移Vector3D向量
    def translated(self, vec):
        res = copy.deepcopy(self) # 这里一定要采用深拷贝，浅拷贝会对调用对象产生影响
        for seg in res.segs:
            seg.A.x, seg.A.y, seg.A.z = seg.A.x + vec.dx, seg.A.y + vec.dy, seg.A.z + vec.dz
            seg.B.x, seg.B.y, seg.B.z = seg.B.x + vec.dx, seg.B.y + vec.dy, seg.B.z + vec.dz
        return res
    
    # 旋转，X、Y、Z轴旋转，弧度制
    def rotated(self, a, b, c):
        res = copy.deepcopy(self)
        mx = GeomBase.Matrix3D.createRotateMatrix('X', a)
        my = GeomBase.Matrix3D.createRotateMatrix('Y', b)
        mz = GeomBase.Matrix3D.createRotateMatrix('Z', c)
        m = mx * my * mz
        for seg in res.segs:
            seg.multiply(m)
        return res