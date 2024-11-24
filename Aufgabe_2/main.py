# Importieren benötigter Klassen
import inputFileReader as ifr
import vtk
import mbsObject as MBS

# Definieren des einzulesenden Files
file = "C:/Users/Startklar/OneDrive/Desktop/10_Studium/02_Master/03_Semester/Visualisierung_Datenaufbereitung/02_Aufgabe/test.fdd"

# Aufrufen des Inputfilereaders
listOfMbsObjects = ifr.inputFileReader(file)

#=======================================================================
# Visualisieren eines OBJ-Files
#=======================================================================

# Liste der Aktoren initialisieren
listOfActors = []

# Schleife über die Liste der Mbs-Objekte
for mbsObject in listOfMbsObjects:
    # Fertigen Aktor der Aktorliste hinzufügen
    listOfActors.append(mbsObject.getActor(mbsObject))

# Koordinatensystem erstellen
axes = vtk.vtkAxesActor()
axes.SetTotalLength(10, 10, 10)  # Länge der Achsen (X, Y, Z)
axes.SetShaftTypeToCylinder()    # Achsentyp (Linien, Zylinder, usw.)
axes.SetAxisLabels(True)         # Achsenbeschriftungen einblenden

# Zeichnen des Bildes
ren1 = vtk.vtkRenderer()
ren1.AddActor(listOfActors[0])
ren1.AddActor(listOfActors[1])
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