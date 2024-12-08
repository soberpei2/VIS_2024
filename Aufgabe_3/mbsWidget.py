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

        # File-Submenü Buttons anlegen
        #-----------------------------
        self.LoadButton = QPushButton("Load")
        self.SaveButton = QPushButton("Save")
        self.ImportButton = QPushButton("ImportFdd")
        self.ExitButton = QPushButton("Exit")

        # Layout des Menü-Widgets
        self.menu_layout = QVBoxLayout()
        self.menu_layout.addWidget(FileButton, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Layout dem Widget zuweisen
        self.setLayout(self.menu_layout)

    # Funktion - Anlegen der Submenü-Buttons
    #=======================================
    @Slot()
    def submenu(self):
        # Hinzufügen zum Layout
        self.menu_layout.addWidget(self.LoadButton, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.menu_layout.addWidget(self.SaveButton, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.menu_layout.addWidget(self.ImportButton, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.menu_layout.addWidget(self.ExitButton, alignment=Qt.AlignTop | Qt.AlignLeft)
