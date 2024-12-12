# main.py
from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from main_widget import Widget



# Qt Application
app = QApplication(sys.argv)

# Create central widget (with VTK renderer)
widget = Widget()

# Create main window with status bar and menus
window = MainWindow(widget)
window.show()

# Start VTK interactor
widget.vtk_widget.Initialize()
widget.vtk_widget.Start()

sys.exit(app.exec())



#C:\Users\alexa/AppData/Local/Programs/Python/Python313/python.exe "QT_Tutorial/main.py" -f "QT_Tutorial/all_day.csv" unten im powershell eingeben
#C:\Users\alexa/AppData/Local/Programs/Python/Python312/python.exe -m pip install pandas