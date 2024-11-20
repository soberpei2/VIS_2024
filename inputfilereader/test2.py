import inputfilereader
import vtk

#listOfMyObjects = inputfilereader.readInput4Output("inputfilereader/test.fdd","inputfilereader/test1.json","inputfilereader/test1.fds")

ColorBackground = [0.0, 0.0, 0.0]
FirstobjPath = r"inputfilereader/quader.obj"
reader = vtk.vtkOBJReader()
reader.SetFileName(FirstobjPath)
reader.Update()


mapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
     mapper.SetInput(reader.GetOutput())
else:
     mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a rendering window and renderer
ren = vtk.vtkRenderer()
ren.SetBackground(ColorBackground)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

# Create a renderwindowinteractor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Assign actor to the renderer
ren.AddActor(actor)

# Enable user interface interactor
iren.Initialize()
renWin.Render()
iren.Start()