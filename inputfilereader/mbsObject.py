
class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        

        for line in text:
            if ":" in line:
            # Nur beim ersten ':' splitten
                splitted = line.split(":", 1)
                key = splitted[0].strip()
                value = splitted[1].strip()
            for key in parameter.keys():
                if(splitted[0].strip() == key):            # strip: Leerzeichen entfernen
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = (splitted[1].strip())
                    elif(parameter[key]["type"] == "vectorInt"):
                        parameter[key]["value"] = self.str2vectorInt(splitted[1])
                    elif (parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif (parameter[key]["type"] == "bool"):
                        parameter[key]["value"] = self.str2bool(splitted[1])
                    

    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if (self.parameter[key]["type"] == "float"):
                text.append("\t" + key+" = "+ self.float2str(self.parameter[key]["value"])+"\n")
            elif (self.parameter[key]["type"] == "vector"):
                text.append("\t" + key+" = "+ self.vector2str(self.parameter[key]["value"])+"\n")
            elif (self.parameter[key]["type"] == "string"):
                text.append("\t" + key + " = " + self.parameter[key]["value"] + "\n")
            elif (self.parameter[key]["type"] == "vectorInt"):
                text.append("\t" + key + " = " + self.vectorInt2str(self.parameter[key]["value"]) + "\n")
            elif (self.parameter[key]["type"] == "int"):
                text.append("\t" + key + " = " + self.int2str(self.parameter[key]["value"]) + "\n")
            elif (self.parameter[key]["type"] == "bool"):
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
        return str(inVector[0])+","+str(inVector[1])+ "," +str(inVector[2])
    
    def str2vectorInt(self, inString):
        return [int(inString.split()[0]),int(inString.split()[1]),int(inString.split()[2])]
    def vectorInt2str(self, inVector):
        return str(inVector[0]) + " " + str(inVector[1]) + " " + str(inVector[2])
    
    def str2int(self,inString):
        return int(inString)
    def int2str(self,inInt):
        return str(inInt)
    
    def str2bool(self,inString):
        return bool(inString)           #bool gibt True oder False aus, mit int kommt 0 oder 1
    def bool2str(self,inbool):
        return str(inbool)

#====================================================================================================================

class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":         {"type": "string", "value": "NAME_UNKOWN"},
            "geometry":     {"type": "string", "value": "UNKOWN"},
            "position":     {"type": "vector", "value": [1.,1.,1.]},
            "x_axis":       {"type": "vector", "value": [1.,1.,1.]},
            "y_axis":       {"type": "vector", "value": [1.,1.,1.]},
            "z_axis":       {"type": "vector", "value": [1.,1.,1.]},
            "color":        {"type": "vectorInt", "value": [0, 0, 0]},
            "transparency": {"type": "int", "value": 0},
            "mass":         {"type": "float", "value": 1.},
            "COG":          {"type": "vector", "value": [0.,0.,0.]},            
        }

        mbsObject.__init__(self,"rigidBody","Rigid_EulerParameter_PAI",text,parameter)

#====================================================================================================================

class constraint(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":         {"type": "string", "value": "NAME_UNKOWN"},
            "body1":        {"type": "string", "value": "NAME_UNKOWN"},
            "body2":        {"type": "string", "value": "NAME_UNKOWN"},
            "dx":           {"type": "bool", "value": 0},
            "dy":           {"type": "bool", "value": 0},
            "dz":           {"type": "bool", "value": 0},
            "ax":           {"type": "bool", "value": 0},
            "ay":           {"type": "bool", "value": 0},
            "az":           {"type": "bool", "value": 0},
            "position":     {"type": "vector", "value": [1.,1.,1.]},
            "x_axis":       {"type": "vector", "value": [1.,1.,1.]},
            "y_axis":       {"type": "vector", "value": [1.,1.,1.]},
            "z_axis":       {"type": "vector", "value": [1.,1.,1.]},
        }

        mbsObject.__init__(self,"constraint","Rigid_EulerParameter_PAI",text,parameter)

#============================================================================================================

class force_GenericForce(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":                         {"type": "string", "value": "NAME_UNKOWN"},
            "body1":                        {"type": "string", "value": "NAME_UNKOWN"},
            "body2":                        {"type": "string", "value": "NAME_UNKOWN"},
            "PointOfApplication_Body1":     {"type": "vector", "value": [1.,1.,1.]},
            "PointOfApplication_Body2":     {"type": "vector", "value": [1.,1.,1.]},
            "mode":                         {"type": "string", "value": "UNKOWN"},
            "direction":                    {"type": "vector", "value": [1.,1.,1.]},
            "ForceExpression":              {"type": "string", "value": "UNKOWN"},
        }

        mbsObject.__init__(self,"force_GenericForce","GenericForce",text,parameter)

#================================================================================================================

class force_GenericTorque(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":                         {"type": "string", "value": "NAME_UNKOWN"},
            "body1":                        {"type": "string", "value": "NAME_UNKOWN"},
            "body2":                        {"type": "string", "value": "NAME_UNKOWN"},
            "mode":                         {"type": "string", "value": "UNKOWN"},
            "direction":                    {"type": "vector", "value": [1.,1.,1.]},
            "TorqueExpression":              {"type": "string", "value": "UNKOWN"},
        }

        mbsObject.__init__(self,"force_GenericTorque","GenericTorque",text,parameter)

#===================================================================================================================

class measure1(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":                         {"type": "string", "value": "NAME_UNKOWN"},
            "body1":                        {"type": "string", "value": "NAME_UNKOWN"},
            "body2":                        {"type": "string", "value": "NAME_UNKOWN"},
            "type":                         {"type": "string", "value": "UNKOWN"},
            "location_body1":               {"type": "vector", "value": [1.,1.,1.]},
            "location_body2":               {"type": "vector", "value": [1.,1.,1.]},
            "use_initial_value":            {"type": "int", "value": 0},
        }

        mbsObject.__init__(self,"measure","Rigid_EulerParameter_PAI",text,parameter)

#====================================================================================================================

class measure2(mbsObject):
    def __init__(self,text):
        parameter = {
            "name":                         {"type": "string", "value": "NAME_UNKOWN"},
            "body1":                        {"type": "string", "value": "NAME_UNKOWN"},
            "body2":                        {"type": "string", "value": "NAME_UNKOWN"},
            "type":                         {"type": "string", "value": "UNKOWN"},
            "vector_body1":                {"type": "vector", "value": [1.,1.,1.]},
            "vector1_body2":                {"type": "vector", "value": [1.,1.,1.]},
            "vector2_body2":                {"type": "vector", "value": [1.,1.,1.]},
            "use_initial_value":            {"type": "int", "value": 0},
        }

        mbsObject.__init__(self,"measure","Rigid_EulerParameter_PAI",text,parameter)

class gravity(mbsObject):
    def __init__(self,text):
        parameter = {
            "gravity_vector":               {"type": "vector", "value": [1.,1.,1.]}
        }

        mbsObject.__init__(self,"force","gravity",text,parameter)