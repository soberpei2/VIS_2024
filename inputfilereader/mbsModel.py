import os

# Importiere die notwendigen Klassen (stellen Sie sicher, dass mbsObject, rigidBody, force, etc. bereits definiert sind)
from mbsObject import mbsObject, rigidBody, constraint, force, measure  # Beispiel-Import

class mbsModel:
    def __init__(self):
        # Die Liste der Objekte im Modell
        self.objects = []

    def add_object(self, mbs_object):
        """Fügt ein neues mbsObject zum Modell hinzu"""
        if isinstance(mbs_object, mbsObject):
            self.objects.append(mbs_object)
        else:
            print(f"Fehler: Das Objekt {mbs_object} ist kein gültiges mbsObject.")

    def get_objects(self):
        """Gibt alle Objekte im Modell zurück"""
        return self.objects

    def show_model(self):
        """Zeigt alle Objekte im Modell und deren Eigenschaften"""
        for obj in self.objects:
            obj.show()

    def write_model_to_file(self, filename):
        """Schreibt das Modell in eine Input-Datei"""
        with open(filename, 'w') as file:
            for obj in self.objects:
                obj.writeInputfile(file)

    def load_from_inputfile(self, input_filename):
        """Lädt das Modell aus einer Input-Datei"""
        try:
            with open(input_filename, 'r') as file:
                lines = file.readlines()
                current_object = None
                text = []
                for line in lines:
                    if line.startswith("Body") or line.startswith("Constraint") or line.startswith("Force") or line.startswith("Measure"):
                        if current_object is not None:
                            # Objekt zum Modell hinzufügen
                            self.add_object(current_object)
                        # Start eines neuen Objekts
                        text = [line.strip()]
                        if "Body" in line:
                            current_object = rigidBody(text)
                        elif "Constraint" in line:
                            current_object = constraint(text)
                        elif "Force" in line:
                            current_object = force(text)
                        elif "Measure" in line:
                            current_object = measure(text)
                    else:
                        if current_object is not None:
                            text.append(line.strip())

                # Zum Schluss das letzte Objekt hinzufügen
                if current_object is not None:
                    self.add_object(current_object)

        except Exception as e:
            print(f"Fehler beim Laden der Input-Datei: {e}")

    def get_vtk_actors(self):
        """Gibt alle VTK-Actors des Modells zurück, um die Visualisierung zu ermöglichen"""
        actors = []
        for obj in self.objects:
            actor = obj.get_vtk_actor()
            if actor:
                actors.append(actor)
        return actors


