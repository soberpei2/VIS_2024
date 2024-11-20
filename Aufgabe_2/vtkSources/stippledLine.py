from vtkmodules.all import(
    vtkDoubleArray,
    VTK_UNSIGNED_CHAR,
    vtkImageData,
    vtkTexture
)

def StippledLine(actor, lineStipplePattern, lineStippleRepeat):
    tcoords = vtkDoubleArray()
    image = vtkImageData()
    texture = vtkTexture()

    # Create texture
    dimension = 16 * lineStippleRepeat

    image.SetDimensions(dimension, 1, 1)
    image.AllocateScalars(VTK_UNSIGNED_CHAR, 4)
    image.SetExtent(0, dimension - 1, 0, 0, 0, 0)
    on = 255
    off = 0
    i_dim = 0
    while i_dim < dimension:
        for i in range(0, 16):
            mask = (1 << i)
            bit = (lineStipplePattern & mask) >> i
            value = bit
            if value == 0:
                for j in range(0, lineStippleRepeat):
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 0, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 1, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 2, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 3, off)
                    i_dim += 1
            else:
                for j in range(0, lineStippleRepeat):
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 0, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 1, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 2, on)
                    image.SetScalarComponentFromFloat(i_dim, 0, 0, 3, on)
                    i_dim += 1
    polyData = actor.GetMapper().GetInput()
    # Create texture coordinates
    tcoords.SetNumberOfComponents(1)
    tcoords.SetNumberOfTuples(polyData.GetNumberOfPoints())
    for i in range(0, polyData.GetNumberOfPoints()):
        value = i * 0.5
        tcoords.SetTypedTuple(i, [value])
    polyData.GetPointData().SetTCoords(tcoords)
    texture.SetInputData(image)
    texture.InterpolateOff()
    texture.RepeatOn()

    actor.SetTexture(texture)