from inputFileReader import read_input_file, write_json, read_json, write_fds_file

# Parameter
input_file = "test.fdd"
output_json = "Ausgabe.json"
output_fds = "Ausgabe.fds"
search_objects = ["RIGID_BODY", "CONSTRAINT"]

# Lesen der Eingabedatei
list_of_mbs_objects = read_input_file(input_file, search_objects)

# JSON schreiben
model_objects = [{"parameters": obj.parameter} for obj in list_of_mbs_objects]
write_json({"modelObjects": model_objects}, output_json)

# JSON lesen
data = read_json(output_json)

# FDS-Datei schreiben
write_fds_file(list_of_mbs_objects, output_fds)

# Anzahl der Objekte ausgeben
print(f"Anzahl der Objekte: {len(list_of_mbs_objects)}")