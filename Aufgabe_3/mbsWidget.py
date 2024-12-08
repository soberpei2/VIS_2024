import sys
from PySide6.QtCore import Qt
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
        #-------------------------
        super(mbsWidget, self).__init__(parent)

        # Fenstertitel definieren
        self.setWindowTitle("pyFreedyn")

        