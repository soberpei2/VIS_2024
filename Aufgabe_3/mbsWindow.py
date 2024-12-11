# Einlesen benötigte Bibliotheken
#================================
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow

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

        # Import-Aktion definieren
        #-------------------------
        importFdd_action = QAction("importFdd", self)

        # Exit-Aktion definieren
        #-----------------------
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Aktionen zu File-Menü hinzufügen
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(importFdd_action)
        self.file_menu.addAction(exit_action)
        

        # Statusleiste
        #-------------
        self.status = self.statusBar()
        self.status.showMessage("Hallo!")

        # Abmessungen des Main-Windows festlegen
        #---------------------------------------
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
