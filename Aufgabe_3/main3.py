import mbsModel
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLineEdit
from PySide6.QtGui import QIcon
import sys
import main_window as mwin
import main_widget as mwid
from PySide6.QtWidgets import QApplication

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.all import vtkInteractorStyleTrackballCamera


# Qt Application
app= QApplication(sys.argv)

widget = mwid.Widget()
window = mwin.MainWindow(widget)
window.show()

# Erstelle das Modell
newModel = mbsModel.mbsModel()

sys.exit(app.exec())