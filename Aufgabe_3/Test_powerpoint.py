from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QPalette, QColor
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setze die Farbe des Hauptfensters
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # Hintergrundfarbe des Fensters

        # Setze die Farbe für den Titel (unter Windows möglich, aber auf anderen Plattformen meist nicht)
        palette.setColor(QPalette.Background, QColor(173, 216, 230))  # Hellblau für die Titelleiste
        self.setPalette(palette)

        self.setWindowTitle("Fenster mit benutzerdefinierter Titelleiste")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

