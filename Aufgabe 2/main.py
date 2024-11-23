import inputfilereader as ifr
import vtk

# Freedyn File lesen
fdd_file_path = "Aufgabe 2/test.fdd"
listOfMbsObjects = ifr.read_fdd_file(fdd_file_path)

# Daten in JSON speichern
json_file_path = "Aufgabe 2/test.json"
ifr.write_json_file(listOfMbsObjects, json_file_path)

# JSON lesen
data = ifr.read_json_file(json_file_path)

# Daten in .fds-Datei schreiben
fds_file_path = "Aufgabe 2/test.fds"
ifr.write_fds_file(listOfMbsObjects, fds_file_path)

#---------------------------------------------------------------------

#Koordinatensystem anzeigen
axes = vtk.vtkAxesActor()
axes.SetTotalLength(20, 20, 20)  # Längen der Achsen auf 1 setzen


# Initialisiere VTK Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(axes)
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)
#render_window.SetFullScreen(True) #ACHTUNG hier kommt man mit q wieder raus
render_interactor = vtk.vtkRenderWindowInteractor()
render_interactor.SetRenderWindow(render_window)

for obj in listOfMbsObjects:
    print(obj)
    print(type(obj))

# Zeige gewünschte Objekte an
for obj in listOfMbsObjects:
    #rigidBodies
    if isinstance(obj,ifr.mbsObject.rigidBody):
        obj.show(renderer)
    #constraints
    if isinstance(obj,ifr.mbsObject.constraint):
        obj.show(renderer)

# Starte die Visualisierung
render_window.Render()
render_interactor.Start()