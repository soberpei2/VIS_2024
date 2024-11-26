


###############################################

import mbsObject
import json


def read_file(filepath):
  
    with open(filepath, "r") as f:
        return f.read().splitlines()


def parse_file_content(fileContent, search4Objects=None):
   
    if search4Objects is None:
        search4Objects = ["RIGID_BODY", "CONSTRAINT"]
    
    currentBlockType = ""
    currentTextBlock = []
    listOfMbsObjects = []

    for line in fileContent:
        if line.find("$") >= 0:  
            if currentBlockType != "":
                if currentBlockType == "RIGID_BODY":
                    listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
                
                currentBlockType = ""

        for type_i in search4Objects:
            if line.find(type_i, 1, len(type_i) + 1) >= 0:
                currentBlockType = type_i
                currentTextBlock.clear()
                break
        
        currentTextBlock.append(line)

    return listOfMbsObjects

def process_file(filepath, search4Objects=None):
    
    fileContent = read_file(filepath)
    return parse_file_content(fileContent, search4Objects)

if __name__ == "__main__":
    # Beispielnutzung
    filepath = "inputfilereader/test.fdd"
    mbsObjects = process_file(filepath)
    print(f"Anzahl der MBS-Objekte: {len(mbsObjects)}")