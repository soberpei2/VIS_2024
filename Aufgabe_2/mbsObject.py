import vtk
import math

# Basis-Klasse für alle MBS-Objekte
class mbsObject:
    def __init__(self, name: str):
        self.name = name  # Der Name des Objekts, z.B. "new_body_0"
        
    def get_name(self):
        """Gibt den Namen des Objekts zurück."""
        return self.name

# Klasse für einen starren Körper (RigidBody) im System
class rigidBody(mbsObject):
    def __init__(self, block):
        """
        Initialisiert das RigidBody-Objekt mit den Werten aus dem Inputblock.
        
        Parameters:
        block (list): Eine Liste von Strings, die die Parameter des Körpers beschreiben
        """
        super().__init__(block[0].split(":")[1].strip())  # Name des Körpers
        self.geometry = block[1].split(":")[1].strip()  # Pfad zur Geometrie-Datei (.obj)
        self.position = [float(i) for i in block[2].split(":")[1].strip().split(",")]  # Position des Körpers
        self.x_axis = [float(i) for i in block[3].split(":")[1].strip().split(",")]  # X-Achse
        self.y_axis = [float(i) for i in block[4].split(":")[1].strip().split(",")]  # Y-Achse
        self.z_axis = [float(i) for i in block[5].split(":")[1].strip().split(",")]  # Z-Achse
        self.color = [int(i) for i in block[6].split(":")[1].strip().split()]  # Farbe des Körpers (RGB)
        self.transparency = float(block[7].split(":")[1].strip())  # Transparenz des Körpers
        self.initial_velocity = [float(i) for i in block[8].split(":")[1].strip().split(",")]  # Anfangsgeschwindigkeit
        self.initial_omega = [float(i) for i in block[9].split(":")[1].strip().split(",")]  # Anfangsdrehgeschwindigkeit
        self.mass = float(block[10].split(":")[1].strip())  # Masse des Körpers
        self.COG = [float(i) for i in block[11].split(":")[1].strip().split(",")]  # Schwerpunkt (Center of Gravity)
        self.inertia = [float(i) for i in block[12].split(":")[1].strip().split(",")]  # Trägheitsmomente
        self.i_axes = {  # Trägheitsachsen
            'i1': [float(i) for i in block[13].split(":")[1].strip().split(",")],
            'i2': [float(i) for i in block[14].split(":")[1].strip().split(",")],
            'i3': [float(i) for i in block[15].split(":")[1].strip().split(",")]
        }

    def create_vtk_representation(self):
        """
        Erstellt eine VTK-Darstellung für das RigidBody-Objekt.
        Diese Darstellung nutzt die .obj-Datei zur Visualisierung des Körpers.
        
        Returns:
        vtkActor: Der Actor, der das RigidBody visualisiert
        """
        reader = vtk.vtkOBJReader()  # VTK Reader zum Einlesen der .obj-Datei
        reader.SetFileName(self.geometry)
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()  # Mapper zur Zuweisung der Geometrie
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()  # VTK Actor, der die Geometrie visualisiert
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(self.color[0] / 255, self.color[1] / 255, self.color[2] / 255)  # Farben normalisieren (0-1)
        actor.GetProperty().SetOpacity(self.transparency)  # Setzt die Transparenz des Körpers

        return actor

# Klasse für Zwangsbedingungen (Constraints) zwischen zwei Objekten
class Constraint(mbsObject):
    def __init__(self, block):
        """
        Initialisiert das Constraint-Objekt mit den Werten aus dem Inputblock.
        
        Parameters:
        block (list): Eine Liste von Strings, die die Parameter des Constraints beschreiben
        """
        super().__init__(block[0].split(":")[1].strip())  # Name des Constraints
        self.body1 = block[1].split(":")[1].strip()  # Erster Körper im Constraint
        self.body2 = block[2].split(":")[1].strip()  # Zweiter Körper im Constraint
        self.dx = float(block[3].split(":")[1].strip())  # Verschiebung in X-Richtung
        self.dy = float(block[4].split(":")[1].strip())  # Verschiebung in Y-Richtung
        self.dz = float(block[5].split(":")[1].strip())  # Verschiebung in Z-Richtung
        self.ax = float(block[6].split(":")[1].strip())  # Drehachse in X-Richtung
        self.ay = float(block[7].split(":")[1].strip())  # Drehachse in Y-Richtung
        self.az = float(block[8].split(":")[1].strip())  # Drehachse in Z-Richtung
        self.position = [float(i) for i in block[9].split(":")[1].strip().split(",")]  # Position des Constraints
        self.x_axis = [float(i) for i in block[10].split(":")[1].strip().split(",")]  # X-Achse des Constraints
        self.y_axis = [float(i) for i in block[11].split(":")[1].strip().split(",")]  # Y-Achse des Constraints
        self.z_axis = [float(i) for i in block[12].split(":")[1].strip().split(",")]  # Z-Achse des Constraints

    def create_vtk_representation(self):
        """
        Erstellt eine VTK-Darstellung für das Constraint-Objekt als Linie.
        
        Returns:
        vtkActor: Der Actor, der das Constraint als Linie darstellt
        """
        # Erzeugt eine Linie, die die Zwangsbedingung visualisiert
        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1(self.position)
        lineSource.SetPoint2([self.position[0] + self.dx, self.position[1] + self.dy, self.position[2] + self.dz])

        lineMapper = vtk.vtkPolyDataMapper()  # Mapper für die Linie
        lineMapper.SetInputConnection(lineSource.GetOutputPort())

        lineActor = vtk.vtkActor()  # Actor, der die Linie darstellt
        lineActor.SetMapper(lineMapper)
        lineActor.GetProperty().SetColor(0, 0, 0)  # Farbe der Linie auf Schwarz setzen

        return lineActor

# Klasse für eine generische Kraft (GenericForce) zwischen zwei Körpern
class GenericForce(mbsObject):
    def __init__(self, block):
        """
        Initialisiert das GenericForce-Objekt mit den Werten aus dem Inputblock.
        
        Parameters:
        block (list): Eine Liste von Strings, die die Parameter der Kraft beschreiben
        """
        super().__init__(block[0].split(":")[1].strip())  # Name der Kraft
        self.body1 = block[1].split(":")[1].strip()  # Erster Körper, auf den die Kraft wirkt
        self.body2 = block[2].split(":")[1].strip()  # Zweiter Körper, auf den die Kraft wirkt
        self.PointOfApplication_Body1 = [float(i) for i in block[3].split(":")[1].strip().split(",")]  # Punkt der Anwendung
        self.PointOfApplication_Body2 = [float(i) for i in block[4].split(":")[1].strip().split(",")]  # Punkt der Anwendung
        self.mode = block[5].split(":")[1].strip()  # Modus (z.B. "Space fixed")
        self.direction = [float(i) for i in block[6].split(":")[1].strip().split(",")]  # Richtung der Kraft
        self.ForceExpression = block[7].split(":")[1].strip()  # Ausdruck für die Kraft (z.B. Sinusfunktion)

    def create_vtk_representation(self):
        """
        Erstellt eine VTK-Darstellung für die Kraft als Pfeil.
        
        Returns:
        vtkActor: Der Actor, der die Kraft darstellt
        """
        # Erzeugt einen Pfeil, um die Richtung und den Punkt der Anwendung der Kraft darzustellen
        arrowSource = vtk.vtkArrowSource()
        arrowSource.SetTipResolution(20)
        arrowSource.SetShaftResolution(20)

        arrowMapper = vtk.vtkPolyDataMapper()  # Mapper für den Pfeil
        arrowMapper.SetInputConnection(arrowSource.GetOutputPort())

        arrowActor = vtk.vtkActor()  # Actor, der den Pfeil darstellt
        arrowActor.SetMapper(arrowMapper)
        arrowActor.SetPosition(self.PointOfApplication_Body1)  # Position des Pfeils auf Basis des Anwendungsorts
        arrowActor.GetProperty().SetColor(1, 0, 0)  # Rot für die Darstellung der Kraft

        return arrowActor

# Klasse für ein Drehmoment (GenericTorque)
class GenericTorque(mbsObject):
    def __init__(self, block):
        """
        Initialisiert das GenericTorque-Objekt mit den Werten aus dem Inputblock.
        
        Parameters:
        block (list): Eine Liste von Strings, die die Parameter des Drehmoments beschreiben
        """
        super().__init__(block[0].split(":")[1].strip())  # Name des Drehmoments
        self.body1 = block[1].split(":")[1].strip()  # Erster Körper, auf den das Drehmoment wirkt
        self.body2 = block[2].split(":")[1].strip()  # Zweiter Körper, auf den das Drehmoment wirkt
        self.mode = block[3].split(":")[1].strip()  # Modus (z.B. "Body fixed")
        self.direction = [float(i) for i in block[4].split(":")[1].strip().split(",")]  # Richtung des Drehmoments

    def create_vtk_representation(self):
        """
        Erstellt eine VTK-Darstellung für das Drehmoment als Pfeil.
        
        Returns:
        vtkActor: Der Actor, der das Drehmoment darstellt
        """
        # Erzeugt einen Pfeil, der das Drehmoment visualisiert
        torqueArrowSource = vtk.vtkArrowSource()
        torqueArrowSource.SetTipResolution(20)
        torqueArrowSource.SetShaftResolution(20)

        torqueArrowMapper = vtk.vtkPolyDataMapper()  # Mapper für den Drehmoment-Pfeil
        torqueArrowMapper.SetInputConnection(torqueArrowSource.GetOutputPort())

        torqueArrowActor = vtk.vtkActor()  # Actor für das Drehmoment
        torqueArrowActor.SetMapper(torqueArrowMapper)
        torqueArrowActor.GetProperty().SetColor(0, 0, 1)  # Blau für das Drehmoment

        return torqueArrowActor
