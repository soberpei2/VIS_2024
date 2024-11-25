import mbsObject  # Import der Datei mit der Definition von mbsObject und seinen Subklassen
import json       # Modul für die Verarbeitung von JSON-Dateien

def readInputFile(filePath):
    """
    Liest eine Eingabedatei und erstellt eine Liste von mbsObjects basierend auf den enthaltenen Datenblöcken.

    Argumente:
        filePath (str): Pfad zur Eingabedatei.
        
    Rückgabe:
        list: Eine Liste von Objekten (mbsObject), die aus der Datei erstellt wurden.
    """
    # Datei öffnen und Inhalt zeilenweise lesen
    with open(filePath, "r") as f:
        fileContent = f.read().splitlines()
        fileContent.append("$") # Nötig um den letzten Block lesen zu können

    # Variablen für die Verarbeitung der Datei
    currentBlockType = ""  # Speichert den aktuellen Blocktyp, z. B. "RIGID_BODY"
    currentTextBlock = []  # Temporärer Speicher für den Inhalt eines Blocks
    listOfMbsObjects = []  # Liste, in der die erstellten Objekte gespeichert werden

    # Schlüsselwörter, nach denen in der Datei gesucht wird
    search4Objects = ["RIGID_BODY", "CONSTRAINT", "SETTINGS"]

    # Datei zeilenweise durchgehen
    for line in fileContent:
        # Prüfen, ob ein neuer Block beginnt (Start mit '$')
        if line.startswith("$"):
            # Falls ein Block aktiv ist, Objekt erstellen und hinzufügen
            if currentBlockType:
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                elif currentBlockType == "CONSTRAINT":
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))
                elif currentBlockType == "SETTINGS":
                    listOfMbsObjects.append(mbsObject.settings(currentTextBlock))
                # Nach Verarbeitung des Blocks wird der Typ zurückgesetzt
                currentBlockType = ""

        # Prüfen, ob eine Zeile einen bekannten Blocktyp enthält
        for type_i in search4Objects:
            if line.find(type_i) >= 0:  # Wenn der Blocktyp gefunden wird
                currentBlockType = type_i  # Typ speichern
                currentTextBlock.clear()  # Inhalt des vorherigen Blocks löschen
                break

        # Zeile zum aktuellen Block hinzufügen, falls ein Block aktiv ist
        currentTextBlock.append(line)
            
    # Rückgabe der Liste mit allen erstellten Objekten
    return listOfMbsObjects

def saveToJson(inputFilePath, jsonFilePath):
    """
    Verarbeitet die Eingabedatei und speichert die Objekte in einer Fds-Datei.

    Argumente:
        inputFilePath (str): Pfad zur Eingabedatei.
        jsonFilePath (str): Pfad und Name der Json Datei, in die die Daten gespeichert werden sollen.
    """

    # Eingabedatei lesen und Objekte erstellen
    listOfMbsObjects = readInputFile(inputFilePath)

    # JSON-kompatible Struktur erstellen
    modelObjects = []
    for obj in listOfMbsObjects:
        modelObjects.append(obj.parameter)

    # Daten als JSON speichern
    jDataBase =json.dumps({"modelObjects": modelObjects})
    with open(jsonFilePath, "w") as outfile:
        outfile.write(jDataBase)
    
    return listOfMbsObjects

def saveToFds(inputFilePath, fdsFilePath):
    """
    Verarbeitet die Eingabedatei und speichert die Objekte in einer Fds-Datei.

    Argumente:
        inputFilePath (str): Pfad zur Eingabedatei.
        fdsFilePath (str): Pfad und Name zur Ausgabedatei im FDS-Format.
    """
    # Eingabedatei lesen und Objekte erstellen
    listOfMbsObjects = readInputFile(inputFilePath)
    
    # Objekte in JSON-Datei speichern
       # Erstellen und Anlegen einer fds datei
    fds = open(fdsFilePath,"w")
    for mbsObject_i in listOfMbsObjects:
        mbsObject_i.writeInputfile(fds)
    fds.close()

    # Rückgabe der Liste der Objekte
    return listOfMbsObjects
