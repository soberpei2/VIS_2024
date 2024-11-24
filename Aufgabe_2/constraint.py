import vtk
from mbsObject import mbsObject


class constraint(mbsObject):

    def __init__(self, text):
        parameter = {
            "dx": {"type": "int", "value": 1},
            "dy": {"type": "int", "value": 1},
            "dz": {"type": "int", "value": 1},
            "ax": {"type": "int", "value": 1},
            "ay": {"type": "int", "value": 1},
            "az": {"type": "int", "value": 1},
            "position":{"type":"vector","value": [0.,0.,0.]}
        }
        mbsObject.__init__(self,"Constraint", "Fixed", text, parameter)

    def vtk_constraint(self, constraintrenderer):
        position = self.parameter["position"]["value"]

        # Prüfen und Kegel für jede Richtung erstellen
        if self.parameter["dx"]["value"] == 1:
            self.create_cone(constraintrenderer, [1, 0, 0], position)
        if self.parameter["dy"]["value"] == 1:
            self.create_cone(constraintrenderer, [0, 1, 0], position)
        if self.parameter["dz"]["value"] == 1:
            self.create_cone(constraintrenderer, [0, 0, 1], position)

    def create_cone(self, constraintrenderer, direction, position):
        # Erstelle Kegel im Ursprung
        coneSource = vtk.vtkConeSource()
        coneSource.SetHeight(4.0)
        coneSource.SetRadius(1.2)
        coneSource.SetResolution(20)

        # Transformation initialisieren
        transform = vtk.vtkTransform()

        # 1. Translation anwenden (Position im Weltkoordinatensystem)
        transform.Translate(position[0], position[1], position[2])

        # 2. Drehung um die gewünschte Achse anwenden
        if direction == [1, 0, 0]:  # Kegel zeigt in x-Achse
            pass  
        elif direction == [0, 1, 0]:  # Kegel zeigt in y-Achse
            transform.RotateZ(90)  
        elif direction == [0, 0, 1]:  # Kegel zeigt in z-Achse
            transform.RotateY(90) 

        # Mapper und Actor erstellen
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(coneSource.GetOutputPort())
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        coneActor.SetUserTransform(transform)

        # Färbe den Kegel orange
        coneActor.GetProperty().SetColor(1.0, 0.5, 0.0)  # RGB für Orange
        # Füge den Kegel zum Renderer hinzu
        constraintrenderer.AddActor(coneActor)

    def visualize_constraint(self):
        # Renderer erstellen
        constraintRenderer = vtk.vtkRenderer()
        constraintRenderer.SetBackground(0.0, 0.0, 1.0)  # Hintergrundfarbe

        # Constraint-Objekt visualisieren
        self.vtk_constraint(constraintRenderer)

        # Render-Fenster erstellen
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(constraintRenderer)
        render_window.SetSize(600, 600)

        # Interactor erstellen
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        # Rendern und interaktiv anzeigen
        render_window.Render()
        render_window_interactor.Start()

    def writeInputfile(self, file):
        super().writeInputfile(file)