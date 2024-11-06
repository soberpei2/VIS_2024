
class mbsObject: 
    def __init__(self,type,text): 
        self.__type = type

        for line in text:
            splitted = line.split(":")
            if(splitted[0].strip() == "mass"):         #strip leert 
                self.mass = float(splitted[1])