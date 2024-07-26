# 扫描线法计算hatch

from GeomAlgo import *

class SweepLine:
    def __init__(self):
        self.segs = []

    def intersect(self, y):
        ips = []
        yLine = Line(Point3D(0, y, self.segs[0].A.z), Vector3D(1, 0, 0))
        for seg in self.segs:
            if seg.A.y == y:
                ips.append(seg.A.clone())
            elif seg.B.y == y:
                ips.append(seg.B.clone())
            else:
                ip = intersect(yLine, seg)
                if ip is not None:
                    ips.append(ip)
        ips.sort(key=lambda p: p.x)

        i = len(ips) - 1
        while i > 0:
            if ips[i].distance(ips[i-1]) == 0:
                del ips[i]
                del ips[i-1]
                i = i - 2
            else:
                i = i - 1

        return ips


def calcHatchPoints_bak(polygons, ys):
    segs = []
    for poly in polygons:
        for i in range(poly.count() - 1):
            seg = Segment(poly.point(i), poly.point(i + 1))
            segs.append(seg)
            seg.yMin = min(seg.A.y, seg.B.y)
            seg.yMax = max(seg.A.y, seg.B.y)
    segs.sort(key=lambda s: s.yMin)

    k, sweep = 0, []
    ipses = []  # intersection points es
    for y in ys:
        for i in range(len(sweep) - 1, -1, -1):
            if y > sweep[i].yMax:
                del sweep[i]
        for i in range(k, len(segs)):
            if y >= segs[i].yMin and y <= segs[i].yMax:   # 等号取到取不到很重要
                sweep.append(segs[i])
            elif y < segs[i].yMin:
                k = i
                break

        if len(sweep) > 0:
            itDic = {}
            yLine = Line(Point3D(0, y, segs[0].A.z), Vector3D(1, 0, 0))
            for seg in sweep:
                ip = intersect(yLine, seg)
                if ip is not None:
                    itDic[(round(ip.x, 7), round(ip.y, 7))] = ip
            ips = list(itDic.values())
            ips.sort(key=lambda p: p.x)
            ipses.append(ips)

    return ipses


def calcHatchPoints(polygons, ys):
    segs = []
    for poly in polygons:
        for i in range(poly.count() - 1):
            seg = Segment(poly.point(i), poly.point(i + 1))
            segs.append(seg)
            seg.yMin = min(seg.A.y, seg.B.y)
            seg.yMax = max(seg.A.y, seg.B.y)
    segs.sort(key=lambda s: s.yMin)

    k, sweep = 0, SweepLine()
    ipses = []  # intersection points es
    for y in ys:
        for i in range(len(sweep.segs) - 1, -1, -1):
            if sweep.segs[i].yMax < y:
                del sweep.segs[i]
        for i in range(k, len(segs)):
            if segs[i].yMin < y and segs[i].yMax >= y:
                sweep.segs.append(segs[i])
                if i == len(segs) - 1:
                    k = len(segs)
            elif segs[i].yMin >= y:
                k = i
                break

        if len(sweep.segs) > 0:
            ips = sweep.intersect(y)
            ipses.append(ips)

    return ipses



def genSweepHatches(polygons, interval, angle):
    mt = Matrix3D.createRotateMatrix('Z', -angle)
    mb = Matrix3D.createRotateMatrix('Z', angle)
    rotPolys = []
    for poly in polygons:
        rotPolys.append(poly.multiplied(mt))

    yMin, yMax = float('inf'), float('-inf')
    for poly in rotPolys:
        for pt in poly.points:
            yMin = min(yMin, pt.y)
            yMax = max(yMax, pt.y)
    ys = []
    y = yMin + interval
    while y < yMax:
        ys.append(y)
        y += interval
    segs = genHatches(rotPolys, ys)

    for seg in segs:
        seg.multiply(mb)

    return segs

def genHatches(polygons, ys):
    segs = []
    ipses = calcHatchPoints(polygons, ys)
    for ips in ipses:
        for i in range(0, len(ips), 2):
            try:
                seg = Segment(ips[i], ips[i + 1])
                segs.append(seg)
            except:
                print('ad')
    return segs

from ClipperAdaptor import *
def genClipHatches(polygons, interval, angle):
    xMin, xMax = float('inf'), float('-inf')
    yMin, yMax = float('inf'), float('-inf')
    z = polygons[0].points[0].z
    for poly in polygons:
        for pt in poly.points:
            xMin, xMax = min(xMin, pt.x), max(xMax, pt.x)
            yMin, yMax = min(yMin, pt.y), max(yMax, pt.y)
    v = Vector3D(math.cos(angle), math.sin(angle))
    n = Vector3D(math.cos(angle+math.pi/2), math.sin(angle+math.pi/2))
    O = Point3D((xMin+xMax)/2, (yMin+yMax)/2, z)
    R = math.sqrt((xMax-xMin)**2 + (yMax-yMin)**2)/2
    P1 = O - n.amplified(R)
    parallels = []
    for i in range(0, int(2*R/interval)+1, 1):
        Q = P1 + n.amplified(interval*i)
        seg = Polyline()
        seg.addPoint(Q - v.amplified(R))
        seg.addPoint(Q + v.amplified(R))
        parallels.append(seg)

    hatchSegs = []
    ca = ClipperAdaptor()
    clipper = Pyclipper()
    clipper.AddPaths(ca.toPaths(polygons), PT_CLIP, True)
    clipper.AddPaths(ca.toPaths(parallels), PT_SUBJECT, False)
    sln = clipper.Execute2(CT_INTERSECTION)
    for child in sln.Childs:
        if len(child.Contour) > 0:
            poly = ca.toPoly(child.Contour, z, False)
            seg = Segment(poly.startPoint(), poly.endPoint())
            hatchSegs.append(seg)

    return hatchSegs




def test_clipHatches():


    va = VtkAdaptor()

    va.drawSegment(Segment(Point3D(0, 0, 0), Point3D(200, 0, 0))).GetProperty().SetColor(1, 0, 0)
    va.drawSegment(Segment(Point3D(0, 0, 0), Point3D(0, 200, 0))).GetProperty().SetColor(1, 0, 0)

    layers = readSlcFile(r"C:\Users\Francis\Desktop\Rectangle5_10_0.8 at 0.4mm.slc")

    start = time.clock()

    for i in range(0, len(layers), 1):
        print(i)
        layer = layers[i]
        angle =  Utility.degToRad(45)

        segs = genSweepHatches(layer.contours, 1, angle)

        for contour in layer.contours:
            prop = va.drawPolyline(contour).GetProperty()
            prop.SetColor(0, 0, 0)
            prop.SetLineWidth(1)

        for seg in segs:
            prop = va.drawSegment(seg).GetProperty()
            prop.SetColor(1, 0, 0)
            pass

        # draw text on segs
        '''
        for i in range(len(segs)):
            textSrc = vtk.vtkVectorText()
            textSrc.SetText('%d'%i)
            textActor = va.drawPdSrc(textSrc)
            textActor.SetPosition(segs[i].A.x, segs[i].A.y, segs[i].A.z)
            textActor.SetScale(2)
            textActor.GetProperty().SetColor(0, 0, 0)
        '''
        #break

    end = time.clock()
    print("GenCpt time: %f CPU seconds" % (end - start))

    va.display()

def test_clipHatchesSegDir():
    A = Point3D(1, 1, 1)
    v = Vector3D(1, 1, 1)
    B = A - v.amplified(2)
    print(B)

    print(2**3)

    va = VtkAdaptor()

    va.drawSegment(Segment(Point3D(0, 0, 0), Point3D(200, 0, 0))).GetProperty().SetColor(1, 0, 0)
    va.drawSegment(Segment(Point3D(0, 0, 0), Point3D(0, 200, 0))).GetProperty().SetColor(1, 0, 0)

    rect = Polyline()
    rect.addPoint(Point3D(0, 0))
    rect.addPoint(Point3D(100, 0))
    rect.addPoint(Point3D(100, 100))
    rect.addPoint(Point3D(0, 100))
    rect.addPoint(Point3D(0, 0))

    angle = Utility.degToRad(0)
    segs = genClipHatches([rect], 4, angle)

    for seg in segs:
        prop = va.drawSegment(seg).GetProperty()
        prop.SetColor(1, 0, 0)
        pass

    # draw text on segs
    for i in range(len(segs)):
        textSrc = vtk.vtkVectorText()
        textSrc.SetText('%d' % i)
        textActor = va.drawPdSrc(textSrc)
        textActor.SetPosition(segs[i].A.x, segs[i].A.y, segs[i].A.z)
        textActor.SetScale(1.5)
        textActor.GetProperty().SetColor(1, 0, 0)


    va.display()



from VtkAdaptor import *
from SliceAlgo import *
import Utility
if __name__ == '__main__':

    test_clipHatches()