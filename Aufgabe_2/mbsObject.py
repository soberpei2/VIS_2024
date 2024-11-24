# Importieren benötigter Biblotheken
import vtk
import numpy as np

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

    # Memberfunktion - Erstellen eines Kugel-Aktors
    #==============================================
    def getSphere(self, mbsObject):
        # Erzeugen einer Kugelquelle
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(3.0)
        sphere.SetPhiResolution(10)
        sphere.SetThetaResolution(10)

        # Erzeugen eines Filters mit dem Eingang body
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)

        # Position des Aktors lt. fdd-File vorgeben
        sphereActor.SetPosition(mbsObject.parameter["position"]["value"])

        # Farbe des Aktors ändern
        sphereActor.GetProperty().SetColor(1, 0, 0)

        # Rückgabe des Aktors
        return sphereActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Kugel-Aktors
    #==============================================
    def getCube(self, mbsObject):
        # Erzeugen einer Kugelquelle
        cube = vtk.vtkCubeSource()
        cube.SetXLength(3.0)
        cube.SetYLength(3.0)
        cube.SetZLength(3.0)

        # Erzeugen eines Filters mit dem Eingang body
        cubeMapper = vtk.vtkPolyDataMapper()
        cubeMapper.SetInputConnection(cube.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        cubeActor = vtk.vtkActor()
        cubeActor.SetMapper(cubeMapper)

        # Position des Aktors lt. fdd-File vorgeben
        cubeActor.SetPosition(mbsObject.parameter["position"]["value"])

        # Farbe des Aktors ändern
        cubeActor.GetProperty().SetColor(1, 0, 0)

        # Rückgabe des Aktors
        return cubeActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Pyramiden-Aktors
    #==================================================
    def getCone(self, mbsObject):
        # Erzeugen einer Kugelquelle
        cone = vtk.vtkConeSource()
        cone.SetHeight(4.0)
        cone.SetRadius(3.0)
        cone.SetResolution(50)

        # Erzeugen eines Filters mit dem Eingang body
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(cone.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)

        # Position des Aktors lt. fdd-File vorgeben
        coneActor.SetPosition(mbsObject.parameter["position"]["value"])

        # Farbe des Aktors ändern
        coneActor.GetProperty().SetColor(1, 0, 0)

        # Rückgabe des Aktors
        return coneActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Zylinder-Aktors
    #=================================================
    def getCylinder(self, mbsObject):
        # Erzeugen einer Kugelquelle
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetHeight(4.0)
        cylinder.SetRadius(3.0)
        cylinder.SetResolution(50)

        # Erzeugen eines Filters mit dem Eingang body
        cylinderMapper = vtk.vtkPolyDataMapper()
        cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        cylinderActor = vtk.vtkActor()
        cylinderActor.SetMapper(cylinderMapper)

        # Position des Aktors lt. fdd-File vorgeben
        cylinderActor.SetPosition(mbsObject.parameter["position"]["value"])

        # Farbe des Aktors ändern
        cylinderActor.GetProperty().SetColor(1, 0, 0)

        # Rückgabe des Aktors
        return cylinderActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Ebenen-Aktors
    #===============================================
    def getPlane(self, mbsObject):
        # Erzeugen einer Kugelquelle
        plane = vtk.vtkRegularPolygonSource()
        plane.SetNumberOfSides(4)
        plane.SetRadius(3.0)

        # Erzeugen eines Filters mit dem Eingang body
        planeMapper = vtk.vtkPolyDataMapper()
        planeMapper.SetInputConnection(plane.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        planeActor = vtk.vtkActor()
        planeActor.SetMapper(planeMapper)

        # Position des Aktors lt. fdd-File vorgeben
        planeActor.SetPosition(mbsObject.parameter["position"]["value"])

        # Farbe des Aktors ändern
        planeActor.GetProperty().SetColor(1, 0, 0)

        # Rückgabe des Aktors
        return planeActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Vektor-Aktors
    #===============================================
    def getArrow(self, mbsObject):
        # Erzeugen einer Pfeilquelle
        arrow = vtk.vtkArrowSource()
        arrow.SetTipLength(0.35)       # Spitze größer machen
        arrow.SetTipRadius(0.1)       # Spitze breiter machen
        arrow.SetShaftRadius(0.05)    # Schaft breiter machen
        arrow.SetTipResolution(50)
        arrow.SetShaftResolution(50)

        # Erzeugen eines Filters mit dem Eingang body
        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(arrow.GetOutputPort())

        # Erzeugen eines Aktors (Filter als Eingang)
        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)

        # Farbe des Aktors ändern
        arrowActor.GetProperty().SetColor(0, 0, 0)

        # Transformation erstellen
        transform = vtk.vtkTransform()

        # Schwerkraft in y-Richtung -> Drehung um z-Achse um 90°
        if mbsObject.parameter["gravity_vector"]["value"][1] != 0:
            transform.RotateZ(-90)

        # Schwerkraft in z-Richtung -> Drehung um y-Achse um 90°
        if mbsObject.parameter["gravity_vector"]["value"][2] != 0:
            transform.RotateY(90)   

        # Anwenden der Transformation
        arrowActor.SetUserTransform(transform)
        arrowActor.SetScale(10,10,10)

        # Rückgabe des Aktors
        return arrowActor
    #===================================================================================================

    # Memberfunktion - Erstellen eines Aktors lt. .fdd-File
    #======================================================
    def getActor(self, mbsObject):
        # Abfrage, ob mbsObject von der Unterklasse rigidBody ist
        #--------------------------------------------------------
        if isinstance(mbsObject, rigidBody):
            # Erzeugen eines obj-Readers
            bodyReader = vtk.vtkOBJReader()

            # Erzeugen einer Quelle
            bodyReader.SetFileName(mbsObject.parameter["geometry"]["value"])
            bodyReader.Update()
            body = bodyReader.GetOutputPort()

            # Erzeugen eines Filters mit dem Eingang body
            bodyMapper = vtk.vtkPolyDataMapper()
            bodyMapper.SetInputConnection(body)

            # Erzeugen eines Aktors (Filter als Eingang)
            bodyActor = vtk.vtkActor()
            bodyActor.SetMapper(bodyMapper)

            # Position des Aktors lt. fdd-File vorgeben
            bodyActor.SetPosition(mbsObject.parameter["position"]["value"])

            # Farbe und Transparenz des Aktors ändern
            bodyActor.GetProperty().SetColor(mbsObject.parameter["color"]["value"])
            bodyActor.GetProperty().SetOpacity(mbsObject.parameter["transparency"]["value"] / 100)

            # Rückgabe des Aktors
            return bodyActor
        #------------------------------------------------------------------------------------

        # Abfrage, ob mbsObject von der Unterklasse constraint ist
        #---------------------------------------------------------
        elif isinstance(mbsObject, constraint):
            # Erstellen von 2 Vektoren mit den Freiheitsgraden (trans. und rot.)
            transBlockVec = [mbsObject.parameter["dx"]["value"],
                             mbsObject.parameter["dy"]["value"],
                             mbsObject.parameter["dz"]["value"]]
                             
            rotBlockVec = [mbsObject.parameter["ax"]["value"],
                           mbsObject.parameter["ay"]["value"],
                           mbsObject.parameter["az"]["value"]]

            # Fixe Einspannung (keine Freiheitsgrade)
            if sum(transBlockVec) == 3 and sum(rotBlockVec) == 3:
                return self.getCube(mbsObject)
            
            # Festlager (1 rot. Freiheitsgrad)
            elif sum(transBlockVec) == 3 and sum(rotBlockVec) == 2:
                return self.getCone(mbsObject)
            
            # Loslager (1 trans. + 1 rot. Freiheitsgrad)
            elif sum(transBlockVec) == 2 and sum(rotBlockVec) == 2:
                return self.getCylinder(mbsObject)
            
            # Planare Auflage (2 trans. + 1 rot. Freiheitsgrad)
            elif sum(transBlockVec) == 1 and sum(rotBlockVec) == 2:
                return self.getPlane(mbsObject)

            # Kugelgelenk (nur rotatorische Freiheitsgrade)
            elif sum(transBlockVec) == 3 and sum(rotBlockVec) == 0:
                return self.getSphere(mbsObject)
        #------------------------------------------------------------------------------------

        # Abfrage, ob mbsObject von der Unterklasse setting ist
        #------------------------------------------------------
        elif isinstance(mbsObject, setting):
            # Darstellen des Schwerkraftvektors
            return self.getArrow(mbsObject)
    #===================================================================================================

    # Memberfunktion - Zeigen der mbsObject-Properties
    #=================================================
    def showProps(self):
        # Überschrift
        print("Properties of ", type(self))

        # Schleife über alle Parameter im dictionary
        for key in self.parameter.keys():
            print("\t", key, " = ", self.parameter[key]["value"])
        
        # Leerzeile nach dem letzten Eintrag
        print("\n")




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

                        "transparency": { 
                                            "type": "int",
                                            "value": 0
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
#=======================================================================================================

class solver(mbsObject):
    # Constructor
    #============
    def __init__(self, text):
        # Initialisieren eines Dictionaries mit den Parametern
        #-----------------------------------------------------
        parameter = {
                        "SimulationTimeBegin":  {
                                                    "type": "float",
                                                    "value": 0.
                                                },

                        "SimulationTimeEnd":    {
                                                    "type": "float",
                                                    "value": 0.
                                                },

                        "OutputTimeBegin":  {
                                                "type": "float",
                                                "value": 0.
                                            },

                        "OutputTimeStepSize":   {
                                                    "type": "float",
                                                    "value": 0.
                                                },

                        "SimulationMinTimeStep":    {
                                                        "type": "float",
                                                        "value": 0.
                                                    },

                        "SimulationMaxTimeStep":    {
                                                        "type": "float",
                                                        "value": 0.
                                                    },
                    }
        
        # Aufrufen des Mutterklassenkonstruktors (Ginge auch mit super, dann müsste man self nicht
        # übergeben)
        mbsObject.__init__(self, "Solver", "Rigid_EulerParameter_PAI", text, parameter)