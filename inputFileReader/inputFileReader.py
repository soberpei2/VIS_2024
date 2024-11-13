
import mbsObject
import json

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
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
            currentBlockType = ""
    
    for type_i in search4Objects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)

jDataBase = json.dumps({"modelObjects": modelObjects})
with open("inputfilereader/test.json","w") as outfile:
    outfile.write(jDataBase)

f = open("inputfilereader/test.json","r")
data = json.load(f)
f.close()

fds = open("inputfilereader/test.fds","w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputFile(fds)
fds.close()

print(len(listOfMbsObjects))