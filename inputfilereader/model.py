
#import/export functionality (for later use in model.py)
modelObjects = []
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)
jDataBase = json.dumps({"modelObjects": modelObjects})
with open("inputfilereader/test.json", "w") as outfile:
    outfile.write(jDataBase)

f = open("inputfilereader/test.json","r")
data = json.load(f)
f.close()

fds = open("inputfilereader/test.fds","w")
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)
fds.close()
#-------------------------------------------------------