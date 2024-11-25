

import mbsObject
import json

#Funktion für Inputfilereader
def inputfilereader(FilePath):
    f = open(FilePath,"r")

    fileContent = f.read().splitlines() # einlesen der Zeilen in eine Liste
    f.close()

    #initialisieren der Variablen
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    search4Objects  = ["RIGID_BODY", "CONSTRAINT", "FORCE_GenericForce", "FORCE_GenericTorque"]
    
    for line in fileContent:
        if(line.find("$") >= 0):#new block found bei $
            if(currentBlockType != ""): # # Verarbeiten des Blocks, wenn Typ existiert

                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                
                if(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                
                elif currentBlockType == "FORCE_GenericForce":
                    listOfMbsObjects.append(mbsObject.genericForce(currentTextBlock))

                elif currentBlockType == "FORCE_GenericTorque":
                    listOfMbsObjects.append(mbsObject.genericTorque(currentTextBlock))

                currentBlockType = "" #reset des Blocktyps
          
                
#Blocktyp erkennen
        for type_i in search4Objects:
            if(line.find(type_i,1,len(type_i)+1) >= 0): # nach Schlagwort suchen
                currentBlockType = type_i
                currentTextBlock.clear() # bereinigen
                break
        
        currentTextBlock.append(line) # neue Zeile hinzufügen

    print(len(listOfMbsObjects))


    #import/export functionality (for later use in model.py)
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)
    

    jDataBase = json.dumps({"modelObjects": modelObjects})

    with open("Aufgabe 2/test.json", "w") as outfile:
        outfile.write(jDataBase)

    f = open("Aufgabe 2/test.json","r")
    data = json.load(f)
    f.close()

    fds = open("Aufgabe 2/test.fds","w")
    for mbsObject_i in listOfMbsObjects:
        mbsObject_i.writeInputfile(fds)
    fds.close()

    
    return listOfMbsObjects
#-------------------------------------------------------