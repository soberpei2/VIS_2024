from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Eartquakes information")
        self.setCentralWidget(widget)
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        ## Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Load QAction
        load_action = QAction("Load", self)
        load_action.setShortcut("Ctrl+L")
        #load_action.triggered.connect(self.load_file)

        self.file_menu.addAction(load_action)

        # Save QAction
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        #save_action.triggered.connect(self.save_file)

        self.file_menu.addAction(save_action)

        # ImportFdd QAction
        import_fdd_action = QAction("ImportFdd", self)
        import_fdd_action.setShortcut("Ctrl+I")
        #import_fdd_action.triggered.connect(self.import_fdd_file)

        self.file_menu.addAction(import_fdd_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
