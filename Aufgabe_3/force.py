from mbsObject import mbsObject
import vtk
import numpy as np

class force(mbsObject):
    def __init__(self, subtype, **kwargs):
        mbsObject.__init__(self, "Force", subtype, **kwargs)

class genericForce(force):
    def __init__(self, **kwargs):
        if "text" in kwargs:
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

            force.__init__(self, "GenericForce", text=kwargs["text"], parameter=parameter)
        else:
            force.__init__(self, "GenericForce", **kwargs)
        
       
        direction = self.parameter["direction"]["value"]
        size = self._symbolScale*1.5
        arrow = vtk.vtkArrowSource()
        arrow.SetShaftResolution(100)
        arrow.SetTipResolution(100)

        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(arrow.GetOutputPort())
        
        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)
        arrowActor.SetScale(size,size,size)
        arrowActor.GetProperty().SetColor(1,0,0)
        self.actors.append(arrowActor)

        directionLength = np.linalg.norm(direction)
        directionNorm = direction / directionLength

        directionArrow = [1, 0, 0]
        if np.array_equal(directionArrow,directionNorm):
            axis = [0,1,0]
            angle = 0
        elif np.array_equal(directionArrow,-directionNorm):
            axis = [0,1,0]
            angle = 180
        else:
            axis = np.cross(directionArrow,directionNorm)
            angle = np.degrees(np.acos(np.dot(directionArrow,directionNorm)))
        

        transform = vtk.vtkTransform()
        transform.Translate(self.parameter["PointOfApplication_Body1"]["value"])
        transform.RotateWXYZ(angle, axis[0], axis[1], axis[2])

        for actor in self.actors:
            actor.SetUserTransform(transform)
        

    
class genericTorque(force):    
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "name": {"type": "str", "value": "testName"},
                "body1": {"type": "str", "value": "testBody1"},
                "body2": {"type": "str", "value": "testBody2"},
                "mode": {"type": "str", "value": "testMode"},
                "direction": {"type": "vector", "value": [0.,0.,0.]},
                "TorqueExpression": {"type": "str", "value": "testForceExpression"}

            }

            force.__init__(self,"GenericTorque",text=kwargs["text"],parameter=parameter)
        
        else:
            force.__init__(self, "GenericTorque", **kwargs)


        
        
        size = self._symbolScale
        center = [0, 0, 0]
        normal = np.array([1.,0.,0.])
        vec2 = np.array([0,1,0])
        vec3 = np.array([0,0,1])

        start = center - 0.5*normal*size
        end = center + 0.5*normal*size
        axis = vtk.vtkLineSource()
        axis.SetPoint1(*start)
        axis.SetPoint2(*end)

        axisTube = vtk.vtkTubeFilter()
        axisTube.SetInputConnection(axis.GetOutputPort())
        axisTube.SetRadius(0.05*size)
        axisTube.SetNumberOfSides(50) 
        axisTube.CappingOn()

        axisTubeMapper = vtk.vtkPolyDataMapper()
        axisTubeMapper.SetInputConnection(axisTube.GetOutputPort())

        axisTubeActor = vtk.vtkActor()
        axisTubeActor.SetMapper(axisTubeMapper)
        axisTubeActor.GetProperty().SetColor(1,0,0)

        arc = vtk.vtkArcSource()
        arc.SetCenter(center)

        arc.SetPoint1(vec2*size)
        arc.SetPoint2(vec3*size)
        arc.SetResolution(10)

        tube = vtk.vtkTubeFilter()
        tube.SetInputConnection(arc.GetOutputPort())
        tube.SetRadius(0.05*size)
        tube.SetNumberOfSides(50)
        tube.CappingOn()

        tubeMapper = vtk.vtkPolyDataMapper()
        tubeMapper.SetInputConnection(tube.GetOutputPort())

        tubeActor = vtk.vtkActor()
        
        tubeActor.SetMapper(tubeMapper)
        tubeActor.GetProperty().SetColor(1,0,0)

        arrow = vtk.vtkConeSource()
        arrow.SetRadius(0.15*size)
        arrow.SetHeight(0.5*size)
        arrow.SetResolution(100)

        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(arrow.GetOutputPort())

        arrowTransform = vtk.vtkTransform()
        arrowTransform.Translate(vec2*size)
        angle = np.arccos(np.dot(vec2, vec3))*180/np.pi
        arrowTransform.RotateY(angle)

        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)
        arrowActor.SetUserTransform(arrowTransform)
        arrowActor.GetProperty().SetColor(1,0,0)

        assembly = vtk.vtkAssembly()
        assembly.AddPart(axisTubeActor)
        assembly.AddPart(tubeActor)
        assembly.AddPart(arrowActor)
        self.actors.append(assembly)

        direction = self.parameter["direction"]["value"]
        directionLength = np.linalg.norm(direction)
        directionNorm = direction / directionLength
        directionArrow = [0, 0, 1]      
        axis = np.cross(directionArrow,directionNorm)
        angle = np.degrees(np.acos(np.dot(directionArrow,directionNorm)))

        transform = vtk.vtkTransform()
        position = [0,0,0]
        transform.Translate(position)
        transform.RotateWXYZ(angle, axis)

        for actor in self.actors:
            actor.SetUserTransform(transform)

class gravity(force):
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "gravity_vector": {"type": "vector", "value": [0.,0.,0.]},
            }

            force.__init__(self,"Gravity",text=kwargs["text"],parameter=parameter)
        else:
            force.__init__(self,"Gravity",**kwargs)

        self.gravityArrow()

    def gravityArrow(self):
        self.actors = []
        direction = self.parameter["gravity_vector"]["value"]
        size = 1
        arrow = vtk.vtkArrowSource()
        arrow.SetShaftResolution(100)
        arrow.SetTipResolution(100)

        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(arrow.GetOutputPort())
        
        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)
        arrowActor.GetProperty().SetColor(1,1,1)
        

        directionLength = np.linalg.norm(direction)
        directionNorm = direction / directionLength

        directionArrow = [1, 0, 0]
        if np.array_equal(directionArrow,directionNorm):
            axis = [0,1,0]
            angle = 0
        elif np.array_equal(directionArrow,-directionNorm):
            axis = [0,1,0]
            angle = 180
        else:
            axis = np.cross(directionArrow,directionNorm)
            angle = np.degrees(np.acos(np.dot(directionArrow,directionNorm)))
        
        vectorText = vtk.vtkVectorText()
        vectorText.SetText("gravity")
        textMapper = vtk.vtkPolyDataMapper()
        textMapper.SetInputConnection(vectorText.GetOutputPort())
        
        transformText = vtk.vtkTransform()
        transformText.Scale(0.2,0.2,0.2)

        textActor = vtk.vtkFollower()
        textActor.SetMapper(textMapper)
        textActor.SetUserTransform(transformText)
        textActor.SetPosition(0, 1, 0)

        assembly = vtk.vtkAssembly()
        assembly.AddPart(arrowActor)
        assembly.AddPart(textActor)
        assembly.SetScale(size,size,size)
        self.actors.append(assembly)

        transform = vtk.vtkTransform()
        transform.Translate([0,0,0])
        transform.RotateWXYZ(angle, axis[0], axis[1], axis[2])

        for actor in self.actors:
            actor.SetUserTransform(transform)
    

