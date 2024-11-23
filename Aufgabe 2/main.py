import inputfilereader as ifr

# Freedyn File lesen
fdd_file_path = "Aufgabe 2/test.fdd"
listOfMbsObjects = ifr.read_fdd_file(fdd_file_path)

# Daten in JSON speichern
json_file_path = "Aufgabe 2/test.json"
ifr.write_json_file(listOfMbsObjects, json_file_path)

# JSON lesen
data = ifr.read_json_file(json_file_path)

# Daten in .fds-Datei schreiben
fds_file_path = "Aufgabe 2/test.fds"
ifr.write_fds_file(listOfMbsObjects, fds_file_path)

# Anzahl der Objekte ausgeben
print(len(listOfMbsObjects))
