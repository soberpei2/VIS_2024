from mbsObject import mbsObject

import vtk
import numpy as np

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
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "name": {"type": "str", "value": "testName"},
                "body1": {"type": "str", "value": "testBody1"},
                "body2": {"type": "str", "value": "testBody2"},
                "type": {"type": "str", "value": "testType"},
                "component": {"type": "int", "value": 0},
                "location_body1": {"type": "vector", "value": [0.,0.,0.]},
                "location_body2": {"type": "vector", "value": [0.,0.,0.]},
                "vector_body1": {"type": "vector", "value": [0.,0.,0.]},
                "vector1_body2": {"type": "vector", "value": [0.,0.,0.]},
                "vector2_body2": {"type": "vector", "value": [0.,0.,0.]},
                "use_initial_value": {"type": "bool", "value": 0},
            }

            mbsObject.__init__(self,"Measure","",text=kwargs["text"],parameter=parameter)
        else:
            mbsObject.__init__(self,"Measure","",**kwargs)


        if(self.parameter["type"]["value"] == "displacement"):
            self._subtype = "Translational"
        if(self.parameter["type"]["value"] == "velocity"):
            self._subtype = "Translational"        
        if(self.parameter["type"]["value"] == "angle"):
            self._subtype = "Rotational"   
        if(self.parameter["type"]["value"] == "angular velocity"):
            self._subtype = "Rotational"

        colors = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }
        opacity = 0.5


        
        if self._subtype == "Translational":
            
            for i, body in enumerate([self.parameter["location_body1"]["value"],self.parameter["location_body2"]["value"]]):
                assembly = vtk.vtkAssembly()
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
                    assembly.AddPart(lineActor)

                transform = vtk.vtkTransform()
                transform.Translate(body)
                assembly.SetUserTransform(transform)
                
                self.actors.append(assembly)

            
            start = self.parameter["location_body1"]["value"]
            end = self.parameter["location_body2"]["value"]
            line = vtk.vtkLineSource()
            line.SetPoint1(*start)
            line.SetPoint2(*end)

            tube = vtk.vtkTubeFilter()
            tube.SetInputConnection(line.GetOutputPort())
            tube.SetRadius(0.025*self._symbolScale)
            tube.SetNumberOfSides(50) 
            tube.CappingOn()

            tubeMapper = vtk.vtkPolyDataMapper()
            tubeMapper.SetInputConnection(tube.GetOutputPort())

            tubeActor = vtk.vtkActor()
            tubeActor.SetMapper(tubeMapper)
            tubeActor.GetProperty().SetColor(1,1,1)
            self.actors.append(tubeActor)
            

        elif self._subtype == "Rotational":
            vec2 = np.array(self.parameter["vector1_body2"]["value"])
            vec3 = np.array(self.parameter["vector2_body2"]["value"])
            normal = np.cross(vec2, vec3)
            normal = normal/np.linalg.norm(normal)

            center = [0, 0, 0]

            start = center - 0.5*normal*self._symbolScale
            end = center + 0.5*normal*self._symbolScale
            axis = vtk.vtkLineSource()
            axis.SetPoint1(*start)
            axis.SetPoint2(*end)

            axisTube = vtk.vtkTubeFilter()
            axisTube.SetInputConnection(axis.GetOutputPort())
            axisTube.SetRadius(0.025*self._symbolScale)
            axisTube.SetNumberOfSides(50) 
            axisTube.CappingOn()

            axisTubeMapper = vtk.vtkPolyDataMapper()
            axisTubeMapper.SetInputConnection(axisTube.GetOutputPort())

            axisTubeActor = vtk.vtkActor()
            axisTubeActor.SetMapper(axisTubeMapper)
            axisTubeActor.GetProperty().SetColor(1,1,1)
            self.actors.append(axisTubeActor)

            arc = vtk.vtkArcSource()
            arc.SetCenter(center)

            arc.SetPoint1(vec2*self._symbolScale)
            arc.SetPoint2(vec3*self._symbolScale)
            arc.SetResolution(10)

            tube = vtk.vtkTubeFilter()
            tube.SetInputConnection(arc.GetOutputPort())
            tube.SetRadius(0.025*self._symbolScale)
            tube.SetNumberOfSides(50)
            tube.CappingOn()

            tubeMapper = vtk.vtkPolyDataMapper()
            tubeMapper.SetInputConnection(tube.GetOutputPort())

            tubeActor = vtk.vtkActor()
            
            tubeActor.SetMapper(tubeMapper)
            tubeActor.GetProperty().SetColor(1,1,1)
            self.actors.append(tubeActor)

            arrow = vtk.vtkConeSource()
            arrow.SetRadius(0.075*self._symbolScale)
            arrow.SetHeight(0.25*self._symbolScale)
            arrow.SetResolution(100)

            arrowMapper = vtk.vtkPolyDataMapper()
            arrowMapper.SetInputConnection(arrow.GetOutputPort())

            arrowTransform = vtk.vtkTransform()
            arrowTransform.Translate(vec3*self._symbolScale)
            angle = np.arccos(np.dot(vec3, vec2))*180/np.pi
            arrowTransform.RotateZ(90+angle)

            arrowActor = vtk.vtkActor()
            arrowActor.SetMapper(arrowMapper)
            arrowActor.SetUserTransform(arrowTransform)
            arrowActor.GetProperty().SetColor(1,1,1)
            self.actors.append(arrowActor)
    
