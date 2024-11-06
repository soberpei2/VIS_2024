
class mbsObject:
    # Constructor
    def __init__(self, type, text):
        # Save the type to the protected variable __type
        self.__type = type
        
        for line in text:
            # Split line (left and rigth to :)
            splitted = line.split(":")

            # Search for key "mass" (.strip() -> removes Leerzeichen)
            if(splitted[0].strip() == "mass"):
                # Save value under key mass to variable
                self.mass = float(splitted[1])