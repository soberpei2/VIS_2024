from __future__ import annotations
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("VTK Integration in QT")
        self.setCentralWidget(widget)

        # Menüs erstellen
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.edit_menu = self.menu.addMenu("Edit")

        # Q Actions erstellen
        load_action = QAction("load",self)

        save_action = QAction("save",self)

        openfdd_action = QAction("open fdd",self)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Q Actions zu den Menüs hinzufügen
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(openfdd_action)
        self.file_menu.addAction(exit_action)

        # Status Bar 
        self.status = self.statusBar()
        self.status.showMessage("Test 1234")

        # Fenstergröße variabel
        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)
