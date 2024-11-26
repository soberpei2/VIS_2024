
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
    search4Objects = ["RIGID_BODY" , "CONSTRAINT" , "FORCE_GenericForce" , "FORCE_GenericTorque" , "MEASURE1" , "MEASURE2","SETTINGS"]

    for line in fileContent:
        if(line.find("$") >= 0):                                      #new block found
            if(currentBlockType != ""):
                if(currentBlockType == "RIGID_BODY"):
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif(currentBlockType == "CONSTRAINT"):
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                elif(currentBlockType == "FORCE_GenericForce"):
                    listOfMbsObjects.append(mbsObject.force_GenericForce(currentTextBlock))
                elif(currentBlockType == "FORCE_GenericTorque"):
                    listOfMbsObjects.append(mbsObject.force_GenericTorque(currentTextBlock))
                elif(currentBlockType == "MEASURE1"):
                    listOfMbsObjects.append(mbsObject.measure1(currentTextBlock))
                elif(currentBlockType == "MEASURE2"):
                    listOfMbsObjects.append(mbsObject.measure2(currentTextBlock))
                elif(currentBlockType == "SETTINGS"):
                    listOfMbsObjects.append(mbsObject.gravity(currentTextBlock))
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
        with open("inputfilereader/test.json","w")as outfile:
            outfile.write(jDataBase)

        fds = open("inputfilereader/test.fds","w")
        for mbsObjects_i in listOfMbsObjects:
            mbsObjects_i.writeInputfile(fds)
        fds.close

        txt = open("inputfilereader/test.txt","w")
        for mbsObjects_i in listOfMbsObjects:
            mbsObjects_i.writeInputfile(txt)
        txt.close

    print(len(listOfMbsObjects))
