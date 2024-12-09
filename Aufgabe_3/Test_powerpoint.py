import mbsModel
import sys
from pathlib import Path
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QFileDialog, QStatusBar, QMessageBox
from PySide6.QtCore import Qt
from vtkmodules.vtkRenderingCore import vtkRenderer
import QVTKRenderWindowInteractor as QVTK


QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Hauptfenster konfigurieren
        self.setWindowTitle("3D Modell in Qt mit VTK")
        self.setGeometry(100, 100, 800, 600)
        
        # Menüleiste erstellen
        self.create_menu()

        # Statusleiste erstellen
        self.create_status_bar()

        # VTK-Renderer und -Widget
        self.renderer = vtkRenderer()
        self.widget = QVTKRenderWindowInteractor(self)
        self.widget.GetRenderWindow().AddRenderer(self.renderer)
        self.setCentralWidget(self.widget)

    def create_menu(self):
        menubar = self.menuBar()
        
        # Datei-Menü
        file_menu = menubar.addMenu('File')

        # Load Action
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)

        # Save Action
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_model)
        file_menu.addAction(save_action)

        # ImportFdd Action
        import_action = QAction('ImportFdd', self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        # Exit Action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def create_status_bar(self):
        self.statusBar().showMessage("Kein Modell geladen")

    def load_model(self):
        """Lädt das Modell aus einer JSON-Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Model File", "", "JSON Files (*.json)", options=options)
        
        if filename:
            if filename.lower().endswith(".json"):
                # Wenn es eine gültige JSON-Datei ist, lade das Modell
                self.load_json_model(filename)
            else:
                # Wenn es keine JSON-Datei ist, zeige eine Warnung
                self.show_error_message("Ungültige Datei", "Bitte wählen Sie eine gültige JSON-Datei aus.")
        else:
            # Wenn der Benutzer keine Datei auswählt
            self.statusBar().showMessage("Modell-Laden abgebrochen")

    def load_json_model(self, filename):
        """Lädt das Modell aus einer JSON-Datei."""
        try:
            self.myModel = mbsModel.mbsModel()
            self.myModel.loadDatabase(Path(filename))
            self.statusBar().showMessage(f"Modell geladen: {filename}")
            self.update_renderer()
        except Exception as e:
            self.statusBar().showMessage(f"Fehler beim Laden des Modells: {e}")

    def save_model(self):
        """Speichert das Modell in einer JSON-Datei."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Model File", "", "JSON Files (*.json)", options=options)
        if filename:
            self.myModel.saveDatabase(Path(filename))
            self.statusBar().showMessage(f"Modell gespeichert: {filename}")

    def import_fdd(self):
        """Importiert ein FDD-Modell."""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Import FDD File", "", "FDD Files (*.fdd)", options=options)
        if filename:
            self.import_fdd_file(Path(filename))

    def import_fdd_file(self, filename):
        """Lädt das Modell aus einer FDD-Datei."""
        try:
            self.myModel = mbsModel.mbsModel()
            self.myModel.importFddFile(filename)
            self.statusBar().showMessage(f"FDD-Datei importiert: {filename}")
            self.update_renderer()
        except Exception as e:
            self.statusBar().showMessage(f"Fehler beim Importieren der FDD-Datei: {e}")

    def update_renderer(self):
        """Aktualisiert den Renderer mit den neuen Modellobjekten."""
        self.renderer.RemoveAllViewProps()  # Löscht alte Modelle
        self.myModel.showModel(self.renderer)  # Fügt neue Modelle hinzu
        self.widget.GetRenderWindow().Render()

    def show_error_message(self, title, message):
        """Zeigt eine Fehlermeldung an."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def closeEvent(self, event):
        """Beendet die Anwendung und gibt Ressourcen frei."""
        self.widget.GetRenderWindow().Finalize()
        event.accept()


def QVTKRenderWidgetConeExample(argv):
    app = QApplication(argv)
    window = MainWindow()
    window.show()
    window.widget.Initialize()  # Initialisiere den VTK-Interactor
    sys.exit(app.exec())

if __name__ == "__main__":
    QVTKRenderWidgetConeExample(sys.argv)

