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

        #read fdd file path from input arguments
        fdd_path = Path("C:\Users\126al\Desktop\VIS3UE\VIS_2024\Aufgabe_3/test.fdd")
        self.model.importFddFile(fdd_path)
        #create path for solver input file (fds)
        fds_path = fdd_path.with_suffix(".fds")
        self.model.exportFdsFile(fds_path)
        #create path for model database file (json)
        json_path = fdd_path.with_suffix(".json")
        self.model.saveDatabase(json_path)

        #create new model and load json generated above
        #(content should be the same)
        #newModel = mbsModel.mbsModel()
        #newModel.loadDatabase(json_path)
        self.model =  mbsModel.mbsModel()
        self.model.loadDatabase(json_path)

        # Creating a QTableView
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # QTableView Headers
        resize = QHeaderView.ResizeToContents
        self.horizontal_header = self.table_view.horizontalHeader()
        self.vertical_header = self.table_view.verticalHeader()
        self.horizontal_header.setSectionResizeMode(resize)
        self.vertical_header.setSectionResizeMode(resize)
        self.horizontal_header.setStretchLastSection(True)

                # QWidget Layout
        self.main_layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left layout
        size.setHorizontalStretch(1)
        self.table_view.setSizePolicy(size)
        self.main_layout.addWidget(self.table_view)

        # Right Layout
        size.setHorizontalStretch(4)
        self.chart_view.setSizePolicy(size)
        self.main_layout.addWidget(self.chart_view)

        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

    