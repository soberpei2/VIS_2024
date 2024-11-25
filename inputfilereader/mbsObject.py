import vtk
import math

class mbsObject: 
    def __init__(self,type,subtype,text,parameter): 
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actor = vtk.vtkActor()      # wird immer benötigt
        self.arrow_actor = vtk.vtkActor()   
        self.arrow_source = vtk.vtkArrowSource() # erstellen eines Pfeiles (standart position)

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys():
                if(splitted[0].strip() == key):         #strip leert 
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = (splitted[1])         # für constraint
                    elif(parameter[key]["type"] == "path"):
                        parameter[key]["value"] = self.Path2str(line)         # für constraint 
                    elif(parameter[key]["type"] == "integer"):
                        parameter[key]["value"] = self.str2integer(splitted[1])        # für constraint 
                    elif(parameter[key]["type"] == "color"):
                        parameter[key]["value"] = self.color2vec(splitted[1])        

    def writeInputfile(self, file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            if(self.parameter[key]["type"] == "float"):
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "vector"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "string"):
                text.append("\t" + key + " = " + (self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "path"):
                text.append("\t" + key + " = " + (self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "integer"):
                text.append("\t" + key + " = " + self.integer2str(self.parameter[key]["value"])+"\n")
            elif(self.parameter[key]["type"] == "color"):
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"])+"\n")
        text.append("End" + self.__type + "\n%\n")

        file.writelines(text)

    # zum umrechnen 
    def str2float(self,inString):
        return float(inString)
    def float2str(self,inFloat):
        return str(inFloat)
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2])
    def Path2str(self,inString):
        return inString[10:]
    def str2integer(self,inString):
        return int(inString)
    def integer2str(self,inInteger):
        return str(inInteger)
    def color2vec(self,inString):
        stringcolor = inString[:12].split()
        return [float(v)/255 for v in stringcolor]  # color wird hier normiert --> einzelner float kein vektor
        

class rigidBody(mbsObject):
    def __init__(self, text):
        parameter = {
            # dictonary mit keys 
            "mass": {"type": "float", "value": 1.},
            "COG": {"type": "vector", "value": [0.,0.,0.]}, #center of gravity
            "position": {"type": "vector", "value": [0.,0.,0.]}, # position des Vektors
            "geometry": {"type": "path", "value": "unbekannt"}, # Pfad der Geometrie
            "transparency": {"type": "float", "value": 0.},
            "x_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in x 
            "y_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in y
            "z_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in z
            "color": {"type": "color", "value": [0.,0.,0.]} # Ausrichtung in z
            
        }
        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI", text,parameter)  # euler koordinaten und PAI pricip ... inertia

        # Einlesen der Geometrie
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Actor erstellen
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(self.parameter["color"]["value"])
        self.actor.GetProperty().SetOpacity(self.parameter["transparency"]["value"]/100) # Transparentz übernehmen/ einstellen

        # Transformation basierend auf der Position und Orientierung
        self.apply_transformations()

        
    def apply_transformations(self):
        """Wendet die Position und Orientierung an den Actor an."""
        transform = vtk.vtkTransform()
        
        # Setze Translation
        pos = self.parameter["position"]["value"]
        transform.Translate(pos[0], pos[1], pos[2])

        # Setze Orientierung (Rotationsmatrix aus x_axis, y_axis, z_axis)
        x_axis = self.parameter["x_axis"]["value"]
        y_axis = self.parameter["y_axis"]["value"]
        z_axis = self.parameter["z_axis"]["value"]
        transform.Concatenate([x_axis[0], y_axis[0], z_axis[0], 0,
                               x_axis[1], y_axis[1], z_axis[1], 0,
                               x_axis[2], y_axis[2], z_axis[2], 0,
                               0, 0, 0, 1])

        # Transformation dem Actor zuweisen
        self.actor.SetUserTransform(transform)

class constraint(mbsObject):
    def __init__(self, text):
        parameter = {
            # dict
            "body1": {"type": "string", "value": "leer"},
            "body2": {"type": "string", "value": "leer"},
            "position": {"type": "vector", "value": [0.,0.,0.]}, # position des Vektors
            "x_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in x 
            "y_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in y
            "z_axis": {"type": "vector", "value": [0.,0.,0.]}, # Ausrichtung in z
            "dx": {"type": "integer", "value": [0]},
            "dy": {"type": "integer", "value": [0]},
            "dz": {"type": "integer", "value": [0]},
            "ax": {"type": "integer", "value": [0]},
            "ay": {"type": "integer", "value": [0]},
            "az": {"type": "integer", "value": [0]}
            
        }

        mbsObject.__init__(self,"Constraint","Constraint_EulerParameter_PAI", text,parameter)
        # Position und Achsen laden
 

        self.visualize_constraint( parameter)

    def visualize_constraint(self, parameter):
        colors =  vtk.vtkNamedColors()
        # Kugellager
        if parameter["dx"]["value"] == 1 and parameter["dy"]["value"] == 1 and parameter["dz"]["value"] == 1 and parameter["ax"]["value"] == 0 and parameter["ay"]["value"] == 0 and parameter["az"]["value"] == 0 :
            # Nutze einen Punkt und Linien für die Darstellung
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetCenter(parameter["position"]["value"])
            sphere_source.SetRadius(1)

            # Mapping und Actor
            sphere_mapper = vtk.vtkPolyDataMapper()
            sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
            # Actor für die Kugel
            self.actor.SetMapper(sphere_mapper)
            self.actor.GetProperty().SetColor(1.0, 1.0, 0.0)  # Gelbe Farbe für Constraints
            # Text erstellen und anzeigen 
            
            pos_vec = parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('Kugellager')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.1, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(colors.GetColor3d('White')) # Textfarbe
        #Festlager
        elif parameter["dx"]["value"] == 1 and parameter["dy"]["value"] == 1 and parameter["dz"]["value"] == 1 and parameter["ax"]["value"] == 1 and parameter["ay"]["value"] == 1 and parameter["az"]["value"] == 1 :
            # Parameter
            h = 1.0  # Höhe des Tetraeders
            a = 1.0  # Seitenlänge der Basis
            # 1. Punkte definieren
            points = vtk.vtkPoints()
            points.InsertNextPoint(0, 0, 0)  # Spitze im Ursprung
            points.InsertNextPoint(0, a/2, h)  # Erster Basispunkt auf der z-Achse
            points.InsertNextPoint(-a / 2,  -math.sqrt(3) / 6 * a, h)  # Zweiter Basispunkt
            points.InsertNextPoint(a / 2,  -math.sqrt(3) / 6 * a, h)  # Dritter Basispunkt
            # Tetraeder definieren
            tetra = vtk.vtkTetra()
            tetra.GetPointIds().SetId(0, 0)
            tetra.GetPointIds().SetId(1, 1)
            tetra.GetPointIds().SetId(2, 2)
            tetra.GetPointIds().SetId(3, 3)
            # Unstructured Grid erstellen
            ugrid = vtk.vtkUnstructuredGrid()
            ugrid.SetPoints(points)
            ugrid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
            # Transformation definieren
            transform = vtk.vtkTransform()
            transform.Translate(parameter["position"]["value"])  # Verschieben zur Position
            transformFilter = vtk.vtkTransformFilter() 
            transformFilter.SetTransform(transform) 
            transformFilter.SetInputData(ugrid) 
            transformFilter.Update()
            # Mapper und Actor
            tet_mapper = vtk.vtkDataSetMapper() 
            tet_mapper.SetInputConnection(transformFilter.GetOutputPort())
            self.actor.SetMapper(tet_mapper)
             # Text erstellen und anzeigen 
            
            pos_vec = parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('Festlager')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.1, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(colors.GetColor3d('White')) # Textfarbe
        else:
            # 1. Quader erstellen
            cube = vtk.vtkCubeSource()
            cube.SetXLength(1.0)  # Länge entlang der x-Achse
            cube.SetYLength(1.0)  # Breite entlang der y-Achse
            cube.SetZLength(1.0)  # Höhe entlang der z-Achse
            cube.Update()

            # 2. Transformationsfilter für Positionierung
            transform = vtk.vtkTransform()
            transform.Translate(parameter["position"]["value"])  
            transform.RotateWXYZ(0, 0, 0, 1)  # Optional: 45 Grad um die z-Achse drehen

            transformFilter = vtk.vtkTransformFilter()
            transformFilter.SetTransform(transform)
            transformFilter.SetInputConnection(cube.GetOutputPort())
            transformFilter.Update()

            # 3. Mapper und Actor
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformFilter.GetOutputPort())

            self.actor = vtk.vtkActor()
            self.actor.SetMapper(mapper)
             # Text erstellen und anzeigen 
            
            pos_vec = parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('andere Constrains --> noch ned definiert')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.6, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(colors.GetColor3d('White')) # Textfarbe
    

class settings(mbsObject):
    def __init__(self, text):
        parameter = {
            #dict
    	    "gravity_vector": {"type": "vector", "value": [0.,0.,-9.81]},
            "background_color": {"type": "color", "value": [0.,0.,0.]},
        }
        mbsObject.__init__(self,"Settings","Visualization", text,parameter)
        
        # Visualisierung des Schwerkraftpfeils erstellen
        self.create_gravity_arrow()


    def create_gravity_arrow(self):
            colors = vtk.vtkNamedColors()

            # Definiere Start- und Endpunkte des Pfeils
            start_point = [0, 0, 0]  # Startpunkt des Pfeils
            end_point = [0, 0, -9.81]  # Endpunkt des Pfeils

            # Normalisiere den Vektor zwischen Start- und Endpunkt
            normalized_x = [0] * 3
            vtk.vtkMath.Subtract(end_point, start_point, normalized_x)
            length = vtk.vtkMath.Norm(normalized_x)  # Länge des Pfeils
            vtk.vtkMath.Normalize(normalized_x)  # Vektor normalisieren

            # Erstelle einen beliebigen Vektor für das Kreuzprodukt
            arbitrary = [1, 0, 0]  # Beliebiger Vektor (nicht parallel zu normalized_x)
            normalized_z = [0] * 3
            vtk.vtkMath.Cross(normalized_x, arbitrary, normalized_z)
            vtk.vtkMath.Normalize(normalized_z)

            # Berechne die Y-Achse
            normalized_y = [0] * 3
            vtk.vtkMath.Cross(normalized_z, normalized_x, normalized_y)

            # Erstelle eine 3D-Rotationsmatrix
            matrix = vtk.vtkMatrix4x4()
            matrix.Identity()
            for i in range(3):
                matrix.SetElement(i, 0, normalized_x[i])  # X-Achse
                matrix.SetElement(i, 1, normalized_y[i])  # Y-Achse
                matrix.SetElement(i, 2, normalized_z[i])  # Z-Achse

            # Transformationen anwenden
            transform = vtk.vtkTransform()
            transform.Translate(start_point)  # Verschieben zum Startpunkt
            transform.Concatenate(matrix)  # Rotationsmatrix anwenden
            transform.Scale(2, 2, 2)  # Skaliere den Pfeil

            # Berechne die Mitte des normierten Vektors
            middle_of_vector = [start_point[i] + normalized_x[i] * (1 / 2) * 2 for i in range(3)]
            # Transformiere die PolyData (Pfeil-Daten) direkt
            transform_pd = vtk.vtkTransformPolyDataFilter()
            transform_pd.SetTransform(transform)
            transform_pd.SetInputConnection(self.arrow_source.GetOutputPort())  # Wende Transformation auf den Pfeil an

            # Mapper und Actor für den Pfeil erstellen
            arrow_mapper = vtk.vtkPolyDataMapper()
            arrow_mapper.SetInputConnection(transform_pd.GetOutputPort())  # Die transformierten Pfeil-Daten verwenden
            self.actor.SetMapper(arrow_mapper)
            self.actor.GetProperty().SetColor(colors.GetColor3d('White'))  # Pfeilfarbe
            # Text erstellen und anzeigen 
            atext = vtk.vtkVectorText()
            atext.SetText('Schwerkraftrichtung')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(middle_of_vector[0] + 0.1, middle_of_vector[1] + 0.1, middle_of_vector[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(colors.GetColor3d('White')) # Textfarbe