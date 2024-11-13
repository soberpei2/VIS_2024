import inputFileReader as iFR


test = iFR.readFile("Aufgabe_2","test.fdd")
list = iFR.parseText2blocksOfMbsObjects(test,["RIGID_BODY","CONSTRAINT"])
iFR.writeFdsFile(list,"Aufgabe_2","test2.fds")
iFR.writeJsonFile(list,"Aufgabe_2","test2.json")

testjson = iFR.readJsonFile("Aufgabe_2","test.json")
print(testjson)