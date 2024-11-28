from body import rigidBody
import inputfilereader
import json
import os

import inputfilereader

class mbsModel:
    def __init__(self):
        self.__mbsObjectList = []
        self.__databaseFilepath = ""
    
    def importFddFile(self,filepath):
        file_name, file_extension = os.path.splitext(filepath)

        if(file_extension == ".fdd"):
            self.__mbsObjectList = inputfilereader.readInput(filepath)
        else:
            print("Wrong file type: " + file_extension)
            return False
        
        for object in self.__mbsObjectList:
            object.setModelContext(self)

        return True
        
    def exportFdsFile(self,filepath):
        f = open(filepath,"w")
        for object in self.__mbsObjectList:
            object.writeSolverInput(f)
        f.close()
        
    def loadDatabase(self,database2Load):
        f = open(database2Load)
        data = json.load(f)
        f.close()
        for modelObject in data["modelObjects"]:
            if(modelObject["type"] == "Body" and modelObject["subtype"] == "rigidBody"):
                self.__objectList.append(rigidBody(modelObject["parameter"]))
        
        return True

    def saveDatabase(self):
        # Serializing json
        modelObjects = []
        for object in self.__mbsObjectList:
            modelObjects.append(object.getDictionary())
        
        jDataBase = json.dumps({"modelObjects": modelObjects})

        # Writing to sample.json
        with open(self.__databaseFilepath, "w") as outfile:
            outfile.write(jDataBase)
    
    def showModel(self, renderer):
        for object in self.__mbsObjectList:
            object.show(renderer) #show method adds individual actor (depending on object-type) to renderer