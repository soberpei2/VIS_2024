import mbsObject as mbsObj
import vtkSources.stippledLine as stippLine

from vtkmodules.all import(
    vtkLineSource,
    vtkPolyDataMapper
)

class measure(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"measure","",input,[])
        else:
            parameter = {
                "name": {"type":"string", "value":"init"},
                "body1": {"type":"string", "value":"init"},
                "body2": {"type":"string", "value":"init"},
                "type": {"type":"string", "value":"init"},
                "component": {"type":"int", "value":1},
                "location_body1": {"type":"vector", "value":[0.,0.,0.]},
                "location_body2": {"type":"vector", "value":[0.,0.,0.]},
                "use_initial_value": {"type":"boolean", "value":False},
                }

            mbsObj.mbsObject.__init__(self,"measure","",input,parameter)
        
        line = vtkLineSource()
        line.SetResolution(11)
        line.SetPoint1(self.parameter["location_body1"]["value"])
        line.SetPoint2(self.parameter["location_body2"]["value"])
        line.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())

        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetLineWidth(5)
        self.actor.GetProperty().SetColor(0,1,0)

        stippLine.StippledLine(self.actor, 0xA1A1, 2)