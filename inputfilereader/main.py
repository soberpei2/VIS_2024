import sys
import os
import vtk
from mbsModel import mbsModel
from inputfilereader import import_fdd_file, export_to_json, import_from_json, write_fds

def create_renderer():
    """
    Erstellt einen VTK-Renderer und ein Render-Fenster.
    """
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    return renderer, render_window

def create_interactor(render_window):
    """
    Erstellt einen VTK-Interactor für das Render-Fenster.
    """
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(render_window)
    return iren

def display_model(model):
    """
    Zeigt das Modell im VTK-Renderfenster an.
    """
    renderer, render_window = create_renderer()
    iren = create_interactor(render_window)
    
    # Extrahiere die VTK-Actors des Modells
    actors = model.get_vtk_actors()
    for actor in actors:
        renderer.AddActor(actor)
    
    renderer.SetBackground(0.1, 0.1, 0.1)  # Setzt den Hintergrund auf dunkel
    render_window.Render()
    
    # Interaktivität starten
    iren.Start()

def main():
    """
    Hauptfunktion zum Laden des Modells, Export und Anzeige.
    """
    # Pfade für die Ein- und Ausgabedateien
    input_file = "VIS_2024/inputfilereader/test.fdd"
    json_output_file = "VIS_2024/inputfilereader/test.json"
    fds_output_file = "VIS_2024/inputfilereader/test.fds"

    print("== Starte FDD-Datei-Parser ==")

    # Schritt 1: FDD-Datei einlesen
    print(f"Lese FDD-Datei: {input_file}")
    mbs_objects = import_fdd_file(input_file)
    print(f"{len(mbs_objects)} Objekte aus der FDD-Datei geladen.")

    # Schritt 2: Exportiere Objekte als JSON
    print(f"Exportiere Objekte in JSON-Datei: {json_output_file}")
    export_to_json(mbs_objects, json_output_file)
    print("JSON-Export abgeschlossen.")

    # Schritt 3: Lese die JSON-Datei und zeige sie an
    print(f"Lese JSON-Datei: {json_output_file}")
    json_data = import_from_json(json_output_file)
    print("Geladene JSON-Daten:")
    print(json_data)

    # Schritt 4: Exportiere Objekte als FDS
    print(f"Exportiere Objekte in FDS-Datei: {fds_output_file}")
    write_fds(mbs_objects, fds_output_file)
    print("FDS-Export abgeschlossen.")

    # 5. Erstelle das Modell für die Anzeige
    model = mbsModel()
    model.load_from_inputfile(input_file)

    # 6. Zeige das Modell im VTK-Renderfenster an
    display_model(model)

    print("== Verarbeitung abgeschlossen ==")

if __name__ == "__main__":
    main()
