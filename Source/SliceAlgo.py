from GeomAlgo import *
from Layer import *
from VtkAdaptor import *
from StlModel import *
import vtk
import struct
from IntersectStl_sweep import *
from IntersectStl_match import *
from LinkSegs_dorder import *
from LinkSegs_dlook import *
from TopoSlicer import *


def intersectStl_brutal(stlModel, layerThk):
    layers = []
    xMin, xMax, yMin, yMax, zMin, zMax = stlModel.getBounds()
    z = zMin + layerThk
    while z < zMax:
        layer = Layer(z)
        for tri in stlModel.triangles:
            seg = intersectTriangleZPlane(tri, z)
            if seg is not None:
                layer.segments.append(seg)
        layers.append(layer)
        z += layerThk
    return layers

#   linkSegments_brutal
def linkSegs_brutal(segs):
    segs = list(segs)
    contours = []
    while len(segs) > 0:
        contour = Polyline()
        contours.append(contour)
        while len(segs) > 0:
            for seg in segs:
                if contour.appendSegment(seg):
                    segs.remove(seg)
                    break
            if contour.isClosed():
                break
    return contours

def writeSlcFile(layers, path):
    f = None
    try:
        f = open(path, 'w+b')
        f.write(bytes("-SLCVER 2.0 -UNIT MM", encoding='utf-8'))
        f.write(bytes([0x0d, 0x0a, 0x1a]))
        f.write(bytes([0x00]*256))
        f.write(struct.pack('b', 1))
        f.write(struct.pack('4f', 0, 0, 0, 0))
        for layer in layers:
            f.write(struct.pack('fI', layer.z, len(layer.contours)))
            for contour in layer.contours:
                f.write(struct.pack('2I', contour.count(), 0))
                for pt in contour.points:
                    f.write(struct.pack('2f', pt.x, pt.y))
        f.write(struct.pack('fI', layers[-1].z, 0xFFFFFFFF))
    except Exception as ex:
        print("writeSlcFile exception:", ex)
    finally:
        if f: f.close()

def readSlcFile(path):
    f = None
    layers = []
    try:
        f = open(path, 'rb')
        data = f.read()
        i = 0
        while True:
            if data[i] == 0x0d and data[i+1] == 0x0a and data[i+2] == 0x1a:
                break
            i += 1
        i += (3 + 256)
        channelCount = data[i]
        i += (1 + channelCount * 16)
        while True:
            z, = struct.unpack('f', data[i: i+4])
            i += 4
            contourCount, = struct.unpack('I', data[i: i+4])
            i += 4
            if contourCount == 0xFFFFFFFF:
                break
            layer = Layer(z)
            for j in range(contourCount):
                pointCount, = struct.unpack('I', data[i: i+4])
                i += 4
                gapCount, = struct.unpack('I', data[i: i+4])
                i += 4
                contour = Polyline()
                for k in range(pointCount):
                    x, y = struct.unpack('2f', data[i: i+8])
                    i += 8
                    contour.addPoint(Point3D(x, y, z))
                layer.contours.append(contour)
            layers.append(layer)
    except Exception as ex:
        print("readSlcFile exception:", ex)
    finally:
        if f: f.close()
        return layers

def intersectStl_sweep(stlModel, layerThk):
    return IntersectStl_sweep(stlModel, layerThk).layers

def intersectStl_match(stlModel, layerThk):
    return IntersectStl_match(stlModel, layerThk).layers

def linkSegs_dorder(segs):
    return LinkSegs_dorder(segs).contours

def linkSegs_dlook(segs):
    return LinkSegs_dlook(segs).contours

def slice_combine(stlModel, layerThk):
    layers = intersectStl_sweep(stlModel, layerThk)
    for layer in layers:
        layer.contours = linkSegs_dlook(layer.segments)
        layer.segments.clear()
        adjustPolygonDirs(layer.contours)
    return layers

def slice_topo(stlModel, layerThk):
    return TopoSlicer(stlModel, layerThk).layers



if __name__ == '__main__':
    # f = 2
    # fb = struct.pack('1b', f)
    # gb = struct.pack('1f', f)
    # print(fb)
    # xf = struct.unpack('b', fb)
    # print(xf)
    #
    #
    # if True:
    #     layers = readSlcFile("E:\\man head.slc")
    #
    #     vtkAdaptor = VtkAdaptor()
    #     #vtkAdaptor.drawAxes()
    #     print(len(layers))
    #     for i in range(0, len(layers), 20):
    #         layer = layers[i]
    #         for seg in layer.contours:
    #             segActor = vtkAdaptor.drawPolyline(seg)
    #             segActor.GetProperty().SetColor(0, 0, 0)
    #             segActor.GetProperty().SetLineWidth(1)
    #
    #     vtkAdaptor.display()
    # else:
    #     vtkAdaptor = VtkAdaptor()
    #
    #     vtkStlReader = vtk.vtkSTLReader()
    #     vtkStlReader.SetFileName("E:\\model.STL")
    #     vtkAdaptor.drawPdSrc(vtkStlReader).GetProperty().SetOpacity(0.1)
    #
    #
    #     stlModel = StlModel()
    #     stlModel.extractFromVtkStlReader(vtkStlReader)
    #
    #     print(stlModel.getFacetNumber())
    #     print(stlModel.getBounds())
    #
    #
    #     layers = slice_brutal(stlModel, 1.5)
    #     for layer in layers:
    #         segments2Contours_brutal(layer)
    #         for seg in layer.contours:
    #             segActor = vtkAdaptor.drawPolyline(seg)
    #             segActor.GetProperty().SetColor(0, 0, 0)
    #             segActor.GetProperty().SetLineWidth(2)
    #
    #         indentifyContourDirections(layer.contours)
    #
    #         for poly in layer.contours:
    #             print(poly.isCCW())
    #
    #         #break
    #
    #     writeSlcFile(layers, "E:\\model.slc")
    #
    #
    #
    #     vtkAdaptor.display()
    va = VtkAdaptor()
    vtkStlReader = vtk.vtkSTLReader()
    vtkStlReader.SetFileName(r"D:\Research\Model\MSR.STL")
    # va.drawPdSrc(vtkStlReader).GetProperty().SetOpacity(0.5)
    stlModel = StlModel()
    stlModel.extractFromVtkStlReader(vtkStlReader)
    layers = intersectStl_brutal(stlModel, 0.2)
    for layer in layers:
        layer.contours = linkSegs_brutal(layer.segments)
        for contour in layer.contours:
            polyActor = va.drawPolyline(contour)
            polyActor.GetProperty().SetLineWidth(2)
            polyActor.GetProperty().SetColor(0, 0, 0)
    va.display()
