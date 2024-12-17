from pathlib import Path
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import main_widget as mwid

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("3D Modell in QT mit VTK")
        self.setCentralWidget(widget)
        self.setGeometry(100, 100, 800, 600)  # Setze die Fenstergröße und Position

        # Initialisiere MBS Modell
        self.myModel = mbsModel.mbsModel()

        # Menü und Aktionen erstellen
        self._create_menus()

        # Statusleiste initialisieren
        self.statusBar().showMessage("Laden Sie ein JSON oder FDD File ein, um es anzuzeigen")

    def _create_menus(self):
        """Erstellt die Menüs und fügt Aktionen hinzu."""
        menu_bar = self.menuBar()

        # Datei-Menü
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self._create_action("Load from JSON", self.load_model))
        file_menu.addAction(self._create_action("Save to JSON", self.save_model))
        file_menu.addAction(self._create_action("Open FDD", self.import_fdd))
        file_menu.addAction(self._create_action("EXIT", self.close, QKeySequence.Quit))

    def _create_action(self, name, method, shortcut=None):
        """Hilfsmethode zum Erstellen von Aktionen."""
        action = QAction(name, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.triggered.connect(method)
        return action

    def load_model(self):
        """Lädt ein Modell aus einer JSON-Datei."""
        filename, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json)")
        if filename:
            if filename.lower().endswith(".json"):
                self.myModel.loadDatabase(Path(filename))
                self.statusBar().showMessage(f"Modell aus JSON geladen: {filename}")
                self.centralWidget().update_renderer(self.myModel)
            else:
                self._show_message("Ungültiges Dateiformat", "Bitte wählen Sie eine JSON-Datei aus.")
        else:
            self.statusBar().showMessage("Modell-Laden abgebrochen")

    def save_model(self):
        """Speichert das aktuelle Modell in einer JSON-Datei."""
        filename, _ = QFileDialog.getSaveFileName(self, "Save Model File", "", "JSON Files (*.json)")
        if filename:
            self.myModel.saveDatabase(Path(filename))
            self.statusBar().showMessage(f"Modell gespeichert: {filename}")

    def import_fdd(self):
        """Importiert ein Modell aus einer FDD-Datei."""
        filename, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)")
        if filename.lower().endswith(".fdd"):
            self.myModel.importFddFile(filename)
            self.statusBar().showMessage(f"FDD-Datei importiert: {filename}")
            self.centralWidget().update_renderer(self.myModel)
        else:
            self._show_message("Ungültiges Dateiformat", "Bitte wählen Sie eine FDD-Datei aus.")

    def _show_message(self, title, text):
        """Zeigt eine Fehlermeldung an."""
        QMessageBox.critical(self, title, text)