import vtk
import numpy as np
import math

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.parameter = parameter  #self.parameter ist membervariable, der wird referenz auf parameter zugewiesen
                                    # es ist also egal, ob man self.parameter oder parameter schreibt
        self.__subtype = subtype

        #Defaultparameter
        self.default_vec = [1.,1.,1.]
        self.default_intvec = [1,1,1]
        self.default_float = 1.
        self.default_int = 1
        self.default_bool = 0
        self.default_string = "DEFAULT"

        #Aktor erstellen
        self.actor = vtk.vtkActor()
        self.textactor = vtk.vtkTextActor()

        #Mapper anlegen
        self.mapper = vtk.vtkPolyDataMapper()


        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():                    #über dictionary drüber suchen... parameter.keys() = mass, COG...
                if(splitted[0].strip() == key):             # strip = alle unnötigen Leerzeichen weg
                    if(parameter[key]["type"] == "float"):                          # Behandlung, wenn key ein float ist
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):                       # Behandlung, wenn key ein vector ist
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "str"):                          # Behandlung, wenn key ein string ist
                        parameter[key]["value"] = self.str2str(splitted[1].strip())
                    elif(parameter[key]["type"] == "bool"):                          # Behandlung, wenn key ein bool ist
                        parameter[key]["value"] = self.str2bool(splitted[1])
                    elif(parameter[key]["type"] == "intvec"):                        # Behandlung, wenn key ein intvec (color) ist
                        parameter[key]["value"] = self.str2intvec(splitted[1])
                    elif(parameter[key]["type"] == "int"):                        # Behandlung, wenn key ein int ist
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif(parameter[key]["type"] == "geom_path"):                        # Behandlung, wenn key ein geom_path ist
                        parameter[key]["value"] = self.str2str(line[10:])

    def forceArrow(self, direction, position, color, size, renderer):
        #Pfeil erstellen
        arrow = vtk.vtkArrowSource()
        self.mapper.SetInputConnection(arrow.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        #Richtung auf Einheitsvektor normieren
        dirLength = np.linalg.norm(direction)
        if dirLength == 0:
            raise ValueError("Die Richtung darf kein Nullvektor sein.")
        directionNorm = direction / dirLength

        #Richtungsvektor als Basis zum Berechnen der 2 fehlenden Vektoren
        xdir = directionNorm

        #orthogonale Vektoren finden durch Kreuzprodukt
        hilfsvec = np.array([0.0, 0.0, 1.0])
        if np.allclose(xdir, hilfsvec) or np.allclose(xdir, -hilfsvec):
            hilfsvec = np.array([0.0, 1.0, 0.0])  #Anderen Vektor wählen, wenn parallel

        ydir = np.cross(hilfsvec, xdir)  #y Achse normal zu x (Richtung)
        ydir = ydir / np.linalg.norm(ydir)  #Einheitsvektor
        zdir = np.cross(xdir, ydir)  #z Achse normal zu x und y
        zdir = zdir / np.linalg.norm(zdir) #Einheitsvektor

        #Transformation
        transform = vtk.vtkTransform()
        transform.Translate(position[0], position[1], position[2])
        transform.Concatenate([
            xdir[0], ydir[0], zdir[0], 0,
            xdir[1], ydir[1], zdir[1], 0,
            xdir[2], ydir[2], zdir[2], 0,
            0, 0, 0, 1])

        #Anwenden der Transformation
        self.actor.SetUserTransform(transform)
        self.actor.SetScale(size, size, size)
        self.actor.GetProperty().SetColor(color[0], color[1], color[2])

        #Actor zum Renderer hinzufügen
        renderer.AddActor(self.actor)


    def writeInputFile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "str"):
                text.append("\t" + key + " = " + self.str2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "bool"):
                 text.append("\t" + key + " = " + self.bool2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "intvec"):
                 text.append("\t" + key + " = " + self.intvec2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "int"):
                 text.append("\t" + key + " = " + self.int2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "geom_path"):
                 text.append("\t" + key + " = " + self.str2str(self.parameter[key]["value"]) + "\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)   #writelines ist eine Zugriffsfunktion auf Datei

    # Datentypen konvertieren
    def str2float(self,inString):  # string in Float konvertieren
        return float(inString)
    
    def float2str(self,inFloat):  
        return str(inFloat)

    def str2vector(self,inString): # string in Vektor umbasteln
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]

    def vector2str(self,inVector): 
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    def str2str(self,inString):
        return str(inString)
    
    def str2bool(self,inString):
        return bool(inString)
    
    def bool2str(self,inBool):
        return str(inBool)
    
    def str2intvec(self,inString):
        return [int(inString.split()[0]),int(inString.split()[1]),int(inString.split()[2])]
    
    def intvec2str(self,inIntvec):
        return str(inIntvec[0]) + "," + str(inIntvec[1]) + "," + str(inIntvec[2])
    
    def str2int(self,inString):
        return int(inString)
    
    def int2str(self,inInt):
        return str(inInt)


class rigidBody(mbsObject):
    def __init__(self,text):                            #type brauchen wir nicht, weil ich bin ein Rigid Body
        super().__init__("Body","Rigid_EulerParameter_PAI", text, {})  # Mutterklasse initialisieren
        parameter = {                                   #dictionary (key & value) mit den parametern
            "name": {"type": "str", "value": self.default_string},
            "mass": {"type": "float", "value": self.default_float},     #sollte die Masse nicht gefunden werden, wird der default Wert 1 gesetzt bleiben
            "COG": {"type": "vector", "value": self.default_vec},
            "position": {"type": "vector", "value": self.default_vec},
            "geometry": {"type": "geom_path", "value": "C:\test"},  
            "x_axis": {"type": "vector", "value": self.default_vec},
            "y_axis": {"type": "vector", "value": self.default_vec},
            "z_axis": {"type": "vector", "value": self.default_vec},
            "color": {"type": "intvec", "value": self.default_intvec},
            "transparency": {"type": "int", "value": self.default_int}, 
            "inertia": {"type": "vector", "value": self.default_vec},
            "initial_velocity": {"type": "vector", "value": self.default_vec},
            "initial_omega": {"type": "vector", "value": self.default_vec},
            "i1_axis": {"type": "vector", "value": self.default_vec},
            "i2_axis": {"type": "vector", "value": self.default_vec},
            "i3_axis": {"type": "vector", "value": self.default_vec}
        } 

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)       #wenn man es so aufruft, braucht man auch das init

    def show(self, renderer):
        """
        Visualisierung des rigidBodies 
        """
        #Geometriepfad des OBJ einlesen
        geometry_path = self.parameter["geometry"]["value"]
        reader = vtk.vtkOBJReader()
        reader.SetFileName(geometry_path)
        reader.Update()

      
        self.mapper.SetInputConnection(reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        #Position aus Parametern setzen
        position = self.parameter["position"]["value"]
        self.actor.SetPosition(position)

        #Rotation mittels Achsen des rigidBody (sind aus Freedyn bereits Einheitsvektoren :))
        transform = vtk.vtkTransform()
        xdir = self.parameter["x_axis"]["value"]
        ydir = self.parameter["y_axis"]["value"]
        zdir = self.parameter["z_axis"]["value"]
        transform.Concatenate([xdir[0],ydir[0],zdir[0],0,
                               xdir[1],ydir[1],zdir[1],0,
                               xdir[2],ydir[2],zdir[2],0,
                               0,0,0,1])
        self.actor.SetUserTransform(transform)

        #Farbe aus Parametern setzen
        color = self.parameter["color"]["value"]
        self.actor.GetProperty().SetColor(color[0] / 255, color[1] / 255, color[2] / 255)

        #Transparenz aus Parametern setzen
        transparency = self.parameter["transparency"]["value"]
        self.actor.GetProperty().SetOpacity(1 - transparency / 100)

        #Actor zum Renderer hinzufügen
        renderer.AddActor(self.actor)


class constraint(mbsObject):
    def __init__(self, text):
        super().__init__("Constraint", "GenericConstraint", text, {})  # Mutterklasse initialisieren
        parameter = {
            "name": {"type": "str", "value": self.default_string},
            "body1": {"type": "str", "value": self.default_string},
            "body2": {"type": "str", "value": self.default_string},
            "dx": {"type": "bool", "value": self.default_bool},
            "dy": {"type": "bool", "value": self.default_bool},
            "dz": {"type": "bool", "value": self.default_bool},
            "ax": {"type": "bool", "value": self.default_bool},
            "ay": {"type": "bool", "value": self.default_bool},
            "az": {"type": "bool", "value": self.default_bool},
            "position": {"type": "vector", "value": self.default_vec},
            "x_axis": {"type": "vector", "value": self.default_vec},
            "y_axis": {"type": "vector", "value": self.default_vec},
            "z_axis": {"type": "vector", "value": self.default_vec}
        }
        super().__init__("Constraint", "GenericConstraint", text, parameter)
        #self.add_constraint_actor()

    def show(self, renderer):
        """
        Visualisierung der Constraint
        """
        # Erstelle eine Kugel
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(2)  # Radius der Kugel
        sphere.SetPhiResolution(10)
        sphere.SetThetaResolution(10)
        

        self.mapper.SetInputConnection(sphere.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        #Position aus Parametern setzen
        position = self.parameter["position"]["value"]
        self.actor.SetPosition(position)  # Position des Constraints

        #Farbe 
        self.actor.GetProperty().SetColor(0, 0, 1)  # RGB-Werte

        #Actor zum Renderer hinzufügen
        renderer.AddActor(self.actor)


class settings(mbsObject):
    def __init__(self,text):
        super().__init__("Settings", "Settings", text, {})  # Mutterklasse initialisieren
        self.parameter = {                                   
            "gravity_vector": {"type": "vector", "value": self.default_vec},
        } 
        mbsObject.__init__(self,"Settings","Settings",text,self.parameter)

    def show(self, renderer):
        if self.parameter["gravity_vector"]["value"] == self.default_vec:
            self.textactor.SetInput("GRAVITY (x y z) = error")
        else:
            self.textactor.SetInput("GRAVITY (x y z) = " + self.vector2str(self.parameter["gravity_vector"]["value"]))
        self.textactor.GetTextProperty().SetFontSize(24)
        self.textactor.GetTextProperty().SetColor(0, 0, 0)  #Schwarzer Text
        self.textactor.SetPosition(10, 40)
        renderer.AddActor2D(self.textactor)


class genericForce(mbsObject):
    def __init__(self,text):
        super().__init__("Force", "Generic_Force", text, {})  # Mutterklasse initialisieren
        self.parameter = {                                   
            "name": {"type": "str", "value": self.default_string},
            "body1": {"type": "str", "value": self.default_string},
            "body2": {"type": "str", "value": self.default_string},
            "PointOfApplication_Body1": {"type": "vector", "value": self.default_vec},
            "PointOfApplication_Body2": {"type": "vector", "value": self.default_vec},
            "direction": {"type": "vector", "value": self.default_vec},
        } 
        mbsObject.__init__(self,"Force","Generic_Force",text,self.parameter)

    def show(self, renderer):
        """
        Visualisierung des rigidBodies 
        """
        self.forceArrow(self.parameter["direction"]["value"],self.parameter["PointOfApplication_Body1"]["value"],[1,0,0],15,renderer)


class genericTorque(mbsObject):
    def __init__(self,text):
        super().__init__("Force", "Generic_Torque", text, {})  # Mutterklasse initialisieren
        self.parameter = {                                   
            "name": {"type": "str", "value": self.default_string},
            "body1": {"type": "str", "value": self.default_string},
            "body2": {"type": "str", "value": self.default_string},
            "direction": {"type": "vector", "value": self.default_vec},
        } 
        mbsObject.__init__(self,"Force","Generic_Torque",text,self.parameter)