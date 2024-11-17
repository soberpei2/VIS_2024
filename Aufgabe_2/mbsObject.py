import vtk

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter

        for line in text:
            splitted = line.split(":",1)
            for key in parameter.keys():
                if(splitted[0].strip() == key):
                    if (parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif (parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif (parameter[key]["type"] == "integer"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif (parameter[key]["type"] == "vectorInteger"):
                        parameter[key]["value"] = self.str2vectorInt(splitted[1])
                    elif (parameter[key]["type"] == "str"):
                        parameter[key]["value"] = self.str2str(splitted[1].strip())
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
    
    def str2bool(self,inString):
        return bool(inString)
    def bool2str(self,inBool):
        return str(inBool)

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "geometry": {"type": "str", "value": "testPathGeometry"},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]},
            "color": {"type": "vectorInt", "value": [0,0,0]},
            "transparency": {"type": "int", "value": 0},
            "initial velocity": {"type": "vector", "value": [0.,0.,0.]},
            "initial omega": {"type": "vector", "value": [0.,0.,0.]},
            "consider vel inertia forces": {"type": "bool", "value": 0},
            "mass": {"type": "float", "value": 0.},
            "COG": {"type": "vector", "value": [0.,0.,0.]},
            "inertia": {"type": "vector", "value": [0.,0.,0.]},
            "i1_axis": {"type": "vector", "value": [0.,0.,0.]},
            "i2_axis": {"type": "vector", "value": [0.,0.,0.]},
            "i3_axis": {"type": "vector", "value": [0.,0.,0.]}
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParamter_PAI",text,parameter)
    

class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "dx": {"type": "int", "value": 0},
            "dy": {"type": "int", "value": 0},
            "dz": {"type": "int", "value": 0},
            "ax": {"type": "int", "value": 0},
            "ay": {"type": "int", "value": 0},
            "az": {"type": "int", "value": 0},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]}
        }

        mbsObject.__init__(self,"Constraint","Generic",text,parameter)

class force(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "PointOfApplication_Body1": {"type": "vector", "value": [0.,0.,0.]},
            "PointOfApplication_Body2": {"type": "vector", "value": [0.,0.,0.]},
            "mode": {"type": "str", "value": "testMode"},
            "direction": {"type": "vector", "value": [0.,0.,0.]},
            "ForceExpression": {"type": "str", "value": "testForceExpression"}

        }

        mbsObject.__init__(self,"Force","Generic",text,parameter)


def mbsObjectFactory(object,textblock):
    mbsObjectList = {
        "RIGID_BODY": rigidBody,
        "CONSTRAINT": constraint,
        "FORCE_GenericForce": force,
    }

    return mbsObjectList[object](textblock)