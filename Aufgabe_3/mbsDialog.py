# Einlesen benötigte Bibliotheken
#================================
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QDialog,
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

        # Erzeugen einer Schließfläche
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        self.layout().addWidget(close_button)
