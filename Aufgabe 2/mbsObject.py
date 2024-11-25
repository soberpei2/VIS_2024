import vtk

#Mutterklasse
class mbsObject: 
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actor = None
        self.create_actor()
        
        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
    
    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t"+key+" = "+self.float2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")
            #elif(self.parameter[key]["type"] == "string"):     ##################################################################################################
            elif(self.parameter[key]["type"] == "filepath"):
                text.append("\t"+key+" = "+ self.parameter[key]["value"] +"\n")

        text.append("End"+self.__type+"\n\n") #text.append("End"+self.__type+"\n%\n")############
        file.writelines(text)

    def show(self, renderer):
        #self.renderer = renderer
        #self.renderer.AddActor(self.actor)
        print(f"Rendering object: {self.parameter}")
        renderer.AddActor(self.actor)

    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)

    def str2vector(self, inString):
        # Entferne überflüssige Leerzeichen und trenne bei Leerzeichen oder Kommata
        values = [v for v in inString.replace(",", " ").split() if v.strip()]
        # Konvertiere die ersten drei Werte in Floats und ignoriere den Rest/ wegen der Farbe mit 4 Werten. Transparenz ist ja in nächster Zeile gegeben
        try:
            return [float(values[i]) for i in range(min(3, len(values)))]
        except ValueError as e:
            print(f"Fehler beim Konvertieren von Werten: {values}")
            raise e
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    
class rigidBody(mbsObject):
    def __init__(self,text):

        parameter = {
            "position":          {"type": "vector", "value": [0.,0.,0.]},
            "color":             {"type": "vector", "value": [0.,0.,0.]},
            "transparency":       {"type": "float", "value": 1},
            "initial velocity":  {"type": "vector", "value": [0.,0.,0.]},
            "initial omega":     {"type": "vector", "value": [0.,0.,0.]},
            "mass":              {"type": "float", "value": 1.},
            "COG":               {"type": "vector", "value": [0.,0.,0.]},
            "inertia":           {"type": "vector", "value": [0.,0.,0.,]}
        }


        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)

        
    def create_actor(self):
        obj_path = r"C:/Users/hanne\Desktop/VIS/VIS_2024\Aufgabe 2/quader.obj"  # Absoluter Pfad zur Datei
        obj_reader = vtk.vtkOBJReader()
        obj_reader.SetFileName(obj_path)  # Beispiel: Ihre Datei "quader.obj"
        obj_reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(obj_reader.GetOutputPort())

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        #color = [c / 255 for c in self.parameter["color"]["value"]]
        #self.actor.GetProperty().SetColor(color)
        #self.actor.GetProperty().SetOpacity(self.parameter["transparency"]["value"])


class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            #"name":     {"type": "string", "value": ""}, #string!!
            "dx":       {"type": "float", "value": 0.},
            "dy":       {"type": "float", "value": 0.},
            "dz":       {"type": "float", "value": 0.},
            "ax":       {"type": "float", "value": 0.},
            "ay":       {"type": "float", "value": 0.},
            "az":       {"type": "float", "value": 0.},

            "bodies":   {"type": "list", "value": []},  # Unterstützung für beliebig viele Körper!!!!?
            "position": {"type": "vector", "value": [0., 0., 0.]},
            #"x_axis": {"type": "vector", "value": [1., 0., 0.]},
            #"y_axis": {"type": "vector", "value": [0., 1., 0.]},
            #"z_axis": {"type": "vector", "value": [0., 0., 1.]}            
        }

        mbsObject.__init__(self, "Constraint", "Generic", text, parameter)

    def create_actor(self):
        arrow = vtk.vtkArrowSource()
        arrow.SetTipLength(0.3)
        arrow.SetTipRadius(0.1)
        arrow.SetShaftRadius(0.03)

        transform = vtk.vtkTransform()
        transform.Translate(self.parameter["position"]["value"])
        transform.Scale([self.parameter["dx"]["value"], self.parameter["dy"]["value"], self.parameter["dz"]["value"]])

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(arrow.GetOutputPort())
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

class genericForce(mbsObject):
    def __init__(self, text):
        parameter = {
            #"name":                   {"type": "string", "value": ""}, #string!!
            "bodies":                 {"type": "list", "value": []},  # Unterstützung für beliebig viele Körper!!!!?
            "PointOfApplication":     {"type": "vector", "value": [0., 0., 0.]}, # zwishen 2 bodies!
            "mode":                   {"type": "string", "value": ""}, #string!!
            "direction":              {"type": "vector", "value": [0., 0., 0.]}
            #"ForceExpression":       {"type": "string", "value": ""}
        }
        mbsObject.__init__("Force", "GenericForce", text, parameter)

    def create_actor(self):
        arrow = vtk.vtkArrowSource()
        arrow.SetTipLength(0.3)
        arrow.SetTipRadius(0.1)
        arrow.SetShaftRadius(0.03)

        transform = vtk.vtkTransform()
        direction = self.parameter["direction"]["value"]
        position = self.parameter["position"]["value"]

        transform.Translate(position)
        transform.Scale([d * self.parameter["magnitude"]["value"] for d in direction])

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(arrow.GetOutputPort())
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        
class genericTorque(mbsObject):
    def __init__(self, text):
        parameter = {
            #"name":                   {"type": "string", "value": ""}, #string!!
            "bodies":                 {"type": "list", "value": []},  # Unterstützung für beliebig viele Körper!!!!?
            "mode":                   {"type": "string", "value": ""}, #string!!
            "direction":              {"type": "vector", "value": [0., 0., 0.]}
            #"TorqueExpression":
        }
        mbsObject.__init__("Force", "GenericForce", text, parameter)
    
    def create_actor(self):
        circle = vtk.vtkRegularPolygonSource()
        circle.SetCenter(self.parameter["position"]["value"])
        circle.SetNormal(self.parameter["direction"]["value"])
        circle.SetRadius(1.0)
        circle.SetNumberOfSides(50)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(circle.GetOutputPort())

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(0, 1, 0)
