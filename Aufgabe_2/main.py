import mbsModel
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

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

def windowtype(type):
        hint = vtkTextActor()
        hint.SetInput("MKS Reader by fpointin: Press 'q' to exit.")
        hint.GetTextProperty().SetFontSize(24)
        hint.GetTextProperty().SetColor(1, 1, 1)  #Schwarzer Text
        hint.SetPosition(10, 10)  #Position unten links
        renderer.AddActor2D(hint)
        
        #kleines Fenster
        if type == 1:
            renWin.SetSize(1024,768)
            renWin.SetWindowName("MKS Reader by fpointin")
        #Fullscreen
        if type == 2:
            renWin.SetFullScreen(True)

windowtype(2)

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