
class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        
        for line in text:
            splitted = line.split(":")
            for key in parameter.keys(): #zeile für zeile
                 if(splitted[0].strip() == key): #split entfernt alle leerzeichen links und rechts ,splitted[0] == text links vom doppelpkt. in fdd file
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif(parameter[key]["type"] == "intvec"):
                        parameter[key]["value"] = self.str2intvec(splitted[1])


    def writeInputfile(self,file):
        text= []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"]=="float"):
                text.append("\t"+key+" = "+self.float2str(self.parameter[key]["value"])+"\n")
            
            elif(self.parameter[key]["type"]=="vector"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")

            elif(self.parameter[key]["type"]=="int"):
                text.append("\t"+key+" = "+self.int2str(self.parameter[key]["value"])+"\n")

            elif(self.parameter[key]["type"]=="intvec"):
                text.append("\t"+key+" = "+self.intvec2str(self.parameter[key]["value"])+"\n")
        text.append("End"+ self.__type+"\n%\n")

        file.writelines(text)

    def str2float(self,inString):
        return float(inString)
    
    def float2str(Self,inFloat):
        return str(inFloat)
    
    def str2int(self,inInt):
        return float(inInt)
    
    def int2str(Self,inInt):
        return str(inInt)
    
                  
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
     
    
    def str2intvec(self,inIntvec):
        return [int (inIntvec.split()[0]),int (inIntvec.split()[1]),int (inIntvec.split()[2])]
    
    def intvec2str(self,inIntvec):
        return str(inIntvec[0]) + " " + str(inIntvec[1]) + " " + str(inIntvec[2])
    
class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {  #Dictionary
            "mass": {"type": "float", "value": 1.},   #mass wird gesucht, float ist datentyp, value wird beschrieben, 1. = defaulkt value falls keine masse gefunden wird
            "COG": {"type": "vector", "value": [0.,0.,0.]}, #Center of Gravity
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "color": {"type": "intvec", "value": [0.,0.,0.]},
            "transparency": {"type": "float", "value": 1.}
        }

        mbsObject.__init__(self,"Body","RIGID_EulerParamter_PAI",text, parameter) #super... wäre auch möglich gewesen

class constraint(mbsObject):
    def __init__(self,text):
        parameter = {  #Dictionary 
            "position": {"type": "vector", "value": [0.,0.,0.]}, #Positionsvektor
            "dx": {"type": "int", "value": 1.},
            "dy": {"type": "int", "value": 1.},
            "dz": {"type": "int", "value": 1.},
            "ax": {"type": "int", "value": 1.},
            "ay": {"type": "int", "value": 1.},
            "az": {"type": "int", "value": 1.},
        }

        mbsObject.__init__(self,"constraint","constraint_fixed",text, parameter)

class settings(mbsObject):
    def __init__(self,text):
        parameter = {  #Dictionary
            "constraint icon scale": {"type": "float", "value": 1.},
            "COG marker scale": {"type": "float", "value": 1.}, 
            "gravity_vector": {"type": "vector", "value": [0.,0.,0.]}, 
            "background color": {"type": "intvec", "value": [0.,0.,0.]}
        }

        mbsObject.__init__(self,"settings","settings_fixed",text, parameter)
