# Einlesen benötigte Bibliotheken
#================================
import sys
from pathlib import Path
from PySide6.QtCore import Slot
import vtk
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from mbsModel import mbsModel

#===================================================================================
#                               KLASSE - mbsWindow                                 #
#===================================================================================

class mbsWindow(QMainWindow):
    # Konstruktor
    #============
    def __init__(self, widget):
        # Mutterklassenkonstruktor
        #-------------------------
        QMainWindow.__init__(self)

        # Fenstertitel / zentrales Widget definieren
        #-------------------------------------------
        self.setWindowTitle("pyFreedyn")
        self.setCentralWidget(widget)

        # Initialisiere Instanzvariable für das VTK-Widget
        self.vtkWidget = None

        # File-Menü anlegen
        #------------------
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Load-Aktion definieren
        #-----------------------
        load_action = QAction("Load", self)


        # Speicher-Aktion defnieren
        #--------------------------
        save_action = QAction("Save", self)

        # Import-Aktion definieren (Achtung: lambda für callable Aktion, sonst wird
        # diese sofort ausgeführt)
        #-------------------------
        importFdd_action = QAction("importFdd", self)
        importFdd_action.triggered.connect(lambda: self.importFdd(widget))

        # Exit-Aktion definieren
        #-----------------------
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Aktionen zu File-Menü hinzufügen
        #---------------------------------
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(importFdd_action)
        self.file_menu.addAction(exit_action)

        # Statusleiste
        #-------------
        self.status = self.statusBar()
        self.status.showMessage("Hallo!")

        # Interaktion mit VTK
        #--------------------
        self.loadVTKbackGround(widget)

        # Abmessungen des Main-Windows festlegen
        #---------------------------------------
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
    #=======================================================================================

    # Fkt. - loadVTKbackGround
    #=========================
    def loadVTKbackGround(self, widget):
        # QVTKRenderWindowInteractor hinzufügen
        self.vtkWidget = QVTKRenderWindowInteractor(widget)
        widget.main_layout.addWidget(self.vtkWidget)

        # VTK Renderer einrichten
        self.renderer = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.renderer)

        # Interactor initialisieren
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.renderer.SetBackground(0.1, 0.2, 0.4)  # Hintergrundfarbe
        self.interactor.Initialize()
    #=======================================================================================

    def importFdd(self, widget):
        # Überprüfen, ob schon ein vtk-Widget existiert (wenn nicht -> Widget erstellen)
        if not self.vtkWidget:
            self.loadVTKbackGround(widget)

        # fdd-File einlesen
        mbsModel().importFddFile(Path(sys.argv[1]))

        # Renderer aktualisieren
        self.renderer.SetBackground(0.1, 0.1, 0.1)
        self.vtkWidget.GetRenderWindow().Render()
        
    
