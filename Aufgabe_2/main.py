import vtk
import inputFileReader as iFR


test = iFR.readFile("Aufgabe_2","test.fdd")
list = iFR.parseText2blocksOfMbsObjects(test,"$",["RIGID_BODY","CONSTRAINT","FORCE_GenericForce","FORCE_GenericTorque","MEASURE","SETTINGS"])
#iFR.writeFdsFile(list,"Aufgabe_2","test2.fds")
#iFR.writeJsonFile(list,"Aufgabe_2","test2.json")
#testjson = iFR.readJsonFile("Aufgabe_2","test.json")
#print(testjson)



renderer = vtk.vtkRenderer()
for i in list:
    renderer.AddActor(i.getActor())
renderer.SetBackground(0.1, 0.2, 0.4)

# Erstelle das vtkAxesActor für die Koordinatenachsen
axes = vtk.vtkAxesActor()

# Setze die Farben der Achsen
axes.GetXAxisCaptionActor2D().GetTextActor().GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
axes.GetYAxisCaptionActor2D().GetTextActor().GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
axes.GetZAxisCaptionActor2D().GetTextActor().GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()

# Setze die Farben der Achsenpfeile

axes.GetXAxisShaftProperty().SetColor(1.0, 0.0, 0.0)  # Rot für X-Achse
axes.GetXAxisTipProperty().SetColor(1.0, 0.0, 0.0)  # Rot für X-Achse
axes.GetYAxisShaftProperty().SetColor(0.0, 1.0, 0.0)  # Rot für Y-Achse
axes.GetYAxisTipProperty().SetColor(0.0, 1.0, 0.0)  # Rot für Y-Achse
axes.GetZAxisShaftProperty().SetColor(0.0, 0.0, 1.0)  # Rot für Z-Achse
axes.GetZAxisTipProperty().SetColor(0.0, 0.0, 1.0)  # Rot für Z-Achse

# Skaliere die Achsen, um ihre Längen zu ändern
axes.SetTotalLength(100, 100, 100)  # Länge der Achsen auf 10 Einheiten setzen

# Füge die Achsen zum Renderer hinzu
renderer.AddActor(axes)


renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(1000,600)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

    
renderWindow.Render()
renderWindowInteractor.Start()
