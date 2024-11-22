import inputfilereader
import vtk

listOfMyObjects = inputfilereader.readInput4Output("inputfilereader/test.fdd","inputfilereader/test1.json","inputfilereader/test1.fds")

# VTK-Renderer erstellen
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)  # Dunkelblauer Hintergrund

# Geometrien zur Szene hinzufügen
for obj in listOfMyObjects:
    if isinstance(obj, inputfilereader.mbsObject.rigidBody):  # Nur RigidBody-Objekte
        renderer.AddActor(obj.actor)

# Render-Fenster einrichten
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(800, 600)

# Interactor erstellen
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Interactor-Style festlegen
interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
renderWindowInteractor.SetInteractorStyle(interactorStyle)

# Szene rendern und Interaktion starten
renderWindow.Render()
print("Starte interaktive Visualisierung.")
renderWindowInteractor.Start()