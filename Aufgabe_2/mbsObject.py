import vtk
import numpy as np
import math

# Base class for MBS objects
class mbsObject:
    def __init__(self, type, subtype, text, parameter):
        """
        Initializes the mbsObject with type, subtype, parameters, and text data.
        Sets default values and creates a vtkActor for visualization.

        Args:
            type (str): Type of the object (e.g., "Body", "Force").
            subtype (str): Subtype of the object (e.g., "Rigid_EulerParameter_PAI").
            text (list): Text lines from input that define the object's properties.
            parameter (dict): Dictionary of object parameters, each having a type and value.
        """
        self.__type = type
        self.parameter = parameter
        self.__subtype = subtype

        # Default values for various parameter types
        self.default_vec = [1.0, 1.0, 1.0]
        self.default_intvec = [1, 1, 1]
        self.default_float = 1.0
        self.default_int = 1
        self.default_bool = 0
        self.default_string = "DEFAULT"

        # Create VTK actor and mapper for visualization
        self.actor = vtk.vtkActor()
        self.textactor = vtk.vtkTextActor()
        self.mapper = vtk.vtkPolyDataMapper()

        # Parse input text to set parameter values
        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if splitted[0].strip() == key:
                    # Determine the correct data type and set the parameter value accordingly
                    if parameter[key]["type"] == "float":
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif parameter[key]["type"] == "vector":
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif parameter[key]["type"] == "str":
                        parameter[key]["value"] = self.str2str(splitted[1].strip())
                    elif parameter[key]["type"] == "bool":
                        parameter[key]["value"] = self.str2bool(splitted[1])
                    elif parameter[key]["type"] == "intvec":
                        parameter[key]["value"] = self.str2intvec(splitted[1])
                    elif parameter[key]["type"] == "int":
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif parameter[key]["type"] == "geom_path":
                        parameter[key]["value"] = self.str2str(line[10:])

    def forceArrow(self, direction, position, color, size, renderer):
        """
        Creates a force arrow in the specified direction and position, adds it to the renderer.

        Args:
            direction (list): Direction of the force vector (x, y, z).
            position (list): Position to apply the force (x, y, z).
            color (list): RGB color values for the arrow.
            size (float): Size scale for the arrow.
            renderer (vtkRenderer): Renderer to add the actor to.
        """
        # Create arrow geometry
        arrow = vtk.vtkArrowSource()
        self.mapper.SetInputConnection(arrow.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        # Normalize the direction vector
        dirLength = np.linalg.norm(direction)
        if dirLength == 0:
            raise ValueError("The direction cannot be a zero vector.")
        directionNorm = direction / dirLength

        # Calculate orthogonal basis for the transformation (X, Y, Z axes)
        xdir = directionNorm
        hilfsvec = np.array([0.0, 0.0, 1.0])
        if np.allclose(xdir, hilfsvec) or np.allclose(xdir, -hilfsvec):
            hilfsvec = np.array([0.0, 1.0, 0.0])

        ydir = np.cross(hilfsvec, xdir)
        ydir = ydir / np.linalg.norm(ydir)
        zdir = np.cross(xdir, ydir)
        zdir = zdir / np.linalg.norm(zdir)

        # Apply transformation to the actor (translation and rotation)
        transform = vtk.vtkTransform()
        transform.Translate(position[0], position[1], position[2])
        transform.Concatenate([
            xdir[0], ydir[0], zdir[0], 0,
            xdir[1], ydir[1], zdir[1], 0,
            xdir[2], ydir[2], zdir[2], 0,
            0, 0, 0, 1])

        self.actor.SetUserTransform(transform)
        self.actor.SetScale(size, size, size)
        self.actor.GetProperty().SetColor(color[0], color[1], color[2])

        # Add actor to the renderer
        renderer.AddActor(self.actor)

    def writeInputFile(self, file):
        """
        Writes the object's parameters to a file in a specific format.

        Args:
            file (file object): File to write the object data to.
        """
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            value = self.parameter[key]["value"]
            param_type = self.parameter[key]["type"]
            if param_type == "float":
                text.append(f"\t{key} = {self.float2str(value)}\n")
            elif param_type == "vector":
                text.append(f"\t{key} = {self.vector2str(value)}\n")
            elif param_type == "str":
                text.append(f"\t{key} = {self.str2str(value)}\n")
            elif param_type == "bool":
                text.append(f"\t{key} = {self.bool2str(value)}\n")
            elif param_type == "intvec":
                text.append(f"\t{key} = {self.intvec2str(value)}\n")
            elif param_type == "int":
                text.append(f"\t{key} = {self.int2str(value)}\n")
            elif param_type == "geom_path":
                text.append(f"\t{key} = {self.str2str(value)}\n")
        text.append(f"End{self.__type}\n%\n")

        # Write the data to the file
        file.writelines(text)

    # Helper methods for converting between strings and various data types
    def str2float(self, inString):
        return float(inString)

    def float2str(self, inFloat):
        return str(inFloat)

    def str2vector(self, inString):
        return [float(x) for x in inString.split(",")]

    def vector2str(self, inVector):
        return ",".join(map(str, inVector))

    def str2str(self, inString):
        return str(inString)

    def str2bool(self, inString):
        return bool(inString)

    def bool2str(self, inBool):
        return str(inBool)

    def str2intvec(self, inString):
        return [int(x) for x in inString.split()]

    def intvec2str(self, inIntvec):
        return ",".join(map(str, inIntvec))

    def str2int(self, inString):
        return int(inString)

    def int2str(self, inInt):
        return str(inInt)


# Example subclasses for specific MBS objects (RigidBody, Constraint, etc.)
class rigidBody(mbsObject):
    def __init__(self, text):
        """
        Initializes a rigid body with specific parameters.
        """
        super().__init__("Body", "Rigid_EulerParameter_PAI", text, {
            "name": {"type": "str", "value": self.default_string},
            "mass": {"type": "float", "value": self.default_float},
            "COG": {"type": "vector", "value": self.default_vec},
            "position": {"type": "vector", "value": self.default_vec},
            "geometry": {"type": "geom_path", "value": "C:\\test"},
            "x_axis": {"type": "vector", "value": self.default_vec},
            "y_axis": {"type": "vector", "value": self.default_vec},
            "z_axis": {"type": "vector", "value": self.default_vec},
            "color": {"type": "intvec", "value": self.default_intvec},
            "transparency": {"type": "int", "value": self.default_int},
            "inertia": {"type": "vector", "value": self.default_vec},
            "initial_velocity": {"type": "vector", "value": self.default_vec},
            "initial_omega": {"type": "vector", "value": self.default_vec},
            "i1_axis": {"type": "vector", "value": self.default_vec},
            "i2_axis": {"type": "vector", "value": self.default_vec},
            "i3_axis": {"type": "vector", "value": self.default_vec}
        })

    def show(self, renderer):
        """
        Visualizes the rigid body in the renderer.
        """
        # Read geometry path (OBJ file) for the rigid body
        geometry_path = self.parameter["geometry"]["value"]
        reader = vtk.vtkOBJReader()
        reader.SetFileName(geometry_path)
        reader.Update()

        self.mapper.SetInputConnection(reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)

        # Set the body's color
        color = self.parameter["color"]["value"]
        self.actor.GetProperty().SetColor(color[0], color[1], color[2])

        # Add the actor to the renderer
        renderer.AddActor(self.actor)
