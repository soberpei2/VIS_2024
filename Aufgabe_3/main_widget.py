from vtkmodules.vtkRenderingCore import vtkRenderer, vtkRenderWindow
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mbsModel
from vtkmodules.all import vtkRenderer, vtkInteractorStyleTrackballCamera
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QMainWindow, QMenuBar, QMessageBox


class Widget(QWidget):
    def __init__(self):

        # Setup VTK Renderer 
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtkRenderer()
        self.renderer.SetBackground(1.,1.,1.)
        render_window = self.vtk_widget.GetRenderWindow()
        render_window.AddRenderer(self.renderer)

        # Setup Layout 
        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        self.setLayout(layout)

    def update_renderer(self, model):

        """Initialisiert das Modell und rendert es im VTK-Renderer."""
        # Modell im Renderer
        model.showModel(self.renderer)
        
        # Kamera zurücksetzen, um die Ansicht zu optimieren
        self.renderer.ResetCamera()

        # Rendering Fenster
        self.vtk_widget.GetRenderWindow().Render()