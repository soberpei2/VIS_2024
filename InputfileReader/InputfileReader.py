import mbsObject

f = open("InputfileReader/test.fdd","r")

fileContent = f.read().splitlines()     #was auf der Festplatte ist kommt in den Arbeitsspeicher
f.close()

currentBlockType = ""
currentTextBlock = []
listofmbsObjects = []
search4Objects = ["RIGID_BODY", "CONSTRAINT"]

for line in fileContent:                #für alle Zeilen
    if(line.find("$")>=0):              #neuer Block gefunden
        if(currentBlockType != ""):
            if(currentBlockType == "RIGID_BODY"):
                listofmbsObjects.append(mbsObject.rigidBody(currentTextBlock))
            currentBlockType = ""
            
    for type_i in search4Objects:
        if(line.find(type_i,1,len(type_i)+1) >= 0):
            currentBlockType = type_i
            currentTextBlock.clear()
            break

    currentTextBlock.append(line)

print("List of mbsObjects = ",len(listofmbsObjects))