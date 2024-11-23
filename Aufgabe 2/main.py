import vtk
import inputfilereader as ifr
import mbsModel
import sys

# # Freedyn File lesen
# fdd_file_path = "Aufgabe 2/test.fdd"
# listOfMbsObjects = ifr.read_fdd_file(fdd_file_path)

# # Daten in JSON speichern
# json_file_path = "Aufgabe 2/tespythot.json"
# ifr.write_json_file(listOfMbsObjects, json_file_path)

# # JSON lesen
# data = ifr.read_json_file(json_file_path)

# # Daten in .fds-Datei schreiben
# fds_file_path = "Aufgabe 2/test.fds"
# ifr.write_fds_file(listOfMbsObjects, fds_file_path)

#---------------------------------------------------------------------

def main(input_file_path):
    # Erstelle ein mbsModel-Objekt
    model = mbsModel.mbsModel()

    # Lese die FDD-Datei und erhalte eine Liste der MKS-Objekte
    listOfMbsObjects = ifr.read_fdd_file(input_file_path)

    # Füge alle MKS-Objekte zum Modell hinzu
    for obj in listOfMbsObjects:
        model.add_object(obj)

    # Initialisiere VTK Renderer
    renderer = vtk.vtkRenderer()

    # Zeige das Modell im Renderer an
    model.show(renderer)

    # Koordinatensystem anzeigen
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(20, 20, 20)  # Längen der Achsen
    renderer.AddActor(axes)

    # Initialisiere das Renderfenster
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 600)

    # Initialisiere den Interaktor für das Renderfenster
    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    # Starte die Visualisierung
    render_window.Render()
    render_interactor.Start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_inputfile>")
    else:
        input_file_path = sys.argv[1]
        main(input_file_path)