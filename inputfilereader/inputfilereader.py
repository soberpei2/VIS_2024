
import mbsObject
import json


def inputfilereader(file):  #als Funktion definiert

    f = open(file,"r")

    fileContent = f.read().splitlines()
    f.close()

    numOfRigidBodys = 0
    numOfConstraints = 0
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects =[]
    search4Objects = ["RIGID_BODY" , "CONSTRAINT"]

    for line in fileContent:
        if(line.find("$") >= 0):                                      #new block found
            if(currentBlockType != ""):
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                    #numOfConstraints+=1
                currentBlockType = ""

        for type_i in search4Objects:
            if(line.find(type_i,1,len(type_i)+1) >= 0):
                currentBlockType = type_i
                currentTextBlock.clear()
                break
        
        currentTextBlock.append(line)

        modelObjects=[]

        for object in listOfMbsObjects:
            modelObjects.append(object.parameter)
        jDataBase = json.dumps({"modelObjects":modelObjects})
        with open("inputfilereader/test.vis3","w")as outfile:
            outfile.write(jDataBase)

        fds = open("inputfilereader/test.fds","w")
        for mbsObjects_i in listOfMbsObjects:
            mbsObjects_i.writeInputfile(fds)
        fds.close

    print(len(listOfMbsObjects))
