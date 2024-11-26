# Aufgabe 2
# 1. Verwenden Sie die Klassen aus /VIS_2024/inputfilereader (mbsObject)
#       Importieren der Klasse mbsObject, die in Aufgabe 2 erstellt wurde.

import sys
import os

# Aktuelles Verzeichnis von main.py abrufen
current_dir = os.path.dirname(__file__)

# Verzeichnisse zum Suchpfad hinzufügen
sys.path.append(os.path.abspath(os.path.join(current_dir, "..")))

# Anschließend importieren
from inputfilereader.mbsObject import mbsObject, rigidBody

# --+--+--+--+--+--+--+--+--+--+--+--+--+--



