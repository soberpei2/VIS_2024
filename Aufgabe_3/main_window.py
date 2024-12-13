from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, QScreen
from PySide6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("FDD-File Reader")

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        load_action = QAction("Load", self)              #Load
        self.file_menu.addAction(load_action)


        save_action = QAction("Save", self)              #Save
        self.file_menu.addAction(save_action)

        import_action = QAction("Import", self)          #Import
        #import_action.triggered.connect(self.import_fdd_file)
        self.file_menu.addAction(import_action)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        def import_fdd_file(self):
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)")
            if file_path:
                print(f"FDD-Datei geladen: {file_path}")
            # Weiterverarbeitung des Modells


        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Status wird geladen ...")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        #self.setCentralWidget(widget)
