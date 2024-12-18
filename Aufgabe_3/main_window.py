from __future__ import annotations

# Import der notwendigen PySide6-Module zur Erstellung der GUI und Charts
from PySide6.QtWidgets import QWidget, QHeaderView, QHBoxLayout, QTableView, QSizePolicy
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis

# Importiere das QVTKRenderWindowInteractor-Modul von QVTK (zur Integration von VTK in Qt)
import QVTKRenderWindowInteractor as QVTK

# Importiere VTK-Module zur Visualisierung und Rendererstellung
from vtkmodules.vtkRenderingCore import vtkRenderer
from vtkmodules.vtkCommonDataModel import vtkBoundingBox
from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer
from vtkmodules.all import vtkInteractorStyleTrackballCamera

# Definition der Widget-Klasse
class Widget(QWidget):
    def __init__(self, parent=None):
        # Initialisiere das QWidget (Basisklasse)
        super().__init__(parent)

        # Layout für das Widget erstellen
        self.layout = QHBoxLayout()

    def rendererMbsModel(self, mbsModel):
        # Erstelle ein QVTKRenderWindowInteractor-Widget und füge es dem Layout hinzu
        self.QVTKWidget = QVTK.QVTKRenderWindowInteractor(self)
        self.layout.addWidget(self.QVTKWidget)
        self.setLayout(self.layout)

        # VTK-Renderer erstellen und zum RenderWindow hinzufügen
        self.renderer = vtkRenderer()
        self.renderWindow = self.QVTKWidget.GetRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        # Interactor für das RenderWindow konfigurieren
        interactor = self.renderWindow.GetInteractor()
        interactor.SetRenderWindow(self.renderWindow)

        # Setze den Interaktionsstil auf Trackball-Kamera
        style = vtkInteractorStyleTrackballCamera()
        interactor.SetInteractorStyle(style)

        # Modell im Renderer anzeigen
        mbsModel.showModel(self.renderer)

        # Rendering starten
        self.renderWindow.Render()
        interactor.Start()
