import json
import mbsObject


def read_file(file_path):
    """Liest die Datei und gibt die Zeilen als Liste zurück."""
    with open(file_path, "r") as file:
        return file.read().splitlines()


def parse_file_content(file_content, search_objects):
    
    list_of_mbs_objects = []
    current_block_type = ""
    current_text_block = []

    for line in file_content:
        # Suche nach $-Symbol: Neue Blockerkennung
        if line.find("$") >= 0:
            # Verarbeite aktuellen Block
            if current_block_type:
                if current_block_type == "RIGID_BODY":
                    list_of_mbs_objects.append(mbsObject.rigidBody(current_text_block))

                # Weitere Typen können hier hinzugefügt werden
                # if current_block_type == "CONSTRAINT":
                #     list_of_mbs_objects.append(mbsObject.constraint(currentTextBlock))

            # Suche neuen Blocktyp
            current_block_type = ""
            for type_i in search_objects:
                if line.find(type_i, 1, len(type_i) + 1) >= 0:
                    current_block_type = type_i
                    current_text_block.clear()
                    break

            current_text_block.clear()

        current_text_block.append(line)

    return list_of_mbs_objects


def write_to_json(objects, output_file):
    """Speichert die Objekte in eine JSON-Datei."""
    model_objects = [obj.parameter for obj in objects]
    with open(output_file, "w") as outfile:
        json.dump({"modelObjects": model_objects}, outfile)


def read_from_json(input_file):
    """Liest eine JSON-Datei ein und gibt den Inhalt zurück."""
    with open(input_file, "r") as infile:
        return json.load(infile)


def write_fds_file(objects, output_file):
    """Schreibt die Objekte in eine FDS-Datei."""
    with open(output_file, "w") as fds:
        for mbs_object in objects:
            mbs_object.writeInputfile(fds)


def main(input_file, json_file, fds_file, search_objects=None):
    """Hauptfunktion für die Verarbeitung."""
    if search_objects is None:
        search_objects = ["RIGID_BODY", "CONSTRAINT"]

    # Datei einlesen
    file_content = read_file(input_file)

    # Objekte parsen
    list_of_mbs_objects = parse_file_content(file_content, search_objects)

    # In JSON speichern
    write_to_json(list_of_mbs_objects, json_file)

    # JSON lesen (optional)
    data = read_from_json(json_file)

    # In FDS speichern
    write_fds_file(list_of_mbs_objects, fds_file)

    print(f"Anzahl gefundener Objekte: {len(list_of_mbs_objects)}")


if __name__ == "__main__":
    # Dateipfade als Beispiel
    input_file = "Aufgabe_2/test.fdd"
    json_file = "Aufgabe_2/Ausgabe.json"
    fds_file = "Aufgabe_2/Ausgabe.fds"
    main(input_file, json_file, fds_file)
