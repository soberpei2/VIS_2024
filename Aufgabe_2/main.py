import mbsModel
import sys
from pathlib import Path

if len(sys.argv) < 2:
    sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")    

myModel = mbsModel.mbsModel()

#read fdd file path from input arguments
fdd_path = Path(sys.argv[1])
myModel.importFddFile(fdd_path)
#create path for solver input file (fds)
fds_path = fdd_path.with_suffix(".fds")
myModel.exportFdsFile(fds_path)


from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

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
myModel.showModel(renderer)

# Render- und Interaktionsloop starten
renWin.Render()
interactor.Start()