import os
import sys


class mbsObject:
    def __init__(self,type,subtype,**kwargs):
        self.__type = type
        self.__subtype = subtype
        self._symbolScale = 10.
        self.actors = []
        if "parameter" in kwargs:
            self.parameter = kwargs["parameter"]
        else:
            sys.exit("parameter not provided, cannot create mbsObject!")
        
        if "text" in kwargs:
            for line in kwargs["text"]:
                splitted = line.split(":",1)
                for key in self.parameter.keys():
                    keyString = splitted[0].strip()
                    valueString = line[len(key)+1:].strip()
                    if(keyString == key):
                        if (self.parameter[key]["type"] == "float"):
                            self.parameter[key]["value"] = self.str2float(valueString)
                        elif (self.parameter[key]["type"] == "vector"):
                            self.parameter[key]["value"] = self.str2vector(valueString)
                        elif (self.parameter[key]["type"] == "int"):
                            self.parameter[key]["value"] = self.str2int(valueString)
                        elif (self.parameter[key]["type"] == "vectorInt"):
                            self.parameter[key]["value"] = self.str2vectorInt(valueString)
                        elif (self.parameter[key]["type"] == "str"):
                            self.parameter[key]["value"] = valueString
                        elif (self.parameter[key]["type"] == "path"):
                            self.parameter[key]["value"] = os.path.normpath(valueString)    
                        elif (self.parameter[key]["type"] == "bool"):
                            self.parameter[key]["value"] = self.str2bool(valueString)

    
    def getType(self):
        return self.__type
    
    def getSubtype(self):
        return self.__subtype

    def show(self,renderer):
        for actor in self.actors:
            renderer.AddActor(actor)
    
    def hide(self,renderer):
        for actor in self.actors:
            renderer.RemoveActor(actor)

    def setModelContext(self, modelContext):
        return





    def writeSolverFile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            value = self.parameter[key]["value"]
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(value) + "\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(value) + "\n")
            elif(self.parameter[key]["type"] == "int"):
                text.append("\t" + key + " = " + self.int2str(value) + "\n")
            elif(self.parameter[key]["type"] == "vectorInt"):
                text.append("\t" + key + " = " + self.vectorInt2str(value) + "\n")
            elif(self.parameter[key]["type"] == "str"):
                text.append("\t" + key + " = " + value + "\n")
            elif(self.parameter[key]["type"] == "path"):
                text.append("\t" + key + " = " + os.path.normpath(value) + "\n")
            elif(self.parameter[key]["type"] == "bool"):
                text.append("\t" + key + " = " + self.bool2str(value) + "\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)

    @staticmethod
    def str2float(inString):
        return float(inString)
    @staticmethod
    def float2str(inFloat):
        return str(inFloat)

    @staticmethod
    def str2vector(inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    @staticmethod
    def vector2str(inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    
    @staticmethod
    def str2int(inString):
        return int(inString)
    @staticmethod
    def int2str(inInt):
        return str(inInt)
    
    @staticmethod
    def str2vectorInt(inString):
        return [int(inString.split()[0]),int(inString.split()[1]),int(inString.split()[2])]
    @staticmethod
    def vectorInt2str(inVectorInt):
        return str(inVectorInt[0]) + " " + str(inVectorInt[1]) + " " + str(inVectorInt[2])
    
    @staticmethod
    def str2bool(inString):
        return bool(int(inString))
    @staticmethod
    def bool2str(inBool):
        if inBool:
            return "yes"
        else:
            return "no"
    
    
    

