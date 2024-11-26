import vtk

class mbsObject:
    def __init__(self, type_, subtype, text, parameter):
        self.__type = type_
        self.__subtype = subtype
        self.parameter = parameter
        self.vtk_actor = None  # VTK Actor für Visualisierung

        # Parameter aus dem Text extrahieren
        for line in text:
            splitted = line.split(":")
            if len(splitted) == 2:  # Nur wenn Schlüssel und Wert vorhanden sind
                key = splitted[0].strip()
                value = splitted[1].strip()
                if key in self.parameter:
                    try:
                        if self.parameter[key]["type"] == "float":
                            self.parameter[key]["value"] = self.str2float(value)
                        elif self.parameter[key]["type"] == "vector":
                            self.parameter[key]["value"] = self.str2vector(value)
                    except ValueError as e:
                        print(f"Warnung: Ungültiger Wert für '{key}' in Zeile: '{line}'. Fehler: {e}")
            else:
                print(f"Warnung: Ungültige Zeile übersprungen: '{line}'")

    def show(self):
        print(f"Typ: {self.__type}")
        print(f"Subtyp: {self.__subtype}")
        print("Eigenschaften:")
        for key, param in self.parameter.items():
            print(f"{key}: {param['value']}")

    def writeInputfile(self, file):
        text = []
        text.append(f"{self.__type} {self.__subtype}\n")  
        for key, param in self.parameter.items():
            if param["type"] == "float":
                text.append(f"\t{key} = {self.float2str(param['value'])}\n")
            elif param["type"] == "vector":
                text.append(f"\t{key} = {self.vector2str(param['value'])}\n")
        text.append(f"End{self.__type}\n%\n")
        file.writelines(text)

    def str2float(self, in_string):
        try:
            return float(in_string)
        except ValueError:
            raise ValueError(f"Ungültiger Float-Wert: {in_string}")

    def str2vector(self, in_string):
        try:
            values = [float(v.strip()) for v in in_string.split(",")]
            if len(values) != 3:
                raise ValueError(f"Ein Vektor muss 3 Elemente haben: {in_string}")
            return values
        except ValueError:
            raise ValueError(f"Ungültiger Vektorwert: {in_string}")

    @staticmethod
    def float2str(in_float):
        return f"{in_float:.6f}"

    @staticmethod
    def vector2str(in_vector):
        return ",".join([f"{v:.6f}" for v in in_vector])

    def get_vtk_actor(self):
        """Gibt den VTK-Actor für die Visualisierung zurück"""
        return self.vtk_actor


# Subklassen für spezifische Objekte

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            "mass": {"type": "float", "value": 1.0},
            "COG": {"type": "vector", "value": [0.0, 0.0, 0.0]},
        }
        super().__init__("Body", "Rigid_EulerParameter_PAI", text, parameter)

        # Geometrische Darstellung für den Körper hinzufügen (z. B. als VTK-PolyData für ein 3D-Modell)
        self.create_vtk_representation()

    def create_vtk_representation(self):
        """Erstellt eine VTK-Darstellung für den Körper (z.B. ein 3D-Objekt wie eine Kugel oder ein Würfel)"""
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(self.parameter["mass"]["value"] * 0.1)  # Beispiel: Masse beeinflusst den Radius
        sphere_source.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere_source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.vtk_actor = actor


class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "float", "value": 0.0},
            "value": {"type": "float", "value": 0.0},
        }
        super().__init__("Constraint", "Generic", text, parameter)

        # Darstellung der Zwangsbedingung (z.B. als Linie oder Punkt)
        self.create_vtk_representation()

    def create_vtk_representation(self):
        """Erstellt eine VTK-Darstellung für die Zwangsbedingung"""
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(0.0, 0.0, 0.0)
        line_source.SetPoint2(self.parameter["value"]["value"], 0.0, 0.0)
        line_source.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line_source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.vtk_actor = actor


class force(mbsObject):
    def __init__(self, text):
        parameter = {
            "magnitude": {"type": "float", "value": 0.0},
            "direction": {"type": "vector", "value": [0.0, 0.0, 0.0]},
        }
        super().__init__("Force", "GenericForce", text, parameter)

        # Visualisierung von Kräften (z.B. als Pfeil für Gravitation oder Torque)
        self.create_vtk_representation()

    def create_vtk_representation(self):
        """Erstellt eine VTK-Darstellung für die Kraft (z.B. ein Pfeil für Gravitation)"""
        arrow_source = vtk.vtkArrowSource()
        arrow_source.SetShaftRadius(0.02)
        arrow_source.SetTipLength(0.1)
        arrow_source.SetTipRadius(0.05)
        arrow_source.Update()

        # Transformiert den Pfeil, um ihn an die richtige Position zu setzen
        transform = vtk.vtkTransform()
        transform.Translate(self.parameter["direction"]["value"])

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(arrow_source.GetOutputPort())
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.vtk_actor = actor


class measure(mbsObject):
    def __init__(self, text):
        parameter = {
            "sensorType": {"type": "float", "value": 0.0},
            "reading": {"type": "float", "value": 0.0},
        }
        super().__init__("Measure", "GenericMeasure", text, parameter)

        # Visualisierung der Messung (z.B. als kleiner Punkt oder Kugel)
        self.create_vtk_representation()

    def create_vtk_representation(self):
        """Erstellt eine VTK-Darstellung für das Messgerät"""
        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(0.05)  # Kleine Kugel für Messpunkt
        sphere_source.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere_source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.vtk_actor = actor


