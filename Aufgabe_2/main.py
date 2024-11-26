import matplotlib.pyplot as plt
import json

def visualize():
    """Visualisiert die Modelle basierend auf den geladenen Daten"""
    # Laden der JSON-Daten
    with open("Aufgabe_2/test.json", "r") as json_file:
        data = json.load(json_file)
    
    # Visualisierung 
    for obj in data["modelObject"]:
        # Parametern für Visualisierungen erzeugen
        position = obj["parameter"].get("position", [0, 0, 0])
        color = obj["parameter"].get("color", [0, 0, 0])
        
        # Eine einfache 3D-Darstellung der Objekte
        plt.scatter(position[0], position[1], position[2], c=[color], label=obj["parameter"]["name"])
    
    plt.legend()
    plt.show()

# Diese Funktion wird aufgerufen, um die Visualisierung durchzuführen
visualize()
