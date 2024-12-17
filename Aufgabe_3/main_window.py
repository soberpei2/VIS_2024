from __future__ import annotations

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget
import vtkmodules.all as vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from inputfilereader import readInput
from pathlib import Path
import json
import mbsModel
import os
import main_widget

newModel = mbsModel.mbsModel()

class MainWindow(QMainWindow):
    def __init__(self, widget=None):
        super().__init__()
        self.setWindowTitle("Eartquakes information")

        # Central Widget: VTK Render Window
        self.vtk_widget = QWidget(self)
        self.vtk_layout = QVBoxLayout(self.vtk_widget)
        self.vtk_widget.setLayout(self.vtk_layout)

        self.vtk_interactor = QVTKRenderWindowInteractor(self.vtk_widget)
        self.vtk_layout.addWidget(self.vtk_interactor)

        self.renderer = vtk.vtkRenderer()
        self.vtk_interactor.GetRenderWindow().AddRenderer(self.renderer)
        self.setCentralWidget(self.vtk_widget)
        
        
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
        load_action.triggered.connect(self.load_file)

        self.file_menu.addAction(load_action)

        # Save QAction
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        self.file_menu.addAction(save_action)

        # ImportFdd QAction
        import_fdd_action = QAction("ImportFdd", self)
        import_fdd_action.setShortcut("Ctrl+I")
        import_fdd_action.triggered.connect(self.import_fdd_file)

        self.file_menu.addAction(import_fdd_action)

        # Status Bar
        self.status = self.statusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("No model loaded")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)

        # Model data placeholder
        self.mbs_model = None

    def load_file(self):
        """Methode, um eine Datei zu laden."""
        jason_path, _ = QFileDialog.getOpenFileName(self, "Load Database", "", "JSON Files (*.json);;All Files (*)")
        if jason_path:
            if jason_path.lower().endswith(".json"):
                self.model.loadDatabase(Path(jason_path))
                newModel.loadDatabase(jason_path)
                self.centralWidget().update_renderer(self.model)
                QMessageBox.information(self, "Success", f"Database loaded successfully: {jason_path}")
            else:
                QMessageBox.warning(self, "Failed", "Failed to load the database.")
        else:
                QMessageBox.critical(self, "Error", f"Error loading database:\n{str(e)}")
  


    def save_file(self):
        """Methode, um das aktuelle Modell zu speichern."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Database", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
                self.model.saveDatabase(Path(file_path))
                QMessageBox.information(self, "Success", f"Database saved successfully: {file_path}")



    def import_fdd_file(self):
        """Methode zum Importieren einer .fdd-Datei."""
        fddfilename, _ = QFileDialog.getOpenFileName(self, "Import Fdd File", "", "Fdd Files (*.fdd);;All Files (*)")

        if fddfilename.lower().endswith(".fdd"):
            try:
                # Importiere die FDD-Datei
                self.model.importFddFile(Path(fddfilename))

                # Konvertiere die FDD-Daten in JSON-kompatibles Format (Python-Dictionary)
                json_data = self.model.switch_to_json()

                # JSON-Daten ausgeben (optional für Debugging)
                print(json.dumps(json_data, indent=4))  # Dies zeigt die JSON-Daten im Terminal an

                # Renderer aktualisieren
                self.centralWidget().update_renderer(self.model)

                # Erfolgsmeldung
                QMessageBox.information(self, "Success", f"Fdd file imported and converted to JSON successfully: {fddfilename}")
            except Exception as e:
                # Fehlerbehandlung, wenn etwas schiefgeht
                QMessageBox.critical(self, "Error", f"An error occurred while importing and converting the Fdd file:\n{str(e)}")
        else:
            # Fehler, wenn die Datei keine FDD-Datei ist
            QMessageBox.warning(self, "Failed", "Failed to import the Fdd file.")
    


    def export_fds_file(self):
        """Exportiert das Modell als FDS-Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export FDS File", "", "FDS Files (*.fds);;All Files (*)")
        if file_path:
            try:
                self.model.exportFdsFile(Path(file_path))
                QMessageBox.information(self, "Success", f"FDS File exported successfully: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error exporting FDS file:\n{str(e)}")