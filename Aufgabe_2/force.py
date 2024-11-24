from mbsObject import mbsObject
import vtk
import math
import numpy as np

class force(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "PointOfApplication_Body1": {"type": "vector", "value": [0.,0.,0.]},
            "PointOfApplication_Body2": {"type": "vector", "value": [0.,0.,0.]},
            "mode": {"type": "str", "value": "testMode"},
            "direction": {"type": "vector", "value": [0.,0.,0.]},
            "ForceExpression": {"type": "str", "value": "testForceExpression"}

        }

        mbsObject.__init__(self,"Force","GenericForce",text,parameter)


        arrow = vtk.vtkArrowSource()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(arrow.GetOutputPort())
        self.actor.SetMapper(mapper)

        #Achtung direction muss Einheitsvektor sein
        direction = parameter["direction"]["value"]
        directionArrow = [1, 0, 0]      
        axis = np.cross(directionArrow,direction)
        angle = math.degrees(math.acos(np.dot(directionArrow,direction)))
        
        transform = vtk.vtkTransform()
        position = parameter["PointOfApplication_Body1"]["value"]
        transform.Translate(position[0], position[1], position[2])
        transform.RotateWXYZ(angle, axis[0], axis[1], axis[2])

        self.actor.SetUserTransform(transform)
        self.actor.SetScale(100,100,100)
    
    
class torque(mbsObject):    
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "mode": {"type": "str", "value": "testMode"},
            "direction": {"type": "vector", "value": [0.,0.,0.]},
            "TorqueExpression": {"type": "str", "value": "testForceExpression"}

        }

        mbsObject.__init__(self,"Force","GenericTorque",text,parameter)


        assembly = vtk.vtkAssembly()
        size = 100
        torusSource = vtk.vtkParametricTorus()
        torusSource.SetRingRadius(size)
        torusSource.SetCrossSectionRadius(size/10)
        torus = vtk.vtkParametricFunctionSource()
        torus.SetParametricFunction(torusSource)
        torus.Update()
        torus.SetUResolution(100)
        torus.SetVResolution(100)
        torus.SetWResolution(100)
        torusMapper = vtk.vtkPolyDataMapper()
        torusMapper.SetInputConnection(torus.GetOutputPort())
        torusActor = vtk.vtkActor()
        torusActor.SetMapper(torusMapper)
        torusTransform = vtk.vtkTransform()
        torusTransform.Translate(0,0,0)
        torusActor.SetUserTransform(torusTransform)
        assembly.AddPart(torusActor)

        cone = vtk.vtkConeSource()
        cone.SetHeight(size)
        cone.SetRadius(size/3)
        cone.SetResolution(100)
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone.GetOutputPort())
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        coneTransform = vtk.vtkTransform()
        coneTransform.Translate(0,-size*0.95,0)
        coneActor.SetUserTransform(coneTransform)
        assembly.AddPart(coneActor)

        self.actor = assembly

        #Achtung direction muss Einheitsvektor sein
        direction = parameter["direction"]["value"]
        directionArrow = [0, 0, 1]      
        axis = np.cross(directionArrow,direction)
        angle = math.degrees(math.acos(np.dot(directionArrow,direction)))
        
        transform = vtk.vtkTransform()
        position = [0,0,0]
        transform.Translate(position[0], position[1], position[2])
        transform.RotateWXYZ(angle, axis[0], axis[1], axis[2])

        self.actor.SetUserTransform(transform)

