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

        self.mbsModel = None
        self.widget = mbsModelWidget()

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

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")


        self.setCentralWidget(self.widget)

    def newMbsModel(self):
        if self.mbsModel == None:
            self.mbsModel = mbsModel()
            self.widget.renderModelWithTree(self.mbsModel)      
        else:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.hideModel(self.mbsModel)
                self.mbsModel = mbsModel()
                self.widget.showModel(self.mbsModel)

            

    def loadFile(self):
        if self.mbsModel == None:
            self.mbsModel = mbsModel()
            filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
            self.mbsModel.importJsonFile(filePath)
            self.widget.renderModelWithTree(self.mbsModel)
        else:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.hideModel(self.mbsModel)
                self.mbsModel = mbsModel()
                filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
                self.mbsModel.importJsonFile(filePath)
                self.widget.showModel(self.mbsModel)
        

    def saveFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            [fileName, fileExtension] = os.path.splitext(self.mbsModel._filePath)
            if fileExtension == ".json":
                self.widget.saveJsonFile(self.mbsModel._filePath)
            else:
                filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
                self.widget.saveJsonFile(filePath)

    def saveAsFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
            self.widget.saveJsonFile(filePath)

    def importFile(self):
        if self.mbsModel == None:
            filePath, _ = QFileDialog.getOpenFileName(self, "import file", "", "FreeDyn-File (*.fdd)")
            self.mbsModel = mbsModel()
            self.mbsModel.importFddFile(filePath)
        else:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.hideModel(self.mbsModel)
                self.mbsModel = mbsModel()
                filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
                self.mbsModel.importFddFile(filePath)
                self.widget.showModel(self.mbsModel)

    def exportFile(self,exportModel):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot export a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "export file", "", "pyFreeDyn-File (*.fds)")
            exportModel.exportFdsFile(filePath)

    




