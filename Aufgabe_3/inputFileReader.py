import json

import body
import constraint
import force
import measure
import dataobject



def readFile(filePath):
    file2read = open(filePath,"r")
    file2readContent = file2read.read().splitlines()
    file2read.close()
    return file2readContent

def parseText2blocksOfMbsObjects(fileContent,keySign,search4Typ):
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in fileContent:
        if(line.find(keySign) >= 0):
            if(currentBlockType != ""):   
                for obj in search4Typ:             
                    if(currentBlockType == obj):
                        listOfMbsObjects.append(mbsObjectFactory(obj,currentTextBlock))
                currentBlockType = ""
        
        for type_i in search4Typ:
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)
    return listOfMbsObjects

def mbsObjectFactory(object,currentTextblock):
    mbsObjectList = {
        "RIGID_BODY": body.rigidBody,
        "CONSTRAINT": constraint.genericConstraint,
        "FORCE_GenericForce": force.genericForce,
        "FORCE_GenericTorque": force.genericTorque,
        "MEASURE": measure.measure,
        "DATAOBJECT_PARAMETER": dataobject.parameter,
        "SETTINGS": force.gravity,
    }

    return mbsObjectList[object](text=currentTextblock)