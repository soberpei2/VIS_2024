from pathlib import Path
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import mbsModel
import main_widget as mwid
import vtk

class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("3D Modell in QT mit VTK")
        self.setCentralWidget(widget)
        self.setGeometry(100, 100, 800, 600)  # Setze die Fenstergröße und Position

        # Initialisiere MBS Modell
        self.myModel = mbsModel.mbsModel()

        # Standard Interactor Style
        self.current_interactor_style = "default"

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
        file_menu.addAction(self._create_action("Open FDD", self.import_fdd))
        file_menu.addSeparator()
        file_menu.addAction(self._create_action("Save to JSON", self.save_model))
        file_menu.addSeparator()
        file_menu.addAction(self._create_action("EXIT", self.close, QKeySequence.Quit))

        # View-Menü
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction(self._create_action("Fullscreen", self.toggle_fullscreen, QKeySequence("F11")))
        view_menu.addAction(self._create_action("Reset View", self.reset_view))
        view_menu.addSeparator()
        view_menu.addAction(self._create_action("Front View", self.set_front_view))
        view_menu.addAction(self._create_action("Back View", self.set_back_view))
        view_menu.addAction(self._create_action("Left View", self.set_left_view))
        view_menu.addAction(self._create_action("Right View", self.set_right_view))
        view_menu.addAction(self._create_action("Top View", self.set_top_view))
        view_menu.addAction(self._create_action("Bottom View", self.set_bottom_view))

        # Steuerung-Menü
        control_menu = menu_bar.addMenu("Control")
        control_menu.addAction(self._create_action("Switch Interactor Style", self.toggle_interactor_style))

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

    def toggle_fullscreen(self):
        """Schaltet zwischen Vollbild und Standardgröße um."""
        if self.isFullScreen():
            self.showNormal()
            self.setGeometry(100, 100, 800, 600)  # Setze die Standardfenstergröße
        else:
            self.showFullScreen()

    def toggle_interactor_style(self):
        """Wechselt zwischen dem Standard-Interactor und Trackball-Interactor."""
        render_window = self.centralWidget().GetRenderWindow()
        interactor = render_window.GetInteractor()

        if self.current_interactor_style == "default":
            trackball_style = vtk.vtkInteractorStyleTrackballCamera()
            interactor.SetInteractorStyle(trackball_style)
            self.current_interactor_style = "trackball"
            self.statusBar().showMessage("Trackball Interactor aktiviert")
        else:
            default_style = vtk.vtkInteractorStyleSwitch()
            interactor.SetInteractorStyle(default_style)
            self.current_interactor_style = "default"
            self.statusBar().showMessage("Standard Interactor aktiviert")

    def reset_view(self):
        """Zentriert die Ansicht auf das Modell und setzt die Kamera zurück."""
        renderer = self.centralWidget().GetRenderer()
        camera = renderer.GetActiveCamera()
        
        # Berechne Bounding-Box des aktuellen Modells
        renderer.ResetCamera()  # Standard-Reset
        bounds = renderer.ComputeVisiblePropBounds()
        
        if bounds:
            center_x = (bounds[0] + bounds[1]) / 2.0
            center_y = (bounds[2] + bounds[3]) / 2.0
            center_z = (bounds[4] + bounds[5]) / 2.0
            camera.SetFocalPoint(center_x, center_y, center_z)
            
            # Setze Kamera-Position zurück (z. B. auf eine Distanz basierend auf Bounding-Box)
            diagonal = ((bounds[1] - bounds[0]) ** 2 + (bounds[3] - bounds[2]) ** 2 + (bounds[5] - bounds[4]) ** 2) ** 0.5
            camera.SetPosition(center_x, center_y, center_z + 2.0 * diagonal)  # Kamera etwas entfernt setzen
            camera.SetViewUp(0, 1, 0)  # Standard-Ausrichtung der Kamera

        renderer.ResetCameraClippingRange()  # Sicherstellen, dass die Clipping-Range korrekt ist
        self.centralWidget().GetRenderWindow().Render()
        self.statusBar().showMessage("Ansicht zurückgesetzt")


    def set_front_view(self):
        self._set_camera_orientation(0, -1, 0, 0, 0, 1)
        self.statusBar().showMessage("Front-Ansicht")

    def set_back_view(self):
        self._set_camera_orientation(0, 1, 0, 0, 0, 1)
        self.statusBar().showMessage("Back-Ansicht")

    def set_left_view(self):
        self._set_camera_orientation(-1, 0, 0, 0, 0, 1)
        self.statusBar().showMessage("Left-Ansicht")

    def set_right_view(self):
        self._set_camera_orientation(1, 0, 0, 0, 0, 1)
        self.statusBar().showMessage("Right-Ansicht")

    def set_top_view(self):
        self._set_camera_orientation(0, 0, 1, 0, -1, 0)
        self.statusBar().showMessage("Top-Ansicht")

    def set_bottom_view(self):
        self._set_camera_orientation(0, 0, -1, 0, 1, 0)
        self.statusBar().showMessage("Bottom-Ansicht")

    def _set_camera_orientation(self, pos_x, pos_y, pos_z, up_x, up_y, up_z):
        """Hilfsmethode zum Einstellen der Kameraausrichtung."""
        renderer = self.centralWidget().GetRenderer()
        camera = renderer.GetActiveCamera()
        camera.SetPosition(pos_x, pos_y, pos_z)
        camera.SetFocalPoint(0, 0, 0)
        camera.SetViewUp(up_x, up_y, up_z)
        renderer.ResetCamera()
        self.centralWidget().GetRenderWindow().Render()

    def _show_message(self, title, text):
        """Zeigt eine Fehlermeldung an."""
        QMessageBox.critical(self, title, text)
