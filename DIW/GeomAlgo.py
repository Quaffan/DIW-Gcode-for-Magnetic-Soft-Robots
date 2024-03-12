from GeomBase import *
from Line import *
from Ray import *
from Segment import *
from Plane import *
from Polyline import *

def nearZero(x):
    if math.fabs(x) < epsilon:
        return True
    return False

def distance(obj1, obj2):
    if isinstance(obj1, Point3D) and isinstance(obj2, Line):
        P, Q, V = obj2.P, obj1, obj2.V
        t = P.pointTo(Q).dotProduct(V)
        R = P + V.amplified(t)
        return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Ray):
        P, Q, V = obj2.P, obj1, obj2.V
        t = P.pointTo(Q).dotProduct(V)
        if t >= 0:
            R = P + V.amplified(t)
            return Q.distance(R)
        else:
            return Q.distance(P)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Segment):
        Q, P, P1, V = obj1, obj2.A, obj2.B, obj2.direction().normalized()
        L = obj2.length()
        t = P.pointTo(Q).dotProduct(V)
        if t <= 0:
            return Q.distance(P)
        elif t >= L:
            return Q.distance(P1)
        else:
            R = P + V.amplified(t)
            return Q.distance(R)
    elif isinstance(obj1, Point3D) and isinstance(obj2, Plane):
        P, Q, N = obj2.P, obj1, obj2.N
        angle = N.getAngle(P.pointTo(Q))
        return P.distance(Q)*math.cos(angle)
    elif isinstance(obj1, Line) and isinstance(obj2, Line):
        P1, V1, P2, V2 = obj1.P, obj1.V, obj2.P, obj2.V
        N = V1.crossProduct(V2)
        if N.isZeroVector():
            return distance(P1, obj2)
        else:
            return distance(P1, Plane(P2, N))
    elif isinstance(obj1, Line) and isinstance(obj2, Plane):
        if obj1.V.dotProduct(obj2.N) == 0:
            return distance(obj1.P, obj2)
        else:
            return 0
    elif isinstance(obj1, Ray) and isinstance(obj2, Plane):
        pass
    elif isinstance(obj1, Segment) and isinstance(obj2, Plane):
        pass
    pass

def intersectLineLine(line1 : Line, line2 : Line):
    P1, V1, P2, V2 = line1.P, line1.V, line2.P, line2.V
    P1P2 = P1.pointTo(P2)
    deno = V1.dy * V2.dx - V1.dx * V2.dy
    if deno != 0:
        t1 = -(-P1P2.dy * V2.dx + P1P2.dx * V2.dy) / deno
        t2 = -(-P1P2.dy * V1.dx + P1P2.dx * V1.dy) / deno
        return P1 + V1.amplified(t1), t1, t2
    else:
        deno = V1.dz * V2.dy - V1.dy * V2.dz
        if deno != 0:
            t1 = -(-P1P2.dz * V2.dy + P1P2.dy * V2.dz) / deno
            t2 = -(-P1P2.dz * V1.dy + P1P2.dy * V1.dz) / deno
            return P1 + V1.amplified(t1), t1, t2
        else:
            return None, 0, 0

def intersectSegmentPlane(seg : Segment, plane : Plane):
    A, B, P, N = seg.A, seg.B, plane.P, plane.N
    V = A.pointTo(B)
    PA = P.pointTo(A)
    if V.dotProduct(N) == 0:
        return None
    else:
        t = -(PA.dotProduct(N)) / V.dotProduct(N)
        if t >= 0 and t <= 1:
            return A + (V.amplified(t))
        else:
            return None

def intersect(obj1, obj2):
    try:
        if isinstance(obj1, Line) and isinstance(obj2, Line):
            P, t1, t2 = intersectLineLine(obj1, obj2)
            return P
        elif isinstance(obj1, Segment) and isinstance(obj2, Segment):
            line1, line2 = Line(obj1.A, obj1.direction()), Line(obj2.A, obj2.direction())
            P, t1, t2 = intersectLineLine(line1, line2)
            if P is not None:
                if t1 >= 0 and t1 <= obj1.length() and t2 >= 0 and t2 <= obj2.length():
                    return P
            return None
        elif isinstance(obj1, Line) and isinstance(obj2, Segment):
            line1, line2 = obj1, Line(obj2.A, obj2.direction())
            P, t1, t2 = intersectLineLine(line1, line2)
            len = obj2.length()
            if P is not None and t2 >= 0 and t2 <= obj2.length():
                return P
            return None
        elif isinstance(obj1, Line) and isinstance(obj2, Ray):
            pass
        elif isinstance(obj1, Ray) and isinstance(obj2, Segment):
            pass
        elif isinstance(obj1, Ray) and isinstance(obj2, Ray):
            pass
        elif isinstance(obj1, Line) and isinstance(obj2, Plane):
            P0, V, P1, N = obj1.P, obj1.V, obj2.P, obj2.N
            dotPro = V.dotProduct(N)
            if dotPro != 0:
                t = P0.pointTo(P1).dotProduct(N) / dotPro
                return P0 + V.amplified(t)
            else:
                return None
        elif isinstance(obj1, Ray) and isinstance(obj2, Plane):
            pass
        elif isinstance(obj1, Segment) and isinstance(obj2, Plane):
            return intersectSegmentPlane(obj1, obj2)
        pass
    except:
        return None


def pointOnRay(p : Point3D, ray : Ray):
    v = ray.P.pointTo(p)
    if v.dotProduct(ray.V) >= 0 and v.crossProduct(ray.V).isZeroVector():
        return True
    return False

# 1 inside, 0 outside, -1 on
def pointInPolygon(p : Point3D, polygon : Polyline):
    passCount = 0
    ray = Ray(p, Vector3D(1, 0, 0))
    segments = []
    for i in range(polygon.count() - 1):
        seg = Segment(polygon.point(i), polygon.point(i + 1))
        segments.append(seg)
    for seg in segments:
        if seg.length() == 0: continue
        line1, line2 = Line(ray.P, ray.V), Line(seg.A, seg.direction())
        P, t1, t2 = intersectLineLine(line1, line2)
        if P is not None:
            if nearZero(t1):
                return -1
            elif seg.A.y != p.y and seg.B.y != p.y and t1 > 0 and t2 > 0 and t2 < seg.length():
                passCount += 1
    upSegments, downSegments = [], []
    for seg in segments:
        if seg.A.isIdentical(ray.P) or seg.B.isIdentical(ray.P):
            return -1
        elif pointOnRay(seg.A, ray) ^ pointOnRay(seg.B, ray):
            if seg.A.y >= p.y and seg.B.y >= p.y:
                upSegments.append(seg)
            elif seg.A.y <= p.y and seg.B.y <= p.y:
                downSegments.append(seg)
    passCount += min(len(upSegments), len(downSegments))
    if passCount % 2 == 1:
        return 1
    return 0


def intersectTrianglePlane(triangle, plane):
    AB = Segment(triangle.A, triangle.B)
    AC = Segment(triangle.A, triangle.C)
    BC = Segment(triangle.B, triangle.C)
    c1 = intersectSegmentPlane(AB, plane)
    c2 = intersectSegmentPlane(AC, plane)
    c3 = intersectSegmentPlane(BC, plane)
    if c1 is None:
        if c2 is not None and c3 is not None:
            if c2.distance(c3) != 0.0:     # if only one point of a triangle touches the plane, they don't intersect
                return Segment(c2, c3)
    elif c2 is None:
        if c1 is not None and c3 is not None:
            if c1.distance(c3) != 0.0:
                return Segment(c1, c3)
    elif c3 is None:
        if c1 is not None and c2 is not None:
            if c1.distance(c2) != 0.0:
                return Segment(c1, c2)
    elif c1 is not None and c2 is not None and c3 is not None:
        if c1.isIdentical(c2):
            return Segment(c1, c3)
        else:
            return Segment(c1, c2)
    return None

def intersectTriangleZPlane(triangle, z):
    if triangle.zMinPnt().z > z or triangle.zMaxPnt().z < z:
        return None
    line = intersectTrianglePlane(triangle, Plane.zPlane(z))
    return line

# 2020-3-2 去掉函数，改成参数带center
'''
def rotatePolygons(polygons, axis, angle):
    m = Matrix3D.createRotateMatrix(axis, angle)
    newPolys = []
    for poly in polygons:
        newPolys.append(poly.multiplied(m))
    return newPolys
'''

def rotatePolygons(polygons, angle, center = None):
    dx = 0 if center is None else center.x
    dy = 0 if center is None else center.y
    mt = Matrix3D.createTranlsateMatrix(-dx, -dy, 0)
    mr = Matrix3D.createRotateMatrix('Z', angle)
    mb = Matrix3D.createTranlsateMatrix(dx, dy, 0)
    m = mt * mr * mb
    newPolys = []
    for poly in polygons:
        newPolys.append(poly.multiplied(m))
    return newPolys

def adjustPolygonDirs(polygons):
    for i in range(len(polygons)):
        pt = polygons[i].startPoint()
        insideCount  = 0
        for j in range(len(polygons)):
            if j == i:
                continue
            restPoly = polygons[j]
            if 1== pointInPolygon(pt, restPoly):
                insideCount  += 1
        if insideCount % 2 == 0:
            polygons[i].makeCCW()
        else:
            polygons[i].makeCW()

if __name__ == '__main__':
    p = Point3D(1, 1, 1)
    ln = Line(Point3D(2, 2, 2), Vector3D(1, 1, 1))
    pln = Plane(Point3D(0,0,0), Vector3D(1, 2, 3))
    print(distance(p, ln))
    print(distance(p, pln))

    v1 = Vector3D(1, 0, 0)
    v2 = Vector3D(2, 0, 0)
    print(v1.crossProduct(v2))



    poly = Polyline()
    poly.addPoint(Point3D(0, 0, 0))
    poly.addPoint(Point3D(20, 0, 0))
    poly.addPoint(Point3D(20, 20, 0))
    poly.addPoint(Point3D(60, 20, 0))
    poly.addPoint(Point3D(60, 0, 0))
    poly.addPoint(Point3D(100, 0, 0))
    poly.addPoint(Point3D(100, 20, 0))
    poly.addPoint(Point3D(100, 100, 0))
    poly.addPoint(Point3D(90, 100, 0))
    poly.addPoint(Point3D(90, 20, 0))
    poly.addPoint(Point3D(80, 20, 0))
    poly.addPoint(Point3D(80, 100, 0))
    poly.addPoint(Point3D(0, 100, 0))
    poly.addPoint(Point3D(0, 0, 0))

    p = Point3D(19, 20, 0)
    print(pointInPolygon(p, poly))

    poly1 = Polyline()
    poly1.addPoint(Point3D(0, 0))
    poly1.addPoint(Point3D(100, 0))
    poly1.addPoint(Point3D(100, 50))
    poly1.addPoint(Point3D(60, 50))
    poly1.addPoint(Point3D(60, 0))
    poly1.addPoint(Point3D(40, 0))
    poly1.addPoint(Point3D(40, 50))
    poly1.addPoint(Point3D(0, 50))
    poly1.addPoint(Point3D(0, 0))

    p = Point3D(60, 40)
    print(pointInPolygon(p, poly1))