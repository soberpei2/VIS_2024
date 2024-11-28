from mbsObject import mbsObject

from vtkmodules.vtkFiltersSources import (
    vtkLineSource,
    vtkSphereSource,
    vtkRegularPolygonSource
)
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkRenderingCore import vtkActor

class constraint(mbsObject):
    def __init__(self,subtype,text,parameter):

        mbsObject.__init__(self,"Constraint",subtype,text,parameter)

class genericConstraint(constraint):
    def __init__(self,text):
        parameter = {
            "body1": {"type": "string", "value": "no"},
            "body2": {"type": "string", "value": "no"},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]},
            "dx": {"type": "bool", "value": False},
            "dy": {"type": "bool", "value": False},
            "dz": {"type": "bool", "value": False},
            "ax": {"type": "bool", "value": False},
            "ay": {"type": "bool", "value": False},
            "az": {"type": "bool", "value": False}
        }

        constraint.__init__(self,"Generic",text,parameter)

        self.__locks = {"translation":  [parameter["dx"]["value"],parameter["dy"]["value"],parameter["dz"]["value"]],
                        "rotation":     [parameter["ax"]["value"],parameter["ay"]["value"],parameter["az"]["value"]]}

        colors = {
            "X": (1, 0, 0),
            "Y": (0, 1, 0),
            "Z": (0, 0, 1),
        }

        scale = 10.0
        for i, axis in enumerate(["X", "Y", "Z"]):
            line = vtkLineSource()
            start = [0, 0, 0]
            end = [0, 0, 0]
            end[i] = scale
            line.SetPoint1(*start)
            line.SetPoint2(*end)

            line_mapper = vtkPolyDataMapper()
            line_mapper.SetInputConnection(line.GetOutputPort())

            line_actor = vtkActor()
            self.actors.append(line_actor)
            line_actor.SetMapper(line_mapper)
            line_actor.GetProperty().SetColor(colors[axis])

            if self.__locks["translation"][i]:
                sphere = vtkSphereSource()
                sphere.SetCenter(*end)
                sphere.SetRadius(0.05*scale)

                sphere_mapper = vtkPolyDataMapper()
                sphere_mapper.SetInputConnection(sphere.GetOutputPort())

                sphere_actor = vtkActor()
                self.actors.append(sphere_actor)
                sphere_actor.SetMapper(sphere_mapper)
                sphere_actor.GetProperty().SetColor(colors[axis])

            if self.__locks["rotation"][i]:
                ring = vtkRegularPolygonSource()
                ring.SetCenter([0.7 * v for v in end])
                ring.SetRadius(0.2*scale)
                ring.SetNumberOfSides(50)
                if axis == "X":
                    ring.SetNormal(1, 0, 0)
                elif axis == "Y":
                    ring.SetNormal(0, 1, 0)
                elif axis == "Z":
                    ring.SetNormal(0, 0, 1)

                ring_mapper = vtkPolyDataMapper()
                ring_mapper.SetInputConnection(ring.GetOutputPort())

                ring_actor = vtkActor()
                self.actors.append(ring_actor)
                ring_actor.SetMapper(ring_mapper)
                ring_actor.GetProperty().SetColor(colors[axis])

        # Transformation erstellen
        transform = vtkTransform()
        transform.Translate(parameter["position"]["value"])
        #transform.RotateWXYZ(*orientation)
        
        for actor in self.actors:
            actor.SetUserTransform(transform)