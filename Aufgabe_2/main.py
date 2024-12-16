import mbsModel
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

#if len(sys.argv) < 2:
#    sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

myModel = mbsModel.mbsModel()

#read fdd file path from input arguments
#fdd_path = Path(sys.argv[1])
# Fester Pfad zur fdd-Datei
fdd_path = Path(r"C:\Users\hanne\Documents\SynologyDrive\Uni\01 Master\3 Semester\Datenaufbereitung und Visualisierung\UE\VIS_2024\VIS_2024\Aufgabe_2\test.fdd")
if not fdd_path.exists():
    sys.exit(f"FDD file not found at the specified path: {fdd_path}")
    
myModel.importFddFile(fdd_path)
#create path for solver input file (fds)
fds_path = fdd_path.with_suffix(".fds")
myModel.exportFdsFile(fds_path)
#create path for model database file (json)
json_path = fdd_path.with_suffix(".json")
myModel.saveDatabase(json_path)

#create new model and load json generated above
#(content should be the same)
newModel = mbsModel.mbsModel()
newModel.loadDatabase(json_path)

#visualization part
#-----------------------------------------------------------------------------
renderer = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetWindowName('pyFreeDyn')
renWin.SetSize(1024,768)

# Interactor einrichten
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)

style = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Modell anzeigen
newModel.showModel(renderer)

# Render- und Interaktionsloop starten
renWin.Render()
interactor.Start()
#-----------------------------------------------------------------------------