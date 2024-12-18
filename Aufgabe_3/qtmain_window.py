from pathlib import Path
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import qt_widget as mwid


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("BODIES UND CONSTRAINTS")
        self.setCentralWidget(widget)
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        ## Load QAction Button
        load_action = QAction("Load", self)
        load_action.setShortcut(QKeySequence.Open)
        load_action.triggered.connect(self.load_file)

        ## Save QAction Button
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_file)

        ## SaveAs QAction Button
        saveas_action = QAction("SaveAs", self)
        saveas_action.setShortcut(QKeySequence.SaveAs)
        saveas_action.triggered.connect(self.saveas_file)

        ## ImportFdd QAction Button
        import_action = QAction("ImportFdd", self)
        import_action.setShortcut("Crtl+I")
        import_action.triggered.connect(self.import_file)

        ## ImportFdd QAction Button
        exit_action = QAction("Exit", self)    
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        #Add QActions
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(saveas_action)
        self.file_menu.addAction(import_action)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Anzeigen der Körper")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.9, geometry.height() * 0.9)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei laden", "", "Alle Dateien (*.*)")
        if file_path:
            self.status.showMessage(f"Geladen: {file_path}")

    def save_file(self):
        # Implementieren Sie hier die Logik für das Speichern
        self.status.showMessage("Datei gespeichert")

    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Datei speichern unter", "", "Alle Dateien (*.*)")
        if file_path:
            self.status.showMessage(f"Gespeichert unter: {file_path}")

    def import_file(self):
        # Implementieren Sie hier die Logik für den Import
        self.status.showMessage("FDD-Datei importiert")

