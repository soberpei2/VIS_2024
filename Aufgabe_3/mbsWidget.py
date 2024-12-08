import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QApplication, QLabel, QWidget, QListWidget,
                               QListWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout)

#================================================================================
#                               KLASSE - mbsWidget                                 #
#================================================================================

class mbsWidget(QWidget):
    # Konstruktor
    #============
    def __init__(self, parent = None):
        # Mutterklassenkonstruktor
        super(mbsWidget, self).__init__(parent)

        # Menüwidget
        #-----------
        # Fenstertitel definieren
        self.setWindowTitle("pyFreedyn")

        # Button für File
        #----------------
        FileButton = QPushButton("File")
        FileButton.clicked.connect(self.submenu)

        # Layout des Menü-Widgets
        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(FileButton, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Layout dem Widget zuweisen
        self.setLayout(self.menu_layout)

    # Funktion - Anlegen der Submenü-Buttons
    #=======================================
    @Slot()
    def submenu(self):
        # File-Submenü Buttons
        #---------------------
        LoadButton = QPushButton("Load")
        SaveButton = QPushButton("Save")
        ImportButton = QPushButton("ImportFdd")
        ExitButton = QPushButton("Exit")

        self.menu_layout.addWidget(LoadButton)
        self.menu_layout.addWidget(SaveButton)
        self.menu_layout.addWidget(ImportButton)
        self.menu_layout.addWidget(ExitButton)
