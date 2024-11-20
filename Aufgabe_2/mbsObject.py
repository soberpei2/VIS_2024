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
    
    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype +"\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "Float"):
                text.append("\t"+ key +"="+self.float2str(self.parameter[key]["value"])+"\n")
            if(self.parameter[key]["type"] == "vector"):
                text.append("\t"+ key +"="+self.vector2str(self.parameter[key]["value"])+"\n")
        text.append("End" + self.__type+"\n%\n")

        file.writelines(text)
                
    
    #Umwandlung string in float
    def str2float(self,inString):
        return float(inString)
    
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def vector2str(self,inVector):
        return str(inVector[0])+","+str(inVector[1])+","+str(inVector[2])
    
    def add_vtk_representation(self):
        # Standardimplementierung, wenn keine spezifische Darstellung definiert ist
        print(f"Keine VTK-Darstellung für {self.__type} {self.__subtype} definiert.")
        return None
    
    def get_vtk_actor(self):
        return self.vtk_actor
  

#wir wollen das erweiteren damit nicht nur abstrakte Klasse
class rigidbody(mbsObject):
    def __init__(self,text):                    #type brauch ma ned, weil wir wissen dass es ein Rigid Body ist
        parameter={
            "mass": {"type": "float","value":1.},
            "COG":{"type":"vector","value": [0.,0.,0.]}#dictionary --> man gibt hinweise wonach mach sucht
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParamter_PAI",text,parameter)

    def add_vtk_representation(self):
        reader = vtk.vtkOBJReader()
        reader.SetFileName("path/to/your/model.obj")
        reader.Update()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(mapper)
        self.vtk_actor.GetProperty().SetColor(0.5, 0.5, 1.0)

