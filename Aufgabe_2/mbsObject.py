
class mbsObject:
    # Constructor
    #------------
    def __init__(self, type, subtype, text, parameter):
        # Save the type to the protected variable __type
        self.__type = type
        self.__subtype = subtype

        # Abspeichern des Parametersatzes (self.parameter enthält nur einer Ref. auf parameter)
        self.parameter = parameter

        # Durchsuchen des Textes
        for line in text:
            # Split line (left and rigth to :)
            splitted = line.split(":")

            # Schleife über die Schlüssel des Dictionaries
            for key in parameter.keys():
                # Search for key "mass" (.strip() -> removes Leerzeichen)
                if(splitted[0].strip() == key):
                    #Überprüfen ob der Parametertyp float ist
                    if(parameter[key]["type"] == "float"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2float(splitted[1])

                    #Überprüfen ob der Parametertyp vector ist
                    elif(parameter[key]["type"] == "vector"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2vector(splitted[1])

    # Memberfunktion -> Inputfile schreiben
    #--------------------------------------
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

    # Memberfunktion -> Umwandlung eines string in float
    #---------------------------------------------------
    def str2float(self, inString):
        return float(inString)
    
    # Memberfunktion -> Umwandlung eines float in string
    #---------------------------------------------------
    def float2str(self, inFloat):
        return str(inFloat)
    
    # Memberfunktion -> Umwandlung eines string in vector
    #----------------------------------------------------
    def str2vector(self, inString):
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]
    
    # Memberfunktion -> Umwandlung eines vector in string
    #----------------------------------------------------
    def vector2str(self, inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])

            
#=============================================================================

class rigidBody(mbsObject):
    # Constructor
    #------------
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        parameter = {
                        "mass": {
                                    "type": "float",
                                    "value": 1.
                                },
                        "COG": {
                                    "type": "vector",
                                    "value": [0., 0., 0.]
                               }
                    }

        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht übergeben)
        mbsObject.__init__(self, "rigidBody", "Rigid_EulerParameter_PAI", text, parameter)