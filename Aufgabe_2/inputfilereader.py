import os
import json
import mbsObject

# Diese Funktion liest die Datei und extrahiert die Modelle
def process_input_file(input_file):
    with open(input_file, "r") as file:
        lines = file.read().splitlines()
    
    num_of_objects = 0
    current_block_type = ""
    current_text_block = []
    model_objects = []
    
    # Schlüsselwörter, nach denen wir suchen werden
    object_types = ["RIGID_BODY", "CONSTRAINT", "FORCE_GenericForce", "FORCE_GenericTorque", "MEASURE1", "MEASURE2", "SETTINGS"]

    for line in lines:
        # Wenn ein neuer Block gefunden wird
        if "$" in line:
            if current_block_type:
                # Zuordnen des aktuellen Blocks zu einem bestimmten Objekt
                if current_block_type == "RIGID_BODY":
                    model_objects.append(mo.RigidBody(current_text_block))
                elif current_block_type == "CONSTRAINT":
                    model_objects.append(mo.Constraint(current_text_block))
                elif current_block_type == "FORCE_GenericForce":
                    model_objects.append(mo.GenericForce(current_text_block))
                elif current_block_type == "FORCE_GenericTorque":
                    model_objects.append(mo.GenericTorque(current_text_block))
                elif current_block_type == "MEASURE1":
                    model_objects.append(mo.Measure1(current_text_block))
                elif current_block_type == "MEASURE2":
                    model_objects.append(mo.Measure2(current_text_block))
                elif current_block_type == "SETTINGS":
                    model_objects.append(mo.Gravity(current_text_block))

            current_block_type = ""
        
        # Identifizierung des aktuellen Blocktyps
        for obj_type in object_types:
            if obj_type in line:
                current_block_type = obj_type
                current_text_block.clear()
                break

        current_text_block.append(line)
    
    # Ausgabe der Modelle als JSON
    model_data = [{"parameter": obj.parameter} for obj in model_objects]
    with open("output_data.json", "w") as outfile:
        json.dump({"modelObjects": model_data}, outfile)
    
    # Speichern der Modelle in einer neuen Datei
    with open("output_file.fds", "w") as fds:
        for obj in model_objects:
            obj.write_input_file(fds)

    # Optional: Ausgabe im TXT-Format
    with open("output_file.txt", "w") as txt:
        for obj in model_objects:
            obj.write_input_file(txt)

    print(f"Verarbeitete {len(model_objects)} Objekte.")

# Aufruf der Funktion, um die Eingabedatei zu verarbeiten
input_file = "path/to/your/input_file.fdd"  # Beispielpfad
process_input_file(input_file)
