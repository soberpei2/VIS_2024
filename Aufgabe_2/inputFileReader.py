# Importieren benötigter Biblitheken
#===================================
import mbsObject
import json

# Funktion zum Einlesen von .fdd-Files
#=====================================
def inputFileReader(file):
    # Open FreeDyne-file
    f = open(file, "r")

    # Read opened file (save to variable) -> each line is saved as a string
    fileContent = f.read().splitlines()

    # Hinzufügen eines $-Zeichens am Ende der Liste, damit der letzte Block
    # abgeschlossen werden kann und mitaufgenommen wird
    fileContent.append("$")

    # Close file after saving its content
    f.close()

    # List of Mbs Objects
    listOfMbsObjects = []

    # Definition of a current textblock
    currentBlockType = ""
    currentTextBlock = []

    # Define list of objects, which should be searched
    search4Objects = ["RIGID_BODY", "CONSTRAINT", "SETTINGS"]

    #############################
    # Read lines of fileContent #
    #############################
    for line in fileContent:
        # Search for $-symbol (each Freedyn object starts with a $) -> new block found when >= 0
        #=======================================================================================
        if(line.find("$") >= 0):
            # Testing, if current Block has a type -> counting number certain objects
            #------------------------------------------------------------------------
            if(currentBlockType != ""):
                # Wenn Rigid Body -> Objekt vom Typ rigidBody anlegen
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))

                # Wenn Constraint -> Objekt vom Typ constraint anlegen
                elif(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                
                # Wenn Setting -> Objekt vom Typ setting anlegen
                elif(currentBlockType == "SETTINGS"):
                    listOfMbsObjects.append(mbsObject.setting(currentTextBlock))

                # Set current block Type to empty
                currentBlockType = ""

            # Search for object type_i, this has to be in line with $
            #--------------------------------------------------------
            for type_i in search4Objects:
                if(line.find(type_i, 1, len(type_i) + 1) >= 0):
                    # Set current block Type
                    currentBlockType = type_i
                    currentTextBlock.clear()
                    break

            # Delete content of current textblock
            #------------------------------------
            currentTextBlock.clear()
            
        currentTextBlock.append(line)

    # Informationen in ein json-File schreiben
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)
    jDataBase = json.dumps({"modelObjects": modelObjects})
    with open("Aufgabe_2/test.json", "w") as outfile:
        outfile.write(jDataBase)

    # Einlesen eines json-Files
    f = open("Aufgabe_2/test.json", "r")
    data = json.load(f)

    # Schreiben des Inputfiles (open mit "w" aufrufen, um Schreibrechte zu haben)
    fds = open("Aufgabe_2/test.fds", "w")
    for mbsObject_i in listOfMbsObjects:
        mbsObject_i.writeInputfile(fds)
    fds.close()

    print(len(listOfMbsObjects))

    return listOfMbsObjects