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
    
    # Abfrage, ob genug Argumente für Aufruf
    #=======================================
    if len(sys.argv) < 2:
        sys.exit("No fdd file provided! Please run script with additional argument: fdd-filepath!")
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



