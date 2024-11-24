
class mbsModel:

    # Konstruktor
    #============
    """
    Legt ein Objekt der Klasse mbsModel an. Dieses Objekt enthält alle benötigten
    Instanzen eines MBS-Modells und soll die zentrale Verwaltung des MBS-Modells
    ermöglichen.
    """
    def __init__(self, listOfMbsObjects):
        self.__listOfMbsObjects = listOfMbsObjects
    #============================================================================