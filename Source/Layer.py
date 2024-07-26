import GeomAlgo

class Layer:
    def __init__(self, z):
        self.z = z
        self.segments = []
        self.contours = []

        self.sptContours = []
        self.sptDpPaths = []
        self.sptCpPaths = []

        self.shellContours = []
        self.ffContours = []
        self.sfContours = []

    def drawSegments(self, vtkAdaptor, clr, lineWidth):
        for seg in self.segments:
            vtkAdaptor.drawSegment(seg)

    def sortLinesToPolylines(self):
        self.polylines = GeomAlgo.sortLinesToPolylines_stupid(self.lines)

