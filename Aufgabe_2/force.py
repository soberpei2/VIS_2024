import vtk
from mbsObject import mbsObject
import math

class genericForce(mbsObject):
    def __init__(self, text):
        # Parameter definieren
        parameter = {
            "PointOfApplication_Body1": {"type": "vector", "value": [0., 0., 0.]},
            "PointOfApplication_Body2": {"type": "vector", "value": [0., 0., 0.]},
            "mode": {"type": "string", "value": text},
            "direction": {"type": "vector", "value": [0., 0., 0.]},
            "ForceExpression": {"type": "string", "value": text},
        }
        mbsObject.__init__(self, "Force", "GenericForce", text, parameter)

    def vtk_force(self, renderer, sim_time):
        # Kraftinformationen abrufen
        point = self.parameter["PointOfApplication_Body1"]["value"]
        direction = self.parameter["direction"]["value"]
        #force_expr = self.parameter["ForceExpression"]["value"]
        force_expr = 10.
        

        # Berechne die Kraftgröße (hier als statischer Wert)
        magnitude = 10  # Du kannst hier eine andere Berechnung verwenden
        vtk.vtkMath.Normalize(direction)  # Richtung normieren

        # Pfeil erstellen
        arrowSource = vtk.vtkArrowSource()

        # Transformationsfilter für Position, Skalierung und Richtung
        transform = vtk.vtkTransform()
        transform.Translate(point)  # Setze den Punkt der Anwendung
        transform.Scale(magnitude, magnitude, magnitude)  # Setze die Größe des Pfeils

        # Berechne die Rotation des Pfeils, um ihn in die richtige Richtung auszurichten
        if direction != [0, 0, 0]:
            # Standardrichtung des Pfeils ist (0, 0, 1) (Z-Achse)
            vector1 = [0.0, 0.0, 1.0]  # Originalrichtung des Pfeils
            axis = [0.0, 0.0, 0.0]
            vtk.vtkMath.Cross(vector1, direction, axis)  # Bestimme die Achse der Rotation

            # Überprüfen, ob die Achse gültig ist
            if vtk.vtkMath.Norm(axis) != 0.0:
                angle = vtk.vtkMath.AngleBetweenVectors(vector1, direction)  # Berechne den Drehwinkel
                transform.RotateWXYZ(vtk.vtkMath.DegreesFromRadians(angle), axis[0], axis[1], axis[2])  # Drehung anwenden

        # Transformationsfilter anwenden
        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetTransform(transform)
        transformFilter.SetInputConnection(arrowSource.GetOutputPort())

        # Mapper und Actor erstellen
        arrowMapper = vtk.vtkPolyDataMapper()
        arrowMapper.SetInputConnection(transformFilter.GetOutputPort())

        arrowActor = vtk.vtkActor()
        arrowActor.SetMapper(arrowMapper)
        arrowActor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Rot

        # Zum Renderer hinzufügen
        renderer.AddActor(arrowActor)

    def writeInputfile(self, file):
        super().writeInputfile(file)