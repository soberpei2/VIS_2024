"""Main File einer Testversion eines eigenständigen VTK Visualizers. Hängt zusammen mit "testEigenesVTK". """
"""Stand: Funktioniert nicht """

import inputfilereader
import os
import testEigenesVtk


# Überprüfen, ob das neue Arbeitsverzeichnis gesetzt wurde
print("Neues Arbeitsverzeichnis:", os.getcwd())

file = "Aufgabe_2/test.fdd"

inputfilereader.readInputFile(file)

# Neues Arbeitsverzeichnis setzen
new_dir = "C:/github/VIS_2024/Aufgabe_2"  # Pfad zum Zielordner
os.chdir(new_dir)  # Ändert das Arbeitsverzeichnis



testEigenesVtk.visualize()