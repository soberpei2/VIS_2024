
import vtk

class mbsObject:
    # Constructor
    #------------
    def __init__(self, type, subtype, text, parameter, obj_file=None):
        # Save the type to the protected variable __type
        self.__type = type
        self.__subtype = subtype
        

        # Abspeichern des Parametersatzes (self.parameter enthält nur einer Ref. auf parameter)
        self.parameter = parameter

        ## Geometrie/VTK-Darstellung als leeres VTK-Objekt, das später gefüllt wird
        self.vtk_actor = None

        ## Optional: Laden und Darstellen der Geometrie aus einer OBJ-Datei
        if obj_file:
            self.load_geometry(obj_file)

        # Durchsuchen des Textes
        for line in text:
            # Split line (left and rigth to :)
            splitted = line.split(":")

            # Schleife über die Schlüssel des Dictionaries
            for key in parameter.keys():
                # Search for key "mass" (.strip() -> removes Leerzeichen)
                if(splitted[0].strip() == key):
                    #Überprüfen ob der Parametertyp float ist
                    if(parameter[key]["type"] == "float"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2float(splitted[1])

                    #Überprüfen ob der Parametertyp vector ist
                    elif(parameter[key]["type"] == "vector"):
                        # Save value under key mass to variable
                        parameter[key]["value"] = self.str2vector(splitted[1])

# Funktion zum Laden der Geometrie aus einer OBJ-Datei
    def load_geometry(self, obj_file):
        """
        Lädt die Geometrie aus einer OBJ-Datei und erstellt ein VTK-Objekt.
        """
        # Listen für Vertices und Flächen
        vertices = []
        faces = []

        with open(obj_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                
                # Vertices (Zeilen, die mit "v" beginnen)
                if line.startswith("v "):
                    parts = line.split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                
                # Flächen (Zeilen, die mit "f" beginnen)
                elif line.startswith("f "):
                    parts = line.split()
                    # Indexe der Vertices in der Fläche (1-basiert in OBJ)
                    faces.append([int(p.split('/')[0]) - 1 for p in parts[1:]])

        # Erstellen des VTK-PolyData-Objekts
        poly_data = vtk.vtkPolyData()

        # Erstellen eines VTK-Punktes für die Vertices
        vtk_points = vtk.vtkPoints()
        for v in vertices:
            vtk_points.InsertNextPoint(v)  # Punkte in VTK-Objekt einfügen
        
        poly_data.SetPoints(vtk_points)

        # Erstellen der Flächen (Verbindung der Vertices zu Polygonen)
        vtk_cells = vtk.vtkCellArray()
        for face in faces:
            vtk_cells.InsertNextCell(len(face), face)  # Erstellen einer Fläche mit den Vertex-Indices

        poly_data.SetPolys(vtk_cells)

        # Erstellen eines Mappers und Actors für die Visualisierung
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly_data)

        self.vtk_actor = vtk.vtkActor()
        self.vtk_actor.SetMapper(mapper)







    # Memberfunktion -> Inputfile schreiben
    #--------------------------------------
    def writeInputfile(self, file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")      #\n...Leerzeile
        for key in self.parameter.keys():
            # Umwandlung eines float in string
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")    #\t...Einrückung

            # Umwandlung eines Vektors in string
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n") 

        # Anfügen von 2 Leerzeichen am Ende des Files
        text.append("End" + self.__type + "\n%\n")

        # Schreiben der Zeilen in die Variable text
        file.writelines(text)

    # Memberfunktion -> Umwandlung eines string in float
    #---------------------------------------------------
    def str2float(self, inString):
        return float(inString)
    
    # Memberfunktion -> Umwandlung eines float in string
    #---------------------------------------------------
    def float2str(self, inFloat):
        return str(inFloat)
    
    # Memberfunktion -> Umwandlung eines string in vector
    #----------------------------------------------------
    def str2vector(self, inString):
        return [float(inString.split(",")[0]), float(inString.split(",")[1]), float(inString.split(",")[2])]
    
    # Memberfunktion -> Umwandlung eines vector in string
    #----------------------------------------------------
    def vector2str(self, inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])

            
