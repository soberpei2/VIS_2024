import vtk
import inputfilereader as ifr
import mbsModel
import sys

# ALTER CODE

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


def main(input_file_path):
    # Erstelle ein mbsModel-Objekt
    model = mbsModel.mbsModel()

    #Einlesen des FDD Files mittels Inputfilereader
    listOfMbsObjects = ifr.read_fdd_file(input_file_path)

    #mbsModel erstellen mithilfe der vom IFR eingelesenen Daten
    for obj in listOfMbsObjects:
        model.add_object(obj)

    #Anlegen des Renderers
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1,1,1) #weißer Hintergrund

    #Anzeige der Objekte lt. mbsModel
    model.show(renderer)

    #Ursprung-Koordinatensystem anzeigen
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(10, 10, 10)
    renderer.AddActor(axes)

    #Renderfenster anlegen
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    def windowtype(type):
        #kleines Fenster
        if type == 1:
            render_window.SetSize(800, 600)
            render_window.SetWindowName("MKS Reader by fpointin")
        #Fullscreen
        if type == 2:
            render_window.SetFullScreen(True)
            text_actor = vtk.vtkTextActor()
            text_actor.SetInput("MKS Reader by fpointin: Press 'q' to exit.")
            text_actor.GetTextProperty().SetFontSize(24)
            text_actor.GetTextProperty().SetColor(0, 0, 0)  #Schwarzer Text
            text_actor.SetPosition(10, 10)  #Position unten links
            renderer.AddActor2D(text_actor)
    windowtype(2)

    #Interaktor anlegen
    render_interactor = vtk.vtkRenderWindowInteractor()
    render_interactor.SetRenderWindow(render_window)

    #Starten
    render_window.Render()
    render_interactor.Start()


#Aufruf geht nur direkt über main file
if __name__ == "__main__":
    #Fehlermeldung wenn nicht genau 2 Argumente (main.py und Filename) eingegeben werden
    if len(sys.argv) != 2:
        print("\n\n" + "VERWENDUNG DES PROGRAMMS" +"\n" + "in Konsole 'python main.py test.fdd' eingeben!" + "\n" + "Achtung auf korrekten Ordner, ggf. mit cd .. oder cd ''Ordner'' arbeiten!""\n\n")
    #Start des Prozederes mit gewünschtem user input fdd file lt. Konsole
    else:
        input_file_path = sys.argv[1]
        main(input_file_path)