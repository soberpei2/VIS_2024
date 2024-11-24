from mbsObject import mbsObject
import vtk

class measure(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "type": {"type": "str", "value": "testType"},
            "componet": {"type": "int", "value": 0},
            "location_body1": {"type": "vector", "value": [0.,0.,0.]},
            "location_body2": {"type": "vector", "value": [0.,0.,0.]},
            "use_initial_value": {"type": "bool", "value": 0},
        }

        mbsObject.__init__(self,"Measure","Translational",text,parameter)
    

        size = 10
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(size)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())
        self.actor.SetMapper(mapper)

        transform = vtk.vtkTransform()
        position = parameter["location_body1"]["value"]
        transform.Translate(position[0], position[1], position[2])
        self.actor.SetUserTransform(transform)