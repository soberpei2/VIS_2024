import mbsModel
import sys
from pathlib import Path
from vtkmodules.vtkRenderingCore import vtkRenderer
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow

if len(sys.argv) < 2:
    sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

# Load the model
myModel = mbsModel.mbsModel()

# Read FDD file path from input arguments
fdd_path = Path(sys.argv[1])
myModel.importFddFile(fdd_path)

# Create path for solver input file (fds)
fds_path = fdd_path.with_suffix(".fds")
myModel.exportFdsFile(fds_path)

# Create path for model database file (json)
json_path = fdd_path.with_suffix(".json")
myModel.saveDatabase(json_path)

# Load database into a new model
newModel = mbsModel.mbsModel()
newModel.loadDatabase(json_path)

# Create a VTK renderer
renderer = vtkRenderer()
newModel.showModel(renderer)

# Start the Qt application
app = QApplication(sys.argv)
main_window = MainWindow(renderer)
main_window.show()

# Start the Qt event loop
sys.exit(app.exec())
