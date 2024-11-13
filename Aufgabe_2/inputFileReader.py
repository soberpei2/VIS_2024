# Import class mbsObject
import mbsObject

# Open FreeDyne-file
f = open("Aufgabe_2/test.fdd", "r")

# Read opened file (save to variable) -> each line is saved as a string
fileContent = f.read().splitlines()

# Close file after saving its content
f.close()

# List of Mbs Objects
listOfMbsObjects = []

# Definition of a current textblock
currentBlockType = ""
currentTextBlock = []

# Define list of objects, which should be searched
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

# Schreiben des Inputfiles (open mit "w" aufrufen, um Schreibrechte zu haben)
fds = open("Aufgabe_2/test.fdd", "w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()

print(len(listOfMbsObjects))