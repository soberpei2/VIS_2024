import vtk

# Erstelle eine Kugelquelle (SphereSource)
sphere = vtk.vtkSphereSource()
sphere.SetRadius(1.0)  # Setze den Radius der Kugel
sphere.SetThetaResolution(10)  # Auflösung für die Theta-Achse (Azimutalwinkel)
sphere.SetPhiResolution(10)  # Auflösung für die Phi-Achse (Polarwinkel)

# Erstelle einen Mapper und setze die Kugelquelle als Eingabe
sphereMapper = vtk.vtkPolyDataMapper()
sphereMapper.SetInputConnection(sphere.GetOutputPort())

# Erstelle einen Actor und setze den Mapper
sphereActor = vtk.vtkActor()
sphereActor.SetMapper(sphereMapper)

# Farbe der Kugel auf Orange setzen
sphereActor.GetProperty().SetColor(1.0, 0.647, 0.0)  # RGB für Orange

# Transparenz der Kugel setzen (halbtransparent)
sphereActor.GetProperty().SetOpacity(0.5)  # Transparenz von 0 (unsichtbar) bis 1 (vollständig sichtbar)

# Setze Drahtgitter-Darstellung
sphereActor.GetProperty().SetRepresentationToWireframe()  # Drahtgitterdarstellung

# Setze die Linienstärke des Drahtgitters (dicker machen)
sphereActor.GetProperty().SetLineWidth(3.0)  # Erhöhe die Linienstärke auf 3.0 (standardmäßig 1.0)

# Erstelle einen Renderer, füge den Actor hinzu und setze die Hintergrundfarbe
ren1 = vtk.vtkRenderer()
ren1.AddActor(sphereActor)
ren1.SetBackground(0.1, 0.2, 0.4)  # RGB-Werte für Hintergrundfarbe

# Erstelle ein Renderfenster und füge den Renderer hinzu
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)  # Setze die Fenstergröße

# Erstelle einen Interactor und verbinde ihn mit dem Renderfenster
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Initialisiere den Interactor (wichtig für die Interaktion)
iren.Initialize()

# Render das Fenster und rotiere die Kamera
for i in range(360):
    renWin.Render()
    ren1.GetActiveCamera().Azimuth(1)  # Drehe die Kamera um 1 Grad pro Schritt

# Starte die Interaktion
iren.Start()