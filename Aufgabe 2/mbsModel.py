import vtk
import inputfilereader as ifr

class mbsModel:
    def __init__(self):
        self.objects = []  #Liste der MKS Objekte

    def add_object(self, mbs_object):
        #Fügt ein MKS Objekt zum Modell hinzu
        self.objects.append(mbs_object)

    def show(self, renderer):
        #Zeigt alle MKS Objekte im renderer an
        for obj in self.objects:
            if isinstance(obj, ifr.mbsObject.rigidBody):
                obj.show(renderer)
            elif isinstance(obj, ifr.mbsObject.constraint):
                obj.show(renderer)
            elif isinstance(obj, ifr.mbsObject.settings):
                obj.show(renderer)
            #evtl. weitere Typen hinzufügen

    def get_objects(self):
        #Rückgabe der Objekte
        return self.objects
