class mbsObject:
    def __init__(self,type,text,subtype,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])   
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])

    def writeInputfile(self, file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")      #\n...Leerzeile
        for key in self.parameter.keys():
            # Umwandlung eines float in string
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")    #\t...Einrückung
 
            # Umwandlung eines Vektors in string
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")
 
        # Anfügen von 2 Leerzeichen am Ende des Files
        text.append("End" + self.__type + "\n%\n")
 
        # Schreiben der Zeilen in die Variable text
        file.writelines(text)

    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.,]}
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI", text,parameter)