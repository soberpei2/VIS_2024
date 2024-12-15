import json
import os

import inputFileReader as iFR

import body
import constraint
import force
import measure
import dataobject

class mbsModel:
    def __init__(self):
        self.__listOfMbsObject = []
        self._filePath = None

    
    def showModel(self,renderer):
        for obj in self.__listOfMbsObject:
            obj.show(renderer)

    def hideModel(self,renderer):
        for obj in self.__listOfMbsObject:
            obj.hide(renderer)

    def getListOfMbsModel(self):
        return self.__listOfMbsObject
    
    def importFddFile(self,filePathFdd):
        self._filePath = os.path.normpath(filePathFdd)
        [fileName, fileExtension] = os.path.splitext(filePathFdd)

        if(fileExtension == ".fdd"):
            keySign = "$"
            search4Typ = ["RIGID_BODY","CONSTRAINT","FORCE_GenericForce","FORCE_GenericTorque","DATAOBJECT_PARAMETER","MEASURE","SETTINGS"]
            fileContent = iFR.readFile(filePathFdd)
            fileContent.append("$")
            self.__listOfMbsObject = iFR.parseText2blocksOfMbsObjects(fileContent,keySign,search4Typ)
        else:
            print("Wrong file type: " + fileExtension)
            return False
        
        for obj in self.__listOfMbsObject:
            obj.setModelContext(self)

        return True

    def exportFdsFile(self, filePath):
        fds = open(filePath,"w")
        for obj in self.__listOfMbsObject:
            obj.writeSolverFile(fds)
        fds.close()

    def loadJsonFile (self, filePathJson):
        self._filePath = os.path.normpath(filePathJson)
        [fileName, fileExtension] = os.path.splitext(filePathJson)

        file2read = open(filePathJson,"r")
        file2readContent = json.load(file2read)
        file2read.close()
        
        if(fileExtension == ".json"):
            for modelObject in file2readContent["modelObjects"]:
                if(modelObject["type"] == "Body" and modelObject["subtype"] == "Rigid_EulerParameter_PAI"):
                    self.__listOfMbsObject.append(body.rigidBody(parameter=modelObject["parameter"]))
                elif(modelObject["type"] == "Constraint" and modelObject["subtype"] == "Generic"):
                    self.__listOfMbsObject.append(constraint.genericConstraint(parameter=modelObject["parameter"]))
                elif(modelObject["type"] == "Force"):
                    if(modelObject["subtype"] == "GenericForce"):
                        self.__listOfMbsObject.append(force.genericForce(parameter=modelObject["parameter"]))
                    elif(modelObject["subtype"] == "GenericTorque"):
                        self.__listOfMbsObject.append(force.genericTorque(parameter=modelObject["parameter"]))
                    elif(modelObject["subtype"] == "Gravity"):
                        self.__listOfMbsObject.append(force.gravity(parameter=modelObject["parameter"]))
                elif(modelObject["type"] == "Measure"):
                    self.__listOfMbsObject.append(measure.measure(parameter=modelObject["parameter"]))
                elif(modelObject["type"] == "DataObject" and modelObject["subtype"] == "Parameter"):
                    self.__listOfMbsObject.append(dataobject.parameter(parameter=modelObject["parameter"]))
            return True

        else:
            print("Wrong file type: " + fileExtension)
            return False

    def saveJsonFile (self, filePath):
        modelObjects = []
        for obj in self.__listOfMbsObject:
            modelObject = {"type": obj.getType(),
                            "subtype": obj.getSubtype(),
                            "parameter": obj.parameter
            }
            modelObjects.append(modelObject)

        jsonDataBase = json.dumps({"modelObjects": modelObjects})

        with open(filePath,"w") as outfile:
            outfile.write(jsonDataBase)

    
        

