
import mbsObject
import json
import vtk

f = open("Aufgabe_2/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

numOfRigidBodies = 0
numOfConstraints = 0
currentBlockType = ""
currentTextBlock = []
listOfMbsObjects = []
search4Objects = ["RIGID_BODY","CONSTRAINT"]#mögliche Schlagwörter

##Lesen der Zeilen im Inputfile 
for line in fileContent:#Für alle Zeilen (line ist Iterator, alle Zeilen von Filevonten)
    if(line.find("$")>=0):#new block found, im fdd file ist immer das Schlagwort
        if(currentBlockType !=""):
            if(currentBlockType == "RIGID_BODY"):
                listOfMbsObjects.append(mbsObject.rigidbody(currentTextBlock))
            #elif(currentBlockType == "CONSTRAINT"):
                #numOfConstraints += 1
            currentBlockType = ""


    for type_i in search4Objects:#Suche für alle Schlagwörter
        if(line.find(type_i,1,len(type_i)+1)>=0):
            currentBlockType = type_i
            currentTextBlock.clear()

            currentTextBlock.append(line)

modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)
jDataBase = json.dumps({"modelObjects": modelObjects})
with open ("Aufgabe_2/test.json","w") as outfile:
    outfile.write(jDataBase)

f=open("Aufgabe_2/test.json","r")
data=json.load(f)
f.close()
    #if(line.find("RIGID_BODY",1,len("RIGID_BODY")+1)>= 0):
        #currentBlockType = "RIGID_BODY"
       # currentTextBlock.clear()
       # break

#currentTextBlock.append(line)

fds = open("Aufgabe_2/test.fds","w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()
print(len(listOfMbsObjects))


