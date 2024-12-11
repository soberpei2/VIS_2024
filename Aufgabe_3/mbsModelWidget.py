import vtk
import QVTKRenderWindowInteractor as QVTK
import os


from PySide6.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt


class mbsModelWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QHBoxLayout(self)
        self.QVTKWidget = None
        self.treeWidget = None
        
    def modelRenderer(self):
        self.QVTKWidget = QVTK.QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        renderWindow = self.QVTKWidget.GetRenderWindow()
        renderWindow.AddRenderer(self.renderer)

        self.layout.addWidget(self.QVTKWidget)
        self.setLayout(self.layout)
        self.QVTKWidget.Initialize()

    def modelTree(self, mbsModel):
        self.treeWidget = QTreeWidget()
        
        self.treeWidget.setHeaderLabels(["mbsModel"])

        rootItem = QTreeWidgetItem([os.path.basename(mbsModel._filePath)])
        for obj in mbsModel.getListOfMbsModel():
            rootItem.addChild(QTreeWidgetItem([obj.getType()]))
        self.treeWidget.addTopLevelItem(rootItem)

        treeWithPixels = int(self.logicalDpiX() * 50 / 25.4)  # Umrechnung in Pixel
        self.treeWidget.setFixedWidth(treeWithPixels)
        
        self.layout.removeWidget(self.QVTKWidget)
        self.layout.addWidget(self.treeWidget)
        self.layout.addWidget(self.QVTKWidget)
        self.setLayout(self.layout)


    def showModel(self, mbsModel):
        mbsModel.showModel(self.renderer)
        self.renderer.ResetCamera()

    def hideModel(self, mbsModel):
        mbsModel.hideModel(self.renderer)

    #def renderTree(self, mbsModel):

    
    def renderModelWithTree(self, mbsModel):
        self.modelRenderer()
        self.modelTree(mbsModel)
        self.showModel(mbsModel)
        
        

