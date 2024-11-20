import mbsObject
import json

#-----------------------------------------------------------------------------------------------

def read_fdd_file(file_path):
    """
    Liest eine .fdd-Datei ein und erstellt eine Liste von MbsObjects.

    :param file_path: Pfad zur .fdd-Datei.
    :return: Liste der MbsObjects.
    """
    search4Objects = ["RIGID_BODY", "CONSTRAINT"]  # Fix definierte Schlagwörter

    with open(file_path, "r") as f:
        fileContent = f.read().splitlines()
        f.close                                     # sauber arbeiten

    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in fileContent:
        if "$" in line:
            if currentBlockType:
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                # Weitere Typen können hier hinzugefügt werden
                currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)

    return listOfMbsObjects

#----------------------------------------------------------------------------------------------

def save_to_json(listOfMbsObjects, json_file_path):
    """
    Speichert die Parameter der MbsObjects in einer JSON-Datei.

    :param listOfMbsObjects: Liste der MbsObjects.
    :param json_file_path: Pfad zur JSON-Datei.
    """
    modelObjects = [obj.parameter for obj in listOfMbsObjects]
    jDataBase = json.dumps({"modelObjects": modelObjects}, indent=4)
    with open(json_file_path, "w") as outfile:
        outfile.write(jDataBase)


# # Standard Möglichkeit, wie man ? daten/dictionarys speichern bzw lesen kann ?
# modelObjects= [] #leeres array
# for object in listOfMbsObjects:
#     modelObjects.append(object.parameter) # man holt sich alle Parameter
# jDataBase = json.dumps({"modelObjects": modelObjects})
# with open("Aufgabe 2/test.json","w") as outfile:
#     outfile.write(jDataBase)

#--------------------------------------------------------------------------------------------

def load_from_json(json_file_path):
    """
    Lädt Daten aus einer JSON-Datei.

    :param json_file_path: Pfad zur JSON-Datei.
    :return: Geladene Daten.
    """
    with open(json_file_path, "r") as f:
        return json.load(f)


# f = open("Aufgabe 2/test.json","r")
# data = json.load(f)
# f.close()

#---------------------------------------------------------------------------------------------

def write_fds_file(listOfMbsObjects, fds_file_path):
    """
    Schreibt die MbsObjects in eine .fds-Datei.

    :param listOfMbsObjects: Liste der MbsObjects.
    :param fds_file_path: Pfad zur .fds-Datei.
    """
    with open(fds_file_path, "w") as fds:
        for obj in listOfMbsObjects:
            obj.writeInputFile(fds)

# fds = open("Aufgabe 2/test.fds","w")  # w = write
# for mbsObject_i in listOfMbsObjects:
#     mbsObject_i.writeInputFile(fds)
# fds.close()

