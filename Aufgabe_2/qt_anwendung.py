from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QMenuBar, QFileDialog, QMessageBox
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkInteractorStyleTrackballCamera
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication
from inputfilereader import readInput  # Importiere die Funktion readInput
from mbsModel import mbsModel
#import sys

# Hauptfensterklasse
class MainWindow(QMainWindow):
    def __init__(self, renderer):
        super().__init__()

        #  Grundlegendes Fenster einrichten
        self.setWindowTitle("Qt-Widgets-Anwendung")  # Fenstertitel
        self.setGeometry(100, 100, 800, 600)

        # Zentrales Widget mit VTK-Integration
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout für das zentrale Widget
        layout = QVBoxLayout(self.central_widget)
        #self.central_widget.setLayout(layout)

        # VTK-RenderWindowInteractor einfügen
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        layout.addWidget(self.vtk_widget)

        # VTK-Szene erstellen
        # VTK-RenderWindow konfigurieren

        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(renderer)

        # Set up the interactor
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        self.vtk_interactor.SetInteractorStyle(style)
        self.vtk_interactor.Initialize()

        # Statusleiste hinzufügen
        #self.status_bar = QStatusBar()
        #self.setStatusBar(self.status_bar)
        #self.status_bar.showMessage("Kein Modell geladen")

        #  Menüleiste erstellen
        self.create_menu()

    def create_menu(self):
        """Erstellt die Menüleiste mit den geforderten Einträgen."""
        menubar = self.menuBar()  # Menüleiste des Hauptfensters

        # 'File'-Menü erstellen
        file_menu = menubar.addMenu("File")  # Hinzufügen des 'File'-Menüs

        # Menüeinträge hinzufügen
        load_action = QAction("Load", self)  # Eintrag 'Load'
        load_action.triggered.connect(self.load_file)  # Verbinde mit Funktion
        file_menu.addAction(load_action)

        save_action = QAction("Save", self)  # Eintrag 'Save'
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        import_action = QAction("ImportFdd", self)  # Eintrag 'ImportFdd'
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        file_menu.addSeparator()  # Trennlinie

        exit_action = QAction("Exit", self)  # Eintrag 'Exit'
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)

    #  Funktionen für Menüeinträge
    def load_file(self):
        """Öffnet einen Datei-Dialog zum Laden einer Datei."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei laden", "", "Alle Dateien (*)")
        if file_path:
            print(f"Datei geladen: {file_path}")

    def save_file(self):
        """Öffnet einen Datei-Dialog zum Speichern einer Datei."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Datei speichern", "", "Alle Dateien (*)")
        if file_path:
            print(f"Datei gespeichert: {file_path}")

    def import_fdd(self):
        """ Führt die ImportFdd-Funktion aus und zeigt das Modell im Renderer an."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei laden", "", "FDD Datein (*.fdd)")
        if file_path:
            QMessageBox.information(self, "Import FDD", f"Imported FDD file: {file_path}")
            # Import the FDD file into the model
            if self.model.importFddFile(file_path):  # Assuming this method is implemented in mbsModel
                self.update_renderer()  # Update renderer with the new model
            else:
                QMessageBox.critical(self, "Error", "Failed to import FDD file.")
    


    def close_application(self):
        """Schließt die Anwendung nach einer Bestätigung."""
        reply = QMessageBox.question(
            self,
            "Beenden",
            "Möchten Sie die Anwendung wirklich schließen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.instance().quit()

    




        

#  Funktionen für Status-Update
    def load_model(self):
        # Status-Update
        self.status_bar.showMessage("Modell geladen: Modellname.fdd")
            














# Hauptprogramm: Nur ausführen, wenn die Datei direkt gestartet wird
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Qt-Anwendung erstellen
    window = MainWindow()  # Hauptfenster erstellen
    window.show()  # Fenster anzeigen
    sys.exit(app.exec_())  # Anwendung starten





















