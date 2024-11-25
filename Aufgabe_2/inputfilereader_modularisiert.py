import json
import mbsObject


def readFile(filePath):
    """Liest die Datei und gibt die Zeilen als Liste zurück. Fügt am Ende
    ein "$" ein um bis dort hin die Blöcke teilen zu können"""
    with open(filePath, "r") as file:
        fileInhalt = file.read().splitlines()
        fileInhalt.append("$")
        file.close

    listOfMbsObjects = []
    currentBlockType = ""
    currentTextBlock = []

    search4Objects = ["RIGID_BODY", "CONSTRAINT", "Settings", "Force_GenericForce"]


    for line in fileInhalt:
        # Suche nach $-Symbol: Neue Blockerkennung
        if line.find("$") >= 0:
            # Verarbeite aktuellen Block
            if currentBlockType:
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif currentBlockType == "CONSTRAINT":
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                elif currentBlockType == "SETTINGS":
                    listOfMbsObjects.append(mbsObject.settings(currentTextBlock))
                elif currentBlockType == "FORCE_GenericForce":
                    listOfMbsObjects.append(mbsObject.genericForce(currentTextBlock))
                # Suche neuen Blocktyp
                currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        #currentTextBlock.clear()

        currentTextBlock.append(line)

    return listOfMbsObjects


def writeToJson(listOfMbsObjects, jsonPath):
    """Speichert die Objekte in eine JSON-Datei."""
    modelObjects = []
    for object in listOfMbsObjects:
        modelObjects.append(object.parameter)
    jDataBase = json.dumps({"modelObjects": modelObjects})
    with open(jsonPath, "w") as outfile:
        outfile.write(jDataBase)


def readFromJson(jsonPath):
    """Liest eine JSON-Datei ein und gibt den Inhalt zurück."""
    with open(jsonPath, "r") as infile:
        return json.load(infile)


def writeFdsFile(listOfMbsObjects, fdsPath):
    """Schreibt die Objekte in eine FDS-Datei."""
    with open(fdsPath, "w") as fds:
        for mbs_object in listOfMbsObjects:
            mbs_object.writeInputfile(fds)