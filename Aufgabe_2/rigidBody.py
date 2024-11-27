import vtk
from Aufgabe_2 import mbsObject

class rigidBody(mbsObject):
    # Constructor
    #------------
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        parameter = {
                        "mass": {
                                    "type": "float",
                                    "value": 1.
                                },
                        "COG": {
                                    "type": "vector",
                                    "value": [0., 0., 0.]
                               }
                    }

        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht übergeben)
        mbsObject.__init__(self, "rigidBody", "Rigid_EulerParameter_PAI", text, parameter)

    def add_vtk_representation(self):
        reader = vtk.vtkOBJReader()
        reader.SetFileName("path/to/your/model.obj")
        reader.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(mapper)
        self.vtk_actor.GetProperty().SetColor(0.5, 0.5, 1.0)

    def writeInputfile(self, file):
        super().writeInputfile(file)