
import os

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actors = []

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"]=="string"):
                        parameter[key]["value"] = splitted[1].strip()
                    elif(parameter[key]["type"]=="filepath"):
                        parameter[key]["value"] = os.path.normpath(line[len(key)+1:].strip())
                    elif(parameter[key]["type"]=="bool"):
                        parameter[key]["value"] = self.str2bool(splitted[1])
    
    def setModelContext(self, modelContext):
        return
    
    def writeSolverInput(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t"+key+" = "+self.float2str(self.parameter[key]["value"])+"\n")
            if(self.parameter[key]["type"] == "vector"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")
        text.append("End"+self.__type+"\n%\n")

        file.writelines(text)


    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    def str2bool(self,inString):
        return bool(int(inString))
    def bool2str(self,inBool):
        if inBool:
            return "yes"
        else:
            return "no"
    
    def show(self, renderer):
        for actor in self.actors:
            renderer.AddActor(actor)
    def hide(self, renderer):
        for actor in self.actors:
            renderer.RemoveActor(actor)