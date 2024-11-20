import mbsObject as mbsObj

class settings(mbsObj.mbsObject):
    def __init__(self,input):
        if isinstance(input,dict):
            mbsObj.mbsObject.__init__(self,"settings","",input,[])
        else:
            parameter = {
                "background color": {"type":"color", "value":[0,0,0,0]},
                "bounding mode": {"type":"boolean", "value":False},
                "box dim": {"type":"vector", "value":[0.,0.,0.]},
                "COG marker scale": {"type":"float", "value":0.},
                "constraint icon scale": {"type":"float", "value":0.},
                "force icon scale": {"type":"float", "value":0.},
                "gravity_vector": {"type":"vector", "value":[0.,0.,0.]},
                "End of activation period": {"type":"float", "value":0.},
            }

            mbsObj.mbsObject.__init__(self,"settings","",input,parameter)