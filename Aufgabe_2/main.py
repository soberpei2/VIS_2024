# Importieren benötigter Klassen
import inputFileReader as ifr
import vtk

# Definieren des einzulesenden Files
file = "Aufgabe_2/test.fdd"

# Aufrufen des Inputfilereaders
ifr.inputFileReader(file)

#=======================================================================
# Visualisieren eines OBJ-Files
#=======================================================================

# Erzeugen eines obj-Readers
bodyReader = vtk.vtkOBJReader()

# Erzeugen einer Quelle
bodyReader.SetFileName("C:/Users/Startklar/OneDrive/Desktop/10_Studium/02_Master/03_Semester/Visualisierung_Datenaufbereitung/02_Aufgabe/quader.obj")
bodyReader.Update()
body = bodyReader.GetOutputPort()


# Erzeugen eines Filters mit dem Eingang body
bodyMapper = vtk.vtkPolyDataMapper()
bodyMapper.SetInputConnection(body)

# Erzeugen eines Aktors (Filter als Eingang)
bodyActor = vtk.vtkActor()
bodyActor.SetMapper(bodyMapper)

# Zeichnen des Bildes
ren1 = vtk.vtkRenderer()
ren1.AddActor(bodyActor)
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