# Importiere das QVTKRenderWindowInteractor-Modul von QVTK
import QVTKRenderWindowInteractor as QVTK
# Importiere den Renderer aus der VTK-Bibliothek
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.vtkCommonDataModel import vtkBoundingBox


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
        self.GetRenderWindow().Render()  # Rendert das Fenster, um das Modell anzuzeigen

