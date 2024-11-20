import mbsObject as mbsObj

from vtkmodules.all import (
    vtkTransform,
    vtkMatrix4x4,
    vtkAxesActor
)

class constraint(mbsObj.mbsObject):
    def __init__(self,input):  
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"constraint","",input,[])
        else:
            parameter = {
                "name": {"type":"string", "value":"init"},
                "body1": {"type":"string", "value":"init"},
                "body2": {"type":"string", "value":"init"},
                "dx": {"type":"boolean","value":"false"},
                "dy": {"type":"boolean","value":"false"},
                "dz": {"type":"boolean","value":"false"},
                "ax": {"type":"boolean","value":"false"},
                "ay": {"type":"boolean","value":"false"},
                "az": {"type":"boolean","value":"false"},
                "position": {"type":"vector", "value":[0,0,0]},
                "x_axis": {"type":"vector", "value":[0,0,0]},
                "y_axis": {"type":"vector", "value":[0,0,0]},
                "z_axis": {"type":"vector", "value":[0,0,0]}
            }

            mbsObj.mbsObject.__init__(self,"constraint","",input,parameter)

            self.actor = vtkAxesActor()
            self.actor.SetTotalLength(10,10,10)
            self.actor.SetShaftTypeToCylinder()
            self.actor.AxisLabelsOff()

            tdofs = ["dx","dy","dz"]
            rdofs = ["ax","ay","az"]

            for dof in tdofs:
                func = getattr(self.actor, 'Get'+ dof[-1].upper() + 'AxisShaftProperty')
                if(self.parameter[dof]["value"] == True):
                    func().SetColor(1,0,0)
                else:
                    func().SetColor(0,1,0)

            for dof in rdofs:
                func = getattr(self.actor, 'Get'+ dof[-1].upper() + 'AxisTipProperty')
                if(self.parameter[dof]["value"] == True):
                    func().SetColor(1,0,0)
                else:
                    func().SetColor(0,1,0)

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