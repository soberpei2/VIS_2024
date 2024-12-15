import sys  
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow,QStatusBar,  QVBoxLayout, QWidget, QFileDialog, QMessageBox

from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import (
    
    vtkRenderWindowInteractor
)
import mbsModel
from qt_anwendung import MainWindow
from pathlib import Path
from vtkmodules.all import vtkInteractorStyleTrackballCamera

#------------------------------------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

myModel = mbsModel.mbsModel()

# quader.obj
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
#renWin = vtkRenderWindow()
#renWin.AddRenderer(renderer)
#renWin.SetWindowName('pyFreeDyn')
#renWin.SetSize(1024,768)

# Interactor einrichten
#interactor = vtkRenderWindowInteractor()
#interactor.SetRenderWindow(renWin)
#style = vtkInteractorStyleTrackballCamera()
#interactor.SetInteractorStyle(style)

# Modell anzeigen
newModel.showModel(renderer)

# Render- und Interaktionsloop starten
#renWin.Render()
#interactor.Start()

#-----------------------------------------------------------------------------

# Aufgabe 3


def main():
    app = QApplication(sys.argv)  # Qt-Anwendung erstellen
    window = MainWindow()  # Hauptfenster instanziieren
    window.show()  # Fenster anzeigen
    sys.exit(app.exec_())  # Anwendung starten

if __name__ == "__main__":
    main()  # Hauptfunktion aufrufen

# Start the Qt application
app = QApplication(sys.argv)
main_window = MainWindow(renderer)
main_window.show()

# Start the Qt event loop
sys.exit(app.exec())


















