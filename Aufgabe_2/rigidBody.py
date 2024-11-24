from mbsObject import mbsObject
import vtk
import os

class rigidBody(mbsObject):
    def __init__(self, text):
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
  
        mbsObject.__init__(self,"Body","Rigid_EulerParamter_PAI",text,parameter)


        #if parameter["geometry"]["value"][3] == ".obj":
        #    reader = vtk.vtkOBJReader()
        #elif parameter["geometry"]["value"][3] == ".stl":
        #    reader = vtk.vtkSTLReader()
        #reader.SetFileName(os.getcwd() + "\\" + parameter["geometry"]["value"][1] + parameter["geometry"][value][2])
        
        reader = vtk.vtkSTLReader()
        reader.SetFileName(parameter["geometry"]["value"])
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        self.actor.SetMapper(mapper)

        color = [channel / 255 for channel in parameter["color"]["value"]]
        self.actor.GetProperty().SetColor(color[0],color[1],color[2])

        transformationMatrix = vtk.vtkMatrix4x4()
        position = parameter["position"]["value"]
        for i in range(3):
            transformationMatrix.SetElement(i,3,position[i])
        rotationMatrix = [parameter["x_axis"]["value"],parameter["y_axis"]["value"],parameter["z_axis"]["value"]]
        for i in range (3):
            for j in range(3):
                transformationMatrix.SetElement(i,j,rotationMatrix[i][j])
        transform = vtk.vtkTransform()
        transform.SetMatrix(transformationMatrix)
        self.actor.SetUserTransform(transform)


    def getPosition(self):
        return self.parameter["position"]["value"]
    
    def getCOG(self):
        return self.parameter["position"]["value"]

        

        
