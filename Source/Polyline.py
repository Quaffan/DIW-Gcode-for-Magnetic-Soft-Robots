from GeomBase import *
import pyclipper
import copy

class Polyline:
    def __init__(self):
        self.points = []

    def __str__(self):
        if self.count() > 0:

            return "Polyline\nPoint number: %s\nStart %s\nEnd %s\n" \
                   % (self.startPoint(), str(self.endPoint()), str(self.endPoint()))
        else:
            return 'Polyline\nPoint number: 0\n'

    def clone(self):
        poly = Polyline()
        for pt in self.points:
            poly.addPoint(pt.clone())
        return poly

    def count(self):
        return len(self.points)

    def addPoint(self, pt):
        self.points.append(pt)

    def addTuple(self, tuple):
        self.points.append(Point3D(tuple[0], tuple[1], tuple[2]))

    def raddPoint(self, pt):
        self.points.insert(0, pt)

    def removePoint(self, index):
        return self.points.pop(index)

    def point(self, index):
        return self.points[index]

    def startPoint(self):
        return self.points[0]

    def endPoint(self):
        return self.points[-1]

    def isClosed(self):
        if self.count() <= 2:
            return False
        return self.startPoint().isCoincide(self.endPoint())

    def getArea(self):
        area = 0.0
        for i in range(self.count() - 1):
            area += 0.5 * (self.points[i].x* self.points[i+1].y - self.points[i+1].x* self.points[i].y)
        return area

    def reverse(self):
        sz = self.count()
        for i in range(int(sz/2)):
            self.points[i], self.points[sz-1-i] = self.points[sz-1-i], self.points[i]

    def makeCCW(self):
        if self.getArea() < 0:
            self.reverse()

    def makeCW(self):
        if self.getArea() > 0:
            self.reverse()

    def isCCW(self):
        if self.getArea() > 0:
            return True
        return False

    def translate(self, vec):
        for i in range(len(self.points)):
            self.points[i].translate(vec)

    def appendSegment(self, seg):
        if self.count() == 0:
            self.points.append(seg.A)
            self.points.append(seg.B)
        else:
            startPnt = self.startPoint()
            endPnt = self.endPoint()
            if seg.A.isCoincide(endPnt):
                self.addPoint(seg.B)
            elif seg.B.isCoincide(endPnt):
                self.addPoint(seg.A)
            elif seg.A.isCoincide(startPnt):
                self.raddPoint(seg.B)
            elif seg.B.isCoincide(startPnt):
                self.raddPoint(seg.A)
            else:
                return False
        return True

    def multiply(self, m):
        for pt in self.points:
            pt.multiply(m)

    def multiplied(self, m):
        poly = Polyline()
        for pt in self.points:
            poly.addPoint(pt*m)
        return poly

    # make the polyline simpler, remove co-line points
    def simplify(self):
        z = self.points[0].Z()
        poly = pyclipper.SimplifyPolygon(self.toIntTuple2DList())
        self.fromIntTuple2DList(poly, z)

    def simplified(self):
        z = self.points[0].Z()
        poly = pyclipper.SimplifyPolygon(self.toIntTuple2DList())
        myPoly = Polyline()
        myPoly.fromIntTuple2DList(poly, z)
        return myPoly

    def clean(self, delta = 0.001):
        z = self.points[0].Z()
        f = 1.0/delta
        pts = self.toIntTuple2DList(f)
        poly = pyclipper.CleanPolygon(pts)
        self.fromIntTuple2DList(poly, z = z, f = f)
        self.addPoint(self.startPoint())


    def toVtkActor(self,  clr= (1,0,0)):
        return DrawBase.initPolylineActor(self.points, clr)

    # clipper 多边形接口
    def toTuple2DList(self):
        list = []
        for pt in self.points:
            list.append(pt.toTuple2D())
        return list

    def fromTuple2DList(self, tuple2DList, z):
        self.points.clear()
        for pt in tuple2DList:
            p3d = Point3D(pt[0], pt[1], z)
            self.points.append(p3d)

    def toIntTuple2DList(self, f = 1.0e15):
        list = []
        for pt in self.points:
            list.append((pt.X()*1.0e15, pt.Y()*f))
        return list

    def fromIntTuple2DList(self, tuple2DList, z = 0, f = 1.0e15):
        self.points.clear()
        for pt in tuple2DList:
            p3d = Point3D(pt[0]/1.0e15, pt[1]/f, z)
            self.points.append(p3d)
            
    @staticmethod
    def __add__(self, other):
            answer = copy.deepcopy(self)
            answer.points += other.points
            return answer


def writePolyline(path, polyline : Polyline):
    f = None
    try:
        f = open(path, 'w')
        f.write('%s\n' % polyline.count())
        for pt in polyline.points:
            txt = '%s,%s,%s\n'%(pt.x, pt.y, pt.z)
            f.write(txt)
    except Exception as ex:
        print(ex)
    finally:
        if f: f.close()

def readPolyline(path):
    f = None
    try:
        f = open(path, 'r')
        poly = Polyline()
        number = int(f.readline())
        for i in range(number):
            txt = f.readline()
            txts = txt.split(',')
            x, y, z = float(txts[0]), float(txts[1]), float(txts[2])
            poly.addPoint(Point3D(x,y,z))
        return poly
    except Exception as ex:
        print(ex)
    finally:
        if f: f.close()

    

if __name__ == '__main__':
    readPolyline("Asdf")