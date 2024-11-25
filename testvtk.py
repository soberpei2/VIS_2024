import vtk

# Create a cone source
cone = vtk.vtkConeSource()
cone.SetHeight(5.0)
cone.SetRadius(2.0)
cone.SetResolution(50)

# Create a mapper and set the cone as its input
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())

# Create an actor and set the mapper
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)

# Create a renderer, add the actor, and set the background color
ren1 = vtk.vtkRenderer()
ren1.AddActor(coneActor)
ren1.SetBackground(0.1, 0.2, 0.4)

# Create a render window and add the renderer
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(300, 300)

# Create an interactor and connect it to the render window
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Initialize the interactor (important for interaction)
iren.Initialize()

# Render the window and rotate the camera
for i in range(360):
    renWin.Render()
    ren1.GetActiveCamera().Azimuth(1)  # Rotate by 1 degree each step

# Start the interaction
iren.Start()