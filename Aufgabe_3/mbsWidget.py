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
        super(mbsWidget, self).__init__(parent)

        # Fenstertitel definieren
        self.setWindowTitle("pyFreedyn")

        # Anlegen eines Menü-Widgets
        menu_widget = QListWidget()
        item = QListWidgetItem("File")
        menu_widget.addItem(item)

        # Layout des Menü-Widgets
        menu_layout = QHBoxLayout()
        menu_layout.addWidget(menu_widget)

        self.setLayout(menu_layout)