from __future__ import annotations

from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                               QSizePolicy)

import mbsModel
from pathlib import Path

class Widget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        # Getting the Model
        #self.model = CustomTableModel(data)

        
        
        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    