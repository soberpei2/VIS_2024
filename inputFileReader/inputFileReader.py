
f = open("inputFileReader/test.fdd","r")

fileContent = f.read().splitlines()
f.close()

numOfRigidBodies = 0
for line in fileContent:
    if(line.find("$") >= 0): #found new block
        if(line.find("RIGID_BODY",1,len("RIGID_BODY")+1) >= 0):
            numOfRigidBodies += 1

print(numOfRigidBodies)