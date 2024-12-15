import sys
from pathlib import Path

import vtk

import mbsModel


if len(sys.argv) < 2:
    sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

myModel = mbsModel.mbsModel()

#read fdd file path from input arguments
fdd_path = Path(sys.argv[1])
myModel.importFddFile(fdd_path)
#create path for solver input file (fds)
fds_path = fdd_path.with_suffix(".fds")
myModel.exportFdsFile(fds_path)
#create path for model database file (json)
json_path = fdd_path.with_suffix(".json")
myModel.saveJsonFile(json_path)

#create new model and load json generated above
#(content should be the same)
newModel = mbsModel.mbsModel()
newModel.loadJsonFile(json_path)

#visualization part
#-----------------------------------------------------------------------------
renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetWindowName('pyFreeDyn')
renWin.SetSize(1024,768)

# Interactor einrichten
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Modell anzeigen
newModel.showModel(renderer)

# Render- und Interaktionsloop starten
renWin.Render()
interactor.Start()
#-----------------------------------------------------------------------------
