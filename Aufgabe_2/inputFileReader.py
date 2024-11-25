import json
from rigidBody import rigidBody
from constraint import constraint
from force import force
from force import torque
from force import gravity
from measure import measure


def parseText2blocksOfMbsObjects(fileContent,keySign,search4Objects):
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in fileContent:
        if(line.find(keySign) >= 0):
            if(currentBlockType != ""):   
                for obj in search4Objects:             
                    if(currentBlockType == obj):
                        listOfMbsObjects.append(mbsObjectFactory(obj,currentTextBlock))
                currentBlockType = ""
        
        for type_i in search4Objects:
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)
    return listOfMbsObjects

def readFile(filePath,nameWithExtension):
    file2read = open(filePath + "/" + nameWithExtension,"r")
    file2readContent = file2read.read().splitlines()
    file2read.close()
    return file2readContent

def readJsonFile (filePath,nameWithExtension):
    file2read = open(filePath + "/" + nameWithExtension,"r")
    file2readContent = json.load(file2read)
    file2read.close()
    return file2readContent

def writeJsonFile (listOfMbsObjects,filePath,nameWithExtension):
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)

    jsonDataBase = json.dumps({"modelObjects": modelObjects})
    with open(filePath + "/" + nameWithExtension,"w") as outfile:
        outfile.write(jsonDataBase)

def writeFdsFile(listOfMbsObjects,filePath,nameWithExtension):
    fds = open(filePath + "/" + nameWithExtension,"w")
    for mbsObject_i in listOfMbsObjects:
        mbsObject_i.write2File(fds)
    fds.close()

def mbsObjectFactory(object,textblock):
    mbsObjectList = {
        "RIGID_BODY": rigidBody,
        "CONSTRAINT": constraint,
        "FORCE_GenericForce": force,
        "FORCE_GenericTorque": torque,
        "MEASURE": measure,
        "SETTINGS": gravity,
    }

    return mbsObjectList[object](textblock)