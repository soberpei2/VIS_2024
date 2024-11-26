class ModelObject:
    """Basisklasse für alle Modellobjekte"""
    def __init__(self, object_type, subtype, text, parameters):
        self._type = object_type
        self._subtype = subtype
        self.parameters = parameters
        
        # Verarbeite den Text, um Parameter zu extrahieren
        for line in text:
            if ":" in line:
                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                for param_key, param_value in self.parameters.items():
                    if key == param_key:
                        self._set_parameter_value(param_key, param_value, value)

    def _set_parameter_value(self, key, param_info, value):
        """Setzt den Parameterwert basierend auf dem Typ"""
        param_type = param_info["type"]
        if param_type == "float":
            param_info["value"] = float(value)
        elif param_type == "vector":
            param_info["value"] = self._parse_vector(value)
        elif param_type == "string":
            param_info["value"] = value.strip()
        elif param_type == "vectorInt":
            param_info["value"] = self._parse_vector_int(value)
        elif param_type == "int":
            param_info["value"] = int(value)
        elif param_type == "bool":
            param_info["value"] = self._parse_bool(value)

    def _parse_vector(self, value):
        """Parst einen Vektor aus dem String"""
        return [float(v) for v in value.split(",")]

    def _parse_vector_int(self, value):
        """Parst einen Vektor aus Ganzzahlen"""
        return [int(v) for v in value.split()]

    def _parse_bool(self, value):
        """Parst einen Bool-Wert aus der Eingabe"""
        return value.lower() in ['true', '1']

    def write_input_file(self, file):
        """Schreibt die Objektparameter in die Ausgabedatei"""
        lines = [f"{self._type} {self._subtype}\n"]
        for key, param in self.parameters.items():
            lines.append(f"\t{key} = {self._convert_to_string(param['value'])}\n")
        lines.append(f"End {self._type}\n%\n")
        file.writelines(lines)

    def _convert_to_string(self, value):
        """Konvertiert Werte in einen String"""
        if isinstance(value, list):
            return " ".join(map(str, value))
        return str(value)


# Subklassen
class RigidBody(ModelObject):
    def __init__(self, text):
        parameters = {
            "name": {"type": "string", "value": "UNKNOWN"},
            "geometry": {"type": "string", "value": "UNKNOWN"},
            "position": {"type": "vector", "value": [1.0, 1.0, 1.0]},
            "mass": {"type": "float", "value": 1.0}
        }
        super().__init__("rigidBody", "Rigid_EulerParameter_PAI", text, parameters)


class Constraint(ModelObject):
    def __init__(self, text):
        parameters = {
            "name": {"type": "string", "value": "UNKNOWN"},
            "body1": {"type": "string", "value": "UNKNOWN"},
            "body2": {"type": "string", "value": "UNKNOWN"}
        }
        super().__init__("constraint", "Rigid_EulerParameter_PAI", text, parameters)

class GenericForce(ModelObject):
    def __init__(self, text):
        parameters = {
            "name": {"type": "string", "value": "UNKNOWN"},
            "force": {"type": "vector", "value": [1.0, 0.0, 0.0]}
        }
        super().__init__("force_GenericForce", "GenericForce", text, parameters)
