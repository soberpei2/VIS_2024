import model
import vtkmodules.vtkRenderingOpenGL2
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.vtkCommonTransforms import (
    vtkTransform
)

def main():
    currentModel = model.model("Buell.json")
    if not currentModel.importFddFile("C:\\Users\\Stefan\\Documents\\FH-Wels\\VIS3IL\\VIS_2024\\Aufgabe_2\\test.fdd"):
        exit()

    currentModel.saveDatabase()

    currentModel2 = model.model("Buell2.json")
    currentModel2.loadDatabase("Buell.json")
    currentModel2.saveDatabase()

    colors = vtkNamedColors()
    bkg = map(lambda x: x / 255.0, [26, 51, 102, 255])
    colors.SetColor("BkgColor", *bkg)

    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)
    iren = vtkRenderWindowInteractor()
    style = vtkmodules.vtkInteractionStyle.vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)
    iren.SetRenderWindow(renWin)

    currentModel.showModel(renderer)

    renderer.SetBackground(colors.GetColor3d("BkgColor"))
    renWin.SetSize(800, 800)
    renWin.SetWindowName('FreeDyn GUI')

    iren.Initialize()

    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(0.5)
    renWin.Render()

    iren.Start()

if __name__ == '__main__':
    main()