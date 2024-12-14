from __future__ import annotations
from pathlib import Path
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import main_widget as mwid


class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("VTK Integration in QT")
        self.setCentralWidget(widget)

        # MBS Modell initialisieren
        mbsModel.mbsModel()

        # Menüs erstellen
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.edit_menu = self.menu.addMenu("Edit")

        # Q Actions erstellen
        load_action = QAction('Load from JSON', self)
        load_action.triggered.connect(self.load_model)

        save_action = QAction("Save to JSON",self)
        save_action.triggered.connect(self.save_model)

        openfdd_action = QAction("Open FDD",self)
        openfdd_action.triggered.connect(self.import_fdd)

        exit_action = QAction("EXIT", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Q Actions zu den Menüs hinzufügen
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(openfdd_action)
        self.file_menu.addAction(exit_action)

        # Status Bar 
        self.status = self.statusBar()
        self.status.showMessage("Laden Sie ein JSON oder FDD File ein, um es anzuzeigen")

        # Fenstergröße variabel
        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)

        # Hauptfenster konfigurieren
        self.setWindowTitle("3D Modell in QT mit VTK")  # Setze den Titel des Fensters
        self.setGeometry(100, 100, 800, 600)  # Setze die Fenstergröße und Position

        # VTK-Widget und -Renderer initialisieren
        self.widget = mwid.Widget()  # Erstelle ein VTK-Widget
        
        # Setze den Hintergrund des Renderers auf Weiß
        self.widget.renderer.SetBackground(1.0, 1.0, 1.0)

        # Setze das Widget als zentrales Widget des Fensters
        self.setCentralWidget(self.widget)

        # Initialisiere das RenderWindow, um den Hintergrund anzuzeigen
        self.widget.GetRenderWindow().Render()  # Rendere das Fenster, um den schwarzen Hintergrund zu sehen


    def load_model(self):
        """Lädt ein Modell aus einer JSON-Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open json File", "", "JSON and FDD Files (*.json *.fdd)", options=options) # Filter gleich nach fdd und json datein
        
        if filename:
            if filename.lower().endswith(".json"):  # Überprüfe, ob die Datei eine JSON-Datei ist
                self.load_json(filename)
            else:
                self.messagebox("Ungültiges Dateiformat","Bitte wählen Sie eine JSON-Datei aus.")
        else:
            self.statusBar().showMessage("Modell-Laden abgebrochen")
    
    def load_json(self,filename):
            self.myModel = mbsModel.mbsModel()  # Erstelle ein neues Modell
            self.myModel.loadDatabase(Path(filename))  # Lade das Modell aus der JSON-Datei
            self.statusBar().showMessage(f"Modell aus JSON Datei geladen: {filename}")
            self.widget.update_renderer(self.myModel)  # Aktualisiere das Rendering mit dem neuen Modell
        
    def save_model(self):
        """Speichert das Modell in einer JSON-Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Model File", "", "JSON Files (*.json)", options=options)
        if filename:
            self.myModel.saveDatabase(Path(filename))  # Speichert das Modell
            self.statusBar().showMessage(f"Modell gespeichert: {filename}")

    def import_fdd(self):
        """Importiert ein FDD-Modell aus einer Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "JSON and FDD Files (*.json *.fdd)", options=options) # Filter gleich nach fdd und json datein

        if filename.lower().endswith(".fdd"):  # Überprüfe, ob die Datei eine Fdd-Datei ist
            self.myModel = mbsModel.mbsModel()
            self.myModel.importFddFile(filename)
            self.statusBar().showMessage(f"FDD-Datei importiert: {filename}")
            self.widget.update_renderer(self.myModel)
        else:
            self.messagebox("Ungültiges Dateiformat","Bitte wählen Sie eine FDD-Datei aus.")

    def messagebox(self,title,text):
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle(title)
            msg_box.setText(text)
            msg_box.exec()

