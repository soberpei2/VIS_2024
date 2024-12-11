# Importieren benötigter Bibliotheken
#====================================
import sys
from mbsWindow import mbsWindow
from mbsWidget import mbsWidget
from PySide6.QtWidgets import QApplication
import mbsModel
from pathlib import Path

#================================================================================
#                                  MAIN-FILE                                    #
#================================================================================

if __name__ == "__main__":
    
    # Einlesen .fdd-File + Modell erzeugen
    #=====================================
    if len(sys.argv) < 2:
        sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")

    myModel = mbsModel.mbsModel()

    #read fdd file path from input arguments
    fdd_path = Path(sys.argv[1])
    myModel.importFddFile(fdd_path)
    #create path for solver input file (fds)
    fds_path = fdd_path.with_suffix(".fds")
    myModel.exportFdsFile(fds_path)
    #create path for model database file (json)
    json_path = fdd_path.with_suffix(".json")
    myModel.saveDatabase(json_path)

    #create new model and load json generated above
    #(content should be the same)
    newModel = mbsModel.mbsModel()
    newModel.loadDatabase(json_path)
    #======================================================================================

    # Qt-Anwendung
    #=============
    app = QApplication()

    # Widget anlegen
    widget = mbsWidget()

    # Anlegen und zeigen des Hauptfensters
    window = mbsWindow(widget)
    window.show()

    # Ausführen der Anwendung
    sys.exit(app.exec())



