from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QLineEdit, QPushButton, QColorDialog, QDialog, QMessageBox
from PySide6.QtGui import QColor



class settingWindow(QDialog):
    def __init__(self, mbsModel, parent=None):
        super().__init__(parent)

        self.backgroundColorRGB= mbsModel.getBackgroundColor()
        self.gravityVector = mbsModel.getGravityVector()

        self.setWindowTitle("Seetings")
        self.setGeometry(150, 150, 600, 400)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.gravityArea())
        self.layout.addWidget(self.backgroundArea())

        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.okClicked)
        self.layout.addWidget(self.okButton)

    def okClicked(self):
        if self.getGravityVector() !=None:
            self.accept()

    def gravityArea(self):
        gravityBox = QGroupBox("Gravity")
        layout = QVBoxLayout(gravityBox)

        label = QLabel("Gravity Vektor:")

        self.gravityVectorInput = QLineEdit()
        self.gravityVectorInput.setPlaceholderText("e.g. [0, 0, -9810]")

        self.gravityVectorInput.setText(str(self.gravityVector))

        layout.addWidget(label)
        layout.addWidget(self.gravityVectorInput)

        return gravityBox

    def getGravityVector(self):
        vectorText = self.gravityVectorInput.text()

        try:
            vectorText = vectorText.strip("[]")  # Entferne die eckigen Klammern
            x, y, z = map(float, vectorText.split(','))  # Teile und konvertiere in Floats
            self.gravityVector = [x,y,z]
            return self.gravityVector
        except ValueError:
            QMessageBox.information(self, "Attention", "The vector must have the format [0.0,0.0,0.0].")
            return None


    def backgroundArea(self):
        backgroundBox = QGroupBox("Background")
        layout = QVBoxLayout(backgroundBox)

        label = QLabel("Color")
         
        colorButton = QPushButton("Choose color")
        colorButton.clicked.connect(self.colorDialog)

        self.colorInput = QLineEdit()
        self.colorInput.setReadOnly(True)

        self.backgroundColor = QColor(self.backgroundColorRGB[0],self.backgroundColorRGB[1],self.backgroundColorRGB[2])
        self.colorInput.setStyleSheet(f"background-color: {self.backgroundColor.name()};")

        layout.addWidget(label)
        layout.addWidget(self.colorInput)
        layout.addWidget(colorButton)
        return backgroundBox
    

    def colorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.colorInput.setStyleSheet(f"background-color: {color.name()};")
            self.backgroundColorRGB = color.red(), color.green(), color.blue()

