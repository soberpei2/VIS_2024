import vtk
#import rigidBody
#import constraint
#import force
#import measure

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actor = vtk.vtkActor()

        
        for line in text:
            splitted = line.split(":",1)
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if (parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif (parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif (parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif (parameter[key]["type"] == "vectorInt"):
                        parameter[key]["value"] = self.str2vectorInt(splitted[1])
                    elif (parameter[key]["type"] == "str"):
                        parameter[key]["value"] = self.str2str(splitted[1].strip())
                    elif (parameter[key]["type"] == "path"):
                        parameter[key]["value"] = self.str2path(splitted[1].strip())    
                    elif (parameter[key]["type"] == "bool"):
                        parameter[key]["value"] = self.str2bool(splitted[1])

    def writeInputFile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "int"):
                text.append("\t" + key + " = " + self.int2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "vectorInt"):
                text.append("\t" + key + " = " + self.vectorInt2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "str"):
                text.append("\t" + key + " = " + self.str2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "path"):
                text.append("\t" + key + " = " + self.path2str(self.parameter[key]["value"]) + "\n")
            elif(self.parameter[key]["type"] == "bool"):
                text.append("\t" + key + " = " + self.bool2str(self.parameter[key]["value"]) + "\n")
        text.append("End" + self.__type + "\n%\n")
        file.writelines(text)

    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)

    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    def str2int(self,inString):
        return int(inString)
    def int2str(self,inInt):
        return str(inInt)
    
    def str2vectorInt(self,inString):
        return [int(inString.split()[0]),int(inString.split()[1]),int(inString.split()[2])]
    def vectorInt2str(self,inVectorInt):
        return str(inVectorInt[0]) + " " + str(inVectorInt[1]) + " " + str(inVectorInt[2])

    def str2str(self,inString):
        return str(inString)
    
    def str2path(self,inString):
        #path = inString.rsplit("\\",1)
        #realPath = path[0]
        #fileName = path[1].rsplit(".",1)[0]
        #fileType = "." + path[1].rsplit(".",1)[1]
        return str(inString)
    
    def path2str(self,inString):
        return str(inString)
    
    def str2bool(self,inString):
        return bool(inString)
    def bool2str(self,inBool):
        return str(inBool)
    
    def getActor(self):
        return self.actor
    

