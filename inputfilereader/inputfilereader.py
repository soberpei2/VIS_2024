
import mbsObject

f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

numOfRigidBodys = 0
numOfConstraints = 0
currentBlockType = ""
currentTextBlock = []
listofMbsObjects =[]
search4Objects = ["RIGID_BODY" , "CONSTRAINT"]
for line in fileContent:
    if(line.find("$") >= 0):                                      #new block found
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listofMbsObjects.append(mbsObject.mbsObject("body",currentTextBlock))
            currentBlockType = ""

    for type_i in search4Objects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
    
    currentTextBlock.append(line)

print(listofMbsObjects)
