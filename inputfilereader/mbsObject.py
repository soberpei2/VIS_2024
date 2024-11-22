import vtk

class mbsObject: 
    def __init__(self,type,subtype,text,parameter): 
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actor = vtk.vtkActor()      # wird immer benötigt

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):         #strip leert 
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = (splitted[1])         # für constraint
                    elif(parameter[key]["type"] == "path"):
                        parameter[key]["value"] = self.Path2str(line)         # für constraint 


    def writeInputfile(self, file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "string"):
                text.append("\t" + key + " = " + (self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "path"):
                text.append("\t" + key + " = " + (self.parameter[key]["value"])+"\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)

    # zum umrechnen 
    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    def Path2str(self,inString):
        return inString[10:]

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            # dictonary mit keys 
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.]}, #center of gravity
            "position": {"type": "vector", "value": [0.,0.,0.]}, # position des Vektors
            "geometry": {"type": "path", "value": "unbekannt"}, # Pfad der Geometrie
            "x_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in x 
            "y_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in y
            "z_axis": {"type": "vector", "value": [0.,0.,0.]} # Ausrichtung in z
        }
        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI", text,parameter)  # euler koordinaten und PAI pricip ... inertia

        # Einlesen der Geometrie
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Actor erstellen
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(1.0, 0.5, 0.3)

        # Transformation basierend auf der Position und Orientierung
        self.apply_transformations()

    def apply_transformations(self):
        """Wendet die Position und Orientierung an den Actor an."""
        transform = vtk.vtkTransform()
        
        # Setze Translation
        pos = self.parameter["position"]["value"]
        transform.Translate(pos[0], pos[1], pos[2])

        # Setze Orientierung (Rotationsmatrix aus x_axis, y_axis, z_axis)
        x_axis = self.parameter["x_axis"]["value"]
        y_axis = self.parameter["y_axis"]["value"]
        z_axis = self.parameter["z_axis"]["value"]
        transform.Concatenate([x_axis[0], y_axis[0], z_axis[0], 0,
                               x_axis[1], y_axis[1], z_axis[1], 0,
                               x_axis[2], y_axis[2], z_axis[2], 0,
                               0, 0, 0, 1])

        # Transformation dem Actor zuweisen
        self.actor.SetUserTransform(transform)

class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            # dict
            "body1": {"type": "string", "value": "leer"},
            "body2": {"type": "string", "value": "leer"},
        }
        mbsObject.__init__(self,"Constraint","Constraint_EulerParameter_PAI", text,parameter)


class settings(mbsObject):
    def __init__(self,  text):
        parameter = {
            #dict
    	    "gravity_vector": {"type": "vector", "value": [0.,0.,-9.81]},
        }
        mbsObject.__init__(self,"Settings","Visualization", text,parameter)
        
"""""
def visualizeBody(FirstobjPath):
        # input: filepath of the geometrie
        import vtk    
    
        ColorBackground = [0.0, 0.0, 0.0]
        reader = vtk.vtkOBJReader()
        reader.SetFileName(FirstobjPath)
        reader.Update()


        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create a rendering window and renderer
        ren = vtk.vtkRenderer()
        ren.SetBackground(ColorBackground)
        renWin = vtk.vtkRenderWindow()
        renWin.AddRenderer(ren)

        # Create a renderwindowinteractor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(renWin)

        # Assign actor to the renderer
        ren.AddActor(actor)

        # Enable user interface interactor
        iren.Initialize()
        renWin.Render()
        iren.Start()
"""
