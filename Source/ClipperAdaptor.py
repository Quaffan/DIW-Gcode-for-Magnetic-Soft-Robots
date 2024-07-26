from pyclipper import *
from Polyline import *

class ClipperAdaptor:
    def __init__(self, digits = 7):
        self.f = math.pow(10, digits)
        self.arcTolerance = 0.005  # mm
        pass

    def toPath(self, poly): # clipper poly
        path = []
        for pt in poly.points:
            path.append((pt.x * self.f, pt.y * self.f))
        return path

    def toPaths(self, polys):
        paths = []
        for poly in polys:
            paths.append(self.toPath(poly))
        return paths

    def toPoly(self, path, z = 0, closed = True):
        poly = Polyline()
        for tp in path:
            poly.addPoint(Point3D(tp[0] / self.f, tp[1] / self.f, z))
        if len(path) > 0 and closed:
            poly.addPoint(poly.startPoint())
        return poly

    def toPolys(self, paths, z = 0, closed = True):
        polys = []
        for path in paths:
            polys.append(self.toPoly(path, z, closed))
        return polys

    def offset(self, polys, delta, jt = JT_SQUARE):
        pco = PyclipperOffset()
        pco.ArcTolerance = self.arcTolerance * self.f
        pco.AddPaths(self.toPaths(polys), jt, ET_CLOSEDPOLYGON)
        sln = pco.Execute(delta * self.f)
        return self.toPolys(sln, polys[0].point(0).z)

    def pointInPolygon(self, pt, poly):
        path = self.toPath(poly)
        return PointInPolygon((pt.x*self.f, pt.y*self.f), path)

    def simplifyPolygons(self, polys):
        paths = self.toPaths(polys)
        return self.toPolys(SimplifyPolygons(paths), polys[0].point(0).z)

    def cleanPolygons(self, polys):
        paths = self.toPaths(polys)
        return self.toPolys(CleanPolygons(paths), polys[0].point(0).z)

    # new
    def clip(self, subjPolys, clipPolys, clipType, z = 0, minArea = 0.01):
        clipper = Pyclipper()
        clipper.AddPaths(self.toPaths(subjPolys), PT_SUBJECT)
        clipper.AddPaths(self.toPaths(clipPolys), PT_CLIP)
        sln = clipper.Execute(clipType)
        slnPolys = self.toPolys(sln, z)
        for i in range(len(slnPolys)-1,-1,-1):
            if math.fabs(slnPolys[i].getArea()) < minArea:
                del slnPolys[i]
        return slnPolys


