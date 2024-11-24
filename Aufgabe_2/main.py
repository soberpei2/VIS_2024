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
listOfActors.append(axes)        # Hinzufügen zur Aktorliste

# Zeichnen des Bildes
ren1 = vtk.vtkRenderer()
for Actor in listOfActors:
    ren1.AddActor(Actor)
ren1.SetBackground(0.1, 0.2, 0.4)

# Definieren einer Leinwand
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(1000, 1000)
renWin.Render()

# Interaktionseinstellungen
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Start()

# Anzeigen der Properties eines mbs-Objekts
listOfMbsObjects[0].showProps()
