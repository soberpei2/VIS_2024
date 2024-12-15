import sys
from PySide6.QtWidgets import QApplication
from mainwindow1 import MainWindow

class App (QApplication):
    def __inti__ (self, args):
        super().__init__()


app = App(sys.argv)
main_window = MainWindow()
main_window.show()
app.exec()