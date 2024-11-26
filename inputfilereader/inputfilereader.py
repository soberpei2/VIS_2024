import json
import mbsObject

def read_input_file(filepath): #Liest eine Eingabedatei und gibt den Inhalt als Liste von Zeilen zurück.
    with open(filepath, "r") as file:
        f= file.read().splitlines()
        f.append("$")        
        
        return f

def parse_file_content(file_content, search4Objects): #Parst den Inhalt einer Datei und gibt eine Liste von Objekten zurück.
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []
    
    for line in file_content:
        if "$" in line:  # Neuer Block gefunden
            if(currentBlockType != ""):
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))

                elif currentBlockType == "CONSTRAINT":
                    listOfMbsObjects.append(mbsObject.constraint(currentTextBlock))

                elif currentBlockType == "SETTINGS":
                    listOfMbsObjects.append(mbsObject.settings(currentTextBlock))
                    
                
            currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()
                break

        currentTextBlock.append(line)
    
    return listOfMbsObjects

def write_json(filepath, model_objects): #Schreibt die Modellobjekte als JSON-Datei.
    jDataBase = json.dumps({"modelObjects": model_objects}, indent=4)
    with open(filepath, "w") as outfile:
        outfile.write(jDataBase)

def read_json(filepath): #Liest eine JSON-Datei und gibt die Daten zurück.
    with open(filepath, "r") as file:
        return json.load(file)

def write_fds(filepath, list_of_mbs_objects): #Schreibt die Eingabedatei für das FDS-Format.
    with open(filepath, "w") as fds:
        for mbsObject_i in list_of_mbs_objects:
            mbsObject_i.writeInputfile(fds)

def process_file(input_filepath, json_filepath, fds_filepath, search4Objects): #Hauptfunktion zur Verarbeitung der Datei.
    file_content = read_input_file(input_filepath)
    list_of_mbs_objects = parse_file_content(file_content, search4Objects)
    
    model_objects = [obj.parameter for obj in list_of_mbs_objects]
    write_json(json_filepath, model_objects)
    write_fds(fds_filepath, list_of_mbs_objects)
    
    print(f"Anzahl der Objekte: {len(list_of_mbs_objects)}")

# Hauptprogramm
if __name__ == "__main__":
    input_filepath = "inputfilereader/test.fdd"
    json_filepath = "inputfilereader/test.json"
    fds_filepath = "inputfilereader/test.fds"
    search4Objects = ["RIGID_BODY", "CONSTRAINT","SETTINGS"]
    
    process_file(input_filepath, json_filepath, fds_filepath, search4Objects)

