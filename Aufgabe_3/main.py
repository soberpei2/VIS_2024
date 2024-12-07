import sys
import inputFileReader
import vtk
import mbsModel

def main():
    #if len(sys.argv) != 2:
    #    print("Usage: python main.py /path/to/your/fdd-File")
    #    sys.exit(1)
    #inputFile = sys.argv[1]
    inputFile = "Aufgabe_2/test.fdd"
    listOfMbsObjects = inputFileReader.parseText2blocksOfMbsObjects(inputFileReader.readFile(inputFile),"$",["RIGID_BODY","CONSTRAINT","FORCE_GenericForce","FORCE_GenericTorque","MEASURE","SETTINGS"])
    
    model = mbsModel.mbsModel()
    for obj in listOfMbsObjects:
        model.addMbsObject(obj)

    renderer = vtk.vtkRenderer()
    model.showModel(renderer)
    renderer.SetBackground(0.1, 0.2, 0.4)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(1000,600)

    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    renderWindowInteractor.Start()


#if __name__ == "__main__":
main()
