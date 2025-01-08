# Importiere das QVTKRenderWindowInteractor-Modul von QVTK
import QVTKRenderWindowInteractor as QVTK
# Importiere den Renderer aus der VTK-Bibliothek
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.vtkCommonDataModel import vtkBoundingBox
import vtk

class MainWidget(QVTK.QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        """Initialisiert das Widget und den Renderer für das VTK-Renderfenster."""
        super().__init__(parent)  # Initialisiert den QVTKRenderWindowInteractor
        self.renderer = vtkRenderer()  # Erstelle einen VTK-Renderer
        self.GetRenderWindow().AddRenderer(self.renderer)  # Füge den Renderer dem RenderWindow hinzu
    
    def update_renderer(self, model):
        """Aktualisiert den Renderer mit den neuen Modellobjekten."""
        self.renderer.RemoveAllViewProps()  # Löscht alle bisherigen ViewProps (darunter Modelle)
        model.showModel(self.renderer)  # Zeigt das neue Modell im Renderer an
        self.renderer.ResetCamera() # Kamera zurücksetzen, um das gesamte Modell einzufangen
        self.GetRenderWindow().Render()  # Rendert das Fenster, um das Modell anzuzeigen

    def set_interaction(self, mode):
        """Wechselt die Mausinteraktion."""
        if mode == "abaqus":
            self.current_interaction = "abaqus"
            self.set_creo_interaction()  # "Abaqus" nutzt jetzt die "Creo"-Interaktion
        elif mode == "creo":
            self.current_interaction = "creo"
            self.set_abaqus_interaction()  # "Creo" nutzt jetzt die "Abaqus"-Interaktion

    def set_abaqus_interaction(self):
        """Setzt die Mausinteraktion auf 'Abaqus'."""
        print("Interaktion auf Abaqus gesetzt")

        # Interaktionsstil für Abaqus (z.B. Trackball-Kamera)
        style = vtk.vtkInteractorStyleTrackballCamera()  # Standard Interaktionsstil für Abaqus
        self.SetInteractorStyle(style)

    def set_creo_interaction(self):
        """Setzt die Mausinteraktion auf 'Creo'."""
        print("Interaktion auf Creo gesetzt")
        
        # Erstellen eines speziellen Stils für die Creo-Interaktion
        style = vtk.vtkInteractorStyleSwitch()  # Beispielweise eine andere Interaktionsweise
        # Hier kann ein spezifischer Interaktionsstil für Creo hinzugefügt werden
        self.SetInteractorStyle(style)

