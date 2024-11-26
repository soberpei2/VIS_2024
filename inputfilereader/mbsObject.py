import vtk
import numpy as np
import math

class mbsObject:
    def __init__(self,type,subtype,text,parameter):
        self.__type = type
        self.__subtype = subtype
        self.parameter = parameter
        self.actor = vtk.vtkActor() # Anlegen von actor
        self.arrow_source = vtk.vtkArrowSource() # Erstellen eines Pfeils
        self.text_actor = vtk.vtkTextActor()
        self.colors = vtk.vtkNamedColors()
        self.line_source = vtk.vtkLineSource()
        

        for line in text:
            splitted = line.split(":")
            for key in parameter.keys(): 
                if(splitted[0].strip() == key):
                    if(parameter[key]["type"] == "float"):
                        parameter[key]["value"] = self.str2float(splitted[1])
                    elif(parameter[key]["type"] == "vector"):
                        parameter[key]["value"] = self.str2vector(splitted[1])
                    elif(parameter[key]["type"] == "string"):
                        parameter[key]["value"] = (splitted[1])
                    elif(parameter[key]["type"] == "path"):
                        parameter[key]["value"] = self.str2path(line)
                    elif(parameter[key]["type"] == "int"):
                        parameter[key]["value"] = self.str2int(splitted[1])
                    elif(parameter[key]["type"] == "color"):
                        parameter[key]["value"] = self.color(splitted[1])

    def writeInputfile(self,file):
        text = []
        text.append(self.__type + " " + self.__subtype + "\n")
        for key in self.parameter.keys():
            # Umwandeln von einem float in einem string
            if (self.parameter[key]["type"]=="float"):
                text.append("\t"+key+" = "+self.float2str(self.parameter[key]["value"])+"\n")
            # Umwandeln von einem Vektor in einem string
            if (self.parameter[key]["type"]=="vector"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")
            # Ausgabe eines String
            if (self.parameter[key]["type"]=="string"):
                text.append("\t"+key+" = "+ (self.parameter[key]["value"])+"\n")
            # 
            if (self.parameter[key]["type"]=="path"):
                text.append("\t"+key+" = "+ (self.parameter[key]["value"])+"\n")
            # Umwandeln von einem int ind einem strg
            if (self.parameter[key]["type"]=="int"):
                text.append("\t"+key+" = "+ self.int2str(self.parameter[key]["value"])+"\n")
            # Umwandeln von einem Vektor in einem string
            if (self.parameter[key]["type"]=="color"):
                text.append("\t"+key+" = "+self.vector2str(self.parameter[key]["value"])+"\n")

        text.append("End"+self.__type+"\n%\n")

        file.writelines(text)

    #-----------------------------------------------------------------------
    # Hilfsfunktionen 
    def str2int(self,inString):
        return int(inString)
    
    def int2str(self,inint):
        return str(inint)

    def str2float(self,inString):
        return float(inString)
    
    def float2str(self,inFloat):
        return str(inFloat)
    
    def str2vector(self,inString):
        return [float(inString.split(",")[0]),float(inString.split(",")[1]),float(inString.split(",")[2])]
    
    def vector2str(self,inVector):
        return str(inVector[0]) + "," + str(inVector[1]) + "," + str(inVector[2]) 
    
    def str2path(self,inString):
        return inString[10:]
    
    def color(self, inString):
        # nur die ersten 3 Werte werden übernommen und in ein vekotr umgewandelt
        stringcolor = inString[:12]
        values=stringcolor.split()
        # Konvertiere die Werte in Float
        return [float(v)/255 for v in values] #/255 um die Color zwischen 0 und 1 zu nomieren

    #---------------------------------------------------------------------------

class rigidBody(mbsObject):
    def __init__(self,text):
        parameter = {
            "mass": {"type": "float", "value": 1.}, # Default Wert 1 falls er keine Masse für den Körper hat
            "COG": {"type": "vector", "value": [0,0,0]}, # Schwerpunkt der Körper
            "position": {"type": "vector", "value": [0,0,0]}, # Position des Körper
            "geometry": {"type": "path", "value": "unbekannt"}, # Position des Körper
            "transparency": {"type": "float", "value": 0.}, # transparentz des Körper
            "x_axis": {"type": "vector", "value": [1, 0, 0]}, # Ausrichtung in x Richtung
            "y_axis": {"type": "vector", "value": [0, 1, 0]}, # Ausrichtung in y Richtung 
            "z_axis": {"type": "vector", "value": [0, 0, 1]}, # Ausrichtung in z Richtung 
            "color" : {"type": "color", "value" : [0,0,0],} # Einlesen Farbe 
        }

        mbsObject.__init__(self,"Body","Rigid_EulerParameter_PAI",text,parameter)
        
        # Einlesen der Geometrie
        reader = vtk.vtkOBJReader()
        reader.SetFileName(self.parameter["geometry"]["value"])
        reader.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Actor erstellen
        self.actor.SetMapper(mapper)
        self.actor.GetProperty().SetColor(self.parameter["color"]["value"])
        self.actor.GetProperty().SetOpacity(self.parameter["transparency"]["value"]/100) # Transparentz übernehmen/ einstellen 

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
    def __init__(self,text):
        parameter = {
            "body1": {"type": "string", "value": "leer"}, # Default Leer
            "body2": {"type": "string", "value": "leer"}, # Schwerpunkt der Körper
            "position": {"type": "vector", "value": [0,0,0]}, # Position des Körper
            "x_axis": {"type": "vector", "value": [1, 0, 0]}, # Ausrichtung in x Richtung
            "y_axis": {"type": "vector", "value": [0, 1, 0]}, # Ausrichtung in y Richtung 
            "z_axis": {"type": "vector", "value": [0, 0, 1]}, # Ausrichtung in z Richtung 
            "dx": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
            "dy": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
            "dz": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
            "ax": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
            "ay": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
            "az": {"type": "int", "value": 0}, # Freiheitsgrad x -Richtung  
        }

        mbsObject.__init__(self,"Constraint","Constraint_EulerParameter_PAI",text,parameter)

        # Position und Achsen laden

        # Constraint als Linie darstellen (optional: Achsen-Pfeile hinzufügen)
        self.visualize_constraint()

    def visualize_constraint(self):
        # Kugellager
        if self.parameter["dx"]["value"] == 1 and self.parameter["dy"]["value"] == 1 and self.parameter["dz"]["value"] == 1 and self.parameter["ax"]["value"] == 0 and self.parameter["ay"]["value"] == 0 and self.parameter["az"]["value"] == 0 :
            # Nutze einen Punkt und Linien für die Darstellung
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetCenter(self.parameter["position"]["value"])
            sphere_source.SetRadius(1)

            # Mapping und Actor
            sphere_mapper = vtk.vtkPolyDataMapper()
            sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())
            # Actor für die Kugel
            self.actor.SetMapper(sphere_mapper)
            self.actor.GetProperty().SetColor(1.0, 1.0, 0.0)  # Gelbe Farbe für Constraints
            # Text erstellen und anzeigen 
            
            pos_vec = self.parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('Kugellager')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.1, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(self.colors.GetColor3d('White')) # Textfarbe
        #Festlager
        elif self.parameter["dx"]["value"] == 1 and self.parameter["dy"]["value"] == 1 and self.parameter["dz"]["value"] == 1 and self.parameter["ax"]["value"] == 1 and self.parameter["ay"]["value"] == 1 and self.parameter["az"]["value"] == 1 :
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
            transform.Translate(self.parameter["position"]["value"])  # Verschieben zur Position
            transformFilter = vtk.vtkTransformFilter() 
            transformFilter.SetTransform(transform) 
            transformFilter.SetInputData(ugrid) 
            transformFilter.Update()
            # Mapper und Actor
            tet_mapper = vtk.vtkDataSetMapper() 
            tet_mapper.SetInputConnection(transformFilter.GetOutputPort())
            self.actor.SetMapper(tet_mapper)
             # Text erstellen und anzeigen 
            
            pos_vec = self.parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('Festlager')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.1, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(self.colors.GetColor3d('White')) # Textfarbe
        else:
            # 1. Quader erstellen
            cube = vtk.vtkCubeSource()
            cube.SetXLength(1.0)  # Länge entlang der x-Achse
            cube.SetYLength(1.0)  # Breite entlang der y-Achse
            cube.SetZLength(1.0)  # Höhe entlang der z-Achse
            cube.Update()

            # 2. Transformationsfilter für Positionierung
            transform = vtk.vtkTransform()
            transform.Translate(self.parameter["position"]["value"])  
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
            
            pos_vec = self.parameter["position"]["value"]
            atext = vtk.vtkVectorText()
            atext.SetText('andere Constrains --> noch ned definiert')
            text_mapper = vtk.vtkPolyDataMapper()
            text_mapper.SetInputConnection(atext.GetOutputPort())
            self.text_actor = vtk.vtkFollower()
            self.text_actor.SetMapper(text_mapper)
            self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
            self.text_actor.AddPosition(pos_vec[0] + 0.6, pos_vec[1] + 0.1, pos_vec[2] + 0.3)  # Textposition
            self.text_actor.GetProperty().SetColor(self.colors.GetColor3d('White')) # Textfarbe


class settings(mbsObject):
    def __init__(self, text):
        parameter = {
            "gravity_vector": {"type": "vector", "value": [0, 0, -9.81]},  # Standard-Schwerkraftvektor
            "background color" : {"type": "color", "value" : [0, 0, 0]},  # Hintergrundfarbe
        }
        mbsObject.__init__(self, "Settings", "Visualization", text, parameter)

        # Visualisierung des Schwerkraftpfeils erstellen
        self.create_gravity_arrow()

    def create_gravity_arrow(self):

        # Definiere Start- und Endpunkte des Pfeils
        start_point = [0, 0, 0]  # Startpunkt des Pfeils
        end_point = self.parameter["gravity_vector"]["value"]  # Endpunkt des Pfeils

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
        middle_of_vector = [(start_point[i] + normalized_x[i]) * (1 / 2) * 2 for i in range(3)] # *2 wegen skalierung des Vektors 

        # Transformiere die PolyData (Pfeil-Daten) direkt
        transform_pd = vtk.vtkTransformPolyDataFilter()
        transform_pd.SetTransform(transform)
        transform_pd.SetInputConnection(self.arrow_source.GetOutputPort())  # Wende Transformation auf den Pfeil an

        # Mapper und Actor für den Pfeil erstellen
        arrow_mapper = vtk.vtkPolyDataMapper()
        arrow_mapper.SetInputConnection(transform_pd.GetOutputPort())  # Die transformierten Pfeil-Daten verwenden
        self.actor.SetMapper(arrow_mapper)
        self.actor.GetProperty().SetColor(self.colors.GetColor3d('White'))  # Pfeilfarbe
        
        # Text erstellen und anzeigen 
        atext = vtk.vtkVectorText()
        atext.SetText('Schwerkraftrichtung')
        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(atext.GetOutputPort())
        self.text_actor = vtk.vtkFollower()
        self.text_actor.SetMapper(text_mapper)
        self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
        self.text_actor.AddPosition(middle_of_vector[0] + 0.1, middle_of_vector[1] + 0.1, middle_of_vector[2] + 0.3)  # Textposition
        self.text_actor.GetProperty().SetColor(self.colors.GetColor3d('White'))  # Textfarbe

class force(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "leer"}, # Default Leer
            "body1": {"type": "string", "value": "leer"}, # name  body 1
            "body2": {"type": "string", "value": "leer"}, # name body 2
            "PointOfApplication_Body1": {"type": "vector", "value": [0., 0., 0.]}, # Kraftrichtung
            "PointOfApplication_Body2": {"type": "vector", "value": [0., 0., 0.]}, # Kraftrichtung
            "mode": {"type": "string", "value": "leer"}, # Art der Kraft
            "direction": {"type": "vector", "value": [0, 0, 0]}, # Kraftrichtung
            "ForceExpression": {"type": "string", "value": "leer"}, # Beschreibung der Kraft
        }

        mbsObject.__init__(self,"FORCE","GenericForce",text,parameter)
      
        # Aufruf Funktionen
        self.create_applicationPoints()
        self.lineOfAction()
        self.forceLine()

        # Funktion Applikation Punkte visualisieren
    def create_applicationPoints(self):

        if "PointOfApplication_Body1" in self.parameter:
            point1 = self.parameter["PointOfApplication_Body1"]["value"]
            sphere_source1 = vtk.vtkSphereSource()  # Erstelle einen neuen SphereSource für die erste Kugel
            sphere_source1.SetCenter(point1)
            sphere_source1.SetRadius(0.2)  # Standardradius

            sphere_mapper1 = vtk.vtkPolyDataMapper()
            sphere_mapper1.SetInputConnection(sphere_source1.GetOutputPort())

            self.actor1 = vtk.vtkActor()
            self.actor1.SetMapper(sphere_mapper1)
            self.actor1.GetProperty().SetColor(1.0, 1.0, 0.0)  # Gelb für PointOfApplication_Body1

            # Optional: Text für den ersten Punkt
            atext1 = vtk.vtkVectorText()
            atext1.SetText('Applicationpoint_Body1')
            text_mapper1 = vtk.vtkPolyDataMapper()
            text_mapper1.SetInputConnection(atext1.GetOutputPort())
            self.text_actor1 = vtk.vtkFollower()
            self.text_actor1.SetMapper(text_mapper1)
            self.text_actor1.SetScale(0.2, 0.2, 0.2)  # Textgröße
            self.text_actor1.AddPosition(point1[0] + 0.3, point1[1] + 0.3, point1[2] + 0.1)
            self.text_actor1.GetProperty().SetColor(1.0, 1.0, 0.0)  # Weiße Textfarbe

        # Kugel für PointOfApplication_Body2
        if "PointOfApplication_Body2" in self.parameter:
            point2 = self.parameter["PointOfApplication_Body2"]["value"]
            sphere_source2 = vtk.vtkSphereSource()  # Erstelle einen neuen SphereSource für die zweite Kugel
            sphere_source2.SetCenter(point2)
            sphere_source2.SetRadius(0.2)  # Standardradius

            sphere_mapper2 = vtk.vtkPolyDataMapper()
            sphere_mapper2.SetInputConnection(sphere_source2.GetOutputPort())

            self.actor2 = vtk.vtkActor()
            self.actor2.SetMapper(sphere_mapper2)
            self.actor2.GetProperty().SetColor(0.0, 1.0, 0.0)  # Grün für PointOfApplication_Body2

            # Optional: Text für den zweiten Punkt
            atext2 = vtk.vtkVectorText()
            atext2.SetText('Applicationpoint_Body2')
            text_mapper2 = vtk.vtkPolyDataMapper()
            text_mapper2.SetInputConnection(atext2.GetOutputPort())
            self.text_actor2 = vtk.vtkFollower()
            self.text_actor2.SetMapper(text_mapper2)
            self.text_actor2.SetScale(0.2, 0.2, 0.2)  # Textgröße
            self.text_actor2.AddPosition(point2[0] + 0.3, point2[1] + 0.3, point2[2] + 0.1)
            self.text_actor2.GetProperty().SetColor(0.0, 1.0, 0.0)  # Weiße Textfarbe

    def lineOfAction(self):
        # Punkte
        point1 = self.parameter["PointOfApplication_Body1"]["value"]
        point2 = self.parameter["PointOfApplication_Body2"]["value"]
        # Linie zwischen Body1 und Body2
        self.line_source.SetPoint1(point1)
        self.line_source.SetPoint2(point2)
        # Mappen
        line_mapper1 = vtk.vtkPolyDataMapper()
        line_mapper1.SetInputConnection(self.line_source.GetOutputPort())
         # Mapping auf Actor
        self.actor.SetMapper(line_mapper1)  # Body1 zu Body2
        self.actor.GetProperty().SetColor(1.0, 0.0, 1.0) 

        # Berechne die Mitte des normierten Vektors
        middle_of_vector = [(point1[i] + point2[i]) * (1 / 2) for i in range(3)]

        # Text erstellen und anzeigen 
        atext = vtk.vtkVectorText()
        atext.SetText('Wirkungslinie')
        text_mapper = vtk.vtkPolyDataMapper()
        text_mapper.SetInputConnection(atext.GetOutputPort())
        self.text_actor = vtk.vtkFollower()
        self.text_actor.SetMapper(text_mapper)
        self.text_actor.SetScale(0.2, 0.2, 0.2)  # Textgröße skalieren
        self.text_actor.AddPosition(middle_of_vector[0] + 0.1, middle_of_vector[1] + 0.1, middle_of_vector[2] + 0.3)  # Textposition
        self.text_actor.GetProperty().SetColor(1.0, 0.0, 1.0)  # Textfarbe
        
    def forceLine(self):

        point1 = self.parameter["PointOfApplication_Body1"]["value"]
        direction = self.parameter["direction"]["value"]
        direction = self.parameter["direction"]["value"]

                    # Skalierung der Richtung für Visualisierung
        scale = 10.0  # Skaliere die Richtung für die Sichtbarkeit
        scaled_direction = [p1 + scale * d for p1, d in zip(point1, direction)]

        # Linie für die Richtung der Kraft
        line_source2 = vtk.vtkLineSource()
        line_source2.SetPoint1(point1)
        line_source2.SetPoint2(scaled_direction)

        line_mapper2 = vtk.vtkPolyDataMapper()
        line_mapper2.SetInputConnection(line_source2.GetOutputPort())

        self.direction_line_actor = vtk.vtkActor()  # Actor für die Kraft (mit self.actor alleine würde sich das ganze überschreiben)
        self.direction_line_actor.SetMapper(line_mapper2)
        self.direction_line_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Rot

        

class torque(mbsObject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": "leer"}, # Default Leer
            "body1": {"type": "string", "value": "leer"}, # name  body 1
            "body2": {"type": "string", "value": "leer"}, # name body 2
            "mode": {"type": "string", "value": "leer"}, # Art der Kraft
            "direction": {"type": "vector", "value": [0, 0, 0]}, # Kraftrichtung
            "TorqueExpression": {"type": "string", "value": "leer"}, # Beschreibung des Moments
        }

        mbsObject.__init__(self,"FORCE","GenericTorque",text,parameter)



