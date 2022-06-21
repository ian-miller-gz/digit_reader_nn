from bwi.basemanipulator import BaseManipulator
from bwi.simplemanipulator import SimpleManipulator
from bwi.downscale import Downscale


class Manipulator(Downscale):
   # Initialize manipulators
    def __init__(self, array, x=None, y=None):
        BaseManipulator.__init__(self, array, x, y)
        SimpleManipulator.__init__(self, array, x, y)
        Downscale.__init__(self, array, x, y)
