import vtk
import os
import numpy as np
import math


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


# Funktion zur Darstellung der Schwerkraft als Pfeil
def create_gravity_actor(vector):
    """Erstellt einen Pfeil für die Schwerkraft."""
    
    
    arrow_source = vtk.vtkArrowSource()

    vectorNormalized = vector / np.linalg.norm(vector)  #Vektor normieren
    direction = [1, 0, 0]

    if np.array_equal(direction,vectorNormalized):
        rotationvector = [0,1,0]
        angle = 0
    elif np.array_equal(direction,-vectorNormalized):
        rotationvector = [0,1,0]
        angle = 180
    else:
        rotationvector = np.cross(direction,vectorNormalized)
        angle = np.degrees(np.acos(np.dot(direction,vectorNormalized)))





    # Transformiere den Pfeil basierend auf Richtung und Größe
    transform = vtk.vtkTransform()
    position = [0,0,0]
    transform.Translate(position)
    transform.RotateWXYZ(angle,rotationvector[0],rotationvector[1],rotationvector[2])
    scale_factor = np.linalg.norm(vector) / 1000.0  # Skaliere den Pfeil relativ zur Stärke
    transform.Scale(scale_factor, scale_factor, scale_factor)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(arrow_source.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetUserTransform(transform)
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.0, 0.0, 0.0)  # schwarz für Schwerkraft
    return actor


# Funktion zur Erstellung eines Koordinatensystems
def create_axes_actor():
    """Erstellt ein Koordinatensystem mit X-, Y- und Z-Achsen."""
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(10, 10, 10)  # Länge der Achsen
    axes.GetXAxisCaptionActor2D().GetTextActor().GetTextProperty().SetColor(1, 0, 0)  # Rot
    axes.GetYAxisCaptionActor2D().GetTextActor().GetTextProperty().SetColor(0, 1, 0)  # Grün
    axes.GetZAxisCaptionActor2D().GetTextActor().GetTextProperty().SetColor(0, 0, 1)  # Blau
    return axes


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
    """Verarbeitet die Objekte und trennt Rigid Bodies, Constraints und Forces."""
    rigid_bodies = []
    constraints = []
    forces = []

    for obj in objects:
        obj_type = obj[0].split()[0]  # Bestimme den Typ des Objekts (z. B. "rigidBody")
        parameters = {}
        for line in obj[1:]:
            if "=" not in line:
                continue
            key, value = map(str.strip, line.split("=", 1))
            if key in ["position", "x_axis", "y_axis", "z_axis", "COG", "direction"]:
                parameters[key] = [float(x) for x in value.split(",")]
            elif key == "magnitude":
                parameters[key] = float(value)
            elif key == "color":
                parameters[key] = [int(x) / 255.0 for x in value.split()]
            elif key == "transparency":
                parameters[key] = int(value)
            elif key == "gravity_vector":
                parameters[key] = [float(x) for x in value.split(",")]
            else:
                parameters[key] = value

        if obj_type == "rigidBody":
            rigid_bodies.append(parameters)
        elif obj_type == "constraint":
            constraints.append(parameters)
        elif obj_type == "force":
            forces.append(parameters)

    return rigid_bodies, constraints, forces


# Hauptfunktion zur Visualisierung
def visualize():
    """Visualisiert die Rigid Bodies, Constraints, Kräfte und ein Koordinatensystem mit VTK."""
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
    rigid_bodies, constraints, forces = process_objects(objects)

    # VTK-Komponenten erstellen
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Koordinatensystem hinzufügen
    axes_actor = create_axes_actor()
    renderer.AddActor(axes_actor)

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

    # Forces (Schwerkraft) hinzufügen
    for force in forces:

        vector = force["gravity_vector"]
        actor = create_gravity_actor(vector)
        renderer.AddActor(actor)
    
    
    # Hintergrundfarbe und Fenstergröße
    renderer.SetBackground(0.1, 0.2, 0.4)  # Dunkelblau
    render_window.SetSize(800, 600)

    # Interaktive Visualisierung starten
    render_window.Render()
    render_window_interactor.Start()


if __name__ == "__main__":
    visualize()
