import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Awesome App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_load = QAction("load", self)
        button_load.setStatusTip("This is your button")
        button_load.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_load)

        butten_import = QAction("import", self)
        butten_import.setStatusTip("This is your button")
        butten_import.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(butten_import)



    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()