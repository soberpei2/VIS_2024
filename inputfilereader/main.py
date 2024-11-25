
import inputfilereader
import os
import visualize


# Überprüfen, ob das neue Arbeitsverzeichnis gesetzt wurde
print("Neues Arbeitsverzeichnis:", os.getcwd())

file = "inputfilereader/test.fdd"

inputfilereader.inputfilereader(file)

# Neues Arbeitsverzeichnis setzen
new_dir = "C:/VIS_2024/inputfilereader"  # Pfad zum Zielordner
os.chdir(new_dir)  # Ändert das Arbeitsverzeichnis



visualize.visualize()