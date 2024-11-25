import inputfilereader
import vtk
#from inputfilereader import inputfilereader

# definieren vom einzulesendem Pfad der Datei
Pfad = "Aufgabe 2/test.json"
file_path = Pfad
inputfilereader.inputfilereader(Pfad)

#visualisierung
def visualize_model(filepath):
    # Liste der mbsObjects aus der Datei einlesen
    mbs_objects = inputfilereader.inputfilereader(filepath)

    # Renderer und Render Window erstellen
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    # Render Window Interactor hinzufügen
    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    # Alle mbsObjects in den Renderer laden
    for obj in mbs_objects:
        obj.show(renderer)

    # Hintergrundfarbe und Kamera einstellen
    renderer.SetBackground(0.1, 0.2, 0.3)  # Dunkelblauer Hintergrund
    render_window.SetSize(800, 600)

    # Rendern starten
    render_window.Render()
    render_interactor.Start()

if __name__ == "__main__":
    # Pfad zur Eingabedatei
    file_path = Pfad
    visualize_model(file_path)