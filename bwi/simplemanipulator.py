from bwi.basemanipulator import BaseManipulator
from bwi.shave import Shave
from bwi.center import Center

class SimpleManipulator(Center, Shave):
    #initialize simple manipulators
    def __init__(self, *args, **kwargs):
        Shave.__init__(self, *args, **kwargs)
        Center.__init__(self, *args, **kwargs)
        return
