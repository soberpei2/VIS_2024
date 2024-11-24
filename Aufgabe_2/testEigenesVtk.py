import vtk
import os

# Funktion zur Erstellung eines VTK-Actors aus einer OBJ-Datei
def create_actor_from_obj(file_path, position, color, transparency):
    """Erstellt einen VTK-Actor für eine OBJ-Geometrie."""
    reader = vtk.vtkOBJReader()
    reader.SetFileName(file_path)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPosition(*position)
    actor.GetProperty().SetColor(*color)  # RGB-Werte zwischen 0 und 1
    actor.GetProperty().SetOpacity(1 - transparency / 100.0)  # Transparenz
    return actor

# Funktion zur Erstellung eines Constraints als Linie
def create_constraint_actor(position1, position2):
    """Erstellt eine Linie, die zwei Punkte verbindet (Constraint)."""
    line_source = vtk.vtkLineSource()
    line_source.SetPoint1(*position1)
    line_source.SetPoint2(*position2)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(line_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Rot für Constraints
    actor.GetProperty().SetLineWidth(2.0)
    return actor

# Funktion zum Parsen der Eingabedatei
def parse_input_file(file_path):
    """Parst die Eingabedatei und gibt die Objekte als Liste zurück."""
    with open(file_path, "r") as file:
        lines = file.read().splitlines()

    objects = []
    current_block = []
    for line in lines:
        if line.strip() == "%":  # Block-Ende
            if current_block:
                objects.append(current_block)
            current_block = []
        else:
            current_block.append(line.strip())

    return objects

# Funktion zur Verarbeitung der Objekte
def process_objects(objects):
    """Verarbeitet die Objekte und trennt Rigid Bodies und Constraints."""
    rigid_bodies = []
    constraints = []

    for obj in objects:
        obj_type = obj[0].split()[0]  # Bestimme den Typ des Objekts (z. B. "rigidBody")
        if obj_type == "rigidBody":
            parameters = {}
            for line in obj[1:]:
                # Überspringe leere oder nicht relevante Zeilen
                if "=" not in line:
                    print(f"Überspringe ungültige Zeile: {line}")
                    continue
                try:
                    key, value = map(str.strip, line.split("=", 1))
                except ValueError:
                    print(f"Fehlerhafte Zeile: {line}")
                    continue

                # Verarbeite spezielle Schlüssel
                if key in ["position", "x_axis", "y_axis", "z_axis", "COG"]:
                    parameters[key] = [float(x) for x in value.split(",")]
                elif key == "color":
                    parameters[key] = [int(x) / 255.0 for x in value.split()]
                elif key == "transparency":
                    parameters[key] = int(value)
                else:
                    parameters[key] = value
            rigid_bodies.append(parameters)

        elif obj_type == "constraint":
            parameters = {}
            for line in obj[1:]:
                # Überspringe ungültige Zeilen
                if "=" not in line:
                    print(f"Überspringe ungültige Zeile: {line}")
                    continue
                try:
                    key, value = map(str.strip, line.split("=", 1))
                except ValueError:
                    print(f"Fehlerhafte Zeile: {line}")
                    continue

                if key in ["position", "x_axis", "y_axis", "z_axis"]:
                    parameters[key] = [float(x) for x in value.split(",")]
                elif key in ["dx", "dy", "dz", "ax", "ay", "az"]:
                    parameters[key] = value.lower() == "true"
                else:
                    parameters[key] = value
            constraints.append(parameters)

    return rigid_bodies, constraints


# Hauptfunktion zur Visualisierung
def visualize():
    """Visualisiert die Rigid Bodies und Constraints mit VTK."""
    # Eingabedatei und Geometrie definieren
    input_file = "test.fds"  # Beispiel-Eingabedatei
    obj_file = "quader.obj"  # Geometrie-Datei

    # Prüfen, ob die Dateien existieren
    if not os.path.exists(input_file):
        print(f"Eingabedatei {input_file} wurde nicht gefunden.")
        return
    if not os.path.exists(obj_file):
        print(f"OBJ-Datei {obj_file} wurde nicht gefunden.")
        return

    # Eingabedatei parsen und Objekte verarbeiten
    objects = parse_input_file(input_file)
    rigid_bodies, constraints = process_objects(objects)

    # VTK-Komponenten erstellen
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Rigid Bodies hinzufügen
    for body in rigid_bodies:
        actor = create_actor_from_obj(
            obj_file,
            position=body["position"],
            color=body["color"],
            transparency=body["transparency"]
        )
        renderer.AddActor(actor)

    # Constraints hinzufügen
    for constraint in constraints:
        position1 = constraint["position"]
        position2 = rigid_bodies[1]["position"] if len(rigid_bodies) > 1 else constraint["position"]
        actor = create_constraint_actor(position1, position2)
        renderer.AddActor(actor)

    # Hintergrundfarbe und Fenstergröße
    renderer.SetBackground(0.1, 0.2, 0.4)  # Dunkelblau
    render_window.SetSize(800, 600)

    # Interaktive Visualisierung starten
    render_window.Render()
    render_window_interactor.Start()

# Diese Funktion wird direkt in Python ausgeführt
if __name__ == "__main__":
    visualize()
