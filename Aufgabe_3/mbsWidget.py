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
        FileButton.clicked.connect(self.hello)

        # Layout des Menü-Widgets
        menu_layout = QHBoxLayout()
        menu_layout.addWidget(FileButton)

        # Layout dem Widget zuweisen
        self.setLayout(menu_layout)

    # Funktion - hello
    #=================
    @Slot()
    def hello(self):
        print("Hello")