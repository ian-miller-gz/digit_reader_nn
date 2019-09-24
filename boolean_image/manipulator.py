from boolean_image.basemanipulator import BaseManipulator
from boolean_image.simplemanipulator import SimpleManipulator
from boolean_image.downscale import Downscale


class Manipulator(Downscale):
    """
    Initialize BIA manipulators requiring Base and Simple __init__()'s
    """
    def __init__(self, array, x=None, y=None):
        BaseManipulator.__init__(self, array, x, y)
        SimpleManipulator.__init__(self, array, x, y)
        Downscale.__init__(self, array, x, y)
