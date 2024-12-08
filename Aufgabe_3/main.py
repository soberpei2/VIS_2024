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
    # 1. Option: Größe und Position mit setGeometry festlegen
    w.setGeometry(100, 100, 800, 600)
    w.show()

    # Ausführen der Anwendung
    sys.exit(app.exec())



