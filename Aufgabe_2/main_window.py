from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.all import vtkInteractorStyleTrackballCamera


class MainWindow(QMainWindow):
    def __init__(self, renderer):
        super().__init__()

        # Set up the main window properties
        self.setWindowTitle("pyFreeDyn Viewer")
        self.resize(1024, 768)

        # Set up the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set up the layout
        layout = QVBoxLayout(self.central_widget)

        # Use QVTKRenderWindowInteractor to manage the render window
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        layout.addWidget(self.vtk_widget)

        # Bind the renderer to the render window
        self.vtk_render_window = self.vtk_widget.GetRenderWindow()
        self.vtk_render_window.AddRenderer(renderer)

        # Set up the interactor
        self.vtk_interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        self.vtk_interactor.SetInteractorStyle(style)
        self.vtk_interactor.Initialize()
