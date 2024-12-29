
import body
import constraint
import force
import measure
import dataobject
import json

def readInput(path2File):
    f = open(path2File,"r")

    fileContent = f.read().splitlines()
    f.close()

    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    search4Objects  = ["RIGID_BODY", "CONSTRAINT","FORCE_GenericForce","FORCE_GenericTorque","MEASURE","DATAOBJECT_PARAMETER"]
    for line in fileContent:
        if(line.find("$") >= 0):#new block found
            if(currentBlockType != ""):
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(body.rigidBody(text=currentTextBlock))
                elif(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(constraint.genericConstraint(text=currentTextBlock))
                elif(currentBlockType == "FORCE_GenericForce"):
                    listOfMbsObjects.append(force.genericForce(text=currentTextBlock))
                elif(currentBlockType == "FORCE_GenericTorque"):
                    listOfMbsObjects.append(force.genericTorque(text=currentTextBlock))
                elif(currentBlockType == "MEASURE"):
                    listOfMbsObjects.append(measure.measure(text=currentTextBlock))
                elif(currentBlockType == "DATAOBJECT_PARAMETER"):
                    listOfMbsObjects.append(dataobject.parameter(text=currentTextBlock))
                currentBlockType = ""

        for type_i in search4Objects:
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break
        
        currentTextBlock.append(line)
    
    exportToJson(listOfMbsObjects, "test1.json")
    return listOfMbsObjects

def exportToJson(listOfMbsObjects, outputPath):
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)  # Hier muss 'parameter' durch das tatsächliche Attribut ersetzt werden.
    with open(outputPath, "w") as outfile:
        json.dump({"modelObjects": modelObjects}, outfile, indent=4)

readInput("E:\9.Semester\Digitalisierung-Visualisierung-Uebung\VIS_2024\Aufgabe_3\\test.fdd")