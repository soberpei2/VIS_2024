from mbsObject import mbsObject
import vtk

def measureSphere(position):
    size = 0.5
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(size)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    transform = vtk.vtkTransform()
    transform.Translate(position[0], position[1], position[2])
    actor.SetUserTransform(transform)
    return actor

class measure(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "type": {"type": "str", "value": "testType"},
            "component": {"type": "int", "value": 0},
            "location_body1": {"type": "vector", "value": [0.,0.,0.]},
            "location_body2": {"type": "vector", "value": [0.,0.,0.]},
            "use_initial_value": {"type": "bool", "value": 0},
        }

        mbsObject.__init__(self,"Measure","Translational",text,parameter)
    

        assembly = vtk.vtkAssembly()
        assembly.AddPart(measureSphere(parameter["location_body1"]["value"]))
        assembly.AddPart(measureSphere(parameter["location_body2"]["value"]))

        self.actor = assembly
    
    '''
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "type": {"type": "str", "value": "testType"},
            "vector_body1": {"type": "int", "value": 0},
            "vector1_body1": {"type": "vector", "value": [0.,0.,0.]},
            "vector2_body2": {"type": "vector", "value": [0.,0.,0.]},
            "use_initial_value": {"type": "bool", "value": 0},
        }

        mbsObject.__init__(self,"Measure","Rotational",text,parameter)
    

        assembly = vtk.vtkAssembly()
        assembly.AddPart(measureSphere(parameter["location_body1"]["value"]))
        assembly.AddPart(measureSphere(parameter["location_body2"]["value"]))

        self.actor=assembly
    '''