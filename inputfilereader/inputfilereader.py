
import mbsObject
import json

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
                listOfmbsObjects.append(mbsObject.rigidBody(currentTextBlock))
            currentBlockType = ""


    for type_i in searchforObjects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

modelObjects = []
for object in listOfmbsObjects:
    modelObjects.append(object.parameter)
jDataBase = json.dumps({"modelObjects": modelObjects})
with open("inputfilereader/test.json", "w") as outfile:
    outfile.write(jDataBase)

f = open("inputfilereader/test.json", "r")
data = json.load(f)
f.close()

fds = open("inputfilereader/test.fds", "w")
for mbsObject_i in listOfmbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()

print(len(listOfmbsObjects))


