import QVTKRenderWindowInteractor as QVTK
from vtkmodules.vtkRenderingCore import vtkRenderer


class MainWidget(QVTK.QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.renderer)
    
    def update_renderer(self, model):
        """Aktualisiert den Renderer mit den neuen Modellobjekten."""
        self.renderer.RemoveAllViewProps()  # Löscht alte Modelle
        model.showModel(self.renderer)  # Fügt neue Modelle hinzu
        self.GetRenderWindow().Render()
