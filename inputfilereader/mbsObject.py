
class mbsObject:
    def __init__(self,type,text):
        self.__type__ = type

        for line in text:
            splitted = line.split(":")
            if(splitted[0].strip() == "mass"):            # strip: Leerzeichen entfernen
                self.mass = float(splitted[1])