import vtk

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type 
        self.__subtype = subtype
        self.parameter = parameter              # hier speichern wir den Paramtersatz ab, ist eine Membervariable. Weise ich eine Referenz auf parameter (unten erstell)zu
        self.vtk_actor = None  # Der VTK Actor für die spätere Visualisierung
        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():        #er geht jetzt jedes dieser Objekte durch
                if(splitted[0].strip() ==key):
                    if(parameter[key]["type"] =="float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif parameter[key]["type"] == "string":
                        # Den gesamten Pfad nach 'geometry' extrahieren
                        path = " ".join(splitted[1:]).strip()  # Extrahiere den Pfad
    
                        # Korrigiere den Pfad: Füge Doppelpunkt nach 'C' hinzu, falls nötig
                        if path.startswith("C "):  
                            path = "C:" + path[2:]
    
                        # Ersetze Backslashes durch Schrägstriche
                        path = path.replace("\\", "/")
    
                        # Setze den Wert des Parameters
                        parameter[key]["value"] = self.str2str(path)
    
                        # Setze den Wert des Parameters
                        parameter[key]["value"] = self.str2str(path)
                    elif parameter[key]["type"] == "vectorint":
                        parameter[key]["value"] = self.str2intvec(splitted[1])
                    elif parameter[key]["type"] == "int":
                        parameter[key]["value"] = self.str2int(splitted[1])
    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype +"\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t"+ key +"="+self.float2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t"+ key +"="+self.vector2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "vectorint"):
                text.append("\t"+ key +"="+self.intvec2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "int"):
                text.append("\t"+ key +"="+self.int2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "string"):
                path = self.parameter[key]["value"].strip()
                # Einfach den Doppelpunkt an den richtigen Stellen setzen
                if len(path) > 1 and path[1] == " " and path[0].isalpha():
                    path = path[0] + ":" + path[2:]  # Doppelpunkt anfügen
                path = path.replace("\\", "/")  # Backslashes durch Slashes ersetzen
                text.append(f"\t{key}={path}\n")
        text.append("End" + self.__type + "\n%\n")
        file.writelines(text)
                
    def show (self, renderer):
        self.renderer = renderer
        self.renderer.Addactor(self.actor)

    def connect(self, mbsObjectList):
        return
    
    #Umwandlung string in float
    def str2float(self,inString):
        return float(inString)
    
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def vector2str(self,inVector):
        return str(inVector[0])+","+str(inVector[1])+","+str(inVector[2])
    
    def int2str(self,intString):
        return str(intString)
    
    def str2int(self,stringInt):
        return int(stringInt)
    
    def str2str(self,inString):
        return str(inString)
    
    #def bool2string(self,inBool):
        #return str(inBool)
    
    #def string2bool(self,inString):
        #return bool(inString)
    
    def str2intvec(self,inIntvec):
        return[int(inIntvec.split()[0]),int(inIntvec.split()[1]),int(inIntvec.split()[2])]
    
    def intvec2str(self,invecStr):
        return str(invecStr[0])+ " " + str(invecStr[1])+ " " + str(invecStr[2])
    
    #def floatMatrix3x3toString
    
    def add_vtk_representation(self):
        """Platzhalter, der in den Unterklassen implementiert werden sollte."""
        raise NotImplementedError("Die Methode 'add_vtk_representation' muss in der Unterklasse implementiert werden.")
    

  

#wir wollen das erweiteren damit nicht nur abstrakte Klasse
class rigidbody(mbsObject):
    def __init__(self,text):                    #type brauch ma ned, weil wir wissen dass es ein Rigid Body ist
        parameter={
            "geometry": {"type": "string","value": text},
            "mass": {"type": "float","value":1.},
            "COG":{"type":"vector","value": [0.,0.,0.]},#dictionary --> man gibt hinweise wonach mach sucht
            "position":{"type":"vector","value": [0.,0.,0.]},
            "color": {"type": "vectorint","value":[0,0,0]},
            "transparency": {"type": "float","value":1.},
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParamter_PAI",text,parameter)
        self.bodyActor = None

    def vtk_body(self, renderer):
        # Erstelle den Reader und mapper wie zuvor
        body_data = self.parameter
        bodyReader = vtk.vtkOBJReader()
        bodyReader.SetFileName(body_data["geometry"]["value"])
        bodyReader.Update()

        bodymapper = vtk.vtkPolyDataMapper()
        bodymapper.SetInputConnection(bodyReader.GetOutputPort())

        # Erstelle den Actor
        self.bodyActor = vtk.vtkActor()
        self.bodyActor.SetMapper(bodymapper)

        # Setze Farbe und Transparenz des Actors
        color = body_data["color"]["value"]
        r, g, b = color[0] / 255.0, color[1] / 255.0, color[2] / 255.0  # Umwandlung auf 0-1 Skala
        self.bodyActor.GetProperty().SetColor(r, g, b)

        transparency = body_data["transparency"]["value"]
        self.bodyActor.GetProperty().SetOpacity(transparency)

        # Setze Position des Actors
        position = body_data["position"]["value"]
        self.bodyActor.SetPosition(position[0], position[1], position[2])

        # Füge den Actor dem übergebenen Renderer hinzu
        renderer.AddActor(self.bodyActor)
        
        # Setze den Hintergrund auf die im FDS gespeicherte Hintergrundfarbe
        #bg_color = self.parameter.get("background color", {"value": [0.1, 0.2, 0.4]})["value"]
        #bodyrenderer.SetBackground(bg_color[0], bg_color[1], bg_color[2])
        
        # #Erzeugen eines Renderers, Hinzugfügen eines Atkors und Hintergrund
        # bodyrenderer = vtk.vtkRenderer()
        # bodyrenderer.AddActor(bodyActor)
        # bodyrenderer.SetBackground(0.1, 0.2, 0.4)

        #Erzeugen eines Render Fensters und hinzufügen des Renders
        # renWin = vtk.vtkRenderWindow()
        # renWin.AddRenderer(bodyrenderer)
        # renWin.SetSize(600, 600)
        # renWin.Render()

        # # Interactor für die Interaktivität
        # iren = vtk.vtkRenderWindowInteractor()
        # iren.SetRenderWindow(renWin)
        # iren.Start()

    # def vtk_body(self):
    #     reader = vtk.vtkOBJReader()
    #     reader.SetFileName("path/to/your/model.obj")
    #     reader.Update()
    #     mapper = vtk.vtkPolyDataMapper()
    #     mapper.SetInputConnection(reader.GetOutputPort())
    #     self.vtk_actor = vtk.vtkActor()
    #     self.vtk_actor.SetMapper(mapper)
    #     self.vtk_actor.GetProperty().SetColor(0.5, 0.5, 1.0)

class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "dx": {"type": "int", "value": 1},
            "dy": {"type": "int", "value": 1},
            "dz": {"type": "int", "value": 1},
            "ax": {"type": "int", "value": 1},
            "ay": {"type": "int", "value": 1},
            "az": {"type": "int", "value": 1},
            "position":{"type":"vector","value": [0.,0.,0.]}
        }
        mbsObject.__init__(self,"Constraint", "Fixed", text, parameter)

    #Visualisieren eines OBJ-Files
    #-----------------------
    def vtk_body(self):
        body_data=self.parameter
        
        #Erzeugen eines Readers
        bodyReader = vtk.vtkOBJReader()

        #Erzeugen einer Quelle
        body = bodyReader.SetFileName("C:/vis2024/VIS_2024/Aufgabe_2/quader.obj")
        bodyReader.Update()

        #Erzeugen eines Filters mit dem Eingang body
        bodymapper = vtk.vtkPolyDataMapper()
        bodymapper.SetInputConnection(bodyReader.GetOutputPort())

        #Erzeugen eines Aktors (Filter als Eingang) 
        bodyActor = vtk.vtkActor()
        bodyActor.SetMapper(bodymapper)

        #Erzeugen eines Renderers, Hinzugfügen eines Atkors und Hintergrund
        bodyrenderer = vtk.vtkRenderer()
        bodyrenderer.AddActor(bodyActor)
        bodyrenderer.SetBackground(0.1, 0.2, 0.4)

        #Erzeugen eines Render Fensters und hinzufügen des Renders
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(bodyrenderer)
        renWin.SetSize(600, 600)
        renWin.Render()


    def writeInputfile(self, file):
        super().writeInputfile(file)
        
class settings(mbsObject):
    def __init__(self, text):
        parameter = {
            "COG marker scale": {"type": "float","value":1.},
            "constraint icon scale": {"type": "float","value":1.},
            "force icon scale": {"type": "float","value":1.},
            "gravity_vector":{"type":"vector","value": [0.,0.,0.]},
            "background color": {"type": "vectorint","value":[0,0,0]},

        }
        mbsObject.__init__(self,"Settings", "Gravity", text, parameter)