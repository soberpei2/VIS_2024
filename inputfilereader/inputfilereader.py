

import mbsObject
import json

f = open("inputfilereader/test.fdd","r")    #Öffnen des .fdd formates (dort steht der shit auf Freedyn)

fileContent = f.read().splitlines()         #Das file ist in einer Wust, hier wird es in Zeilen formatiert und Abgespeichert
f.close()                                   #Schließen das das Programm wieder benutzt werden kann (von anderen Programmen)

currentBlockType = ""                       #Anlegen einer leeren Variable mit dem Namen currentBlockType (jetztiger Blocktyp)
currentTextBlock = []                       #Anlegen einer leeren Variable mit dem Namen currentTextBlock (Variablen des Types)
listOfMbsObjects = []                       #Anlegen einer leeren Variable mit dem Namen listOfMbsObjects (wie viele Objekte gibt es)
search4Objects  = ["RIGID_BODY", "CONSTRAINT"]  #Suchen nach Gruppen
for line in fileContent:                        #gehe durch die Zeilen im gespeicherten .fdd files
    if(line.find("$") >= 0):                    #Schauen ob eine  Dollarzeichen gefunden wird
        if(currentBlockType != ""):                 #Webn der BlockType nicht leer ist gehe weiter
            if(currentBlockType == "RIGID_BODY"):   #Wenn ein Rigid Body gefunden wird gehe weiter
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))  #Füge die Eigenschaften des Objectes zur Liste dazu
            currentBlockType = ""                   #Leere den currentBlockType

    for type_i in search4Objects:           #for-Schleife bis das if wahr ist, Suchen ob es sich um ein search4Object handel (z.B: Rigid_Body)
        if(line.find(type_i,1,len(type_i)+1) >= 0):    #Suchen ob die Buchstaben zusammenpassen für ein search4Object 
            currentBlockType = type_i       #Schreibe das Wort in currentBlockType
            currentTextBlock.clear()        #TextBlock(Variablen) bereinigen
            break
    
    currentTextBlock.append(line)           #Speichere die Informationen der aktive Zeile in den currentTextBlock

modelObjects =[]                                #Anlegen einer leeren Variable mit dem Namen modelObjects
for object in listOfMbsObjects:                 #gehe durch die Objecte in listOfObjects
    modelObjects.append(object.parameter)       #Wir schreiben in modelObjects alle Parameter der Objecte (search4Objects)
jDataBase = json.dumps({"modelObjects": modelObjects})  #Speichern der Daten in eine Variable (jDataBase) die wir für json brauchen
with open("inputfilereader/test.json","w") as outfile:  #leeres json öffnen
    outfile.write(jDataBase)                          #schreiben der Daten in json

fj = open("inputfilereader/test.json","r")      #öffnen der test.json Datei mit leseberechtigung
data = json.load(fj)                            #Warum?? data ist unverwendet
fj.close()                                      #Speichern und Schließen

fds = open("inputfilereader/test.fds","w")          #Öffnen eines fds files mit dem Namen test.fds mit Schreibberechtigung
for mbsObject_i in listOfMbsObjects:                #for mit mbsObject als Counter in listOfMbsObjects
    mbsObject_i.writeInputfile(fds)                 #Schreibe das fds file (Zeilenweise die Daten von listOfMbsObjects)
fds.close()                                         #Speichern und Schließen

print(len(listOfMbsObjects))                        #Schreiben der Objectanzahl auf die Konsole