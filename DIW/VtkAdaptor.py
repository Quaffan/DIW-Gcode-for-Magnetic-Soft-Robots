import vtk
from Segment import *
from Polyline import *

class VtkAdaptor:
    def __init__(self, bgClr = (0.95, 0.95, 0.95)):
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(bgClr)
        #self.renderer.GetActiveCamera().ParallelProjectionOn()
        self.window = vtk.vtkRenderWindow()
        self.window.AddRenderer(self.renderer)
        self.window.SetSize(600,600)
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()

    def display(self):
        self.interactor.Start()
        del self.renderer
        del self.window
        del self.interactor

    def setBackgroundColor(self, r, g, b):
        return self.renderer.SetBackground(r, g, b)

    def drawAxes(self, length = 100.0):
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(length, length, length)
        axes.SetShaftType(0)
        axes.SetCylinderRadius(length / 10000.0)
        axes.SetConeRadius(length / 500.0)
        axes.SetAxisLabels(0)
        self.renderer.AddActor(axes)
        return axes

    def drawActor(self, actor):
        self.renderer.AddActor(actor)
        return actor

    def drawPdSrc(self, pdSrc):
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(pdSrc.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        #actor.GetProperty().SetRepresentationToWireframe()
        return self.drawActor(actor)

    def drawStlModel(self, stlFilePath):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(stlFilePath)
        return self.drawPdSrc(reader)

    def removeActor(self, actor):
        self.renderer.RemoveActor(actor)

    def drawPoint(self, point, radius = 2.0):
        src = vtk.vtkSphereSource()
        src.SetCenter(point.x, point.y, point.z)
        src.SetRadius(radius)
        return self.drawPdSrc(src)

    def drawSegment(self, seg):
        src = vtk.vtkLineSource()
        src.SetPoint1(seg.A.x, seg.A.y, seg.A.z)
        src.SetPoint2(seg.B.x, seg.B.y, seg.B.z)
        return self.drawPdSrc(src)

    def drawPolyline(self, polyline):
        src = vtk.vtkLineSource()
        points = vtk.vtkPoints()
        for i in range(polyline.count()):
            pt = polyline.point(i)
            points.InsertNextPoint((pt.x, pt.y, pt.z))
        src.SetPoints(points)
        return self.drawPdSrc(src)


if __name__ == '__main__':
    vtkAdaptor = VtkAdaptor()

    vtkAdaptor.drawAxes()
    vtkAdaptor.setBackgroundColor(0.95, 0.95, 0.95)

    vtkAdaptor.drawPoint(Point3D(10, 10, 10)).GetProperty().SetColor(1, 0, 0)
    vtkAdaptor.drawPoint(Point3D(50, 50, 50)).GetProperty().SetColor(1, 0, 0)

    polyline = Polyline()
    polyline.addPoint(Point3D(1,1,1))
    polyline.addPoint(Point3D(50, 2, 10))
    polyline.addPoint(Point3D(20, 10, 30))
    polyline.addPoint(Point3D(50, 80, 55))
    polylineActor = vtkAdaptor.drawPolyline(polyline)
    polylineActor.GetProperty().SetColor(0.1, 0.7, 0.7)
    polylineActor.GetProperty().SetLineWidth(2)

    #stlActor = vtkAdaptor.drawStlModel("E:\\3DP.STL")
    #stlActor.SetPosition(0, 150, 150)

    textSrc = vtk.vtkTextSource()
    textSrc.SetText("sdf")
    vtkAdaptor.drawPdSrc(textSrc)

    vTextSrc = vtk.vtkVectorText()
    vTextSrc.SetText('ssfsdf')
    actor = vtkAdaptor.drawPdSrc(vTextSrc)
    actor.SetPosition(100, 100, 0)
    actor.SetScale(2)
    actor.GetProperty().SetColor(1, 0, 0)

    vtkAdaptor.display()

    actor.RotateY()




