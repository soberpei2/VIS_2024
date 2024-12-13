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
        load_action = QAction('Load', self)
        load_action.triggered.connect(self.load_model)

        save_action = QAction("save",self)

        openfdd_action = QAction("open fdd",self)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Q Actions zu den Menüs hinzufügen
        self.file_menu.addAction(load_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(openfdd_action)
        self.file_menu.addAction(exit_action)

        # Status Bar 
        self.status = self.statusBar()
        self.status.showMessage("Test 1234")

        # Fenstergröße variabel
        geometry = self.screen().availableGeometry()
        self.resize(geometry.width() * 0.8, geometry.height() * 0.7)

        # Hauptfenster konfigurieren
        self.setWindowTitle("3D Modell in Qt mit VTK")  # Setze den Titel des Fensters
        self.setGeometry(100, 100, 800, 600)  # Setze die Fenstergröße und Position
        
        # Menüleiste erstellen
        #self.create_menu()

        # Statusleiste erstellen
        #self.create_status_bar()

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
                self.show_error_message("Ungültige Datei", "Bitte wählen Sie eine gültige JSON-Datei aus.")
        else:
            self.statusBar().showMessage("Modell-Laden abgebrochen")
    
    def load_json(self,filename):
            self.myModel = mbsModel.mbsModel()  # Erstelle ein neues Modell
            self.myModel.loadDatabase(Path(filename))  # Lade das Modell aus der JSON-Datei
            self.statusBar().showMessage(f"Modell geladen: {filename}")
            self.widget.update_renderer(self.myModel)  # Aktualisiere das Rendering mit dem neuen Modell
