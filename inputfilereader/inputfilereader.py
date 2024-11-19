
import mbsObject
import json

f = open("inputfilereader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

currentBlockType = ""
currentTextBlock = []
listOfMbsObjects = []
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
with open("inputfilereader/test.json","w") as outfile:      # mit alt + shift + f zum strukturieren
    outfile.write(jDataBase)

f = open("inputfilereader/test.json","r")   # r für read
data = json.load(f)
f.close()

fds = open("inputfilereader/test.fds","w") # w ... write | a für append wenn es vorhanden ist
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()

print(len(listOfMbsObjects))