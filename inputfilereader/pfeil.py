import vtk
import numpy as np

# Vektoren definieren (als Liste von Vektoren)
vectors = [
    [0, 0, 1],  # Vektor 1
    [1, 0, 0],  # Vektor 2
    [0, 1, 0]   # Vektor 3
]

# Farben für die Vektoren
colors = [
    [1, 0, 0],  # Rot
    [0, 1, 0],  # Grün
    [0, 0, 1]   # Blau
]

# Renderer, RenderWindow und Interactor einrichten
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Schleife für die Vektoren
for i, vector in enumerate(vectors):
    # Erstelle Linie für jeden Vektor
    line = vtk.vtkLineSource()
    line.SetPoint1(0, 0, 0)  # Startpunkt
    line.SetPoint2(vector[0], vector[1], vector[2])  # Endpunkt

    # Mapper für die Linie
    line_mapper = vtk.vtkPolyDataMapper()
    line_mapper.SetInputConnection(line.GetOutputPort())

    # Actor für die Linie
    line_actor = vtk.vtkActor()
    line_actor.SetMapper(line_mapper)
    line_actor.GetProperty().SetColor(colors[i])  # Setze die Farbe aus der Liste

    # Linie zum Renderer hinzufügen
    renderer.AddActor(line_actor)

    # Erstelle Pfeil (ArrowSource)
    arrow_source = vtk.vtkArrowSource()

    # Setze die Parameter für Schaft und Spitze des Pfeils
    arrow_source.SetShaftRadius(0.05)   # Radius des Schaftes
    arrow_source.SetTipRadius(0.1)      # Radius der Spitze
    arrow_source.SetTipLength(0.35)     # Länge der Spitze

    # Berechne die Richtung des Vektors (Normierung)
    vector_length = np.linalg.norm(vector)
    if vector_length == 0:
        continue  # Falls der Vektor die Länge 0 hat, überspringen

    # Normalisiere den Vektor (damit der Pfeil korrekt zeigt)
    normalized_vector = np.array(vector) / vector_length

    # Berechne die Drehachse und den Winkel
    z_axis = np.array([0, 0, 1])  # Die Z-Achse (die Standardausrichtung des Pfeils)
    cross_product = np.cross(z_axis, normalized_vector)  # Kreuzprodukt für Drehachse
    dot_product = np.dot(z_axis, normalized_vector)  # Skalarprodukt für den Winkel
    rotation_angle = np.arccos(dot_product)  # Winkel zwischen den Vektoren

    # Erstelle eine Rotationstransformation
    transform = vtk.vtkTransform()
    transform.RotateWXYZ(np.degrees(rotation_angle), cross_product[0], cross_product[1], cross_product[2])  # Rotieren

    # Erstelle einen Transform-Filter, um die Transformation anzuwenden
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetInputConnection(arrow_source.GetOutputPort())
    transform_filter.SetTransform(transform)

    # Mapper für den Pfeil
    arrow_mapper = vtk.vtkPolyDataMapper()
    arrow_mapper.SetInputConnection(transform_filter.GetOutputPort())

    # Actor für den Pfeil
    arrow_actor = vtk.vtkActor()
    arrow_actor.SetMapper(arrow_mapper)
    arrow_actor.GetProperty().SetColor(colors[i])  # Setze die Farbe aus der Liste

    # Setze die Position des Pfeils (startet bei [0, 0, 0])
    arrow_actor.SetPosition(vector[0], vector[1], vector[2])  # Verschiebe den Pfeil zum Endpunkt des Vektors

    # Pfeil zum Renderer hinzufügen
    renderer.AddActor(arrow_actor)

    
# Setze Hintergrundfarbe
renderer.SetBackground(0.1, 0.1, 0.1)

# Starte den Rendering-Prozess
renderWindow.Render()
renderWindowInteractor.Start()







