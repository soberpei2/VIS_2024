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

        # Prüfen ob ein translatorischer Freiheitsgrad gesperrt ist (dx, dy, dz)
        if self.parameter["dx"]["value"] == 1:
            self.create_cone(constraintrenderer, [1, 0, 0], position)
        if self.parameter["dy"]["value"] == 1:
            self.create_cone(constraintrenderer, [0, 1, 0], position)
        if self.parameter["dz"]["value"] == 1:
            self.create_cone(constraintrenderer, [0, 0, 1], position)

        # Prüfen ob ein rotatorischer Freiheitsgrad gesperrt ist (ax, ay, az)
        if self.parameter["ax"]["value"] == 1:
            self.create_torus(constraintrenderer, [1, 0, 0], position)
        if self.parameter["ay"]["value"] == 1:
            self.create_torus(constraintrenderer, [0, 1, 0], position)
        if self.parameter["az"]["value"] == 1:
            self.create_torus(constraintrenderer, [0, 0, 1], position)

    def create_cone(self, constraintrenderer, direction, position):
        # Kegel erstellen
        coneSource = vtk.vtkConeSource()
        height = 4.0
        coneSource.SetHeight(height)
        coneSource.SetRadius(1.2)
        coneSource.SetResolution(20)

        transform = vtk.vtkTransform()

        # Ausrichtung und Position des Kegels
        # Achtung: Drehung des Koordinatensystems!

        if direction == [1, 0, 0]:  # x-Achse
            transform.Translate(position[0], position[1], position[2])
        elif direction == [0, 1, 0]:  # y-Achse
            transform.RotateZ(90)
            transform.Translate(position[1], -position[0], position[2])
        elif direction == [0, 0, 1]:  # z-Achse
            transform.RotateY(90)
            transform.Translate(-position[2], position[1], position[0])

        # Mapper und Actor für den Kegel
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInputConnection(coneSource.GetOutputPort())
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        coneActor.SetUserTransform(transform)
        coneActor.GetProperty().SetColor(1.0, 0.6, 0.0)  # Orange

        # Zum Renderer hinzufügen
        constraintrenderer.AddActor(coneActor)

    def create_torus(self, constraintrenderer, direction, position):
        # Torus-Objekt erstellen
        torusSource = vtk.vtkParametricTorus()
        torusSource.SetRingRadius(2.0)  # Radius des Torus-Rings
        torusSource.SetCrossSectionRadius(0.5)  # Radius des Querschnitts

        parametricFunctionSource = vtk.vtkParametricFunctionSource()
        parametricFunctionSource.SetParametricFunction(torusSource)
        parametricFunctionSource.Update()

        transform = vtk.vtkTransform()

        # Ausrichtung und Position des Torus 
        #Achtung: Drehung des Koordinatensystems!
        if direction == [1, 0, 0]:  # Torus um Z-Achse
            transform.Translate(position[0], position[1], position[2])
        elif direction == [0, 1, 0]:  # Torus um y-Achse
            transform.RotateX(90)
            transform.Translate(position[0], position[2], -position[1])
        elif direction == [0, 0, 1]:  # Torus um z-Achse
            transform.RotateY(90)
            transform.Translate(-position[2], position[1], position[0])

        # Mapper und Actor für den Torus
        torusMapper = vtk.vtkPolyDataMapper()
        torusMapper.SetInputConnection(parametricFunctionSource.GetOutputPort())
        torusActor = vtk.vtkActor()
        torusActor.SetMapper(torusMapper)
        torusActor.SetUserTransform(transform)
        torusActor.GetProperty().SetColor(0.0, 0.8, 0.8)  # Türkis

        # Zum Renderer hinzufügen
        constraintrenderer.AddActor(torusActor)

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