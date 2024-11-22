import vtk

#------------------------------------------------------------------------------------------------------------------

# MUTTERKLASSE

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.parameter = parameter  #self.parameter ist membervariable, der wird referenz auf parameter zugewiesen
                                    # es ist also egal, ob man self.parameter oder parameter schreibt
        self.__subtype = subtype

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():                    #über dictionary drüber suchen... parameter.keys() = mass und COG
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

    def add_vtk_actor(self, actor):
        """Fügt einen VTK-Actor zur Liste hinzu."""
        self.vtkActors.append(actor)

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
    
    def intvec2str(self,inintvec):
        return str(inintvec[0]) + "," + str(inintvec[1]) + "," + str(inintvec[2])


#in den Unterklassen wird dann nach den Eigenschaften gesucht
# -----------------------------------------------------------------------


class rigidBody(mbsObject):
    def __init__(self,text):                            #type brauchen wir nicht, weil ich bin ein Rigid Body
        parameter = {                                   #dictionary (key & value) mit den parametern
            "name": {"type": "str", "value": "name"},
            "mass": {"type": "float", "value": 1.},     #sollte die Masse nicht gefunden werden, wird der default Wert 1 gesetzt bleiben
            "COG": {"type": "vector", "value": [1.,1.,1.]},
            "geometry": {"type": "str", "value": "body.obj"},  # Standardmäßige Geometrie
            "x_axis": {"type": "vector", "value": [1.,1.,1.]},
            "y_axis": {"type": "vector", "value": [1.,1.,1.]},
            "z_axis": {"type": "vector", "value": [1.,1.,1.]},
            "color": {"type": "intvec", "value": [0,0,0]},
            "inertia": {"type": "vector", "value": [1.,1.,1.]},
            "initial_velocity": {"type": "vector", "value": [1.,1.,1.]},
            "initial_omega": {"type": "vector", "value": [1.,1.,1.]},
            "i1_axis": {"type": "vector", "value": [1.,1.,1.]},
            "i2_axis": {"type": "vector", "value": [1.,1.,1.]},
            "i3_axis": {"type": "vector", "value": [1.,1.,1.]}
        } 

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)       #wenn man es so aufruft, braucht man auch das init
    
    def add_geometry_actor(self):
        """Lädt eine OBJ-Datei und erstellt einen VTK-Actor."""
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.add_vtk_actor(actor)

# -----------------------------------------------------------------------

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

    # def add_constraint_actor(self):
    #     """Erstellt eine grafische Darstellung für Constraints."""
    #     sphere = vtk.vtkSphereSource()
    #     sphere.SetCenter(self.parameter["location"]["value"])
    #     sphere.SetRadius(0.1)
    #     mapper = vtk.vtkPolyDataMapper()
    #     mapper.SetInputConnection(sphere.GetOutputPort())
    #     actor = vtk.vtkActor()
    #     actor.SetMapper(mapper)
    #     actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Rot für Constraints
    #     self.add_vtk_actor(actor)

# -----------------------------------------------------------------------

class settings(mbsObject):
    def __init__(self,text):
        parameter = {                                   
            "gravity_vector": {"type": "vector", "value": [1.,1.,1.]},
        } 

        mbsObject.__init__(self,"Settings","Settings",text,parameter)

# -----------------------------------------------------------------------

class gravityForce(mbsObject):
    def __init__(self, text):
        parameter = {
            "magnitude": {"type": "float", "value": 9.81},
            "direction": {"type": "vector", "value": [0.0, -1.0, 0.0]},
        }
        super().__init__("Force", "Gravity", text, parameter)
        
        #self.add_gravity_actor()

    # def add_gravity_actor(self):
    #     """Erstellt eine Pfeildarstellung für die Schwerkraft."""
    #     arrow = vtk.vtkArrowSource()
    #     mapper = vtk.vtkPolyDataMapper()
    #     mapper.SetInputConnection(arrow.GetOutputPort())
    #     actor = vtk.vtkActor()
    #     actor.SetMapper(mapper)
    #     actor.GetProperty().SetColor(0.0, 0.0, 1.0)  # Blau für Gravity
    #     self.add_vtk_actor(actor)

# -----------------------------------------------------------------------

class genericTorque(mbsObject):
    def __init__(self, text):
        parameter = {
            "magnitude": {"type": "float", "value": 1.0},
            "location": {"type": "vector", "value": [0.0, 0.0, 0.0]},
        }
        super().__init__("Force", "GenericTorque", text, parameter)
        self.add_torque_actor()

    def add_torque_actor(self):
        """Erstellt eine Darstellung für das Drehmoment."""
        cone = vtk.vtkConeSource()
        cone.SetCenter(self.parameter["location"]["value"])
        cone.SetRadius(0.2)
        cone.SetHeight(0.5)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cone.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1.0, 1.0, 0.0)  # Gelb für Drehmoment
        self.add_vtk_actor(actor)

# -----------------------------------------------------------------------

class measure(mbsObject):
    def __init__(self, text):
        parameter = {
            "type": {"type": "string", "value": "distance"},
            "points": {"type": "vector", "value": [0.0, 0.0, 0.0, 1.0, 1.0, 1.0]},
        }
        super().__init__("Measure", "DistanceMeasure", text, parameter)
        self.add_measure_actor()

    def add_measure_actor(self):
        """Erstellt eine Darstellung für Messungen."""
        line = vtk.vtkLineSource()
        line.SetPoint1(self.parameter["points"]["value"][:3])
        line.SetPoint2(self.parameter["points"]["value"][3:])
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.0, 1.0, 0.0)  # Grün für Measures
        self.add_vtk_actor(actor)