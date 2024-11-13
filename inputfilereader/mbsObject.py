class mbsObject:
    def __init__(self,type,text,parameter):
        self.__type = type
        self.parameter = parameter  #self.parameter ist membervariable, der wird referenz auf parameter zugewiesen
                                    # es ist also egal, ob man self.parameter oder parameter schreibt

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys(): #über dictionary drüber suchen... parameter.keys() = mass und COG
                if(splitted[0].strip() == key):          # strip = alle unnötigen Leerzeichen weg
                    if(parameter[key]["type"] == "float"):                          # Behandlung, wenn key ein float ist
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):                       # Behandlung, wenn key ein vector ist
                        parameter[key]["value"] = self.str2vector(splitted[1])


    def str2float(self,inString,):  # string in Float konvertieren
        return float(inString)
    
    def str2vector(self,inString,): # string in Vektor umbasteln
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]


#in den Unterklassen wird dann nach den Eigenschaften gesucht

class rigidBody(mbsObject):
    def __init__(self,text):                            #type brauchen wir nicht, weil ich bin ein Rigid Body
        parameter = {                                   #dictionary (key & value) mit den parametern
            "mass": {"type": "float", "value": 1.},     #sollte die Masse nicht gefunden werden, wird der default Wert 1 gesetzt bleiben
            "COG": {"type": "vector", "value": [1.,1.,1.]}
        } 

        mbsObject.__init__(self,"rigidBody",text,parameter)       #wenn man es so aufruft, braucht man auch das init