from mbsModel import mbsModel
import os

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox
from mbsModelWidget import mbsModelWidget



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("pyFreeDyn")
        self.showMaximized()

        self.status = self.statusBar()
        self.mbsModel = None
        self.widget = mbsModelWidget(self.mbsModel)

        # Menu
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.mbsObjectMenu = self.menu.addMenu("MBS-Object")
        self.optionsMenu = self.menu.addMenu("Options")
        self.helpMenu = self.menu.addMenu("Help")

        # Status Bar
        self.status = self.statusBar()

        newAction = QAction("New",self)
        newAction.triggered.connect(self.newMbsModel)
        self.fileMenu.addAction(newAction)

        loadAction = QAction("Load",self)
        loadAction.setShortcut(QKeySequence.Open)
        loadAction.triggered.connect(self.loadFile)
        self.fileMenu.addAction(loadAction)

        saveAction = QAction("Save",self)
        saveAction.setShortcut(QKeySequence.Save)
        saveAction.triggered.connect(self.saveFile)
        self.fileMenu.addAction(saveAction)

        saveAsAction = QAction("Save as",self)
        saveAsAction.triggered.connect(self.saveAsFile)
        self.fileMenu.addAction(saveAsAction)


        importFddAction = QAction("Import .fdd",self)
        importFddAction.triggered.connect(self.importFile)
        self.fileMenu.addAction(importFddAction)

        exportFdsAction = QAction("Export .fds",self)
        exportFdsAction.triggered.connect(self.exportFile)
        self.fileMenu.addAction(exportFdsAction)

        exitAction = QAction("Exit", self)
        exitAction.setShortcut(QKeySequence.Quit)
        exitAction.triggered.connect(self.close)
        self.fileMenu.addAction(exitAction)

        

    def newMbsModel(self):
        if self.mbsModel != None:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.deleteModel()
                self.widget.deleteTree()
            elif reply == QMessageBox.No:
                return
        self.mbsModel = mbsModel()
        self.mbsWidget()
        self.status.showMessage("New mbs-model created.",2000)

            

    def loadFile(self):
        if self.mbsModel != None:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.deleteModel()
                self.widget.deleteTree()
            elif reply == QMessageBox.No:
                return
        self.mbsModel = mbsModel()
        filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
        self.mbsModel.loadJsonFile(filePath)
        self.mbsWidget()
        self.status.showMessage("Mbs-model " + os.path.basename(self.mbsModel._filePath) + " loaded.",2000)
        

    def saveFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            [fileName, fileExtension] = os.path.splitext(self.mbsModel._filePath)
            if fileExtension == ".json":
                self.mbsModel.saveJsonFile(self.mbsModel._filePath)
            else:
                filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
                self.mbsModel.saveJsonFile(filePath)
            self.status.showMessage("Mbs-model " + os.path.basename(self.mbsModel._filePath) + " saved.",2000)

    def saveAsFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
            self.mbsModel.saveJsonFile(filePath)
            self.status.showMessage("Mbs-model saved as" + os.path.basename(self.mbsModel._filePath) + " .",2000)
        

    def importFile(self):
        if self.mbsModel != None:
            reply = QMessageBox.question(self, "Attention", "You have not saved file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.deleteModel()
                self.widget.deleteTree()
            elif reply == QMessageBox.No:
                return
        filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
        self.mbsModel = mbsModel()
        self.mbsModel.importFddFile(filePath)
        self.mbsWidget()
        self.status.showMessage("Mbs-model from" + os.path.basename(self.mbsModel._filePath) + " imported.",2000)

    def exportFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot export a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "export file", "", "pyFreeDyn-File (*.fds)")
            self.mbsModel.exportFdsFile(filePath)
            self.status.showMessage("Mbs-model exported as" + os.path.basename(self.mbsModel._filePath) + " .",2000)

    
    def mbsWidget(self):
        self.widget = mbsModelWidget(self.mbsModel)
        self.setCentralWidget(self.widget)
        self.widget.modelRenderer()
        self.widget.renderModel()
        self.widget.modelTree()
        self.widget.renderTree()
    




