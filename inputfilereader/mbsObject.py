
class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):            # strip: Leerzeichen entfernen
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = self.str2str(splitted[1])
                    elif(parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    #elif (parameter[key]["type"] == "vector"):
                       # parameter[key]["value"] = self.str2vector(splitted[1])

    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if (self.parameter[key]["type"] == "float"):
                text.append("\t" + key+"="+self.float2str(self.parameter[key]["value"])+"\n")
            elif (self.parameter[key]["type"] == "vector"):
                text.append("\t" + key+"="+self.vector2str(self.parameter[key]["value"])+"\n")
            elif (self.parameter[key]["type"] == "string"):
                text.append("\t" + key + "=" + self.str2str(self.parameter[key]["value"]) + "\n")
            elif self.parameter[key]["type"] == "int":
                text.append("\t" + key + "=" + self.int2str(self.parameter[key]["value"]) + "\n")
            #elif self.parameter[key]["type"] == "vector":
                #text.append("\t" + key + "=" + self.vector2str(self.parameter[key]["value"]) + "\n")
            

        text.append("End" + self.__type + "\n%\n")
        file.writelines(text)


    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0])+","+str(inVector[1])+ "," +str(inVector[2])
    
    #def str2vector(self, inString):
        #return [int(x) for x in inString.split()]
    #def vector2str(self, inVector):
        #return str(inVector[0]) + " " + str(inVector[1]) + " " + str(inVector[2]) + " " + str(inVector[3])
    
    def str2str(self,inString):
        return str(inString)
    
    def str2int(self,inString):
        return int(inString)
    def int2str(self,inInt):
        return str(inInt)

#====================================================================================================================

class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":         {"type":"string", "value": "BODY_UNKOWN"},
            "position":     {"type": "vector", "value": [1.,1.,1.]},
            #"color":        {"type": "vector", "value": [0, 0, 0, 0]},
            "mass":         {"type": "float", "value": 1.},
            "COG":          {"type": "vector", "value": [0.,0.,0.]},
        }

        mbsObject.__init__(self,"rigidBody","Rigid_EulerParameter_PAI",text,parameter)

#====================================================================================================================

class constraint(mbsObject):
    def __init__(self,text):
        parameter = {
            "dx":           {"type": "boolean", "value": 0},
            "dy":           {"type": "boolean", "value": 0},
            "dz":           {"type": "boolean", "value": 0},
            "ax":           {"type": "boolean", "value": 0},
            "ay":           {"type": "boolean", "value": 0},
            "az":           {"type": "boolean", "value": 0}
        }

        mbsObject.__init__(self,"constraint","Rigid_EulerParameter_PAI",text,parameter)