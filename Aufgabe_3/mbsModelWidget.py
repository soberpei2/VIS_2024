import vtk
import QVTKRenderWindowInteractor as QVTK
import os
import numpy as np


from PySide6.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem,QHBoxLayout
from PySide6.QtCore import Qt


class mbsModelWidget(QWidget):
    def __init__(self, mbsModel):
        QWidget.__init__(self)
        self.mbsModel = mbsModel
        self.QVTKWidget = None
        self.treeWidget = None
        self.layout = QHBoxLayout()

        

    def createModelRenderer(self):
        self.QVTKWidget = QVTK.QVTKRenderWindowInteractor(self)
                
        self.renderWindow = self.QVTKWidget.GetRenderWindow()
        self.renderWindow.SetNumberOfLayers(2)
        
        self.renderWindowInteractor = self.QVTKWidget.GetRenderWindow().GetInteractor()
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.renderWindowInteractor.SetInteractorStyle(style)
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)

        self.rendererMbsModel = vtk.vtkRenderer()
        self.rendererMbsModel.SetLayer(0)
        self.renderWindow.AddRenderer(self.rendererMbsModel)
        self.rendererMbsModel.SetBackground([channel / 255 for channel in self.mbsModel.getBackgroundColor()])
    
        self.cameraMbsModel = vtk.vtkCamera()
        self.rendererMbsModel.SetActiveCamera(self.cameraMbsModel)
        self.cameraMbsModel.SetPosition(1,0,0)
        self.cameraMbsModel.SetViewUp(0,0,1)
        self.cameraMbsModel.SetFocalPoint(0,0,0)
        self.rendererMbsModel.ResetCamera()

        self.addCoordinateSystem()
        self.addGravity()
        
        self.layout.addWidget(self.QVTKWidget)
        self.setLayout(self.layout)
    
        self.QVTKWidget.Initialize()
        self.renderWindow.Render()
        self.renderWindowInteractor.Start()


    def syncCameras(self, obj, event):
        self.cameraCosy.SetPosition(self.cameraMbsModel.GetPosition())
        self.cameraCosy.SetViewUp(self.cameraMbsModel.GetViewUp())

        currentCameraPositionMbsModel = np.array(self.cameraMbsModel.GetPosition())
        currentCameraFocalPointMbsModel = np.array(self.cameraMbsModel.GetFocalPoint())
        currentCameraPoitionCosy = np.array(self.cameraCosy.GetFocalPoint())

        distance = np.linalg.norm(currentCameraPositionMbsModel-currentCameraFocalPointMbsModel)

        if not np.isclose(distance, 5):
            scaleFactor = 5 / distance
    
            newCameraPosition = currentCameraPoitionCosy + (currentCameraPositionMbsModel - currentCameraFocalPointMbsModel) * scaleFactor
            self.cameraCosy.SetPosition(newCameraPosition)
        
        self.renderWindow.Render()
    
    def deleteModelRenderer(self):
        self.layout.removeWidget(self.QVTKWidget)

    def addCoordinateSystem(self):
        self.cosy = vtk.vtkAxesActor()
        self.cosy.SetTotalLength(1.0, 1.0, 1.0)

        self.rendererCosy = vtk.vtkRenderer()
        self.rendererCosy.SetLayer(1)
        self.renderWindow.AddRenderer(self.rendererCosy)
        self.rendererCosy.AddActor(self.cosy)
        self.rendererCosy.SetViewport(0.85, 0, 1.0, 0.15)
        
        self.cameraCosy = vtk.vtkCamera()
        self.rendererCosy.SetActiveCamera(self.cameraCosy)
        self.cameraCosy.SetFocalPoint(0,0,0)

        self.renderWindowInteractor.AddObserver('RenderEvent', self.syncCameras)

    def hideCoordinateSystem(self):
        self.rendererCosy.RemoveActor(self.cosy)

    def addGravity(self):
        for obj in self.mbsModel.getListOfMbsModel():
            if obj.getSubtype() == "Gravity":
                obj.hide(self.rendererCosy)
                obj.gravityArrow()
                obj.show(self.rendererCosy)

    def renderModel(self):
        self.mbsModel.showModel(self.rendererMbsModel)
        self.rendererMbsModel.ResetCamera()
    
    def hideModel(self):
        self.mbsModel.hideModel(self.renderer)







    def createModelTree(self):
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
        
        self.layout.addWidget(self.treeWidget)
        self.setLayout(self.layout)


    def deleteModelTree(self):
        self.layout.removeWidget(self.treeWidget)

    def renderTree(self):
        if self.mbsModel._filePath != None:
            self.treeWidget.setHeaderLabels(["mbsModel " + os.path.basename(self.mbsModel._filePath)])
        else:
            self.treeWidget.setHeaderLabels(["mbsModel"])
            
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




        
        

