import sys
import main_window as mwin
import main_widget as mwid
from PySide6.QtWidgets import QApplication


# Qt Application
app = QApplication(sys.argv)


widget = mwid.Widget()
window = mwin.MainWindow(widget)
window.show()

sys.exit(app.exec())
