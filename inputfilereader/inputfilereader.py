import mbsObject
import json

def import_fdd_file(file_path):
    """
    Importiert eine .fdd-Datei und analysiert deren Inhalt, um MBS-Objekte zu erstellen.
    
    Args:
        file_path (str): Pfad zur .fdd-Datei.
    
    Returns:
        list: Liste von MBS-Objekten.
    """
    with open(file_path, "r") as f:
        file_content = f.read().splitlines()

    # Suchbegriffe
    search_objects = ["$RIGID_BODY", "$CONSTRAINT", "$MOTION", "$FORCE", "$MEASURE"]
    search_subtypes = ["GenericForce", "GenericTorque"]

    # Initialisierung
    current_block_type = ""
    current_block_subtype = ""
    current_text_block = []
    list_of_mbs_objects = []

    # Datei parsen
    for line in file_content:
        # Wenn neuer Block beginnt
        if any(line.startswith(obj) for obj in search_objects):
            # Vorherigen Block verarbeiten (falls vorhanden)
            if current_block_type:
                list_of_mbs_objects.append(process_block(current_block_type, current_text_block))
                current_text_block = []

            # Neuen Block starten
            current_block_type = next(obj for obj in search_objects if line.startswith(obj))
            current_text_block = [line]  # Ersten Blockinhalt hinzufügen
        else:
            # Blockinhalt sammeln
            current_text_block.append(line)

    # Letzten Block verarbeiten
    if current_block_type:
        list_of_mbs_objects.append(process_block(current_block_type, current_text_block))

    return list_of_mbs_objects


def process_block(block_type, block_content):
    """
    Erstellt ein MBS-Objekt basierend auf dem Blocktyp und Blockinhalt.
    
    Args:
        block_type (str): Typ des Blocks (z. B. "$RIGID_BODY").
        block_content (list): Inhalt des Blocks.
    
    Returns:
        object: Ein MBS-Objekt.
    """
    # Blocktyp zu Klassenerstellung mappen
    if block_type == "$RIGID_BODY":
        return mbsObject.rigidBody(block_content)
    elif block_type == "$CONSTRAINT":
        return mbsObject.constraint(block_content)
    elif block_type == "$MOTION":
        return mbsObject.motion(block_content)
    elif block_type == "$FORCE":
        return mbsObject.force(block_content)
    elif block_type == "$MEASURE":
        return mbsObject.measure(block_content)
    else:
        raise ValueError(f"Unbekannter Blocktyp: {block_type}")


def write_fds(list_of_mbs_objects, fds_path):
    """
    Exportiert MBS-Objekte in eine .fds-Datei.
    
    Args:
        list_of_mbs_objects (list): Liste von MBS-Objekten.
        fds_path (str): Zielpfad der .fds-Datei.
    """
    with open(fds_path, "w") as fds_file:
        for mbs_object in list_of_mbs_objects:
            mbs_object.writeInputfile(fds_file)


def export_to_json(list_of_mbs_objects, output_path):
    """
    Exportiert MBS-Objekte als JSON-Datei.
    
    Args:
        list_of_mbs_objects (list): Liste von MBS-Objekten.
        output_path (str): Zielpfad der JSON-Datei.
    """
    model_objects = [obj.parameter for obj in list_of_mbs_objects]
    json_data = json.dumps({"modelObjects": model_objects}, indent=4)
    with open(output_path, "w") as outfile:
        outfile.write(json_data)


def import_from_json(input_path):
    """
    Liest eine JSON-Datei ein und gibt die Inhalte zurück.
    
    Args:
        input_path (str): Pfad zur JSON-Datei.
    
    Returns:
        dict: Geladene JSON-Daten.
    """
    with open(input_path, "r") as f:
        data = json.load(f)
    return data


