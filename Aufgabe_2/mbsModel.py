import vtk
import inputfilereader as ifr

class MbsModel:
    def __init__(self):
        """
        Initialisiert die mbsModel Instanz.
        
        Das Modell enthält eine Liste von Objekten (rigide Körper, Einschränkungen, Kräfte, etc.), 
        die Teil des Mehrkörpersystems (MKS) sind. Diese Liste ist zu Beginn leer.
        """
        self.objects = []  # Liste zur Speicherung der MKS-Objekte (rigide Körper, Kräfte, Einschränkungen, etc.)

    def add_object(self, mbs_object):
        """
        Fügt ein MKS-Objekt zum Modell hinzu.

        Args:
            mbs_object (mbsObject): Das Objekt, das zum Modell hinzugefügt wird (z.B. rigider Körper, Kraft, Einschränkung).
        """
        self.objects.append(mbs_object)  # Das Objekt wird zur Liste der Objekte im Modell hinzugefügt

    def show(self, renderer):
        """
        Visualisiert alle Objekte im Modell, indem deren `show()`-Methode aufgerufen wird.
        Jeder Objekttyp (rigider Körper, Einschränkung, etc.) sollte eine eigene `show()`-Methode haben, 
        die für die Visualisierung zuständig ist.
        
        Args:
            renderer (vtkRenderer): Der VTK-Renderer, zu dem die Objekte für die Visualisierung hinzugefügt werden.
        """
        # Iteriere über alle Objekte im Modell und rufe deren `show()`-Methode basierend auf ihrem Typ auf
        for obj in self.objects:
            # Überprüfe den Typ des Objekts und rufe die entsprechende `show()`-Methode auf
            if isinstance(obj, ifr.mbsObject.rigidBody):
                obj.show(renderer)  # Visualisiere den rigiden Körper
            elif isinstance(obj, ifr.mbsObject.constraint):
                obj.show(renderer)  # Visualisiere die Einschränkung
            elif isinstance(obj, ifr.mbsObject.settings):
                obj.show(renderer)  # Visualisiere die Einstellungen
            elif isinstance(obj, ifr.mbsObject.genericForce):
                obj.show(renderer)  # Visualisiere die Kraft
            # Weitere Objekttypen können hier hinzugefügt werden, falls nötig

    def get_objects(self):
        """
        Gibt die Liste der Objekte im Modell zurück.

        Returns:
            list: Eine Liste, die alle Objekte im Modell enthält.
        """
        return self.objects  # Rückgabe der Liste mit allen MKS-Objekten
