import mbsObject  # Importiert das Modul für MBS-Objekte
import json  # Importiert das Modul für die Arbeit mit JSON-Dateien

def read_fdd_file(file_path):
    """
    Liest eine FDD-Datei und extrahiert die MKS-Objekte und deren Attribute.

    Eingabe:
        file_path (str): Der Pfad zur FDD-Datei, die eingelesen werden soll.

    Rückgabe: 
        listOfMbsObjects (list): Eine Liste der MBS-Objekte, die aus der FDD-Datei extrahiert wurden.
    """
    # Definiert die Schlagwörter (Objekttypen), nach denen gesucht wird
    search4Objects = ["RIGID_BODY", "CONSTRAINT", "SETTINGS", "FORCE_GenericForce", "FORCE_GenericTorque"]

    # Öffnen und Einlesen des FDD-Dateiinhalts
    with open(file_path, "r") as f:
        fileContent = f.read().splitlines()  # Liest die Datei Zeile für Zeile
        fileContent.append("$")  # Fügt ein $ am Ende hinzu, um den letzten Block zu markieren

    currentBlockType = ""  # Speichert den Typ des aktuell verarbeiteten Blocks
    currentTextBlock = []  # Speichert die Zeilen eines aktuellen Blocks
    listOfMbsObjects = []  # Liste zur Speicherung der MBS-Objekte

    # Durchlaufen jeder Zeile der Datei
    for line in fileContent:
        # Überprüft, ob ein neuer Block beginnt (diese beginnen immer mit '$')
        if "$" in line:
            if currentBlockType:
                # Je nach Blocktyp wird das MBS-Objekt erstellt und zur Liste hinzugefügt
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
                
                # Zurücksetzen, damit der nächste Block verarbeitet werden kann
                currentBlockType = ""

        # Überprüfen, ob die Zeile den Beginn eines neuen Objekttyps markiert
        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:  # Sucht nach den Objekttypen in der Zeile
                currentBlockType = type_i  # Setzt den Blocktyp
                currentTextBlock.clear()  # Leert den aktuellen Textblock
                break  # Bricht die Schleife ab, wenn ein passender Objekttyp gefunden wurde

        # Fügt die aktuelle Zeile zum Textblock hinzu
        currentTextBlock.append(line)

    # Rückgabe der Liste der MBS-Objekte
    return listOfMbsObjects


def write_json_file(listOfMbsObjects, json_file_path):
    """
    Schreibt die Attribute der MKS-Objekte in eine JSON-Datei.

    Eingabe:
        listOfMbsObjects (list): Eine Liste der MKS-Objekte und deren Attribute.
        json_file_path (str): Der Pfad, an dem die JSON-Datei gespeichert werden soll.
    """
    # Extrahiert die Parameter jedes MBS-Objekts
    modelObjects = [obj.parameter for obj in listOfMbsObjects]

    # Wandelt die Parameter in ein JSON-kompatibles Format um und speichert sie
    jDataBase = json.dumps({"modelObjects": modelObjects}, indent=4)

    # Schreibt die JSON-Daten in die angegebene Datei
    with open(json_file_path, "w") as outfile:
        outfile.write(jDataBase)


def read_json_file(json_file_path):
    """
    Liest die Daten aus einer JSON-Datei.

    Eingabe:
        json_file_path (str): Der Pfad zur JSON-Datei.

    Rückgabe: 
        dict: Die aus der JSON-Datei geladenen Daten.
    """
    # Öffnet die JSON-Datei und lädt die Daten
    with open(json_file_path, "r") as f:
        return json.load(f)  # Gibt die geladenen Daten als Dictionary zurück


def write_fds_file(listOfMbsObjects, fds_file_path):
    """
    Schreibt die MKS-Objekte und deren Attribute in eine FDS-Datei.

    Eingabe: 
        listOfMbsObjects (list): Eine Liste der MKS-Objekte und deren Attribute.
        fds_file_path (str): Der Pfad, an dem die FDS-Datei gespeichert werden soll.
    """
    # Öffnet die FDS-Datei im Schreibmodus
    with open(fds_file_path, "w") as fds:
        # Schreibt für jedes MBS-Objekt in der Liste den Inhalt in die FDS-Datei
        for obj in listOfMbsObjects:
            obj.writeInputFile(fds)  # Ruft die Methode zur Ausgabe des Objekts auf
