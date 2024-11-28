from mbsObject import mbsObject

from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkActor
)
from vtkmodules.all import vtkMatrix4x4, vtkTransform

class body(mbsObject):
    def __init__(self,subtype,text,parameter):

        mbsObject.__init__(self,"Body",subtype,text,parameter)

class rigidBody(body):
    def __init__(self,text):
        parameter = {
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.]},
            "geometry": {"type": "filepath", "value": ""},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [1.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,1.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,1.]}
        }

        body.__init__(self,"Rigid_EulerParameter_PAI",text,parameter)

        # read OBJ file (CAD graphics)
        # this script assumes that .obj is located in current working directory
        reader = vtkOBJReader()
        reader.SetFileName(parameter["geometry"]["value"])  
        reader.Update()
        
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        bodyActor = vtkActor()
        self.actors.append(bodyActor)
        bodyActor.SetMapper(mapper)
        bodyActor.GetProperty().SetDiffuse(0.8)
        bodyActor.GetProperty().SetSpecular(0.3)
        bodyActor.GetProperty().SetSpecularPower(60.0)

        #create transformation matrix
        transformationMatrix = vtkMatrix4x4()
        transformationMatrix.Identity()
        for i in range(0,3):
            transformationMatrix.SetElement(i,3,parameter["position"]["value"][i])
            transformationMatrix.SetElement(i,0,parameter["x_axis"]["value"][i])
            transformationMatrix.SetElement(i,1,parameter["y_axis"]["value"][i])
            transformationMatrix.SetElement(i,2,parameter["z_axis"]["value"][i])

        #create and apply transformation by using transformation-matrix
        transform = vtkTransform()
        transform.SetMatrix(transformationMatrix)
        bodyActor.SetUserTransform(transform)