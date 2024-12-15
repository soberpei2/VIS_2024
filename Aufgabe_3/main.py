# main.py
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLineEdit
from PySide6.QtGui import QIcon
from main_window import MainWindow
from main_widget import Widget

import mbsModel
import sys
from pathlib import Path

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
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

# Qt Application
app = QApplication(sys.argv)

# Erstelle das zentrale Widget (mit VTK-Renderer)
widget = Widget(myModel)  # Übergibt das Modell an das Widget

# Erstelle das Hauptfenster mit Statusleiste und Menüs
window = MainWindow(widget)
window.show()

# Start des Qt-Event-Loops
sys.exit(app.exec())

#C:\Users\alexa/AppData/Local/Programs/Python/Python313/python.exe "QT_Tutorial/main.py" -f "QT_Tutorial/all_day.csv" unten im powershell eingeben
#C:\Users\alexa/AppData/Local/Programs/Python/Python312/python.exe -m pip install pandas