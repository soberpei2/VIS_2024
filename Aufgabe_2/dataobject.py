from mbsObject import mbsObject

class dataobject(mbsObject):
    def __init__(self,subtype,text,parameter):

        mbsObject.__init__(self,"DataObject",subtype,text,parameter)

class parameter(dataobject):
    def __init__(self,text):
        parameter = {
            "name": {"type": "string", "value": ""},
            "InitialValue": {"type": "float", "value": 0.}
        }

        dataobject.__init__(self,"Parameter",text,parameter)
