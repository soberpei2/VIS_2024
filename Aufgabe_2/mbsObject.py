import uuid
from vtkmodules.vtkRenderingCore import vtkActor

class mbsObject:
    def __init__(self,type,subtype,input,parameter):
        self.__id = uuid.uuid4()
        self.__type = type
        self.__subtype = subtype
        self.actor = vtkActor()
        
        if(isinstance(input,dict)):
            self.parameter = input
        else:
            self.parameter = parameter

            for line in input:
                splitted = line.split(":")
                value = splitted[1]
                for block in splitted[2:]:
                    value = value + ":" + block

                for key in parameter.keys():
                    if(splitted[0].strip() == key):
                        if(parameter[key]["type"]=="float"):
                            parameter[key]["value"] = self.str2float(value)
                        if(parameter[key]["type"]=="vector"):
                            parameter[key]["value"] = self.str2floatVector(value)
                        if(parameter[key]["type"]=="rotMat"):
                            parameter[key]["value"] = self.str2floatMatrix3x3(value)
                        if(parameter[key]["type"]=="string"):
                            parameter[key]["value"] = value
                        if(parameter[key]["type"]=="color"):
                            parameter[key]["value"] = self.str2color(value)
                        if(parameter[key]["type"]=="boolean"):
                            parameter[key]["value"] = self.str2boolean(value)
                        if(parameter[key]["type"]=="vec2D"):
                            parameter[key]["value"] = self.str2vec2D(value)
                        if(parameter[key]["type"]=="geometry"):
                            parameter[key]["value"] = self.str2geometry(value)
    
    def getId(self):
        return self.__id

    def getType(self):
        return self.__type
    
    def getSubType(self):
        return self.__subtype

    def getDictionary(self):
        return {"type": self.__type, \
                "subtype": self.__subtype, \
                "parameter": self.parameter}

    def str2float(self,inString):
        return float(inString)

    def float2str(self,floatVal):
        return str(floatVal)

    def str2floatVector(self,inString):
        splitted = inString.split(",")
        return [float(splitted[0]),float(splitted[1]),float(splitted[2])]

    def floatVector2str(self,floatVec):
        return str(floatVec[0]) + "," + str(floatVec[1]) + "," + str(floatVec[2])

    def str2floatMatrix3x3(self,inString):
        retMat = [[1,0,0],[0,1,0],[0,0,1]]
        splitted = inString.split(",")
        for i in range(0,3):
            for j in range(0,3):
                retMat[j][i] = float(splitted[i+3*j])
        return retMat

    def floatMatrix3x3_2str(self,floatMatrix3x3):
        return  str(floatMatrix3x3[0][0]) + "," + str(floatMatrix3x3[0][1]) + "," + str(floatMatrix3x3[0][2]) + "," + \
                str(floatMatrix3x3[1][0]) + "," + str(floatMatrix3x3[1][1]) + "," + str(floatMatrix3x3[1][2]) + "," + \
                str(floatMatrix3x3[2][0]) + "," + str(floatMatrix3x3[2][1]) + "," + str(floatMatrix3x3[2][2])
    
    def str2color(self,inString):
        splitted = inString.split(" ")
        while("" in splitted):
            splitted.remove("")
        return [int(splitted[0]),int(splitted[1]),int(splitted[2]),int(splitted[3])]
    
    def color2str(self,color):
        return color[0] + " " + color[1] + " " + color[2] + "   " + color[3]
    
    def str2boolean(self,inString):
        if(inString.strip()=="1"):
            return True
        else:
            return False
        
    def boolean2str(self,boolVal):
        if(boolVal==True):
            return "1"
        else:
            return "0"

    def str2vec2D(self,inString):
        splitted = inString.split(",")
        while("" in splitted):
            splitted.remove("")
        return [int(splitted[0]),int(splitted[1])]
    
    def vec2D2str(self,vec2D):
        return str(vec2D[0]) + "," + str(vec2D[1])
    
    def str2geometry(self,inString):
        splitted = inString.split(" ")
        while("" in splitted):
            splitted.remove("")
        if len(splitted)==1:
            splitted = inString.split("\\")
            return [splitted[-1]]
        elif len(splitted)==2:
            return [splitted[0], float(splitted[1])]
        elif len(splitted)==3:
            return [splitted[0], float(splitted[1]), float(splitted[2])]
        else:
            return ""
        
    def show(self, renderer):
        renderer.AddActor(self.actor)