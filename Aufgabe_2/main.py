import inputfilereader_modularisiert as inputfilereader
import mbsModel
import sys
import vtk

def main(input_file):
    """
    Visualisiert alle Objekte in einem MBS-Modell mithilfe von VTK.
    """
    model = mbsModel.mbsModel()

    listOfMbsObjects = inputfilereader.readFile(input_file)
    for obj in listOfMbsObjects:
        model.addObject(obj)
    
    # Renderer und RenderWindow initialisieren
    renderer = vtk.vtkRenderer()
    # Renderer-Optionen
    renderer.SetBackground(0.1, 0.2, 0.3)  # Dunkelblauer Hintergrund

    model.show(renderer)
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(10, 10, 10)
    renderer.AddActor(axes)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    # Durchlaufe alle Objekte im MBS-Modell (altes Programm als Referenz falls nocheinmal benötigt)
    '''for obj in mbs_model.objects:
        # Geometrie extrahieren und hinzufügen (angenommen, jedes Objekt hat `geometry`)
        geometry_path = obj.parameter["geometry"]["value"]
        
        # Lade Geometrie
        reader = vtk.vtkOBJReader()
        reader.SetFileName(geometry_path)
        reader.Update()
        
        # Mapper und Actor erstellen
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        # Füge den Actor zum Renderer hinzu
        renderer.AddActor(actor)'''
    
    # Render-Fenster starten
    render_window.Render()
    print("Drücken Sie 'q', um die Visualisierung zu beenden...")
    render_window_interactor.Start()  

#altes Programm als Referenz
'''def main():
    # Überprüfen, ob ein Dateipfad als Argument übergeben wurde
    if len(sys.argv) != 2:
        print("Verwendung: python main.py test.fdd")
    else:
        input_file = sys.argv[1]
    
    # Eingabedatei lesen
    reader = inputfilereader(input_file)
    mbs_model = reader.read()
    
    # Visualisieren
    visualize_mbs_objects(mbs_model)'''

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Verwendung: python main.py test.fdd")
    else:
        input_file = sys.argv[1]
        main(input_file)


#Problem mit Pfad Aufruf, musste quader.obj in anderen Ordner schieben, da vtk reader falschen Ordner ausliest
#weiß aber nicht warum

#Außerdem Problem mit den Farbcodes und der Transparenz der Bodies (wieder entfernt aus Code weil Fehler verursacht)

#Ausgabe in FDS bzw. json funktioniert nicht mehr (Bzw. gibt nur mehr Settings aus)