from __future__ import annotations

from PySide6.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView,
                               QSizePolicy)
import vtk
import QVTKRenderWindowInteractor as QVTK

class Widget(QVTK.QVTKRenderWindowInteractor):
    def __init__(self):
        """Initialisiert das Widget und den Renderer für das VTK-Renderfenster."""
        super().__init__()  # Initialisiert den QVTKRenderWindowInteractor
        self.renderer = vtk.vtkRenderer()  # Erstelle einen VTK-Renderer
        self.GetRenderWindow().AddRenderer(self.renderer)  # Füge den Renderer dem RenderWindow hinzu

    def update_renderer(self, model):
        """Aktualisiert den Renderer mit den neuen Modellobjekten."""
        self.renderer.RemoveAllViewProps()  # Löscht alle bisherigen ViewProps (darunter Modelle)
        model.showModel(self.renderer)  # Zeigt das neue Modell im Renderer an
        self.renderer.ResetCamera() # Kamera zurücksetzen, um das gesamte Modell einzufangen
        self.GetRenderWindow().Render()  # Rendert das Fenster, um das Modell anzuzeigen

