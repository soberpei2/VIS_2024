




filepath = "inputfilereader/test.fdd"

import inputfilereader
objs = inputfilereader.process_file("filepath")

if __name__ == "__main__":
    
    mbsObjects = process_file(filepath)

    print(f"Anzahl der MBS-Objekte: {len(mbsObjects)}")

    