
"""
import mbsModel 
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera

import sys
import argparse
import pandas as pd

from PySide6.QtCore import QDateTime, QTimeZone
from PySide6.QtWidgets import QApplication
from main2_window import MainWindow
from main2_widget import Widget

#if len(sys.argv) < 2:
    #sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

myModel = mbsModel.mbsModel()

#read fdd file path from input arguments
fdd_path = Path("")
print("bis hierher")
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
"""
import sys 
from PySide6.QtWidgets import QMainWindow, QApplication 
from vtkmodules.vtkRenderingCore import vtkRenderer 
from vtkmodules.all import vtkConeSource, vtkPolyDataMapper, vtkActor
import QVTKRenderWindowInteractor as QVTK 
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor
def QVTKRenderWidgetConeExample(argv): 
    app = QApplication(['QVTKRenderWindowInteractor'])
    window = QMainWindow() 
    widget = QVTKRenderWindowInteractor(window) 
    window.setCentralWidget(widget) 
    ren = vtkRenderer() 
    widget.GetRenderWindow().AddRenderer(ren)
    cone = vtkConeSource() 
    cone.SetResolution(8)
    coneMapper = vtkPolyDataMapper() 
    coneMapper.SetInputConnection(cone.GetOutputPort())
    coneActor = vtkActor() 
    coneActor.SetMapper(coneMapper)
    ren.AddActor(coneActor) 
    window.show()
    widget.Initialize() 
    widget.Start() 
    app.exec()

if __name__ == "__main__": 
    QVTKRenderWidgetConeExample(sys.argv)