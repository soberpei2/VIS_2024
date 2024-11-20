
import mbsObject
import json

def readInput4Output(inputfilepath, jsonfilepath, fdsfilepath):
    # Dateiinhalt lesen
    with open(inputfilepath, "r") as f:
        fileContent = f.read().splitlines()


    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    # Wörter nach denen in der Liste "search4Objects" gesucht wird

    search4Objects = ["RIGID_BODY", "CONSTRAINT"]
    for line in fileContent:
        
        if(line.find("$") >= 0): #new block found 
            if(currentBlockType != ""):
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                currentBlockType = ""

        for type_i in search4Objects: #sucht nach Objekten und speichert diese
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)

    # schreibt alles um auf ein json file 
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)
    jDataBase = json.dumps({"modelObjects": modelObjects})

    with open(jsonfilepath, "w") as outfile:
        outfile.write(jDataBase)

    with open(jsonfilepath, "r") as jf:
        data = json.load(jf)

 # FDS-Datei schreiben
    with open(fdsfilepath, "w") as fds:
        for mbsObject_i in listOfMbsObjects:
            mbsObject_i.writeInputfile(fds)
        
    return listOfMbsObjects
