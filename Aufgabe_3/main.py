# Importieren benötigter Bibliotheken
#====================================
import sys
from mbsWindow import mbsWindow
from mbsWidget import mbsWidget
from PySide6.QtWidgets import QApplication

#================================================================================
#                                  MAIN-FILE                                    #
#================================================================================

if __name__ == "__main__":
    app = QApplication()

    # Widget anlegen
    widget = mbsWidget()

    # Anlegen und zeigen des Hauptfensters
    window = mbsWindow(widget)
    window.show()

    # Ausführen der Anwendung
    sys.exit(app.exec())



