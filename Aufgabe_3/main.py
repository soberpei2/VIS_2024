# Importieren benötigter Bibliotheken
#====================================
import sys
import mbsWidget as mbsW
from PySide6.QtWidgets import QApplication

#================================================================================
#                                  MAIN-FILE                                    #
#================================================================================

if __name__ == "__main__":
    app = QApplication()

    # Widget anlegen und zeigen
    w = mbsW.mbsWidget()
    w.show()

    # Ausführen der Anwendung
    sys.exit(app.exec())



