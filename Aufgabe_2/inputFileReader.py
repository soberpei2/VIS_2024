import mbsObject
import json

f = open("Aufgabe_2/test.fdd", "r")
fileContent = f.read().splitlines()
f.close()

listOfMbsObjects = []
currentBlockType = ""
currentTextBlock = []
search4Objects = ["RIGID_BODY", "CONSTRAINT"]

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
            # Count number of rigid bodies
            if(currentBlockType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))

            # Count number of constraints
            #elif(currentBlockType == "CONSTRAINT"):
            #    numOfConstraints +=1

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

# Informationen in ein json-File schreien
modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)
jDataBase = json.dumps({"modelObjects": modelObjects})
with open("Aufgabe_2/Ausgabe.json", "w") as outfile:
    outfile.write(jDataBase)

# Einlesen eines json-Files
f = open("Aufgabe_2/Ausgabe.json", "r")
data = json.load(f)

# Schreiben des Inputfiles (open mit "w" aufrufen, um Schreibrechte zu haben)
fds = open("Aufgabe_2/Ausgabe.fds", "w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()

print(len(listOfMbsObjects))