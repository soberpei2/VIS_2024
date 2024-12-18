import sys
from pathlib import Path

# Import der Module zur Verwendung von VTK (Visualization Toolkit)
from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer
from vtkmodules.all import vtkInteractorStyleTrackballCamera

# Import der PySide6-Module zur Erstellung einer GUI
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, QScreen
from PySide6.QtWidgets import QMainWindow, QApplication

# Import des benutzerdefinierten Hauptfensters
from main_window import MainWindow

# Der Einstiegspunkt der Anwendung
if __name__ == "__main__":
    # Initialisiere die Qt-Anwendung
    app = QApplication(sys.argv)

    # Erstelle eine Instanz des Hauptfensters
    window = MainWindow()

    # Zeige das Hauptfenster an
    window.show()

    # Starte die Ereignisschleife der Anwendung und beende sie mit einem entsprechenden Exit-Code
    sys.exit(app.exec())
