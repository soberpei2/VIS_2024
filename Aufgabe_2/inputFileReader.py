import json
from mbsObject import rigidBody  # Import der rigidBody-Klasse aus dem Modul mbsObject


# Funktion, die die Eingabedatei liest und Objekte basierend auf den Schlagwörtern erstellt
def read_input_file(file_path, search_objects):
    """
    Liest die Eingabedatei und sucht nach Objekten, die den angegebenen Schlagwörtern entsprechen.

    Parameters:
        file_path (str): Der Pfad zur Eingabedatei.
        search_objects (list): Eine Liste von Objektschlagwörtern (z. B. ["RIGID_BODY", "CONSTRAINT"]).

    Returns:
        list: Eine Liste von mbsObject-Instanzen (z. B. rigidBody-Objekten).
    """
    # Öffne die Datei und lese den Inhalt Zeile für Zeile
    with open("Aufgabe_2/test.fdd", "r") as f:
        file_content = f.read().splitlines()

    # Initialisierung der Variablen
    list_of_mbs_objects = []  # Liste zur Speicherung der erstellten MBS-Objekte
    current_block_type = ""  # Der aktuelle Blocktyp (z. B. "RIGID_BODY")
    current_text_block = []  # Der Textblock, der den aktuellen Block beschreibt

    # Durchlaufe jede Zeile im Dateicontent
    for line in file_content:
        # Überprüfen, ob das Zeilenzeichen "$" vorkommt (Kennzeichnung für neue Blöcke)
        if line.find("$") >= 0:
            # Wenn ein Block zuvor gefunden wurde, verarbeite ihn
            if current_block_type != "":
                # Wenn der Blocktyp ein "RIGID_BODY" ist, erstelle ein neues rigidBody-Objekt
                if current_block_type == "RIGID_BODY":
                    list_of_mbs_objects.append(rigidBody(current_text_block))  # Füge das erstellte Objekt zur Liste hinzu
                current_block_type = ""  # Setze den aktuellen Blocktyp zurück

            # Überprüfe, ob die aktuelle Zeile einen der Suchbegriffe enthält (z. B. "RIGID_BODY")
            for type_i in search_objects:
                if line.find(type_i, 1, len(type_i) + 1) >= 0:
                    current_block_type = type_i  # Setze den aktuellen Blocktyp
                    current_text_block.clear()  # Leere den Textblock für den neuen Block
                    break  # Breche die Schleife ab, wenn ein Suchbegriff gefunden wurde

            # Leere den Textblock, bevor der nächste Block verarbeitet wird
            current_text_block.clear()

        # Füge die aktuelle Zeile zum Textblock hinzu
        current_text_block.append(line)

    # Rückgabe der Liste von MBS-Objekten (z. B. rigidBody-Objekten)
    return list_of_mbs_objects


# Funktion, die die Daten in einer JSON-Datei speichert
def write_json(data, file_path):
    """
    Speichert die Daten als JSON-Datei.

    Parameters:
        data (dict or list): Die Daten, die als JSON gespeichert werden sollen.
        file_path (str): Der Pfad zur Ausgabedatei.
    """
    # Öffne die Datei im Schreibmodus und speichere die Daten im JSON-Format
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=4)  # Speichert die Daten mit Einrückungen für bessere Lesbarkeit


# Funktion, die eine JSON-Datei einliest und die Daten zurückgibt
def read_json(file_path):
    """
    Liest eine JSON-Datei und gibt die enthaltenen Daten zurück.

    Parameters:
        file_path (str): Der Pfad zur JSON-Datei.

    Returns:
        dict or list: Die Daten, die aus der JSON-Datei geladen wurden.
    """
    # Öffne die JSON-Datei im Lese-Modus und lade die Daten
    with open(file_path, "r") as f:
        return json.load(f)  # Gibt die geladenen Daten zurück


# Funktion, die eine Liste von MBS-Objekten in einer FDS-Datei speichert
def write_fds_file(mbs_objects, file_path):
    """
    Speichert eine Liste von MBS-Objekten in einer FDS-Datei.

    Parameters:
        mbs_objects (list): Eine Liste von mbsObject-Instanzen.
        file_path (str): Der Pfad zur Ausgabedatei.
    """
    # Öffne die Datei im Schreibmodus und schreibe jedes MBS-Objekt
    with open(file_path, "w") as fds:
        for mbs_object in mbs_objects:
            mbs_object.writeInputfile(fds)  # Ruft die Methode zum Schreiben des Objekts auf
