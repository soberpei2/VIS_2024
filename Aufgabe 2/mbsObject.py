class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.parameter = parameter  #self.parameter ist membervariable, der wird referenz auf parameter zugewiesen
                                    # es ist also egal, ob man self.parameter oder parameter schreibt
        self.__subtype = subtype

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys(): #über dictionary drüber suchen... parameter.keys() = mass und COG
                if(splitted[0].strip() == key):          # strip = alle unnötigen Leerzeichen weg
                    if(parameter[key]["type"] == "float"):                          # Behandlung, wenn key ein float ist
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):                       # Behandlung, wenn key ein vector ist
                        parameter[key]["value"] = self.str2vector(splitted[1])

    def writeInputFile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")
            if(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)   #writelines ist eine Zugriffsfunktion auf Datei

    def str2float(self,inString):  # string in Float konvertieren
        return float(inString)
    
    def float2str(self,inFloat):  
        return str(inFloat)

    def str2vector(self,inString): # string in Vektor umbasteln
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]

    def vector2str(self,inVector): 
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])

#in den Unterklassen wird dann nach den Eigenschaften gesucht

class rigidBody(mbsObject):
    def __init__(self,text):                            #type brauchen wir nicht, weil ich bin ein Rigid Body
        parameter = {                                   #dictionary (key & value) mit den parametern
            "mass": {"type": "float", "value": 1.},     #sollte die Masse nicht gefunden werden, wird der default Wert 1 gesetzt bleiben
            "COG": {"type": "vector", "value": [1.,1.,1.]}
        } 

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)       #wenn man es so aufruft, braucht man auch das init