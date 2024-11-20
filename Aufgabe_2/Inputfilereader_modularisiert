import json
import mbsObject

# Modul-Funktion: Datei einlesen
def read_file(file_path):
    """Liest die Datei und gibt die Zeilen als Liste zurück."""
    with open(file_path, "r") as file:
        return file.read().splitlines()

# Modul-Funktion: Datei analysieren
def analyse_file(file_content):
    """Analysiert die Datei und extrahiert MBS-Objekte."""
    search4Objects = ["RIGID_BODY", "CONSTRAINT"]  # mögliche Schlagwörter
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in file_content:
        if line.find("$") >= 0:  # Neuer Block gefunden
            if currentBlockType != "":
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidbody(currentTextBlock))  # Hier wird ein 'rigidbody' erzeugt
                # elif currentBlockType == "CONSTRAINT":
                #     numOfConstraints += 1
                currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()

        currentTextBlock.append(line)

    return listOfMbsObjects

# Modul-Funktion: JSON erstellen
def write_json(listOfMbsObjects, json_path):
    """Erstellt eine JSON-Datei aus den MBS-Objekten."""
    modelObjects = [obj.parameter for obj in listOfMbsObjects]
    jDataBase = json.dumps({"modelObjects": modelObjects})
    with open(json_path, "w") as outfile:
        outfile.write(jDataBase)

# Modul-Funktion: JSON lesen
def read_json(json_path):
    """Liest und gibt die JSON-Daten zurück."""
    with open(json_path, "r") as file:
        return json.load(file)

# Modul-Funktion: FDS schreiben
def write_fds(listOfMbsObjects, fds_path):
    """Schreibt die Liste der MBS-Objekte in eine FDS-Datei."""
    with open(fds_path, "w") as fds_file:
        for mbsObject_i in listOfMbsObjects:
            mbsObject_i.writeInputfile(fds_file)