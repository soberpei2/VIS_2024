class mbsModel:
    def __init__(self):
       self.listOfBody = []
       self.listOfConstraint = []
       self.listOfForce = []
       self.listOfMeasure = []

    def addMbsObject(self,mbsObject):
        if mbsObject.getType() == "Body":
            self.listOfBody.append(mbsObject)
        elif mbsObject.getType() == "Constraint":
            self.listOfConstraint.append(mbsObject)
        elif mbsObject.getType() == "Force":
            self.listOfForce.append(mbsObject)
        elif mbsObject.getType() == "Measure":
            self.listOfMeasure.append(mbsObject)
    
    def showModel(self,renderer):
        for obj in self.listOfBody:
            obj.show(renderer)
        for obj in self.listOfConstraint:
            obj.show(renderer)
        for obj in self.listOfForce:
            obj.show(renderer)
        for obj in self.listOfMeasure:
            obj.show(renderer)
        
        

