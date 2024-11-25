import mbsObject
import json


def read_fdd_file(file_path):
    """
    Einlesen einer FDD Datei und erkennen der MKS Objekte und deren Attribute

    Eingabe:
        file_path = Pfad zum FDD File

    Rückgabe: 
        Liste der MBS Objekte 
    """
    search4Objects = ["RIGID_BODY", "CONSTRAINT","SETTINGS","FORCE_GenericForce","FORCE_GenericTorque"]  #definierte Schlagwörter, nach denen gesucht wird

    with open(file_path, "r") as f:
        fileContent = f.read().splitlines()
        fileContent.append("$")                     #damit der letzte Block auch noch erkannt wird
        f.close                                     #sauber arbeiten --> file schließen

    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in fileContent:
        #Check, ob ein neuer Block beginnt --> beginnt immer mit $
        if "$" in line:
            if currentBlockType:
                #Einteilung in die verschiedenen Typen
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif currentBlockType == "CONSTRAINT":
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                elif currentBlockType == "SETTINGS":
                    listOfMbsObjects.append(mbsObject.settings(currentTextBlock))
                elif currentBlockType == "FORCE_GenericForce":
                    listOfMbsObjects.append(mbsObject.genericForce(currentTextBlock))
                elif currentBlockType == "FORCE_GenericTorque":
                    listOfMbsObjects.append(mbsObject.genericTorque(currentTextBlock))
                
                #zurücksetzen, damit nächster Block gefunden werden kann
                currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)

    return listOfMbsObjects


def write_json_file(listOfMbsObjects, json_file_path):
    """
    Die gelesenen Attribute der MKS Objekte in ein JSON File schreiben

    Eingabe:
        listOfMbsObjects = Liste der MKS Objekte und deren Attribute
        json_file_path = Pfad, wo die JSON Datei gespeichert werden soll
    """
    modelObjects = [obj.parameter for obj in listOfMbsObjects]
    jDataBase = json.dumps({"modelObjects": modelObjects}, indent=4)
    with open(json_file_path, "w") as outfile:
        outfile.write(jDataBase)


def read_json_file(json_file_path):
    """
    Lädt die Daten aus einer JSON Datei

    Eingabe:
        param json_file_path = Pfad zur JSON Datei

    Rückgabe: 
        aus JSON geladene Daten
    """
    with open(json_file_path, "r") as f:
        return json.load(f)


def write_fds_file(listOfMbsObjects, fds_file_path):
    """
    Die MKS Objekte und deren Attribute in ein fds File schreiben

    Eingabe: 
        listOfMbsObjects = Liste der MKS Objekte und deren Attribute
        fds_file_path = Pfad, wo die fds Datei gespeichert werden soll
    """
    with open(fds_file_path, "w") as fds:
        for obj in listOfMbsObjects:
            obj.writeInputFile(fds)

