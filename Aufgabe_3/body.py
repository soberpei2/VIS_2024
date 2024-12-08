from mbsObject import mbsObject
import vtk
import os
import numpy as np


class body(mbsObject):
    def __init__(self, subtype, **kwargs):
        mbsObject.__init__(self, "Body", subtype, **kwargs)

    def getPosition(self):
        return self.parameter["position"]["value"]
    
    def getCOG(self):
        return self.parameter["position"]["value"]

class rigidBody(body):
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "name": {"type": "str", "value": "testName"},
                "geometry": {"type": "path", "value": "testPathGeometry"},
                "position": {"type": "vector", "value": [0.,0.,0.]},
                "x_axis": {"type": "vector", "value": [0.,0.,0.]},
                "y_axis": {"type": "vector", "value": [0.,0.,0.]},
                "z_axis": {"type": "vector", "value": [0.,0.,0.]},
                "color": {"type": "vectorInt", "value": [0,0,0]},
                "transparency": {"type": "int", "value": 0},
                "initial velocity": {"type": "vector", "value": [0.,0.,0.]},
                "initial omega": {"type": "vector", "value": [0.,0.,0.]},
                "consider vel inertia forces": {"type": "bool", "value": 0},
                "mass": {"type": "float", "value": 0.},
                "COG": {"type": "vector", "value": [0.,0.,0.]},
                "inertia": {"type": "vector", "value": [0.,0.,0.]},
                "i1_axis": {"type": "vector", "value": [0.,0.,0.]},
                "i2_axis": {"type": "vector", "value": [0.,0.,0.]},
                "i3_axis": {"type": "vector", "value": [0.,0.,0.]}
            }
    
            body.__init__(self, "Rigid_EulerParameter_PAI", text = kwargs["text"],parameter=parameter)


        else:
            body.__init__(self, "Rigid_EulerParameter_PAI", **kwargs)

        color = [channel / 255 for channel in self.parameter["color"]["value"]]
        #opacity = 1 - self.parameter["transparency"]["value"]/100
        opacity = 0.5
          
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        reader.Update()
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        bodyActor = vtk.vtkActor()
        bodyActor.SetMapper(mapper)
        bodyActor.GetProperty().SetDiffuse(0.8)
        bodyActor.GetProperty().SetSpecular(0.3)
        bodyActor.GetProperty().SetSpecularPower(60.0)
        bodyActor.GetProperty().SetColor(color)
        bodyActor.GetProperty().SetOpacity(opacity)
        
        self.actors.append(bodyActor)

        colorAxes = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }
        size = self._symbolScale/2
        axesActor = vtk.vtkAxesActor()
        axesActor.SetTotalLength(size,size,size)
        axesActor.GetXAxisShaftProperty().SetColor(colorAxes["X"])
        axesActor.GetXAxisTipProperty().SetColor(colorAxes["X"])
        axesActor.GetYAxisShaftProperty().SetColor(colorAxes["Y"])
        axesActor.GetYAxisTipProperty().SetColor(colorAxes["Y"])
        axesActor.GetZAxisShaftProperty().SetColor(colorAxes["Z"])
        axesActor.GetZAxisTipProperty().SetColor(colorAxes["Z"])
        axesActor.GetXAxisCaptionActor2D().GetTextActor().SetVisibility(False)
        axesActor.GetYAxisCaptionActor2D().GetTextActor().SetVisibility(False)
        axesActor.GetZAxisCaptionActor2D().GetTextActor().SetVisibility(False)

        self.actors.append(axesActor)


        transformationMatrix = np.eye(4)
        transformationMatrix[:3, 0] = np.array(self.parameter["x_axis"]["value"])
        transformationMatrix[:3, 1] = np.array(self.parameter["y_axis"]["value"])
        transformationMatrix[:3, 2] = np.array(self.parameter["z_axis"]["value"])
        transformationMatrix[:3, 3] = np.array(self.parameter["position"]["value"])

        vtkMatrix = vtk.vtkMatrix4x4()
        vtkMatrix.DeepCopy(transformationMatrix.ravel()) 

        transform = vtk.vtkTransform()
        transform.SetMatrix(vtkMatrix)


        for actor in self.actors:
            actor.SetUserTransform(transform)




        
       




        

        
