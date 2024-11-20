import mbsObject as mbsObj

class dataobjectParameter(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"dataobjectParameter","",input,[])
        else:
            parameter = {
                "name": {"type":"string", "value":"init"},
                "InitialValue": {"type":"float", "value":0.},
                }

            mbsObj.mbsObject.__init__(self,"dataobjectParameter","",input,parameter)