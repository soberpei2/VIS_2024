import mbsObject as mbsObj

class motion(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"motion","",input,[])
        else:        
            parameter = {
                "name": {"type":"string", "value":"init"},
                "body1": {"type":"string", "value":"init"},
                "body2": {"type":"string", "value":"init"},
                "PointOfApplication_Body1": {"type":"vector", "value":[0,0,0]},
                "PointOfApplication_Body2": {"type":"vector", "value":[0,0,0]},
                "measure": {"type":"string", "value":"init"},
                "MotionExpression": {"type":"string", "value":"init"},
                "ActivationPeriod": {"type":"float", "value":0.},
                }

            mbsObj.mbsObject.__init__(self,"motion","",input,parameter)