import vtk

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.parameter = parameter  #self.parameter ist membervariable, der wird referenz auf parameter zugewiesen
                                    # es ist also egal, ob man self.parameter oder parameter schreibt
        self.__subtype = subtype

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
        parameter = {                                   #dictionary (key & value) mit den parametern
            "name": {"type": "str", "value": "name"},
            "mass": {"type": "float", "value": 1.},     #sollte die Masse nicht gefunden werden, wird der default Wert 1 gesetzt bleiben
            "COG": {"type": "vector", "value": [1.,1.,1.]},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "geometry": {"type": "geom_path", "value": "C:\test"},  
            "x_axis": {"type": "vector", "value": [1.,1.,1.]},
            "y_axis": {"type": "vector", "value": [1.,1.,1.]},
            "z_axis": {"type": "vector", "value": [1.,1.,1.]},
            "color": {"type": "intvec", "value": [0,0,0]},
            "transparency": {"type": "int", "value": 0}, 
            "inertia": {"type": "vector", "value": [1.,1.,1.]},
            "initial_velocity": {"type": "vector", "value": [1.,1.,1.]},
            "initial_omega": {"type": "vector", "value": [1.,1.,1.]},
            "i1_axis": {"type": "vector", "value": [1.,1.,1.]},
            "i2_axis": {"type": "vector", "value": [1.,1.,1.]},
            "i3_axis": {"type": "vector", "value": [1.,1.,1.]}
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

        #Mapper anlegen
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        #Aktor anlegen
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        #Position aus Parametern setzen
        position = self.parameter["position"]["value"]
        actor.SetPosition(position)

        #Rotation mittels Achsen des rigidBody (sind aus Freedyn bereits Einheitsvektoren :))
        transform = vtk.vtkTransform()
        xdir = self.parameter["x_axis"]["value"]
        ydir = self.parameter["y_axis"]["value"]
        zdir = self.parameter["z_axis"]["value"]
        transform.Concatenate([xdir[0],ydir[0],zdir[0],0,
                               xdir[1],ydir[1],zdir[1],0,
                               xdir[2],ydir[2],zdir[2],0,
                               0,0,0,1])
        actor.SetUserTransform(transform)

        #Farbe aus Parametern setzen
        color = self.parameter["color"]["value"]
        actor.GetProperty().SetColor(color[0] / 255, color[1] / 255, color[2] / 255)

        #Transparenz aus Parametern setzen
        transparency = self.parameter["transparency"]["value"]
        actor.GetProperty().SetOpacity(1 - transparency / 100)

        #Actor zum Renderer hinzufügen
        renderer.AddActor(actor)


class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "nameDEF"},
            "body1": {"type": "str", "value": "body1DEF"},
            "body2": {"type": "str", "value": "body2DEF"},
            "dx": {"type": "bool", "value": "0"},
            "dy": {"type": "bool", "value": "0"},
            "dz": {"type": "bool", "value": "0"},
            "ax": {"type": "bool", "value": "0"},
            "ay": {"type": "bool", "value": "0"},
            "az": {"type": "bool", "value": "0"},
            "position": {"type": "vector", "value": [0.0, 0.0, 0.0]},
            "x_axis": {"type": "vector", "value": [0.0, 0.0, 0.0]},
            "y_axis": {"type": "vector", "value": [0.0, 0.0, 0.0]},
            "z_axis": {"type": "vector", "value": [0.0, 0.0, 0.0]}
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
        
        #Mapper anlegen
        sphere_mapper = vtk.vtkPolyDataMapper()
        sphere_mapper.SetInputConnection(sphere.GetOutputPort())

        #Aktor anlegen
        sphere_actor = vtk.vtkActor()
        sphere_actor.SetMapper(sphere_mapper)

        #Position aus Parametern setzen
        position = self.parameter["position"]["value"]
        sphere_actor.SetPosition(position)  # Position des Constraints

        #Farbe 
        sphere_actor.GetProperty().SetColor(0, 0, 1)  # RGB-Werte

        #Actor zum Renderer hinzufügen
        renderer.AddActor(sphere_actor)


class settings(mbsObject):
    def __init__(self,text):
        parameter = {                                   
            "gravity_vector": {"type": "vector", "value": [1.,1.,1.]},
        } 

        mbsObject.__init__(self,"Settings","Settings",text,parameter)
