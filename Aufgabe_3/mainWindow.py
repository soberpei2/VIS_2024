from mbsModel import mbsModel

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog



class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)

        self.widget = widget

        self.setWindowTitle("pyFreeDyn")
        self.setCentralWidget(self.widget)
        # Menu
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu("File")
        self.editMenu = self.menu.addMenu("Edit")
        self.mbsObjectMenu = self.menu.addMenu("MBS-Object")
        self.optionsMenu = self.menu.addMenu("Options")
        self.helpMenu = self.menu.addMenu("Help")

        # Status Bar
        self.status = self.statusBar()

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

        

    def loadFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "load File", "", "pyFreeDyn-File (*.json)")
        self.widget.loadJsonFile(filePath)

    def saveFile(self, saveModel):
        filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
        self.widget.saveJsonFile(filePath)

    def saveAsFile(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "save File", "", "pyFreeDyn-File (*.json)")
        self.widget.saveJsonFile(filePath)

    def importFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "import file", "", "FreeDyn-File (*.fdd)")
        importModel = mbsModel()
        importModel.importFddFile(filePath)
        return importModel

    def exportFile(self,exportModel):
        filePath, _ = QFileDialog.getSaveFileName(self, "export file", "", "pyFreeDyn-File (*.fds)")
        exportModel.exportFdsFile(filePath)




