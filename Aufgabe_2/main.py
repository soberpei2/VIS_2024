# Importiere alle notwendigen Module
import os  # Für Operationen mit dem Betriebssystem, z.B. Pfadoperationen
import json  # Für das Arbeiten mit JSON-Daten (Ein- und Ausgabe von JSON-Dateien)
from inputfilereader import parse_input_file, save_to_json, write_input_file  # Importiere die Funktionen, die aus der inputfilereader.py Datei stammen

def main():
    # Definiere den Pfad zur Eingabedatei (das FDD-File)
    input_file_path = 'C:/VIS_2024/test.fdd'  # Pfad zur Eingabedatei (beispielhafte .fdd-Datei)
    
    # Gebe eine Nachricht aus, dass die Eingabedatei nun gelesen wird
    print("Eingabedatei wird gelesen und geparst...")
    
    try:
        # Lese und parse die Eingabedatei mit der Funktion aus inputfilereader.py
        objects = parse_input_file(input_file_path)  # Die Funktion gibt eine Liste von mbsObject-Instanzen zurück
        print(f"Die Eingabedatei wurde erfolgreich geparst. {len(objects)} Objekte wurden gefunden.")
    except ValueError as e:
        # Falls ein unbekannter Typ oder Fehler in der Datei auftritt, wird der Fehler hier abgefangen und ausgegeben
        print(f"Fehler beim Parsen der Eingabedatei: {e}")
        return

    # Definiere den Pfad für die Ausgabe-JSON-Datei
    json_output_file = 'C:/VIS_2024/output_data.json'  # Pfad zur Ausgabedatei
    
    # Speichern der geparsten Objekte als JSON-Datei
    try:
        save_to_json(objects, json_output_file)  # Die Objekte werden in die JSON-Datei geschrieben
        print(f"Die Daten wurden erfolgreich in die Datei {json_output_file} gespeichert.")
    except Exception as e:
        # Falls ein Fehler beim Speichern der Daten auftritt, wird dieser hier abgefangen
        print(f"Fehler beim Speichern der Daten: {e}")
    
    # Optional: Eine Eingabedatei zurückschreiben, falls notwendig
    write_output_file = 'C:/VIS_2024/output_inputfile.fdd'  # Pfad für die neue Eingabedatei
    
    try:
        write_input_file(objects, write_output_file)  # Diese Funktion schreibt die geparsten Objekte zurück in das FDD-Format
        print(f"Die Eingabedatei wurde erfolgreich unter {write_output_file} geschrieben.")
    except Exception as e:
        # Fehler beim Schreiben der Eingabedatei werden hier abgefangen
        print(f"Fehler beim Schreiben der Eingabedatei: {e}")

# Der Hauptteil des Programms wird nur ausgeführt, wenn dieses Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()  # Führe die main Funktion aus
