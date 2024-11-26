import vtk

class mbsObject:

    def __init__(self, type, subtype, text, parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        self.actor = vtk.vtkActor()
        self.textactor = vtk.vtkTextActor()
        self.mapper = vtk.vtkPolyDataMapper()

        for line in text:
            splitted = line.split(":")

            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = (splitted[1])
                    elif(parameter[key]["type"] == "path"):
                        parameter[key]["value"] = line[10:]
                    

    def writeInputfile(self, file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n") 
            elif(self.parameter[key]["type"] == "string"):
                text.append("\t" + key + " = " + self.parameter[key]["value"] + "\n") 
            elif(self.parameter[key]["type"] == "path"):
                text.append("\t" + key + " = " + self.parameter[key]["value"] + "\n") 

        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)

    def str2float(self, inString):
        return float(inString)
    def float2str(self, inFloat):
        return str(inFloat)
    def str2vector(self, inString):
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]
    def vector2str(self, inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
      
        
#######################################################################################

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "string", "value": "Name prüfen"},
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0., 0., 0.]},
            "position": {"type": "vector", "value": [0., 0., 0.]},
            "geometry": {"type": "path", "value": "Pfad prüfen"},
            "transparency": {"type": "float", "value": 0.},
            "x_axis": {"type": "vector", "value": [1., 1., 1.]},
            "y_axis": {"type": "vector", "value": [1., 1., 1.]}, 
            "z_axis": {"type": "vector", "value": [1., 1., 1.]},
            "color" : {"type": "color", "value" : [128,128,128]} 
            }
        mbsObject.__init__(self, "rigidBody", "Rigid_EulerParameter_PAI", text, parameter)

    def show(self, renderer):
        path = self.parameter["geometry"]["value"]
        reader = vtk.vtkOBJReader()
        reader.SetFileName(path)
        reader.Update()

        self.mapper.SetInputConnection(reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        position = self.parameter["position"]["value"]
        self.actor.SetPosition(position)

        #color = self.parameter["color"]["value"]
        #self.actor.GetProperty().SetColor(color[0] / 255, color[1] / 255, color[2] / 255)

        #transparency = self.parameter["transparency"]["value"]
        #self.actor.GetProperty().SetOpacity(1 - transparency / 100)

        renderer.AddActor(self.actor)


#######################################################################################
class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "string", "value": "Name prüfen"},
            "body1": {"type": "string", "value": "Body1 Text prüfen"},
            "body2": {"type": "string", "value": "Body2 Text prüfen"},
            "position": {"type": "vector", "value": [0., 0., 0.]},
            "x_axis": {"type": "vector", "value": [1., 1., 1.]},
            "y_axis": {"type": "vector", "value": [1., 1., 1.]}, 
            "z_axis": {"type": "vector", "value": [1., 1., 1.]},
            }
        mbsObject.__init__(self, "constraint", "Constraint", text, parameter)
    
    def show(self, renderer):
        
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1)
        sphere.SetPhiResolution(10)
        sphere.SetThetaResolution(10)

        self.mapper.SetInputConnection(sphere.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        position = self.parameter["position"]["value"]
        self.actor.SetPosition(position)

        self.actor.GetProperty().SetColor(1,1,1)

        renderer.AddActor(self.actor)
#######################################################################################
class genericForce(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "string", "value": "Name prüfen"},
            "body1": {"type": "string", "value": "Body1 Text prüfen"},
            "body2": {"type": "string", "value": "Body2 Text prüfen"},
            "PointOfApplication_Body1": {"type": "vector", "value": [0., 0., 0.]},
            "PointOfApplication_Body2": {"type": "vector", "value": [0., 0., 0.]},
            "direction": {"type": "vector", "value": [0., 0., 0.]},
            }

        mbsObject.__init__(self, "genericForce", "Force", text, parameter)

#######################################################################################
class settings(mbsObject):
    def __init__(self, text):
        parameter = {
                        "gravity_vector": {"type": "vector", "value": [0.,0.,0.]},
                        "geometry": {"type": "path", "value": "C:\\Users\\lukas\\VIS_2024\\Aufgabe_2\\quader.obj"}
                    }   

        mbsObject.__init__(self, "settings", "Settings", text, parameter)

    def show(self, renderer):
        if self.parameter["gravity_vector"]["value"] == [0.,0.,0.]:
            self.textactor.SetInput("Keine Gravitation")
        else:
            self.textactor.SetInput("GRAVITY (x y z) = " + self.vector2str(self.parameter["gravity_vector"]["value"]))
        
        renderer.AddActor2D(self.textactor)