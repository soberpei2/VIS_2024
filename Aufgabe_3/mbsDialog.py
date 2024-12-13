# Einlesen benötigte Bibliotheken
#================================
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QDialog, QHBoxLayout,
                               QVBoxLayout, QLabel, QPushButton, QLineEdit)
from PySide6.QtGui import QAction, QKeySequence


#===================================================================================
#                               KLASSE - mbsDialog                                 #
#===================================================================================

class mbsDialog(QDialog):
    # Konstruktor
    #============
    def __init__(self):
        # Mutterklassenkonstruktor
        super().__init__()

        # Fenster anlegen
        self.setWindowTitle("ImportFdd-File")
        self.setLayout(QVBoxLayout())
        
        # Aufforderung an User
        self.label = QLabel("Bitte geben Sie den Pfad zu ihrem fdd-File ein:")
        self.layout().addWidget(self.label)

        # Eingabefeld
        self.input_field = QLineEdit()
        self.layout().addWidget(self.input_field)

        # Erzeugen eines Ok- und Close-Buttons nebeneinander
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.close_button)
        self.layout().addLayout(button_layout)

        # Buttonverbindungen
        self.ok_button.clicked.connect(self.accept)
        self.close_button.clicked.connect(self.reject)
        
