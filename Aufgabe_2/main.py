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

listOfMbsObjects[0].showMbsObject(body)