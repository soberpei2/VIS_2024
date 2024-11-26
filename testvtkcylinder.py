import vtk

# Create a cylinder Source
cylinder = vtk.vtkCylinderSource()
cylinder.SetHeight(10.0)
cylinder.SetRadius(2.0)
cylinder.SetResolution(100)

# Create a mapper and set the cylinder as its input
cylinderMapper = vtk.vtkPolyDataMapper()
cylinderMapper.SetInputConnection(cylinder.GetOutputPort())

# Create an actor
cylinderActor  = vtk.vtkActor()
cylinderActor.SetMapper(cylinderMapper)

# Create a renderer, add the actor and set the background colour
ren1 = vtk.vtkRenderer()
ren1.AddActor(cylinderActor)
ren1.SetBackground(0.1, 0.3, 0.6)

# Create a render window and add the renderer
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(500, 500)

# Render the window and rotate the camera
for i in range(360):
    renWin.Render()
    ren1.GetActiveCamera().Azimuth(5) # Rotate by 1 degree each step

# Start the interaction
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Start()



