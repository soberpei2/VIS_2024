import os

# Importieren der mbsObject-Klassen (RigidBody, Constraint, Force, Torque)
from mbsObject import rigidBody, Constraint, GenericForce, GenericTorque

def parse_input_file(file_path):
    """
    Liest die Eingabedatei und erstellt entsprechende MBS-Objekte.
    
    Parameters:
    file_path (str): Der Pfad zur Eingabedatei, die verarbeitet werden soll.

    Returns:
    dict: Ein Dictionary, das alle erstellten MBS-Objekte enthält, 
          kategorisiert nach dem Objekttyp (z.B. 'rigidBodies', 'constraints', etc.)
    """
    # Initialisieren der Container für unterschiedliche Objekte
    rigid_bodies = []
    constraints = []
    forces = []
    torques = []
    parameters = {}
    measures = []
    
    # Öffnen der Eingabedatei und Lesen des Inhalts
    try:
        with open("inputfilereader/test.fdd", 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Die Datei {file_path} konnte nicht gefunden werden.")
    
    # Variablen zur Identifizierung von Blöcken
    current_block = None
    block_data = []
    
    # Verarbeiten der Zeilen in der Eingabedatei
    for line in lines:
        line = line.strip()  # Entfernen von führenden und nachgestellten Leerzeichen
        
        # Leerzeilen überspringen
        if not line:
            continue
        
        # Identifikation von Blockbeginn (z.B. $RIGID_BODY, $CONSTRAINT)
        if line.startswith("$"):
            # Falls bereits ein Block verarbeitet wird, füge diesen zum entsprechenden Container hinzu
            if current_block:
                if current_block == "$RIGID_BODY":
                    rigid_bodies.append(rigidBody(block_data))
                elif current_block == "$CONSTRAINT":
                    constraints.append(Constraint(block_data))
                elif current_block == "$FORCE_GenericForce":
                    forces.append(GenericForce(block_data))
                elif current_block == "$FORCE_GenericTorque":
                    torques.append(GenericTorque(block_data))
                elif current_block == "$MEASURE":
                    measures.append(block_data)
                elif current_block == "$DATAOBJECT_PARAMETER":
                    parameters[block_data[0].split(":")[1].strip()] = float(block_data[1].split(":")[1].strip())
                
            # Neuer Block beginnt
            current_block = line
            block_data = []  # Leere die Daten des vorherigen Blocks
        
        # Hinzufügen der aktuellen Zeile zum Block
        else:
            block_data.append(line)
    
    # Falls noch Daten für den letzten Block übrig sind, diesen verarbeiten
    if current_block:
        if current_block == "$RIGID_BODY":
            rigid_bodies.append(rigidBody(block_data))
        elif current_block == "$CONSTRAINT":
            constraints.append(Constraint(block_data))
        elif current_block == "$FORCE_GenericForce":
            forces.append(GenericForce(block_data))
        elif current_block == "$FORCE_GenericTorque":
            torques.append(GenericTorque(block_data))
        elif current_block == "$MEASURE":
            measures.append(block_data)
        elif current_block == "$DATAOBJECT_PARAMETER":
            parameters[block_data[0].split(":")[1].strip()] = float(block_data[1].split(":")[1].strip())

    # Rückgabe der erstellten Objekte und Parameter
    return {
        'rigidBodies': rigid_bodies,
        'constraints': constraints,
        'forces': forces,
        'torques': torques,
        'parameters': parameters,
        'measures': measures
    }

def save_to_json(data, output_file):
    """
    Speichert die Daten als JSON-Datei.
    
    Parameters:
    data (dict): Die Daten, die gespeichert werden sollen.
    output_file (str): Der Pfad zur Ausgabedatei, in der die Daten gespeichert werden sollen.
    """
    import json
    
    # Speichern der Daten als JSON-Datei
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        raise Exception(f"Fehler beim Speichern der Datei: {e}")

def write_input_file(file_path, rigid_bodies, constraints, forces, torques, parameters, measures):
    """
    Schreibt die MBS-Objekte in eine Eingabedatei im ursprünglichen Format zurück.
    
    Parameters:
    file_path (str): Der Pfad zur Eingabedatei.
    rigid_bodies (list): Liste von RigidBody-Objekten.
    constraints (list): Liste von Constraint-Objekten.
    forces (list): Liste von Force-Objekten.
    torques (list): Liste von Torque-Objekten.
    parameters (dict): Dictionary von Parametern.
    measures (list): Liste von Measure-Objekten.
    """
    try:
        with open(file_path, 'w') as file:
            # Schreibe die RigidBodies
            for body in rigid_bodies:
                file.write(f"$RIGID_BODY:\n")
                file.write(f"  name: {body.get_name()}\n")
                file.write(f"  geometry: {body.geometry}\n")
                file.write(f"  position: {', '.join(map(str, body.position))}\n")
                file.write(f"  x_axis: {', '.join(map(str, body.x_axis))}\n")
                file.write(f"  y_axis: {', '.join(map(str, body.y_axis))}\n")
                file.write(f"  z_axis: {', '.join(map(str, body.z_axis))}\n")
                file.write(f"  color: {' '.join(map(str, body.color))}\n")
                file.write(f"  transparency: {body.transparency}\n")
                file.write(f"  initial velocity: {', '.join(map(str, body.initial_velocity))}\n")
                file.write(f"  initial omega: {', '.join(map(str, body.initial_omega))}\n")
                file.write(f"  mass: {body.mass}\n")
                file.write(f"  COG: {', '.join(map(str, body.COG))}\n")
                file.write(f"  inertia: {', '.join(map(str, body.inertia))}\n")
                file.write(f"  i1_axis: {', '.join(map(str, body.i_axes['i1']))}\n")
                file.write(f"  i2_axis: {', '.join(map(str, body.i_axes['i2']))}\n")
                file.write(f"  i3_axis: {', '.join(map(str, body.i_axes['i3']))}\n")
            
            # Schreibe die Constraints
            for constraint in constraints:
                file.write(f"$CONSTRAINT:\n")
                file.write(f"  name: {constraint.get_name()}\n")
                file.write(f"  body1: {constraint.body1}\n")
                file.write(f"  body2: {constraint.body2}\n")
                file.write(f"  dx: {constraint.dx}\n")
                file.write(f"  dy: {constraint.dy}\n")
                file.write(f"  dz: {constraint.dz}\n")
                file.write(f"  ax: {constraint.ax}\n")
                file.write(f"  ay: {constraint.ay}\n")
                file.write(f"  az: {constraint.az}\n")
                file.write(f"  position: {', '.join(map(str, constraint.position))}\n")
                file.write(f"  x_axis: {', '.join(map(str, constraint.x_axis))}\n")
                file.write(f"  y_axis: {', '.join(map(str, constraint.y_axis))}\n")
                file.write(f"  z_axis: {', '.join(map(str, constraint.z_axis))}\n")
            
            # Schreibe die Kräfte und Drehmomente
            for force in forces:
                file.write(f"$FORCE_GenericForce:\n")
                file.write(f"  name: {force.get_name()}\n")
                file.write(f"  body1: {force.body1}\n")
                file.write(f"  body2: {force.body2}\n")
                file.write(f"  PointOfApplication_Body1: {', '.join(map(str, force.PointOfApplication_Body1))}\n")
                file.write(f"  PointOfApplication_Body2: {', '.join(map(str, force.PointOfApplication_Body2))}\n")
                file.write(f"  mode: {force.mode}\n")
                file.write(f"  direction: {', '.join(map(str, force.direction))}\n")
                file.write(f"  ForceExpression: {force.ForceExpression}\n")
            
            for torque in torques:
                file.write(f"$FORCE_GenericTorque:\n")
                file.write(f"  name: {torque.get_name()}\n")
                file.write(f"  body1: {torque.body1}\n")
                file.write(f"  body2: {torque.body2}\n")
                file.write(f"  mode: {torque.mode}\n")
                file.write(f"  direction: {', '.join(map(str, torque.direction))}\n")
            
            # Schreibe die Parameter
            for param, value in parameters.items():
                file.write(f"$DATAOBJECT_PARAMETER:\n")
                file.write(f"  name: {param}\n")
                file.write(f"  InitialValue: {value}\n")
            
            # Schreibe die Messgrößen
            for measure in measures:
                file.write(f"$MEASURE:\n")
                file.write(f"  name: {measure[0].split(':')[1].strip()}\n")
                # Weitere Parameter von Measures (falls erforderlich) hinzufügen...
            
    except Exception as e:
        raise Exception(f"Fehler beim Schreiben der Eingabedatei: {e}")
