from __future__ import annotations
import json
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import os

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Inputfilereader")
        self.setCentralWidget(widget)

        # Instanz der mbsModel-Klasse
        self.model = mbsModel.mbsModel()  # Annahme: Deine Klasse heißt mbsModel

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # File Menu Actions
        load_action = QAction("Load Database", self)
        import_fdd_action = QAction("Import Fdd", self)
        save_action = QAction("Save", self)
        export_fds_action = QAction("Export FDS File", self)
        exit_action = QAction("Exit", self)

        # Connect actions to methods
        load_action.triggered.connect(self.select_and_load_database)
        import_fdd_action.triggered.connect(self.select_and_import_fdd)
        save_action.triggered.connect(self.save_to_file)
        export_fds_action.triggered.connect(self.export_fds_file)

        # Exit action
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(load_action)
        self.file_menu.addAction(import_fdd_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(export_fds_action)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Ready")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

    def select_and_load_database(self):
        """Open a file dialog to select a JSON database file and load it."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Database",           # Dialog Title
            "",                         # Initial Directory
            "JSON Files (*.json);;All Files (*)"  # File Filters
        )

        if file_path:  # If a file was selected
            try:
                success = self.model.loadDatabase(file_path)
                if success:
                    QMessageBox.information(self, "Success", f"Database loaded successfully: {file_path}")
                else:
                    QMessageBox.warning(self, "Failed", "Failed to load the database.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading database:\n{str(e)}")

    def select_and_import_fdd(self):
        """Open a file dialog to select an Fdd file and import it."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Fdd File",          # Dialog Title
            "",                         # Initial Directory
            "Fdd Files (*.fdd);;All Files (*)"  # File Filters
        )

        if file_path:  # If a file was selected
            try:
                success = self.model.importFddFile(file_path)
                if success:
                    QMessageBox.information(self, "Success", f"Fdd file imported successfully: {file_path}")
                else:
                    QMessageBox.warning(self, "Failed", "Failed to import the Fdd file.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error importing Fdd file:\n{str(e)}")

    def save_to_file(self):
        """Open a file dialog to select a location and save the current state as JSON."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Database",           # Dialog Title
            "",                        # Initial Directory
            "JSON Files (*.json);;All Files (*)"  # File Filters
        )

        if file_path:  # If a file was selected
            try:
                # Speichern der Datenbank mit der `saveDatabase` Methode
                self.model.saveDatabase(file_path)
                QMessageBox.information(self, "Success", f"Database saved successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving database:\n{str(e)}")

    def export_fds_file(self):
        """Open a file dialog to select a location and export the model to an FDS file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export FDS File",         # Dialog Title
            "",                        # Initial Directory
            "FDS Files (*.fds);;All Files (*)"  # File Filters
        )

        if file_path:  # If a file was selected
            try:
                # Exportiere das Modell in die FDS-Datei mit der `exportFdsFile` Methode
                self.model.exportFdsFile(file_path)
                QMessageBox.information(self, "Success", f"FDS File exported successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting FDS file:\n{str(e)}")