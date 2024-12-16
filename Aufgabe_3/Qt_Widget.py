import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget, QStatusBar
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
from mbsModel import mbsModel
from inputfilereader import readInput


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualisierungsfenster") # Titel von Fenster
        self.setGeometry(100, 100, 1024, 768) #Fenstergröße und Pos

        # Menüleiste erstellen
        self.create_menu_bar()

        # Statusleiste hinzufügen
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar) # setzen der Statusleiste
        self.update_status("No model loaded")

        # VTK RenderWindow
        self.vtk_widget = VTKRenderWidget()
        self.setCentralWidget(self.vtk_widget) # setzen als zentrales Widget

        # Modellinstanz
        self.model = mbsModel()

    def create_menu_bar(self):
        #erstellen der Menüleiste
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File") # erstellen von "File"-Menü

        # Aktion "Load" für das Laden von Modellen
        load_action = QAction("Load Model", self)
        load_action.triggered.connect(self.load_model)
        file_menu.addAction(load_action)

        # Aktion "Import Fdd" für den Import von Fdd-Dateien
        import_action = QAction("Import Fdd", self)
        import_action.triggered.connect(self.import_fdd)
        file_menu.addAction(import_action)

        # Aktion "Exit" zum Beenden der Anwendung
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_model(self):
        #öffnet DateiDialog um Nodell zu laden
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Model", "", "Model Files (*.vtk *.stl *.obj);;All Files (*)")
        if file_name:
            self.update_status(f"Loaded model: {file_name}")
            self.vtk_widget.load_model(file_name)

    def import_fdd(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Fdd File", "", "Fdd Files (*.fdd);;All Files (*)")
        if file_name:
            try:
                # Lese die Fdd-Datei mit inputfilereader
                mbs_objects = readInput(file_name)
                self.model = mbsModel()
                self.model.load_objects(mbs_objects)  # Neue Methode im mbsModel

                # Visualisiere das Modell im Renderer
                self.vtk_widget.render_model(self.model)
                # Kamera auf das Modell ausrichten
                self.vtk_widget.renderer.ResetCamera() # kamera reseten um nicht zu weit im modell zu sein, funktioniert jedoch nicht
                self.vtk_widget.GetRenderWindow().Render()

                self.update_status(f"Loaded Fdd file: {file_name}")
            except Exception as e:
                self.update_status(f"Error loading Fdd file: {e}")
                print(e)

    def update_status(self, message):
        self.status_bar.showMessage(message)


class VTKRenderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.vtk_widget = QVTKRenderWindowInteractor(self) #erstellen VTK widget
        self.layout.addWidget(self.vtk_widget) #zum layout hinzufügen

        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        self.vtk_widget.GetRenderWindow().Render()
        self.vtk_widget.Start()

    def load_model(self, file_name):
        # Debug-Ausgabe, um zu prüfen, ob die Datei geladen wird
        print(f"Lade Modell aus Datei: {file_name}")

        # Modell aus Datei laden
        reader = vtk.vtkOBJReader()
        reader.SetFileName(file_name) #Dateiname setzen
        reader.Update() # laden der Datei

        # Prüfen, ob Punkte im Modell vorhanden sind
        output = reader.GetOutput()
        if output.GetNumberOfPoints() == 0:
            print("Fehler: .obj Datei enthält keine Punkte. Datei prüfen!")
            return

        #mappen der Geometry zu einem Aktor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort()) # verbinden von mapper und reader

        actor = vtk.vtkActor()
        actor.SetMapper(mapper) # verbinden actor mit mapper


        self.renderer.RemoveAllViewProps() #entfernen vorheriger Objekte
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()  # Kamera auf das Modell ausrichten## wichtig damit fenster nicht weiß
        # Rendern
        self.vtk_widget.GetRenderWindow().Render()

    def render_model(self, model):
        # Fügt alle Akteure des Modells zum Renderer hinzu
        self.renderer.RemoveAllViewProps()

        model.showModel(self.renderer)## visualisiere neues Modell
        for actor in model.get_actors(): #iterieren über alle Akteure
            self.renderer.AddActor(actor)
        self.vtk_widget.GetRenderWindow().Render()
