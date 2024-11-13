
import mbsObject

f = open("inputFileReader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

numOfRigidBodies = 0
numOfConstraints = 0
currentBlockType = ""
currentTextBlock = []
search4Objects = ["RIGID_BODY", "CONSTRAINT"]
listOfMbsObjects = []

#factoryFunction
for line in fileContent:
    if(line.find("$") >= 0): #found new block
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.mbsObject("body",currentTextBlock))
            currentBlockType = ""
    
    for type_i in search4Objects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

print(len(listOfMbsObjects))