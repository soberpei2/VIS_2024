from mbsObject import mbsObject
import vtk



def constraintCone(direction):
    size = 5
    cone = vtk.vtkConeSource()
    cone.SetCenter(-size/2,0,0)
    cone.SetHeight(size)
    cone.SetRadius(size/3)
    cone.SetResolution(100)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cone.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(0.5)
    transform = vtk.vtkTransform()
    if direction == "dx":
        actor.GetProperty().SetColor(1,0,0)
    elif direction == "dy":
        transform.RotateZ(90)
        actor.GetProperty().SetColor(0,1,0)
    elif direction == "dz":
        transform.RotateY(-90)
        actor.GetProperty().SetColor(0,0,1)
    actor.SetUserTransform(transform)
    return actor

def constraintTorus(direction):
    size = 3
    torusSource = vtk.vtkParametricTorus()
    torusSource.SetRingRadius(size)
    torusSource.SetCrossSectionRadius(size/3)
    torus = vtk.vtkParametricFunctionSource()
    torus.SetParametricFunction(torusSource)
    torus.Update()
    torus.SetUResolution(100)
    torus.SetVResolution(100)
    torus.SetWResolution(100)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(torus.GetOutputPort())
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(0.5)
    transform = vtk.vtkTransform()
    if direction == "ax":
        transform.RotateY(90)
        actor.GetProperty().SetColor(1,0,0)
    elif direction == "ay":
        transform.RotateX(-90)
        actor.GetProperty().SetColor(0,1,0)
    elif direction == "az":
        actor.GetProperty().SetColor(0,0,1)
    transform.Translate(0,0,-size*2)
    actor.SetUserTransform(transform)
    return actor





class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            "name": {"type": "str", "value": "testName"},
            "body1": {"type": "str", "value": "testBody1"},
            "body2": {"type": "str", "value": "testBody2"},
            "dx": {"type": "bool", "value": 0},
            "dy": {"type": "bool", "value": 0},
            "dz": {"type": "bool", "value": 0},
            "ax": {"type": "bool", "value": 0},
            "ay": {"type": "bool", "value": 0},
            "az": {"type": "bool", "value": 0},
            "position": {"type": "vector", "value": [0.,0.,0.]},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]},
            "y_axis": {"type": "vector", "value": [0.,0.,0.]},
            "z_axis": {"type": "vector", "value": [0.,0.,0.]}
        }

        mbsObject.__init__(self,"Constraint","Generic",text,parameter)

        assembly = vtk.vtkAssembly()
        if (parameter["dx"]["value"]==True):
            dxActor = constraintCone("dx")
            assembly.AddPart(dxActor)
        if (parameter["dy"]["value"]==True):
            dyActor = constraintCone("dy")
            assembly.AddPart(dyActor) 
        if (parameter["dz"]["value"]==True):
            dzActor = constraintCone("dz")
            assembly.AddPart(dzActor) 
        if (parameter["ax"]["value"]==True):
            axActor = constraintTorus("ax")
            assembly.AddPart(axActor) 
        if (parameter["ay"]["value"]==True):
            ayActor = constraintTorus("ay")
            assembly.AddPart(ayActor)
        if (parameter["az"]["value"]==True):
            azActor = constraintTorus("az")
            assembly.AddPart(azActor)
        
        self.actor = assembly

        transformationMatrix = vtk.vtkMatrix4x4()
        position = parameter["position"]["value"]
        for i in range(3):
            transformationMatrix.SetElement(i,3,position[i])
        rotationMatrix = [parameter["x_axis"]["value"],parameter["y_axis"]["value"],parameter["z_axis"]["value"]]
        for i in range (3):
            for j in range(3):
                transformationMatrix.SetElement(i,j,rotationMatrix[i][j])
        transform = vtk.vtkTransform()
        transform.SetMatrix(transformationMatrix)
        self.actor.SetUserTransform(transform)





        
            
            

