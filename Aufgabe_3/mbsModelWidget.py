import vtk
import QVTKRenderWindowInteractor as QVTK
import os


from PySide6.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt


class mbsModelWidget(QWidget):
    def __init__(self, mbsModel):
        QWidget.__init__(self)
        self.mbsModel = mbsModel
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

    def modelTree(self):
        self.treeWidget = QTreeWidget()
        
        self.treeWidget.setHeaderLabels(["mbsModel"])

        self.rootBody = QTreeWidgetItem(["Body"])
        self.treeWidget.addTopLevelItem(self.rootBody)
        self.childRigidBody = QTreeWidgetItem(["RigidBody"])
        self.childFlexibleBody = QTreeWidgetItem(["FlexibleBody"])
        self.rootBody.addChild(self.childRigidBody)
        self.rootBody.addChild(self.childFlexibleBody)
        #rootBody.setExpanded(True)

        self.rootConstraint = QTreeWidgetItem(["Constraint"])
        self.treeWidget.addTopLevelItem(self.rootConstraint)
        self.childGenericConstraint = QTreeWidgetItem(["Generic"])
        self.rootConstraint.addChild(self.childGenericConstraint)
        #rootConstraint.setExpanded(True)


        self.rootForce = QTreeWidgetItem(["Force"])
        self.treeWidget.addTopLevelItem(self.rootForce)
        self.childGenericForce = QTreeWidgetItem(["GenericForce"])
        self.childGenericTorque = QTreeWidgetItem(["GenericTorque"])
        self.rootForce.addChild(self.childGenericForce)
        self.rootForce.addChild(self.childGenericTorque)
        #rootForce.setExpanded(True)

        self.rootMeasure = QTreeWidgetItem(["Measure"])
        self.treeWidget.addTopLevelItem(self.rootMeasure)
        self.childTranslational = QTreeWidgetItem(["Translational"])
        self.childRotational = QTreeWidgetItem(["Rotational"])
        self.rootMeasure.addChild(self.childTranslational)
        self.rootMeasure.addChild(self.childRotational)
        #rootMeasure.setExpanded(True)

        self.rootDataobject = QTreeWidgetItem(["DataObject"])
        self.treeWidget.addTopLevelItem(self.rootDataobject)
        self.childParameter = QTreeWidgetItem(["Parameter"])
        self.rootDataobject.addChild(self.childParameter)
        #rootDataobject.setExpanded(True)

        self.treeWidget.expandAll()

        treeWithPixels = int(self.logicalDpiX() * 50 / 25.4)  # Umrechnung in Pixel
        self.treeWidget.setFixedWidth(treeWithPixels)
        
        #self.deleteModel()
        self.layout.addWidget(self.treeWidget)
        self.layout.addWidget(self.QVTKWidget)
        self.setLayout(self.layout)

    def deleteModel(self):
        self.layout.removeWidget(self.QVTKWidget)

    def deleteTree(self):
        self.layout.removeWidget(self.treeWidget)

    def renderModel(self):
        self.mbsModel.showModel(self.renderer)
        self.renderer.ResetCamera()

    def renderTree(self):
        self.treeWidget.setHeaderLabels(["mbsModel " + os.path.basename(self.mbsModel._filePath)])
        for obj in self.mbsModel.getListOfMbsModel():
            if obj.getType() == "Body":
                if obj.getSubtype() == "Rigid_EulerParameter_PAI":
                    self.childRigidBody.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
            elif obj.getType() == "Constraint":
                if obj.getSubtype() == "Generic":
                    self.childGenericConstraint.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
            elif obj.getType() == "Force":
                if obj.getSubtype() == "GenericForce":
                    self.childGenericForce.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
                elif obj.getSubtype() == "GenericTorque":
                    self.childGenericTorque.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
            elif obj.getType() == "Measure":
                if obj.getSubtype() == "Translational":
                    self.childTranslational.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
                elif obj.getSubtype() == "Rotational":
                    self.childRotational.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))
            elif obj.getType() == "DataObject":
                if obj.getSubtype() == "Parameter":
                    self.childParameter.addChild(QTreeWidgetItem([obj.parameter["name"]["value"]]))

    def hideModel(self):
        self.mbsModel.hideModel(self.renderer)


        
        

