import mbsObject
import vtk
import inputfilereader
#-----------------------------------------------------------------------------------
#Überprüfen inputfilereader2
# Lesen der File und Ausgabe einer Liste der Objekte, einer Json Datei 
listOfObjects2 = inputfilereader.saveToJson("inputfilereader/test.fdd","inputfilereader/test.json")
# Lesen der File und Ausgabe einer Liste der Objekte, einer Fds Datei 
listOfObjects = inputfilereader.saveToFds("inputfilereader/test.fdd","inputfilereader/test.fds")
# Überprüfen ob die Funktion funktioniert

print("Wie viele Obejkte/ Körper wurden gefunden:",len(listOfObjects2))
print("Wie viele Obejkte/ Körper wurden gefunden:",len(listOfObjects))


# VTK-Renderer erstellen
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.1, 0.2)  # Dunkelblauer Hintergrund

# Geometrien zur Szene hinzufügen
for obj in listOfObjects:
    if isinstance(obj, inputfilereader.mbsObject.rigidBody):  # RigidBody-Objekte
        renderer.AddActor(obj.actor)
    elif isinstance(obj, inputfilereader.mbsObject.constraint):  # Constraint-Objekte
        renderer.AddActor(obj.actor)
        renderer.AddActor(obj.text_actor)
    elif isinstance(obj, inputfilereader.mbsObject.settings):  # Settings-Objekt (einschließlich Gravitationsvektor)
        renderer.AddActor(obj.actor)
        renderer.AddActor(obj.text_actor)
    elif isinstance(obj, inputfilereader.mbsObject.force): 
        renderer.AddActor(obj.actor)
        renderer.AddActor(obj.actor1)  # Erste Kugel
        renderer.AddActor(obj.actor2)  # Zweite Kugel
        renderer.AddActor(obj.text_actor)
        renderer.AddActor(obj.text_actor1)
        renderer.AddActor(obj.text_actor2)
        renderer.AddActor(obj.direction_line_actor)



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
