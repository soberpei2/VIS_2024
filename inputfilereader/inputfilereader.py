
import mbsObject

f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

currentBlockType = ""
currentTextBlock = []
listOfmbsObjects = []
searchforObjects = ["RIGID_BODY", "CONSTRAINT"]
for line in fileContent:
    if(line.find("$") >= 0): #new block found
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listOfmbsObjects.append(mbsObject.mbsObject("body", currentTextBlock))
            currentBlockType = ""


    for type_i in searchforObjects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

print(len(listOfmbsObjects))


