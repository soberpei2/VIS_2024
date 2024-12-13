# Einlesen benötigte Bibliotheken
#================================
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QDialog,
                               QVBoxLayout, QLabel, QPushButton)
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
        self.setWindowTitle("Pfad zum fdd-File")
        self.setLayout(QVBoxLayout())
        
        # Dialoginhalt als Widget hinzufügen
        label = QLabel("Bitte geben Sie den Pfad zu ihrem fdd-File ein:")
        self.layout().addWidget(label)

        # Erzeugen einer Schließfläche
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        self.layout().addWidget(close_button)
