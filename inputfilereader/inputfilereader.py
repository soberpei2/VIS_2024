import mbsObject
import json

def read_file(file_path):
    """
    Liest eine Datei und gibt den Inhalt als Liste von Zeilen zurück.
    
    Parameter:
    - file_path: Der Pfad zur Eingabedatei
    
    Rückgabewert:
    - Eine Liste mit den Zeilen der Datei
    """
    with open(file_path, "r") as f:
        # Die Datei wird Zeile für Zeile eingelesen und in einer Liste gespeichert
        return f.read().splitlines()

def process_blocks(file_content, search_for_objects):
    """
    Verarbeitet die Zeilen der Datei und erstellt eine Liste von mbsObject-Instanzen.
    
    Parameter:
    - file_content: Eine Liste von Zeilen aus der Eingabedatei
    - search_for_objects: Eine Liste der Objekttypen, nach denen gesucht wird, wie "RIGID_BODY" oder "CONSTRAINT"
    
    Rückgabewert:
    - Eine Liste von mbsObject-Instanzen, die auf den gesuchten Objekttypen basieren
    """
    current_block_type = ""          # Der aktuelle Blocktyp (z.B. "RIGID_BODY", "CONSTRAINT")
    current_text_block = []          # Die Textdaten des aktuellen Blocks
    list_of_mbs_objects = []         # Liste, die alle MBS-Objekte speichern wird

    # Durchlaufen jeder Zeile im eingelesenen Dateiinhalt
    for line in file_content:
        # Wenn ein Dollarzeichen "$" gefunden wird, überprüfen wir, ob der aktuelle Block abgeschlossen ist
        if "$" in line:
            if current_block_type != "":  # Wenn ein Blocktyp gesetzt ist
                if current_block_type == "RIGID_BODY":
                    # Falls der Blocktyp "RIGID_BODY" ist, wird das Objekt in die Liste aufgenommen
                    list_of_mbs_objects.append(mbsObject.rigidBody(current_text_block))
                # Der Blocktyp wird nach der Verarbeitung des Blocks zurückgesetzt
                current_block_type = ""

        # Durchlaufe die Objekttypen, nach denen wir suchen (z.B. "RIGID_BODY", "CONSTRAINT")
        for search_type in search_for_objects:
            # Wenn der Objekttyp in der Zeile gefunden wird, wird der Blocktyp gesetzt und der Block gelöscht
            if line.find(search_type, 1, len(search_type) + 1) >= 0:
                current_block_type = search_type
                current_text_block.clear()  # Löscht den Textblock, um die neuen Daten zu speichern
                break  # Beende die Suche, wenn ein passender Blocktyp gefunden wurde

        # Füge die aktuelle Zeile zum Textblock des aktuellen Objekts hinzu
        current_text_block.append(line)

    # Rückgabe der Liste von MBS-Objekten
    return list_of_mbs_objects

def write_json_output(list_of_mbs_objects, output_file_path):
    """
    Schreibt die MBS-Objekte in eine JSON-Datei.
    
    Parameter:
    - list_of_mbs_objects: Liste der verarbeiteten MBS-Objekte
    - output_file_path: Der Pfad zur Ausgabedatei, in der das JSON gespeichert wird
    """
    # Extrahiere die Parameter jedes Objekts und erstelle ein JSON-kompatibles Format
    model_objects = [obj.parameter for obj in list_of_mbs_objects]
    
    # Erstelle den JSON-Datenstring
    json_data = json.dumps({"modelObjects": model_objects})

    # Schreibe den JSON-Datenstring in die Ausgabedatei
    with open(output_file_path, "w") as outfile:
        outfile.write(json_data)

def write_fds_output(list_of_mbs_objects, output_file_path):
    """
    Schreibt die MBS-Objekte in eine FDS-Datei.
    
    Parameter:
    - list_of_mbs_objects: Liste der verarbeiteten MBS-Objekte
    - output_file_path: Der Pfad zur Ausgabedatei, in der das FDS gespeichert wird
    """
    # Öffne die Datei zum Schreiben
    with open(output_file_path, "w") as fds:
        # Schreibe jedes Objekt in die Datei, indem die Methode writeInputfile verwendet wird
        for mbs_object in list_of_mbs_objects:
            mbs_object.writeInputfile(fds)

def print_object_count(list_of_mbs_objects):
    """
    Gibt die Anzahl der MBS-Objekte aus.
    
    Parameter:
    - list_of_mbs_objects: Liste der verarbeiteten MBS-Objekte
    """
    print(len(list_of_mbs_objects))  # Anzahl der Objekte in der Konsole ausgeben
