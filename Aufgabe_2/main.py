# Importieren benötigter Klassen
import inputFileReader as ifr
import vtk
import mbsObject as MBS
import mbsModel

# Definieren des einzulesenden Files
file = "C:/Users/Startklar/OneDrive/Desktop/10_Studium/02_Master/03_Semester/Visualisierung_Datenaufbereitung/02_Aufgabe/test_2.fdd"

# Anlegen eines Objekts vom Typ mbsModel
model = mbsModel.mbsModel(ifr.inputFileReader(file))

#=======================================================================
# Visualisieren eines OBJ-Files
#=======================================================================

# Liste der Aktoren initialisieren
listOfActors = []

# Schleife über die Liste der Mbs-Objekte
for mbsObject in model.listOfMbsObjects:
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
ren1.SetBackground(0.255, 0.255, 0.255)

# Definieren einer Leinwand
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(1000, 1000)
renWin.Render()

# Interaktionseinstellungen
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Start()

#=======================================================================
# Anzeigen der Properties aller mbs-Objekte
#=======================================================================

# Schleife über die Liste der Mbs-Objekte
for mbsObject in model.listOfMbsObjects:
    mbsObject.showProps()
