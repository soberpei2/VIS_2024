class mbsObject:
    def __init__(self,type,text,parameter):
        self.__type = type
        self.parameter = parameter

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])   
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])

    def str2float(self,inString):
        return float(inString)
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.,]}
        }

        mbsObject.__init__(self,"rigidBody", text,parameter)