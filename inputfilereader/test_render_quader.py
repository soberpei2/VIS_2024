

def render_obj_file(file_path):
    # OBJ-Datei laden
    reader = vtk.vtkOBJReader()
    reader.SetFileName(file_path)
    reader.Update()

    # Mapper erstellen
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    # Actor erstellen
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Renderer erstellen
    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)  # Dunkelgrauer Hintergrund

    # Render Window erstellen
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetSize(800, 600)

    # Interactor erstellen
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Start der Interaktion
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    # Pfad zur Quader-OBJ-Datei
    obj_file_path = "inputfilereader/quader.obj"

    # Quader-OBJ-Datei rendern
    render_obj_file(obj_file_path)