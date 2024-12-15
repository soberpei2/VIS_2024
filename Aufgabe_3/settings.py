from mbsObject import mbsObject
import vtk
import numpy as np

class settings(mbsObject):
    def __init__(self, **kwargs):
        if "text" in kwargs:
            parameter = {
                "background color": {"type": "vectorInt", "value": [0,0,0]},
                "COG marker scale": {"type": "float", "value": 0.},
                "constraint icon scale": {"type": "float", "value": 0,},
                "force icon scale": {"type": "float", "value": 0.},
            }

            mbsObject.__init__(self,"Settings","",text=kwargs["text"],parameter=parameter)
        else:
            mbsObject.__init__(self,"Settings","",**kwargs)
