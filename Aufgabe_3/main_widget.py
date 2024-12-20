import vtk
import QVTKRenderWindowInteractor as QVTK

class Widget(QVTK.QVTKRenderWindowInteractor):
    def __init__(self):
        super().__init__()

        # Initialisiere Renderer und füge ihn zum RenderWindow hinzu
        self.renderer = vtk.vtkRenderer()
        self.renderer.SetBackground(1.0, 1.0, 1.0) # weißer Hintergrund
        self.GetRenderWindow().AddRenderer(self.renderer)

    def update_renderer(self, model):
        """Aktualisiert den Renderer mit einem neuen Modell."""
        #self.renderer.RemoveAllViewProps()  # Entfernt alte Modelle
        model.showModel(self.renderer)  # Zeigt das neue Modell an
        self.renderer.ResetCamera()  # Kamera zurücksetzen
        self.GetRenderWindow().Render()  # Rendern des aktualisierten Fensters

