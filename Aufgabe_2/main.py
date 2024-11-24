# Importieren benötigter Klassen
import inputFileReader as ifr
import vtk

# Definieren des einzulesenden Files
file = "C:/Users/Startklar/OneDrive/Desktop/10_Studium/02_Master/03_Semester/Visualisierung_Datenaufbereitung/02_Aufgabe/test.fdd"

# Aufrufen des Inputfilereaders
listOfMbsObjects = ifr.inputFileReader(file)

#=======================================================================
# Visualisieren eines OBJ-Files
#=======================================================================

# Erzeugen eines obj-Readers
bodyReader = vtk.vtkOBJReader()

# Erzeugen einer Quelle
bodyReader.SetFileName(listOfMbsObjects[0].parameter["geometry"]["value"])
bodyReader.Update()
body = bodyReader.GetOutputPort()

# Erzeugen eines Filters mit dem Eingang body
bodyMapper = vtk.vtkPolyDataMapper()
bodyMapper.SetInputConnection(body)

# Erzeugen eines Aktors (Filter als Eingang)
bodyActor = vtk.vtkActor()
bodyActor.SetMapper(bodyMapper)

#Position des Aktors lt. fdd-File vorgeben
bodyActor.SetPosition(listOfMbsObjects[0].parameter["position"]["value"])

# Koordinatensystem erstellen
axes = vtk.vtkAxesActor()
axes.SetTotalLength(10, 10, 10)  # Länge der Achsen (X, Y, Z)
axes.SetShaftTypeToCylinder()    # Achsentyp (Linien, Zylinder, usw.)
axes.SetAxisLabels(True)         # Achsenbeschriftungen einblenden

# Zeichnen des Bildes
ren1 = vtk.vtkRenderer()
ren1.AddActor(bodyActor)
ren1.AddActor(axes)
ren1.SetBackground(0.1, 0.2, 0.4)

# Definieren einer Leinwand
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)
renWin.Render()

# Interaktionseinstellungen
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Start()