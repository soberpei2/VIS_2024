import mbsObjects.rigidBody as rigidBody
import mbsObjects.constraint as constraint
import mbsObjects.motion as motion
import mbsObjects.force as force
import mbsObjects.dataobjectParameter as dataobjectParameter
import mbsObjects.measure as measure
import mbsObjects.solver as solver
import mbsObjects.settings as settings
import inputfilereader
import json
import os

class model:
    def __init__(self,databaseFilepath):
        self.__objectList = []
        self.__databaseFilepath = databaseFilepath
        
    def importFddFile(self,filepath):
        file_name, file_extension = os.path.splitext(filepath)

        if(file_extension == ".fdd"):
            self.__objectList = inputfilereader.importFddFile(filepath)
        else:
            print("Wrong file type: " + file_extension)
            return False
        return True
        
    def loadDatabase(self,database2Load):
        f = open(database2Load)
        data = json.load(f)
        f.close()
        for modelObject in data["modelObjects"]:
            if(modelObject["type"] == "body" and modelObject["subtype"] == "rigidBody"):
                self.__objectList.append(rigidBody.rigidBody(modelObject["parameter"]))
            elif(modelObject["type"] == "constraint"):
                self.__objectList.append(constraint.constraint(modelObject["parameter"]))
            elif(modelObject["type"] == "motion"):
                self.__objectList.append(motion.motion(modelObject["parameter"]))
            elif(modelObject["type"] == "force"):
                if(modelObject["subtype"] == "genericForce"):
                    self.__objectList.append(force.genForce(modelObject["parameter"]))
                elif(modelObject["subtype"] == "tireForce"):
                    self.__objectList.append(force.tireForce(modelObject["parameter"]))
                elif(modelObject["subtype"] == "genericTorque"):
                    self.__objectList.append(force.genTorque(modelObject["parameter"]))
            elif(modelObject["type"] == "dataobjectParameter"):
                self.__objectList.append(dataobjectParameter.dataobjectParameter(modelObject["parameter"]))
            elif(modelObject["type"] == "measure"):
                self.__objectList.append(measure.measure(modelObject["parameter"]))
            #elif(modelObject["type"] == "solver"):
            #    self.__objectList.append(solver.solver(modelObject["parameter"]))
            #elif(modelObject["type"] == "settings"):
            #    self.__objectList.append(settings.settings(modelObject["parameter"]))

    def saveDatabase(self):
        # Serializing json
        modelObjects = []
        for object in self.__objectList:
            modelObjects.append(object.getDictionary())
        
        jDataBase = json.dumps({"modelObjects": modelObjects})

        # Writing to sample.json
        with open(self.__databaseFilepath, "w") as outfile:
            outfile.write(jDataBase)

    def getObjectList(self):
        return self.__objectList
    
    def showModel(self, renderer):
        for object in self.__objectList:
                object.show(renderer)