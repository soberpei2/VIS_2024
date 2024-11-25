import vtk
import inputfilereader_modularisiert as inputFileReader

class mbsModel:
    def __init__(self):
        self.objects = []  

    def addObject(self, mbsObject):
        self.objects.append(mbsObject)

    def show(self, renderer):
        for obj in self.objects:
            if isinstance(obj, inputFileReader.mbsObject.rigidBody):
                obj.show(renderer)
            elif isinstance(obj, inputFileReader.mbsObject.constraint):
                obj.show(renderer)
            elif isinstance(obj, inputFileReader.mbsObject.settings):
                obj.show(renderer)

    def get_objects(self):
        return self.objects
