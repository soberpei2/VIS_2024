import os
import mbsObject
import json

# Funktion für Inputfilereader
def inputfilereader(FilePath):
    # Sicherstellen, dass die Eingabedatei existiert
    if not os.path.exists(FilePath):
        raise FileNotFoundError(f"Die Datei {FilePath} wurde nicht gefunden.")

    # Dateiinhalt lesen
    with open(FilePath, "r") as f:
        fileContent = f.read().splitlines()  # Einlesen der Zeilen in eine Liste

    # Initialisieren der Variablen
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    search4Objects = ["RIGID_BODY", "CONSTRAINT", "FORCE_GenericForce", "FORCE_GenericTorque"]

    # Zeilenverarbeitung
    for line in fileContent:
        if line.find("$") >= 0:  # Neuer Block gefunden bei $
            if currentBlockType != "":  # Verarbeiten des Blocks, wenn Typ existiert
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif currentBlockType == "CONSTRAINT":
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                """elif currentBlockType == "FORCE_GenericForce":
                    listOfMbsObjects.append(mbsObject.genericForce(currentTextBlock))
                elif currentBlockType == "FORCE_GenericTorque":
                    listOfMbsObjects.append(mbsObject.genericTorque(currentTextBlock))"""

                currentBlockType = ""  # Zurücksetzen des Blocktyps

        # Blocktyp erkennen
        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:  # Nach Schlagwort suchen
                currentBlockType = type_i
                currentTextBlock.clear()  # Bereinigen
                break

        currentTextBlock.append(line)  # Neue Zeile hinzufügen

    print(len(listOfMbsObjects))

    # Import-/Export-Funktionalität
    modelObjects = []
    for obj in listOfMbsObjects:
        modelObjects.append(obj.parameter)

    # JSON-Daten erstellen und schreiben
    output_folder = "Aufgabe 2"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    json_path = os.path.join(output_folder, "test.json")
    jDataBase = json.dumps({"modelObjects": modelObjects}, indent=4) #indent 4 für bessere Lesbarkeit

    with open(json_path, "w") as outfile:
        outfile.write(jDataBase)
    print(f"JSON-Datei erfolgreich erstellt: {json_path}")

    # Eingabedatei im gewünschten Format ausgeben
    fds_path = os.path.join(output_folder, "test.fds")
    with open(fds_path, "w") as fds:
        for mbsObject_i in listOfMbsObjects:
            mbsObject_i.writeInputfile(fds)
    print(f"FDS-Datei erfolgreich erstellt: {fds_path}")

    return listOfMbsObjects

# Beispielaufruf
if __name__ == "__main__":
    fdd_path = "Aufgabe 2/test.fdd"
    inputfilereader(fdd_path)
