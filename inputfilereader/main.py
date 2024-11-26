import inputfilereader

def main():
    """
    Hauptfunktion, die alle notwendigen Schritte zur Verarbeitung und Ausgabe der Daten ausführt.
    """
    # Schritt 1: Datei einlesen
    # Liest den Inhalt der .fdd-Datei
    file_content = inputfilereader.read_file("inputfilereader/test.fdd")

    # Schritt 2: Objekte verarbeiten
    # Verarbeitet den Inhalt und sucht nach den Objekttypen "RIGID_BODY" und "CONSTRAINT"
    search_for_objects = ["RIGID_BODY", "CONSTRAINT"]
    list_of_mbs_objects = inputfilereader.process_blocks(file_content, search_for_objects)

    # Schritt 3: JSON-Ausgabe erstellen
    # Schreibt die verarbeiteten Objekte als JSON-Datei
    inputfilereader.write_json_output(list_of_mbs_objects, "inputfilereader/test.json")

    # Schritt 4: FDS-Ausgabe erstellen
    # Schreibt die verarbeiteten Objekte in eine FDS-Datei
    inputfilereader.write_fds_output(list_of_mbs_objects, "inputfilereader/test.fds")

    # Schritt 5: Anzahl der Objekte drucken
    # Gibt die Anzahl der verarbeiteten Objekte auf der Konsole aus
    inputfilereader.print_object_count(list_of_mbs_objects)

# Dies stellt sicher, dass die main-Funktion nur ausgeführt wird, wenn dieses Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()
