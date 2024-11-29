from mbsObject import mbsObject

from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkArcSource,
    vtkConeSource
)
from vtkmodules.vtkFiltersCore import (
    vtkTubeFilter
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import vtkActor
import numpy as np

class measure(mbsObject):
    def __init__(self,text):
        parameter = {
            "body1": {"type": "string", "value": "no"},
            "body2": {"type": "string", "value": "no"},
            "type": {"type": "string", "value": ""},
            "component": {"type": "int", "value": "0"},
            "location_body1": {"type": "vector", "value": [0.,0.,0.]},
            "location_body2": {"type": "vector", "value": [0.,0.,0.]},
            "vector_body1": {"type": "vector", "value": [0.,0.,0.]},
            "vector1_body2": {"type": "vector", "value": [0.,0.,0.]},
            "vector2_body2": {"type": "vector", "value": [0.,0.,0.]},
            "use_initial_value": {"type": "bool", "value": False}
        }

        mbsObject.__init__(self,"Measure","",text,parameter)

        if(parameter["type"]["value"] == "displacement"):
            self.__subtype = "Translational"
        if(parameter["type"]["value"] == "velocity"):
            self.__subtype = "Translational"        
        if(parameter["type"]["value"] == "angle"):
            self.__subtype = "Rotational"   
        if(parameter["type"]["value"] == "angular velocity"):
            self.__subtype = "Rotational"

        colors = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }

        scale = 10.0

        if self.__subtype == "Translational":
            for i, axis in enumerate(["X", "Y", "Z"]):
                start = [0, 0, 0]
                end = [0, 0, 0]
                end[i] = scale
                line = vtkLineSource()
                line.SetPoint1(*start)
                line.SetPoint2(*end)

                tube = vtkTubeFilter()
                tube.SetInputConnection(line.GetOutputPort())
                tube.SetRadius(0.05*scale)
                tube.SetNumberOfSides(50) 
                tube.CappingOn()

                tube_mapper = vtkPolyDataMapper()
                tube_mapper.SetInputConnection(tube.GetOutputPort())

                tube_actor = vtkActor()
                self.actors.append(tube_actor)
                tube_actor.SetMapper(tube_mapper)
                tube_actor.GetProperty().SetColor(colors[axis])

            transform = vtkTransform()
            transform.Translate(parameter["location_body1"]["value"])
            
            for actor in self.actors:
                actor.SetUserTransform(transform)
                
            start = parameter["location_body1"]["value"]
            end = parameter["location_body2"]["value"]
            line = vtkLineSource()
            line.SetPoint1(*start)
            line.SetPoint2(*end)

            tube = vtkTubeFilter()
            tube.SetInputConnection(line.GetOutputPort())
            tube.SetRadius(0.025*scale)
            tube.SetNumberOfSides(50) 
            tube.CappingOn()

            tube_mapper = vtkPolyDataMapper()
            tube_mapper.SetInputConnection(tube.GetOutputPort())

            tube_actor = vtkActor()
            self.actors.append(tube_actor)
            tube_actor.SetMapper(tube_mapper)

        elif self.__subtype == "Rotational":
            vec2 = np.array(parameter["vector1_body2"]["value"])
            vec3 = np.array(parameter["vector2_body2"]["value"])
            normal = np.cross(vec2, vec3)
            normal = normal/np.linalg.norm(normal)

            center = [0, 0, 0]

            start = center - 0.5*normal*scale
            end = center + 0.5*normal*scale
            axis = vtkLineSource()
            axis.SetPoint1(*start)
            axis.SetPoint2(*end)

            axisTube = vtkTubeFilter()
            axisTube.SetInputConnection(axis.GetOutputPort())
            axisTube.SetRadius(0.05*scale)
            axisTube.SetNumberOfSides(50) 
            axisTube.CappingOn()

            axisTube_mapper = vtkPolyDataMapper()
            axisTube_mapper.SetInputConnection(axisTube.GetOutputPort())

            axisTube_actor = vtkActor()
            self.actors.append(axisTube_actor)
            axisTube_actor.SetMapper(axisTube_mapper)

            # Create the arc (a portion of a circle)
            arc = vtkArcSource()
            arc.SetCenter(center)

            arc.SetPoint1(vec2*scale)
            arc.SetPoint2(vec3*scale)
            arc.SetResolution(10)

            tube = vtkTubeFilter()
            tube.SetInputConnection(arc.GetOutputPort())
            tube.SetRadius(0.05*scale)
            tube.SetNumberOfSides(50)  # Glätte der Röhrenoberfläche
            tube.CappingOn()

            tube_mapper = vtkPolyDataMapper()
            tube_mapper.SetInputConnection(tube.GetOutputPort())

            tube_actor = vtkActor()
            self.actors.append(tube_actor)
            tube_actor.SetMapper(tube_mapper)

            arrow = vtkConeSource()
            arrow.SetRadius(0.2*scale)  # Radius der Spitze
            arrow.SetHeight(0.5*scale)  # Höhe der Spitze
            arrow.SetResolution(50)

            arrow_mapper = vtkPolyDataMapper()
            arrow_mapper.SetInputConnection(arrow.GetOutputPort())

            arrow_transform = vtkTransform()
            arrow_transform.Translate(vec3*scale)
            angle = np.arccos(np.dot(vec3, vec2))*180/np.pi
            arrow_transform.RotateZ(90+angle)

            arrow_actor = vtkActor()
            self.actors.append(arrow_actor)
            arrow_actor.SetMapper(arrow_mapper)
            arrow_actor.SetUserTransform(arrow_transform)