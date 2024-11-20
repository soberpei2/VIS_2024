import mbsObject as mbsObj
import os

from vtkmodules.all import (
    vtkCylinderSource,
    vtkOBJReader,
    vtkPolyDataMapper,
    vtkTransform,
    vtkMatrix4x4
)

class rigidBody(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"body","rigidBody",input,[])
        else:
            parameter = {
                "name": {"type":"string", "value":"init"},
                "geometry": {"type":"geometry", "value":"path"},
                "position": {"type":"vector", "value":[0,0,0]},
                "x_axis": {"type":"vector", "value":[0,0,0]},
                "y_axis": {"type":"vector", "value":[0,0,0]},
                "z_axis": {"type":"vector", "value":[0,0,0]},
                "color": {"type":"color", "value":[0,0,0,0]},
                "transparency": {"type":"int", "value":0},
                "initial velocity": {"type":"vector", "value":[0,0,0]},
                "initial omega": {"type":"vector", "value":[0,0,0]},
                "consider vel inertia forces:": {"type":"int", "value":0},
                "mass": {"type":"float", "value":1.},
                "COG": {"type":"vector", "value":[0,0,0]},
                "inertia": {"type":"vector", "value":[0,0,0]},
                "i1_axis": {"type":"vector", "value":[1,0,0]},
                "i2_axis": {"type":"vector", "value":[0,1,0]},
                "i3_axis": {"type":"vector", "value":[0,0,1]}
                }
            
            mbsObj.mbsObject.__init__(self,"body","rigidBody",input,parameter)

        geometry = self.parameter["geometry"]["value"]
        if(len(geometry) == 1):
            extension = geometry[0].split(".")[1]
            if(extension == 'obj'):
                dir = "C:\\Users\\Stefan\\Documents\\FH-Wels\\VIS3IL\\VIS_2024\\Aufgabe_2\\quader.obj"
                reader = vtkOBJReader()
                reader.SetFileName(dir)

                mapper = vtkPolyDataMapper()
                mapper.SetInputConnection(reader.GetOutputPort())
                self.actor.SetMapper(mapper)
                self.actor.GetProperty().SetDiffuse(0.8)
                self.actor.GetProperty().SetSpecular(0.3)
                self.actor.GetProperty().SetSpecularPower(60.0)
        else:
            if(geometry[0] == "Cylinder"):
                cylinderSource = vtkCylinderSource()
                cylinderSource.SetRadius(self.str2float(geometry[1])/2)
                cylinderSource.SetHeight(self.str2float(geometry[2]))
                cylinderSource.SetResolution(100)

                mapper = vtkPolyDataMapper()
                mapper.SetInputConnection(cylinderSource.GetOutputPort())
                self.actor.SetMapper(mapper)

        color = self.parameter["color"]["value"]
        self.actor.GetProperty().SetColor(color[0]/255,color[1]/255,color[2]/255)
        
        transformationMatrix = vtkMatrix4x4()
        transformationMatrix.Identity()
        for i in range(0,3):
            transformationMatrix.SetElement(i,3,self.parameter["position"]["value"][i])
            transformationMatrix.SetElement(i,0,self.parameter["x_axis"]["value"][i])
            transformationMatrix.SetElement(i,1,self.parameter["y_axis"]["value"][i])
            transformationMatrix.SetElement(i,2,self.parameter["z_axis"]["value"][i])

        transform = vtkTransform()
        transform.SetMatrix(transformationMatrix)
        self.actor.SetUserTransform(transform)