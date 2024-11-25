import vtk
from force import genericForce  # Wenn du die Klasse genericForce importierst

def test_arrow_display():
    # Erstelle einen Renderer
    renderer = vtk.vtkRenderer()

    # Erstelle ein Render-Fenster
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)  # Größe des Fensters

    # Setze den weißen Hintergrund
    renderer.SetBackground(1.0, 1.0, 1.0)  # RGB-Werte für Weiß

    # Erstelle einen Interactor, um mit dem Render-Fenster zu interagieren
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # Erstelle eine Instanz der genericForce-Klasse
    force_text = "example_force"
    force_obj = genericForce(force_text)

    # Setze die Parameter für den Pfeil (Richtung und Position)
    force_obj.parameter["direction"]["value"] = [1.0, 0.0, 0.0]  # Richtung: positive x-Achse
    force_obj.parameter["PointOfApplication_Body1"]["value"] = [0.0, 0.0, 0.0]  # Punkt der Anwendung

    # Visualisiere den Pfeil
    force_obj.vtk_force(renderer, 0)  # Setze eine beliebige Simulationszeit (hier 0)

    # Kamera hinzufügen, um sicherzustellen, dass der Pfeil sichtbar ist
    camera = vtk.vtkCamera()
    renderer.SetActiveCamera(camera)
    camera.SetPosition(0, 0, 100)  # Kamera so positionieren, dass der Pfeil sichtbar ist
    camera.SetFocalPoint(0, 0, 0)  # Fokuspunkt auf den Ursprung setzen
    camera.SetViewUp(0, 1, 0)  # Blickrichtung nach oben anpassen

    # Rendern und starten
    renderWindow.Render()
    iren.Start()

# Testfunktion aufrufen
test_arrow_display()