
class mbsObject:                                            #Klasse erstellen
    def __init__(self, type, subtype, text, parameter):     #Definieren (init -> Konstructor) ,sich selbst, 
        self.__type = type                                  #pointer of sich selbt vom Typ type
        self.__subtype = subtype                            #pointer of sich selbt vom Typ subtype
        self.parameter = parameter                            #pointer of sich selbt vom Typ parameter

        for line in text:                                   #line ist counter im text
            splitted = line.split(":")                      #legen die Varibale splitted an und Trenne die Spalte bei Doppelpunkt
            for key in parameter.keys():                    #key ist counter in mbsObject.parameter
                if(splitted[0].strip() == key):             
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    if(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])

    def writeInputfile(self,file):
        text =[]
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t"+key+" = "+ self.float2str(self.parameter[key]["value"])+"\n")
            if(self.parameter[key]["type"] == "vector"):
                text.append("\t"+key+" = "+ self.vec2str(self.parameter[key]["value"])+"\n")
        text.append("End"+self.__type + "\n%""\n")

        file.writelines(text)

    def str2float(self,inString):
        return float(inString)
    
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def vec2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])

class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "mass": {"type": "float", "value": 1.},      #masse ist gesucht, float is datentyp, wert mit defaultvariable
            "COG": {"type": "vector", "value":[0.,0.,0.]}       #Center of Gravity ist gesucht, vector ist datentyp,
        }

        mbsObject.__init__(self,"body","Rigid_EulerParameter_PAI",text, parameter)