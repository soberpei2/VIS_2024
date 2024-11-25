import inputfilereader
import vtk

listOfObjects = inputfilereader.readInputFile("Aufgabe_2/test.fdd")

# VTK-Renderer erstellen
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)  # Dunkelblauer Hintergrund

# Geometrien zur Szene hinzufügen
for obj in listOfObjects:
    if isinstance(obj, inputfilereader.mbsObject.rigidBody):  # RigidBody-Objekte
        renderer.AddActor(obj.actor)
    elif isinstance(obj, inputfilereader.mbsObject.constraint):  # Constraint-Objekte
        renderer.AddActor(obj.actor)
        
        
# Koordinatensystem hinzufügen
axes = vtk.vtkAxesActor()
axes.SetTotalLength(2, 2, 2)    # Länge der Achsen (X, Y, Z)
axes.SetShaftTypeToCylinder()    # Darstellung der Achsen als Zylinder
axes.SetAxisLabels(1)            # Achsenbeschriftungen anzeigen (X, Y, Z)

renderer.AddActor(axes)

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