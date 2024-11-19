import inputfilereader
import vtk

#listOfMyObjects = inputfilereader.readInput4Output("inputfilereader/test.fdd","inputfilereader/test1.json","inputfilereader/test1.fds")

cone = vtk.vtkConeSource() 
cone.SetHeight(3.0) 
cone.SetRadius(1.0) 
cone.SetResolution(6)

coneMapper = vtk.vtkPolyDataMapper() 
coneMapper.SetInputConnection(cone.GetOutputPort())

coneActor = vtk.vtkActor() 
coneActor.SetMapper(coneMapper)

ren1 = vtk.vtkRenderer() 
ren1.AddActor(coneActor) 
ren1.SetBackground(0.1, 0.2, 0.4)

renWin = vtk.vtkRenderWindow() 
renWin.AddRenderer(ren1) 
renWin.SetSize(300, 300)

for i in range(360): 
    renWin.Render() 
    ren1.GetActiveCamera().Azimuth(1)

iren = vtk.vtkRenderWindowInteractor() 
iren.SetRenderWindow(renWin) 
iren.Start()