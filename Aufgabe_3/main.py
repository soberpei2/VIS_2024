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

# Qt Application
app = QApplication(sys.argv)

# Create central widget (with VTK renderer)
widget = Widget(myModel)  # Übergibt das Modell an das Widget

# Create main window with status bar and menus
window = MainWindow(widget)
window.show()

# Start VTK interactor
widget.vtk_widget.Initialize()
widget.vtk_widget.Start()

sys.exit(app.exec())



#C:\Users\alexa/AppData/Local/Programs/Python/Python313/python.exe "QT_Tutorial/main.py" -f "QT_Tutorial/all_day.csv" unten im powershell eingeben
#C:\Users\alexa/AppData/Local/Programs/Python/Python312/python.exe -m pip install pandas