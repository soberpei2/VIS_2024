import os
import mbsObject as mbsObj
import mbsObjects.rigidBody as rigidBody
import mbsObjects.constraint as constraint
import mbsObjects.motion as motion
import mbsObjects.force as force
import mbsObjects.dataobjectParameter as dataobjectParameter
import mbsObjects.measure as measure
import mbsObjects.solver as solver
import mbsObjects.settings as settings


def importFddFile(filepath):
    f = open(filepath, "r")
    fileContent = f.read().splitlines()

    #get count of textlines in file
    numLines = len(fileContent)

    currentBlockType = ""
    currentBlockSubType = ""
    currentTextBlock = []
    objectList = []


    search4Objects = ["$RIGID_BODY","$CONSTRAINT","$MOTION","$FORCE","$MEASURE"]
    search4Subtypes = ["GenericForce","TireForce","GenericTorque","revolute","spherical","fix","hooke"]

    #for loop over all lines in file
    for line in fileContent:
        #check if currentBlockType is empty
        if(currentBlockType == ""):
            for type_i in search4Objects:
                #search element of search4Objects in line
                if(line.find(type_i,0,len(type_i)) >= 0):
                    currentBlockType = type_i
                    for subtype_i in search4Subtypes:
                        if(line.find(subtype_i,len(type_i)+1,len(type_i)+1+len(subtype_i)) >= 0):
                            currentBlockSubType = subtype_i
                    currentTextBlock.clear()
                    break
                
        if(currentBlockType == "$CONSTRAINT"):
            for subtype_i in search4Subtypes:
                if(line.find(subtype_i,len("name: "),len("name: ")+len(subtype_i)) >= 0):
                    currentBlockSubType = subtype_i

        #check if empty line was reached
        #call constructor to generate mbsObject with text block
        if(line == ""):
            if(currentBlockType == "$RIGID_BODY"):
                objectList.append(rigidBody.rigidBody(currentTextBlock))
            elif(currentBlockType == "$CONSTRAINT"):
                objectList.append(constraint.constraint(currentTextBlock))
            elif(currentBlockType == "$MOTION"):
                objectList.append(motion.motion(currentTextBlock))
            elif(currentBlockType == "$FORCE"):
                if(currentBlockSubType == "GenericForce"):
                    objectList.append(force.genForce(currentTextBlock))
                if(currentBlockSubType == "TireForce"):
                    objectList.append(force.tireForce(currentTextBlock))
                if(currentBlockSubType == "GenericTorque"):
                    objectList.append(force.genTorque(currentTextBlock))
            elif(currentBlockType == "$DATAOBJECT_PARAMETER"):
                objectList.append(dataobjectParameter.dataobjectParameter(currentTextBlock))
            elif(currentBlockType == "$MEASURE"):
                objectList.append(measure.measure(currentTextBlock))
            elif(currentBlockType == "$SOLVER"):
                objectList.append(solver.solver(currentTextBlock))
            elif(currentBlockType == "$SETTINGS"):
                objectList.append(settings.settings(currentTextBlock))
            currentBlockType = ""
        else:
            currentTextBlock.append(line)
    return objectList