import mbsObject as mbsObj
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkMinimalStandardRandomSequence
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper
)
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter


class force(mbsObj.mbsObject):
    def __init__(self,subtype,input,parameter):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"force",subtype,input,[])
        else:
            parameter.update({
                "name": {"type":"string", "value":"init"},
                "body1": {"type":"string", "value":"init"}
            })
            mbsObj.mbsObject.__init__(self,"force",subtype,input,parameter)

class genForce(force):
    def __init__(self,input):
        if isinstance(input,dict):
            force.__init__(self,"genericForce",input,[])
        else:
            parameter = {
                "body2": {"type":"string", "value":"init"},
                "PointOfApplication_Body1": {"type":"vector", "value":[0.,0.,0.]},
                "PointOfApplication_Body2": {"type":"vector", "value":[0.,0.,0.]},
                "mode": {"type":"string", "value":"init"},
                "direction": {"type":"vector", "value":[0.,0.,0.]},
                "ForceExpression": {"type":"string", "value":"init"}
            }
            force.__init__(self,"genericForce",input,parameter)

        arrow = vtkArrowSource()
        arrow.SetShaftRadius(0.01)
        arrow.SetTipLength(0.2)
        arrow.SetTipRadius(0.02)
        arrow.SetShaftResolution(100)
        arrow.SetTipResolution(100)
        parameter = self.getDictionary()["parameter"]
        startPoint = parameter["PointOfApplication_Body1"]["value"]
        endPoint = parameter["PointOfApplication_Body2"]["value"]
        
        rng = vtkMinimalStandardRandomSequence()
        normalizedX = [0] * 3
        normalizedY = [0] * 3
        normalizedZ = [0] * 3
        vtkMath.Subtract(endPoint, startPoint, normalizedX)
        length = vtkMath.Norm(normalizedX)
        vtkMath.Normalize(normalizedX)

        arbitrary = [0] * 3
        for i in range(0, 3):
            rng.Next()
            arbitrary[i] = rng.GetRangeValue(-10, 10)
        vtkMath.Cross(normalizedX, arbitrary, normalizedZ)
        vtkMath.Normalize(normalizedZ)

        vtkMath.Cross(normalizedZ, normalizedX, normalizedY)

        matrix = vtkMatrix4x4()
        matrix.Identity()
        for i in range(0, 3):
            matrix.SetElement(i, 0, normalizedX[i])
            matrix.SetElement(i, 1, normalizedY[i])
            matrix.SetElement(i, 2, normalizedZ[i])

        transform = vtkTransform()
        transform.Translate(startPoint)
        transform.Concatenate(matrix)
        transform.Scale(length, length, length)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(arrow.GetOutputPort())
        self.actor.SetMapper(mapper)
        self.actor.SetUserTransform(transform)
        self.actor.GetProperty().SetOpacity(0.5)

class genTorque(force):
    def __init__(self,input):
        if isinstance(input,dict):
            force.__init__(self,"genericTorque",input,[])
        else:
            parameter = {
                "body2": {"type":"string", "value":"init"},
                "mode": {"type":"string", "value":"init"},
                "direction": {"type":"vector", "value":[0.,0.,0.]},
                "TorqueExpression": {"type":"string", "value":"init"}
            }
            force.__init__(self,"genericTorque",input,parameter)