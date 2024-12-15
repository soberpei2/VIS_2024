from mbsModel import mbsModel
import os

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox, QHBoxLayout
from mbsModelWidget import mbsModelWidget
from settingsBox import settingWindow



class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("pyFreeDyn")
        self.showMaximized()

        
        self.mbsModel = None
        self.widget = mbsModelWidget(self.mbsModel)
    

        # Menu
        self.menu = self.menuBar()
        self.status = self.statusBar()



        self.fileMenu = self.menu.addMenu("File")

        # newAction = QAction("New",self)
        # newAction.triggered.connect(self.newMbsModel)
        # self.fileMenu.addAction(newAction)

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


        self.settingsMenu = self.menu.addMenu("Settings")
        settingsAction = QAction("Settings",self)
        settingsAction.triggered.connect(self.settings)
        self.settingsMenu.addAction(settingsAction)


        self.helpMenu = self.menu.addMenu("Help")
        aboutAction = QAction("About",self)
        aboutAction.triggered.connect(self.about)
        self.helpMenu.addAction(aboutAction)

        
        

    # def newMbsModel(self):
    #     if self.mbsModel != None:
    #         reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
    #                                  QMessageBox.Yes | QMessageBox.No,
    #                                  QMessageBox.No)

    #         if reply == QMessageBox.Yes:
    #             self.widget.deleteModelRenderer()
    #             self.widget.deleteModelTree()
    #         elif reply == QMessageBox.No:
    #             return
    #     self.mbsModel = mbsModel()
    #     self.allmbsWidget()
    #     self.status.showMessage("New mbs-model created.",2000)

            

    def loadFile(self):
        if self.mbsModel != None:
            reply = QMessageBox.question(self, "Attention", "You have not saved the file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.deleteModelRenderer()
                self.widget.deleteModelTree()
            elif reply == QMessageBox.No:
                return
        self.mbsModel = mbsModel()
        filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
        self.mbsModel.loadJsonFile(filePath)
        self.allmbsWidget()
        self.status.showMessage("Mbs-model " + os.path.basename(self.mbsModel._filePath) + " loaded.",2000)
        

    def saveFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            [fileName, fileExtension] = os.path.splitext(self.mbsModel._filePath)
            if fileExtension == ".json":
                self.mbsModel.saveJsonFile(self.mbsModel._filePath)
            else:
                filePath, _ = QFileDialog.getSaveFileName(self, "save file", "", "pyFreeDyn-File (*.json)")
                self.mbsModel.saveJsonFile(filePath)
            self.status.showMessage("Mbs-model " + os.path.basename(self.mbsModel._filePath) + " saved.",2000)

    def saveAsFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot save a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "save file", "", "pyFreeDyn-File (*.json)")
            self.mbsModel.saveJsonFile(filePath)
            self.status.showMessage("Mbs-model saved as" + os.path.basename(self.mbsModel._filePath) + " .",2000)
        

    def importFile(self):
        if self.mbsModel != None:
            reply = QMessageBox.question(self, "Attention", "You have not saved file yet do you want to continue? The changes to the current model will be deleted.",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.widget.deleteModelRenderer()
                self.widget.deleteModelTree()
            elif reply == QMessageBox.No:
                return
        filePath, _ = QFileDialog.getOpenFileName(self, "import file", "", "pyFreeDyn-File (*.fdd)")
        self.mbsModel = mbsModel()
        self.mbsModel.importFddFile(filePath)
        self.allmbsWidget()
        self.status.showMessage("Mbs-model from" + os.path.basename(self.mbsModel._filePath) + " imported.",2000)

    def exportFile(self):
        if self.mbsModel == None:
            QMessageBox.information(self, "Attention", "You cannot export a file that does not exist.")
        else:
            filePath, _ = QFileDialog.getSaveFileName(self, "export file", "", "pyFreeDyn-File (*.fds)")
            self.mbsModel.exportFdsFile(filePath)
            self.status.showMessage("Mbs-model exported as" + os.path.basename(self.mbsModel._filePath) + " .",2000)

    def settings(self):
        settingsWindow = settingWindow(self.mbsModel)
        settingsWindow.exec()
        if self.mbsModel.getBackgroundColor() != settingsWindow.backgroundColorRGB:
            self.mbsModel.setBackgroundColor(settingsWindow.backgroundColorRGB)
            self.widget.rendererMbsModel.SetBackground([channel / 255 for channel in self.mbsModel.getBackgroundColor()])
        
        self.mbsModel.setGravityVector(settingsWindow.gravityVector)
        self.widget.addGravity()
        self.widget.renderWindow.Render()

    def about(self):
        QMessageBox.information(self, "About", "There is currently no help browser. If you have any questions, please contact Bernhard Fuerlinger (bernhard.fuerlinger@students.fh-wels.at).")


    def allmbsWidget(self):
        self.widget = mbsModelWidget(self.mbsModel)
        
        self.setCentralWidget(self.widget)
        self.widget.createModelTree()
        self.widget.createModelRenderer()
        self.widget.renderModel()
        self.widget.renderTree()

    
    




