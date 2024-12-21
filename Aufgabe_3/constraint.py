from mbsObject import mbsObject
import vtk
import numpy as np




class constraint(mbsObject):
    def __init__(self, subtype, **kwargs):
        mbsObject.__init__(self, "Constraint", subtype, **kwargs)


class genericConstraint(constraint):
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "name": {"type": "str", "value": "testName"},
                "body1": {"type": "str", "value": "testBody1"},
                "body2": {"type": "str", "value": "testBody2"},
                "dx": {"type": "bool", "value": False},
                "dy": {"type": "bool", "value": False},
                "dz": {"type": "bool", "value": False},
                "ax": {"type": "bool", "value": False},
                "ay": {"type": "bool", "value": False},
                "az": {"type": "bool", "value": False},
                "position": {"type": "vector", "value": [0.,0.,0.]},
                "x_axis": {"type": "vector", "value": [0.,0.,0.]},
                "y_axis": {"type": "vector", "value": [0.,0.,0.]},
                "z_axis": {"type": "vector", "value": [0.,0.,0.]}
            }

            constraint.__init__(self, "Generic", text=kwargs["text"], parameter=parameter)

        else:
            constraint.__init__(self, "Generic", **kwargs)

        self.__locks = {"translation":  [self.parameter["dx"]["value"],self.parameter["dy"]["value"],self.parameter["dz"]["value"]],
                        "rotation":     [self.parameter["ax"]["value"],self.parameter["ay"]["value"],self.parameter["az"]["value"]]}

        colors = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }
        opacity = 0.5

        for i, axis in enumerate(["X", "Y", "Z"]):
            start = [0, 0, 0]
            end = [0, 0, 0]
            end[i] = self._symbolScale/2
           
            line = vtk.vtkLineSource()
            line.SetPoint1(*start)
            line.SetPoint2(*end)

            lineMapper = vtk.vtkPolyDataMapper()
            lineMapper.SetInputConnection(line.GetOutputPort())

            lineActor = vtk.vtkActor()
            lineActor.SetMapper(lineMapper)
            lineActor.GetProperty().SetColor(colors[axis])
            lineActor.GetProperty().SetOpacity(opacity)

            self.actors.append(lineActor)

            if self.__locks["translation"][i]:
                size = 0.5*self._symbolScale

                cone = vtk.vtkConeSource()
                cone.SetCenter(-size/2,0,0)
                cone.SetHeight(size)
                cone.SetRadius(size/3)
                cone.SetResolution(100)

                transform = vtk.vtkTransform()
                if axis == "X":
                    transform.RotateX(0)
                elif axis == "Y":
                    transform.RotateZ(90)
                elif axis == "Z":
                    transform.RotateY(-90)
                
                coneMapper = vtk.vtkPolyDataMapper()
                coneMapper.SetInputConnection(cone.GetOutputPort())

                coneActor = vtk.vtkActor()
                coneActor.SetMapper(coneMapper)
                coneActor.GetProperty().SetColor(colors[axis])
                coneActor.GetProperty().SetOpacity(opacity)
                coneActor.SetUserTransform(transform)

                coneActorAssembly = vtk.vtkAssembly()
                coneActorAssembly.AddPart(coneActor)
                self.actors.append(coneActorAssembly)

            if self.__locks["rotation"][i]:
                size = 0.5*self._symbolScale

                torusSource = vtk.vtkParametricTorus()
                torusSource.SetRingRadius(size)
                torusSource.SetCrossSectionRadius(size/3)

                torus = vtk.vtkParametricFunctionSource()
                torus.SetParametricFunction(torusSource)
                torus.Update()
                torus.SetUResolution(100)
                torus.SetVResolution(100)
                torus.SetWResolution(100)
                
                transform = vtk.vtkTransform()
                if axis == "X":
                    transform.RotateY(90)
                elif axis == "Y":
                    transform.RotateX(-90)
                elif axis == "Z":
                    transform.RotateX(0)
                transform.Translate(0,0,-size*2)
                
                torusMapper = vtk.vtkPolyDataMapper()
                torusMapper.SetInputConnection(torus.GetOutputPort())

                torusActor = vtk.vtkActor()
                torusActor.SetMapper(torusMapper)
                torusActor.GetProperty().SetColor(colors[axis])
                torusActor.GetProperty().SetOpacity(opacity)
                torusActor.SetUserTransform(transform)

                torusActorAssembly = vtk.vtkAssembly()
                torusActorAssembly.AddPart(torusActor)
                self.actors.append(torusActorAssembly)
                

        transform_matrix = np.eye(4) 
        transform_matrix[:3, 0] = np.array(self.parameter["x_axis"]["value"])
        transform_matrix[:3, 1] = np.array(self.parameter["y_axis"]["value"])
        transform_matrix[:3, 2] = np.array(self.parameter["z_axis"]["value"])
        transform_matrix[:3, 3] = np.array(self.parameter["position"]["value"])

        vtk_matrix = vtk.vtkMatrix4x4()
        vtk_matrix.DeepCopy(transform_matrix.ravel()) 
        
        transform = vtk.vtkTransform()
        transform.SetMatrix(vtk_matrix)

        for actor in self.actors:
            actor.SetUserTransform(transform)







        
            
            

