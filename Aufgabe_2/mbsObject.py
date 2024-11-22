# Importieren benötigter Biblotheken
import vtk

class mbsObject:
    # Constructor
    #============
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
                    # Überprüfen ob der Parametertyp float ist
                    if(parameter[key]["type"] == "float"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2float(splitted[1])

                    # Überprüfen ob der Parametertyp vector ist
                    elif(parameter[key]["type"] == "vector"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2vector(splitted[1])

                    # Überprüfen ob der Parametertyp Integer-vector ist
                    elif(parameter[key]["type"] == "vectorInt"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2vectorInt(splitted[1])

                    # Überprüfen ob der Parametertyp int ist
                    elif(parameter[key]["type"] == "int"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2int(splitted[1])

                    # Überprüfen ob der Parametertyp string ist
                    elif(parameter[key]["type"] == "string"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = splitted[1] + ":" + splitted[2]
                        parameter[key]["value"] = parameter[key]["value"].replace("\\", "/")
                        parameter[key]["value"] = parameter[key]["value"].strip()
    #===================================================================================================

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

            # Umwandlung eines Integer-Vektors in string
            elif(self.parameter[key]["type"] == "vectorInt"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")

            # Umwandlung eines int in string
            elif(self.parameter[key]["type"] == "int"):
                text.append("\t" + key + " = " + self.int2str(self.parameter[key]["value"]) + "\n")

            # Ausgabe wenn type = string
            elif(self.parameter[key]["type"] == "string"):
                text.append("\t" + key + " = " + self.parameter[key]["value"] + "\n")

        # Anfügen von 2 Leerzeichen am Ende des Files
        text.append("End" + self.__type + "\n%\n")

        # Schreiben der Zeilen in die Variable text
        file.writelines(text)
    #===================================================================================================

    # Memberfunktion -> Umwandlung eines string in float
    #---------------------------------------------------
    def str2float(self, inString):
        return float(inString)
    
    # Memberfunktion -> Umwandlung eines float in string
    #---------------------------------------------------
    def float2str(self, inFloat):
        return str(inFloat)
    #===================================================================================================
    
    # Memberfunktion -> Umwandlung eines string in vector
    #----------------------------------------------------
    def str2vector(self, inString):
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]
    
    # Memberfunktion -> Umwandlung eines vector in string
    #----------------------------------------------------
    def vector2str(self, inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    #===================================================================================================

    # Memberfunktion -> Umwandlung eines string in einen Integer-vector
    #------------------------------------------------------------------
    def str2vectorInt(self, inString):
        return [int(inString.split()[0]), int(inString.split()[1]), int(inString.split()[2])]
    #===================================================================================================
    
    # Memberfunktion -> Umwandlung eines string in int
    #--------------------------------------------------
    def str2int(self, inString):
        return int(inString)
    
    # Memberfunktion -> Umwandlung eines int in string
    #---------------------------------------------------
    def int2str(self, inInt):
        return str(inInt)
    #===================================================================================================

    # Memberfunktion - Visualisierung von MBS-Objekten
    #=================================================
    def showMbsObject(self, source):
        # Erzeugen eines Filters mit dem Eingang body
        Mapper = vtk.vtkPolyDataMapper()
        Mapper.SetInputConnection(source)

        # Erzeugen eines Aktors (Filter als Eingang)
        Actor = vtk.vtkActor()
        Actor.SetMapper(Mapper)

        # Zeichnen des Bildes
        ren1 = vtk.vtkRenderer()
        ren1.AddActor(Actor)
        ren1.SetBackground(0.1, 0.2, 0.4)

        # Definieren einer Leinwand
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren1)
        renWin.SetSize(300, 300)
        renWin.Render()

        # Interaktionseinstellungen
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)
        iren.Start()

               
#=======================================================================================================

class rigidBody(mbsObject):
    # Constructor
    #============
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        parameter = {
                        "geometry": {
                                        "type": "string",
                                        "value": ""
                                    },

                        "position": { 
                                        "type": "vector", 
                                        "value": [0., 0., 0.]
                                    },

                        "color":    { 
                                        "type": "vectorInt",
                                        "value": [0, 0, 0] 
                                    },

                        "mass":     {
                                        "type": "float",
                                        "value": 1.
                                    },

                         "COG":     {
                                        "type": "vector",
                                        "value": [0., 0., 0.]
                                    }
                    }
        #-----------------------------------------------------------------------------------------------

        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht
        # übergeben)
        mbsObject.__init__(self, "Body", "Rigid_EulerParameter_PAI", text, parameter)
    #=======================================================================================================

#=======================================================================================================

class constraint(mbsObject):
    # Constructor
    #============
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        #-----------------------------------------------------
        parameter = {
                        "dx":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "dy":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "dz":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "ax":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "ay":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "az":   {
                                    "type": "int",
                                    "value": 0
                                },

                        "position": {
                                        "type": "vector", 
                                        "value": [0., 0., 0.]
                                    } 
                        
                    }
        #-----------------------------------------------------------------------------------------------
        
        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht
        # übergeben)
        mbsObject.__init__(self, "Constraint", "Rigid_EulerParameter_PAI", text, parameter)
#=======================================================================================================

class setting(mbsObject):
    # Constructor
    #============
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        #-----------------------------------------------------
        parameter = {
                        "background color": {
                                                "type": "vectorInt",
                                                "value": [0, 0, 0]
                                            },

                        "COG marker scale": {
                                                "type": "float",
                                                "value": 0.
                                            },

                        "constraint icon scale":    {
                                                        "type": "float",
                                                        "value": 0.
                                                    },

                        "force icon scale": {
                                                "type": "float",
                                                "value": 0.
                                            },

                        "gravity_vector":   {
                                                "type": "vector",
                                                "value": [0., 0., 0.]
                                            }
                    }
        #-----------------------------------------------------------------------------------------------
        
        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht
        # übergeben)
        mbsObject.__init__(self, "Settings", "Rigid_EulerParameter_PAI", text, parameter)