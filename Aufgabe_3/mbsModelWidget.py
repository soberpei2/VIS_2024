import vtk
import mbsModel
import QVTKRenderWindowInteractor as QVTK

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout


class mbsModelWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.mbsModel = mbsModel.mbsModel()
        widget = QVTK.QVTKRenderWindowInteractor(self)

        self.renderer = vtk.vtkRenderer()
        renderWindow = widget.GetRenderWindow()
        renderWindow.AddRenderer(self.renderer)

        layout = QVBoxLayout(self)
        layout.addWidget(widget)
        self.setLayout(layout)

        widget.Initialize()

        

    def loadJsonFile(self, filePath):
        self.mbsModel.importJsonFile(filePath)
        self.mbsModel.showModel(self.renderer)

    def saveJsonFile(self, filePath):
        self.mbsModel.exportJsonFile(filePath)




    

    
