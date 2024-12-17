from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QMenuBar, QFileDialog, QMessageBox
)
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

        # Create the menu bar
        self.create_menu_bar()

    def create_menu_bar(self):
        # Menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = menu_bar.addMenu("File")

        # Add actions to the File menu
        file_menu.addAction("Load", self.load_file)
        file_menu.addAction("Save", self.save_file)
        file_menu.addAction("ImportFdd", self.import_fdd)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close_app)

    # Placeholder actions
    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load File", "", "All Files (*.*)")
        if file_name:
            QMessageBox.information(self, "Load File", f"Loaded file: {file_name}")
            # TODO: Add code to load the file into your model

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*.*)")
        if file_name:
            QMessageBox.information(self, "Save File", f"Saved file: {file_name}")
            # TODO: Add code to save your model data

    def import_fdd(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import Fdd File", "", "FDD Files (*.fdd)")
        if file_name:
            QMessageBox.information(self, "Import Fdd", f"Imported FDD file: {file_name}")
            # TODO: Add code to process the imported FDD file

    def close_app(self):
        self.close()
