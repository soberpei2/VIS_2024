import vtk  # Importiert die VTK-Bibliothek für 3D-Visualisierungen
import inputfilereader as ifr  # Importiert das Modul zum Einlesen und Schreiben von Dateien
import mbsModel  # Importiert das Modul für das MBS-Modell
import sys  # Importiert sys, um mit Kommandozeilenargumenten zu arbeiten

def main(input_file_path):
    """
    Hauptfunktion zum Einlesen eines FDD-Dateiformats, Erstellen eines MBS-Modells
    und Visualisieren des Modells mit VTK.
    
    :param input_file_path: Der Pfad zur FDD-Datei
    """
    # Erstelle ein leeres MBS-Modell
    model = mbsModel.mbsModel()

    # Einlesen der FDD-Datei und Umwandeln in eine Liste von MBS-Objekten
    listOfMbsObjects = ifr.read_fdd_file(input_file_path)

    # Füge jedes eingelesene MBS-Objekt dem Modell hinzu
    for obj in listOfMbsObjects:
        model.add_object(obj)

    # Erstelle einen Renderer für die Visualisierung
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)  # Setzt den Hintergrund des Renderers auf weiß

    # Zeige die Objekte im Modell im Renderer an
    model.show(renderer)

    # Erstelle ein Koordinatensystem (Achsen) zur Darstellung des Ursprungs
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(10, 10, 10)  # Setzt die Länge der Achsen auf 10 in jede Richtung
    renderer.AddActor(axes)  # Füge das Achsenobjekt zum Renderer hinzu

    # Erstelle ein Renderfenster und füge den Renderer hinzu
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    def windowtype(type):
        """
        Funktion zum Festlegen des Fenstertyps und der Größe der Anzeige.
        
        :param type: Der Typ des Fensters (1 für kleines Fenster, 2 für Vollbild)
        """
        # Erstelle einen Text-Hinweis, der im Fenster angezeigt wird
        hint = vtk.vtkTextActor()
        hint.SetInput("MKS Reader by fpointin: Press 'q' to exit.")  # Text im Fenster
        hint.GetTextProperty().SetFontSize(24)  # Setzt die Schriftgröße des Textes
        hint.GetTextProperty().SetColor(0, 0, 0)  # Setzt die Textfarbe auf schwarz
        hint.SetPosition(10, 10)  # Setzt die Position des Textes (unten links)
        renderer.AddActor2D(hint)  # Füge den Text als 2D-Actor zum Renderer hinzu
        
        # Fenster im normalen Modus (klein)
        if type == 1:
            render_window.SetSize(800, 600)  # Setzt die Fenstergröße auf 800x600
            render_window.SetWindowName("MKS Reader by fpointin")  # Setzt den Fenstertitel
        # Fenster im Vollbildmodus
        if type == 2:
            render_window.SetFullScreen(True)  # Schaltet den Vollbildmodus ein

    # Initialisierung des Fensters im Vollbildmodus
    windowtype(2)

    # Erstelle einen Interaktor für das Renderfenster (zum Steuern der Anzeige)
    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    # Rendern des Fensters und Start des Interaktors (für die Interaktion mit der Visualisierung)
    render_window.Render()
    render_interactor.Start()

    # Test: Schreibe die FDS-Datei nach der Visualisierung
    ifr.write_fds_file(listOfMbsObjects, "test.fds")


# Debugging: Diese Zeile kann während der Entwicklung verwendet werden
# main("test.fdd")

# Der Programmcode wird nur ausgeführt, wenn das Skript direkt gestartet wird
if __name__ == "__main__":
    # Überprüft, ob genau ein Argument (die FDD-Datei) über die Kommandozeile übergeben wurde
    if len(sys.argv) != 2:
        print("\n\n" + "VERWENDUNG DES PROGRAMMS" + "\n" + "in Konsole 'python main.py test.fdd' eingeben!" + "\n" + "Achtung auf korrekten Ordner, ggf. mit cd .. oder cd ''Ordner'' arbeiten!" + "\n\n")
    else:
        # Wenn das Argument vorhanden ist, wird der Pfad zur FDD-Datei aus den Kommandozeilenargumenten extrahiert
        input_file_path = sys.argv[1]
        main(input_file_path)  # Startet die Hauptfunktion mit dem angegebenen Dateipfad
