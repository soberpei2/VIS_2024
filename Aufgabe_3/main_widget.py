# main_widget.py
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mbsModel


class Widget(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model  # Referenz auf das Modell (mbsModel)
        
        # VTK Renderer Setup
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

        # Zeige das Modell im Renderer
        self._show_model_in_renderer()

    def _show_model_in_renderer(self):
        """Zeigt das Modell im VTK-Renderer."""
        self.model.showModel(self.renderer)  # Aufruf der showModel Methode
        
        self.renderer.ResetCamera()  # Kamera-Ansicht zurücksetzen

    def update_renderer(self, actors):
        """Update the renderer with new actors."""
        self.renderer.RemoveAllViewProps()
        for actor in actors:
            self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()